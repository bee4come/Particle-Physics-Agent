from google.adk.agents import Agent
from google.adk.messages import JSONMessage
from google.adk.runner import call_agent # ADK utility for calling other agents
from feynmancraft_adk.schemas import DiagramRequest, FinalAnswer, TikzSnippet, ValidationReport, PlanStep
import json

class OrchestratorAgent(Agent):
    """
    Main orchestrator agent. This version implements a minimal end-to-end flow
    using stubs for sub-agents.
    """

    # Define sub-agent names as they would be registered or identified by ADK
    # These are logical names; actual agent instances/references would be used in a full ADK setup.
    SUB_AGENTS = {
        PlanStep.RETRIEVE_EXAMPLES: "KBRetrieverAgent",
        PlanStep.GENERATE_TIKZ: "DiagramGeneratorAgent",
        PlanStep.VALIDATE_TIKZ: "TikZValidatorAgent",
        PlanStep.VALIDATE_PHYSICS: "PhysicsValidatorAgent", # Stub for now
        PlanStep.FEEDBACK: "FeedbackAgent",             # Stub for now
        "planner": "PlannerAgent" # Planner is a special first step
    }

    def __init__(self):
        super().__init__(name="OrchestratorAgent")
        # In a full ADK application, sub-agents might be instantiated here or passed
        # if this Orchestrator itself is part of a larger ADK workflow and they are
        # defined as self.sub_agents = [PlannerAgent(), KBRetrieverAgent(), ...]
        # For `call_agent` to work seamlessly in local tests without full ADK runner setup,
        # it often relies on agents being registered or discoverable by the ADK environment.
        # For now, we'll assume `call_agent` can resolve these names.
        print(f"{self.name} initialized.")

    def run(self, message: JSONMessage) -> JSONMessage:
        print(f"{self.name} received initial request: {message.body}")
        # 0. 解析请求
        req = DiagramRequest(**message.body) # user_prompt, style_hint

        # 1. 规划 - Get the plan from PlannerAgent
        print(f"\nCalling {self.SUB_AGENTS['planner']}...")
        plan_message = call_agent(self.SUB_AGENTS["planner"], message) # Pass initial request
        plan_steps = plan_message.body.get("steps", []) # Expecting a list of PlanStep enums/strings
        print(f"Received plan: {plan_steps}")

        # Initialize variables to store intermediate results
        retrieved_examples_body = []
        generated_tikz_body = TikzSnippet(code="% Default empty TikZ", description="Empty").dict()
        tikz_validation_report_body = ValidationReport(ok=False, errors=["Not run"]).dict()
        physics_validation_report_body = ValidationReport(ok=True, errors=["Physics validation stubbed as OK"]).dict() # Stub

        current_data_for_agent = message # Start with the initial request for the first relevant agent

        # Execute plan steps
        if PlanStep.RETRIEVE_EXAMPLES in plan_steps:
            print(f"\nCalling {self.SUB_AGENTS[PlanStep.RETRIEVE_EXAMPLES]}...")
            # Input to retriever could be the original request or specific parts of it
            examples_msg = call_agent(self.SUB_AGENTS[PlanStep.RETRIEVE_EXAMPLES], 
                                      JSONMessage(body={"user_prompt": req.user_prompt}))
            retrieved_examples_body = examples_msg.body # Expected to be List[TikzSnippet]
            print(f"Retrieved examples: {retrieved_examples_body}")

        if PlanStep.GENERATE_TIKZ in plan_steps:
            print(f"\nCalling {self.SUB_AGENTS[PlanStep.GENERATE_TIKZ]}...")
            generator_input_body = {
                "user_prompt": req.user_prompt,
                "style_hint": req.style_hint,
                "examples": retrieved_examples_body # Pass retrieved examples
            }
            tikz_msg = call_agent(self.SUB_AGENTS[PlanStep.GENERATE_TIKZ], 
                                  JSONMessage(body=generator_input_body))
            generated_tikz_body = tikz_msg.body # Expected to be TikzSnippet
            print(f"Generated TikZ: {generated_tikz_body}")

        if PlanStep.VALIDATE_TIKZ in plan_steps:
            print(f"\nCalling {self.SUB_AGENTS[PlanStep.VALIDATE_TIKZ]}...")
            # Input to TikZ validator is the generated TikZ snippet
            val_msg = call_agent(self.SUB_AGENTS[PlanStep.VALIDATE_TIKZ], 
                                 JSONMessage(body=generated_tikz_body))
            tikz_validation_report_body = val_msg.body # Expected to be ValidationReport
            print(f"TikZ validation report: {tikz_validation_report_body}")

        if PlanStep.VALIDATE_PHYSICS in plan_steps:
            print(f"\nCalling {self.SUB_AGENTS[PlanStep.VALIDATE_PHYSICS]} (Stubbed)... ")
            # Placeholder for actual call; for now, we use the predefined stubbed report
            # In reality, input would be some representation of the diagram for physics check.
            # physics_val_input = JSONMessage(body=generated_tikz_body) # Or a more structured input
            # physics_validation_report_body = call_agent(self.SUB_AGENTS[PlanStep.VALIDATE_PHYSICS], 
            #                                             physics_val_input).body
            print(f"Physics validation report (stubbed): {physics_validation_report_body}")

        # 5. 汇总（先忽略 FeedbackAgent, directly construct FinalAnswer）
        # The FeedbackAgent would normally take all reports and produce a final summary.
        # For this stubbed orchestrator, we construct FinalAnswer directly.
        
        final_answer_data = {
            "tikz": generated_tikz_body, # This should be a TikzSnippet dict
            "physics_report": physics_validation_report_body, # ValidationReport dict
            "compile_report": tikz_validation_report_body, # ValidationReport dict
        }
        
        # Ensure the components are dicts if they came from Pydantic models .json() then json.loads()
        # or if they are direct .dict() outputs from Pydantic models.
        # call_agent is expected to return JSONMessage, whose body is already a dict.

        final_answer = FinalAnswer(**final_answer_data) # Validate final structure
        print(f"\nFinal answer constructed: {final_answer.dict()}")
        return JSONMessage(body=json.loads(final_answer.json()))

