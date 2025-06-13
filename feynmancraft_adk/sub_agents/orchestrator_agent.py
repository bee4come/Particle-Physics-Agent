# Copyright 2025 Google LLC
# Licensed under the Apache License, Version 2.0

"""
OrchestratorAgent - Main coordination agent for TikZ Feynman diagram generation.
This agent orchestrates other specialized agents to process a diagram request.
"""

from google.adk import Agent

from ..schemas import DiagramRequest, FinalAnswer, TikzSnippet, ValidationReport, DiagramGenerationInput, FeedbackAgentInput, Plan
# Import sub-agents
from .planner_agent import PlannerAgent
from .kb_retriever_agent import KBRetrieverAgent
from .diagram_generator_agent import DiagramGeneratorAgent
from .tikz_validator_agent import TikZValidatorAgent
from .physics_validator_agent import PhysicsValidatorAgent
from .feedback_agent import FeedbackAgent

# Import shared model and this agent's specific prompt
from .. import MODEL # Shared model constant
from .orchestrator_agent_prompt import PROMPT as ORCHESTRATOR_AGENT_PROMPT

import json
import os
from pathlib import Path
from dotenv import load_dotenv
import sys
from typing import List, Optional # Added for type hint

class OrchestratorAgent(Agent):
    """
    Main agent that orchestrates the generation of TikZ Feynman diagrams
    by coordinating Planner, KBRetriever, Generator, Validators, and Feedback agents.
    """

    def __init__(self, model_id: Optional[str] = None):
        # Use the shared MODEL by default, but allow override via model_id parameter
        effective_model_id = model_id if model_id else MODEL
        
        super().__init__(
            # The Orchestrator itself might not directly use an LLM for its core logic
            # if it's purely delegating. If it does (e.g., for complex conditional logic
            # based on user prompt), then `model=effective_model_id` would be set here.
            # For now, assuming its main job is orchestration of sub-agents which might use LLMs.
            name="OrchestratorAgent",
            description="Orchestrates the generation of TikZ Feynman diagrams from natural language.",
            instruction=ORCHESTRATOR_AGENT_PROMPT, # Use imported prompt
            input_schema=DiagramRequest,
            output_schema=FinalAnswer
        )
        # Instantiate sub-agents
        self.planner_agent = PlannerAgent() # Assumes PlannerAgent uses shared MODEL or is LLM-less
        self.kb_retriever_agent = KBRetrieverAgent() # Assumes KBRetrieverAgent uses shared MODEL or is LLM-less
        # DiagramGeneratorAgent explicitly uses an LLM, pass the effective_model_id
        self.diagram_generator_agent = DiagramGeneratorAgent(model_id=effective_model_id)
        self.tikz_validator_agent = TikZValidatorAgent() # Assumes TikZValidatorAgent is rule-based or uses shared MODEL
        self.physics_validator_agent = PhysicsValidatorAgent() # Assumes PhysicsValidatorAgent is rule-based or uses shared MODEL
        self.feedback_agent = FeedbackAgent() # Assumes FeedbackAgent is rule-based or uses shared MODEL
        
        print(f"{self.name} initialized with its team of specialized agents. Effective model for generator: {effective_model_id}")

    def run(self, request: DiagramRequest) -> FinalAnswer:
        """
        Processes user's natural language description (from DiagramRequest),
        orchestrates specialized agents to generate and validate TikZ code,
        and returns a FinalAnswer object.

        Args:
            request: A DiagramRequest Pydantic model instance.

        Returns:
            A FinalAnswer Pydantic model instance.
        """
        user_prompt = request.user_prompt
        style_hint = request.style_hint
        print(f"[{self.name}] Received request for: '{user_prompt}' with style: '{style_hint}'")

        # 1. Planning
        print(f"[{self.name}] Calling PlannerAgent...")
        # PlannerAgent input_schema is DiagramRequest, output_schema is Plan
        plan_obj: Plan = self.planner_agent.run(request)
        print(f"[{self.name}] PlannerAgent returned plan with {len(plan_obj.steps)} steps: {plan_obj.steps}")

        # 2. Knowledge Retrieval
        print(f"[{self.name}] Calling KBRetrieverAgent...")
        # KBRetrieverAgent input_schema is DiagramRequest, output_schema is List[TikzSnippet]
        retrieved_examples: List[TikzSnippet] = self.kb_retriever_agent.run(request)
        print(f"[{self.name}] KBRetrieverAgent returned {len(retrieved_examples)} examples.")

        # 3. Diagram Generation
        print(f"[{self.name}] Calling DiagramGeneratorAgent...")
        generation_input = DiagramGenerationInput(
            user_prompt=user_prompt,
            style_hint=style_hint,
            examples=retrieved_examples
        )
        # DiagramGeneratorAgent input_schema DiagramGenerationInput, output_schema TikzSnippet
        generated_snippet: TikzSnippet = self.diagram_generator_agent.run(generation_input)
        
        if not generated_snippet or not generated_snippet.code or "Error:" in generated_snippet.code.lower():
            print(f"[{self.name}] DiagramGeneratorAgent failed or returned an error snippet.")
            error_tikz_code = generated_snippet.code if (generated_snippet and generated_snippet.code) else f"% Error: Generation failed for: {user_prompt}"
            error_tikz_desc = generated_snippet.description if (generated_snippet and generated_snippet.description) else "Generation failed."
            error_tikz = TikzSnippet(code=error_tikz_code, description=error_tikz_desc)
            error_report = ValidationReport(ok=False, errors=["Diagram generation by DiagramGeneratorAgent failed."])
            return FinalAnswer(
                tikz=error_tikz,
                physics_report=error_report,
                compile_report=error_report
            )
        print(f"[{self.name}] DiagramGeneratorAgent generated TikZ code (preview): {generated_snippet.code[:100].replace(os.linesep, ' ')}...")

        # 4. TikZ Code Validation (Compilation)
        print(f"[{self.name}] Calling TikZValidatorAgent...")
        # TikZValidatorAgent input_schema TikzSnippet, output_schema ValidationReport
        compile_report: ValidationReport = self.tikz_validator_agent.run(generated_snippet)
        print(f"[{self.name}] TikZValidatorAgent report: ok={compile_report.ok}, errors={len(compile_report.errors)}")

        # 5. Physics Validation
        print(f"[{self.name}] Calling PhysicsValidatorAgent...")
        # PhysicsValidatorAgent input_schema TikzSnippet, output_schema ValidationReport
        physics_report: ValidationReport = self.physics_validator_agent.run(generated_snippet)
        print(f"[{self.name}] PhysicsValidatorAgent report: ok={physics_report.ok}, errors={len(physics_report.errors)}")
        
        # 6. Feedback Aggregation
        print(f"[{self.name}] Calling FeedbackAgent...")
        feedback_input = FeedbackAgentInput(
            generated_snippet=generated_snippet,
            physics_report=physics_report,
            compile_report=compile_report
        )
        # FeedbackAgent input_schema FeedbackAgentInput, output_schema FinalAnswer
        final_answer: FinalAnswer = self.feedback_agent.run(feedback_input)
        
        print(f"[{self.name}] Orchestration complete. Returning FinalAnswer.")
        return final_answer

