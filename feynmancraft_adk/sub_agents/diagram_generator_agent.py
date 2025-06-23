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

"""Diagram Generator Agent for FeynmanCraft ADK."""

from google.adk.agents import Agent
from google.adk.tools import transfer_to_agent

from ..models import GENERATOR_MODEL
from .diagram_generator_agent_prompt import PROMPT as DIAGRAM_GENERATOR_AGENT_PROMPT


def complete_diagram_generation() -> str:
    """
    Helper function to signal completion of diagram generation.
    This ensures the agent knows it needs to transfer control back.
    
    Returns:
        A message indicating the need to transfer control.
    """
    return "Diagram generation complete. You must now call transfer_to_agent(agent_name='root_agent') to continue the workflow."


DiagramGeneratorAgent = Agent(
    model=GENERATOR_MODEL,  # Use gemini-2.5-pro for complex TikZ generation
    name="diagram_generator_agent",
    description="Generates TikZ Feynman diagrams from natural language descriptions.",
    instruction=DIAGRAM_GENERATOR_AGENT_PROMPT,
    tools=[
        complete_diagram_generation,
    ],
    output_key="tikz_code",  # State management: outputs to state.tikz_code
) 