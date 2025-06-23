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

"""Sub-agents module for FeynmanCraft ADK.

This module provides easy access to all agent classes.
Usage:
    from feynmancraft_adk.sub_agents import PlannerAgent, DiagramGeneratorAgent
    # instead of
    # from feynmancraft_adk.sub_agents.planner_agent import PlannerAgent
"""

# Core Agents (6 agents in production workflow)
from .planner_agent import PlannerAgent
from .kb_retriever_agent import KBRetrieverAgent
from .diagram_generator_agent import DiagramGeneratorAgent
from .tikz_validator_agent import TikZValidatorAgent
from .physics_validator_agent import PhysicsValidatorAgent
from .feedback_agent import FeedbackAgent

# Search Functions (for backward compatibility)
from .kb_retriever_agent import search_tikz_examples, search_tikz_examples_wrapper

__all__ = [
    # Core Agent Classes (6 agents)
    "PlannerAgent",
    "KBRetrieverAgent", 
    "DiagramGeneratorAgent",
    "TikZValidatorAgent",
    "PhysicsValidatorAgent",
    "FeedbackAgent",
    
    # Search Functions
    "search_tikz_examples",
    "search_tikz_examples_wrapper",
] 