if __name__ == '__main__':
    print(f"Starting {__file__} local test (OrchestratorAgent)...")
    
    project_root_path = Path(__file__).resolve().parent.parent
    if str(project_root_path) not in sys.path:
        sys.path.insert(0, str(project_root_path))
    print(f"Adjusted sys.path to include: {project_root_path}")

    dotenv_path = project_root_path / '.env'
    print(f"Attempting to load .env from: {dotenv_path}")
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path, override=True)
        print(".env loaded.")
        effective_model_for_test = os.getenv("ADK_MODEL_NAME", os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash-latest"))
        print(f"Effective model for test (from env or default flash): {effective_model_for_test}")
        if not os.getenv("GOOGLE_API_KEY"):
            print("Warning: GOOGLE_API_KEY not found in .env or environment. DiagramGeneratorAgent might fail.")
        else:
            print("GOOGLE_API_KEY found.")
    else:
        effective_model_for_test = "gemini-1.5-flash-latest" # Fallback if .env is missing
        print(f"Warning: .env file not found at {dotenv_path}. Sub-agents requiring API keys might fail. Using default: {effective_model_for_test}")

    from agents.orchestrator_agent import OrchestratorAgent 
    from schemas import DiagramRequest, FinalAnswer

    try:
        print("Initializing OrchestratorAgent for local test...")
        orchestrator = OrchestratorAgent(model_id=effective_model_for_test)
        print(f"Agent {orchestrator.name} initialized successfully for local test.")
        
        test_prompts_for_orchestrator = [
            "electron positron annihilation to two photons",
            "A muon decays into an electron, an electron antineutrino, and a muon neutrino.",
            "A W- boson decays into an electron and an anti-neutrino_e",
        ]
        
        for i, user_prompt_text_test in enumerate(test_prompts_for_orchestrator):
            print(f"\n{'='*20} OrchestratorAgent Local Test Case {i+1} {'='*20}")
            print(f"Input Description: \"{user_prompt_text_test}\"")
            
            request_data_test = DiagramRequest(user_prompt=user_prompt_text_test, style_hint="Standard Model style, modern TikZ-Feynman")
            
            print(f"Calling orchestrator.run() with: {request_data_test.model_dump_json(indent=2)}")
            final_answer_result: FinalAnswer = orchestrator.run(request_data_test)
            
            print("\n--- Final Answer from Orchestrator (Local Test) ---")
            if final_answer_result:
                print(final_answer_result.model_dump_json(indent=2))
                if final_answer_result.tikz and final_answer_result.tikz.code:
                    print(f"Generated TikZ Code:\n{final_answer_result.tikz.code}")
                if final_answer_result.compile_report and not final_answer_result.compile_report.ok:
                    print(f"Compilation Errors: {final_answer_result.compile_report.errors}")
                if final_answer_result.physics_report and not final_answer_result.physics_report.ok:
                    print(f"Physics Errors: {final_answer_result.physics_report.errors}")
            else:
                print("OrchestratorAgent run did not return a result in local test.")
            print(f"{'='*20} End OrchestratorAgent Local Test Case {i+1} {'='*20}")

    except ImportError as e:
        print(f"ImportError during local test setup: {e}")
        print("This might happen if agents or schemas are not correctly found in sys.path.")
        print(f"Current sys.path: {sys.path}")
    except Exception as e:
        print(f"Error during local test of OrchestratorAgent: {e}")
        import traceback
        traceback.print_exc() 