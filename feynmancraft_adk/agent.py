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
    instruction=(
        "You are a specialized agent for generating TikZ Feynman diagrams. "
        "When given a physics process description, coordinate with sub-agents "
        "to plan, retrieve knowledge, generate diagrams, and validate results."
    ),
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