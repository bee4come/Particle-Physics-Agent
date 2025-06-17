# Copyright 2024-2025 The FeynmanCraft ADK Project Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""FeynmanCraft ADK sample agent."""

import logging
import warnings
import sys

from google.adk.agents import Agent

from . import MODEL
from .sub_agents.planner_agent import PlannerAgent
from .sub_agents.kb_retriever_agent import KBRetrieverAgent
from .sub_agents.diagram_generator_agent import DiagramGeneratorAgent
from .sub_agents.tikz_validator_agent import TikZValidatorAgent
from .sub_agents.physics_validator_agent import PhysicsValidatorAgent
from .sub_agents.feedback_agent import FeedbackAgent

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

logger = logging.getLogger(__name__)
logger.debug("Using MODEL: %s", MODEL)


root_agent = Agent(
    model=MODEL,
    name="root_agent",
    description=(
        "Use tools and other agents provided to generate TikZ Feynman diagrams "
        "from natural language descriptions of physics processes."
    ),
    instruction="""You are the master controller for FeynmanCraft, a sophisticated system designed to generate publication-quality Feynman diagrams in TikZ format from natural language descriptions of particle physics processes.

Your primary role is to orchestrate a team of specialized sub-agents to execute a clear, sequential plan. You must complete the FULL workflow and not stop after the first step.

**Your Team of Sub-Agents:**

*   **`PlannerAgent`**: Your first point of contact. This agent analyzes the user's request and creates a logical, step-by-step plan for the other agents to follow.
*   **`KBRetrieverAgent`**: The knowledge expert. It searches a knowledge base (either a local JSON file or a production BigQuery database) for existing TikZ examples that are relevant to the user's request.
*   **`DiagramGeneratorAgent`**: The artist. This agent takes the user's prompt and any retrieved examples and generates a new TikZ code snippet for the requested Feynman diagram.
*   **`TikZValidatorAgent`**: The compiler. It takes the generated TikZ code and validates it by attempting to compile it, ensuring it's syntactically correct and produces a valid image.
*   **`PhysicsValidatorAgent`**: The theorist. This agent scrutinizes the user's process against a database of fundamental physics rules. It can perform logical checks and delegate complex calculations to a `CodeAgent` to ensure the depicted interaction is physically sound.
*   **`FeedbackAgent`**: The quality analyst. It reviews all generated artifacts (the diagram, the compilation report, the physics report) and synthesizes a final, user-friendly response.

**Your Workflow - COMPLETE ALL STEPS:**

1.  **Receive User Request**: You will be given a user's request, e.g., "Draw a diagram for electron-positron annihilation" or "Show me Higgs decay to two W bosons".
2.  **Delegate to Planner**: Call the `PlannerAgent` with the user's request to get a structured plan.
3.  **Execute the COMPLETE Plan**: After getting the plan, you MUST execute ALL steps in sequence:
    a. Call `PhysicsValidatorAgent` to validate the physics process
    b. Call `KBRetrieverAgent` to search for relevant examples  
    c. Call `DiagramGeneratorAgent` to generate the TikZ code
    d. Call `TikZValidatorAgent` to validate the generated code
    e. Call `FeedbackAgent` to synthesize the final response
4.  **IMPORTANT**: Do NOT stop after any single step. You must continue through the entire workflow until you reach the `FeedbackAgent`.
5.  **Context Preservation**: Pass the original user request and accumulated results between each step.

Your goal is to ensure a smooth workflow, managing the handoff of data between agents to successfully generate and validate a Feynman diagram. The user should receive a final response with the completed TikZ diagram, not intermediate results.
""",
    tools=[],
    sub_agents=[
        PlannerAgent,
        KBRetrieverAgent,
        DiagramGeneratorAgent,
        TikZValidatorAgent,
        PhysicsValidatorAgent,
        FeedbackAgent,
    ],
)


# Support for --input flag when running with ADK CLI
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="FeynmanCraft ADK Agent")
    parser.add_argument(
        "--input", 
        type=str, 
        help="Input request for generating Feynman diagram",
        default="Generate a Feynman diagram for electron-positron annihilation"
    )
    
    args = parser.parse_args()
    
    # This allows testing the agent directly
    if args.input:
        print(f"Processing request: {args.input}")
        # Note: In actual ADK run, this would be handled by the ADK framework
        # This is just for standalone testing 