if __name__ == '__main__':
    # This local test is more complex due to `call_agent`.
    # `call_agent` typically requires a running ADK environment or specific mocking.
    # To test this Orchestrator locally in a simple script, you would need to:
    # 1. Mock `google.adk.runner.call_agent`.
    # 2. Or, instantiate sub-agents directly and call their `run` methods.

    print("OrchestratorAgent main block: For full testing, run within ADK Dev UI or with mocked call_agent.")
    
    # Example of how one might mock call_agent for a very basic local test:
    def mock_call_agent(agent_name: str, message: JSONMessage):
        print(f"MOCK call_agent: Called {agent_name} with {message.body}")
        if agent_name == "PlannerAgent":
            # Simulate PlannerAgent's output based on its stub
            from feynmancraft_adk.agents.planner_agent import PlannerAgent
            planner = PlannerAgent()
            return planner.run(message)
        elif agent_name == "KBRetrieverAgent":
            from feynmancraft_adk.agents.kb_retriever_agent import KBRetrieverAgent
            retriever = KBRetrieverAgent()
            return retriever.run(message) # Stub ignores message content
        elif agent_name == "DiagramGeneratorAgent":
            from feynmancraft_adk.agents.diagram_generator_agent import DiagramGeneratorAgent
            generator = DiagramGeneratorAgent()
            return generator.run(message)
        elif agent_name == "TikZValidatorAgent":
            from feynmancraft_adk.agents.tikz_validator_agent import TikZValidatorAgent
            validator = TikZValidatorAgent()
            return validator.run(message)
        # Add other agents if needed for the test flow
        return JSONMessage(body={"status": f"Agent {agent_name} not mocked"})

    # Monkey patch call_agent for this local test run
    import sys
    # Ensure feynmancraft_adk is in path if running from agents dir directly
    # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # Check if running in a context where google.adk.runner is already patched or available
    # For this example, we are directly patching it.
    original_call_agent = None
    try:
        import google.adk.runner
        original_call_agent = google.adk.runner.call_agent
        google.adk.runner.call_agent = mock_call_agent
        
        orchestrator = OrchestratorAgent()
        sample_request_body = {"user_prompt": "e+ e- to mu+ mu-"}
        initial_message = JSONMessage(body=sample_request_body)
        final_output_message = orchestrator.run(initial_message)
        print(f"\nOrchestratorAgent final output (mocked test): {json.dumps(final_output_message.body, indent=2)}")

    except ImportError:
        print("Skipping Orchestrator local test as google.adk.runner is not available for patching.")
    except Exception as e:
        print(f"Error during mocked Orchestrator test: {e}")
    finally:
        # Restore original call_agent if it was patched
        if original_call_agent and 'google.adk.runner' in sys.modules:
            google.adk.runner.call_agent = original_call_agent 