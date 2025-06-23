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

"""Feedback Agent for FeynmanCraft ADK."""

from google.adk.agents import Agent

from ..models import FEEDBACK_MODEL
from .feedback_agent_prompt import PROMPT as FEEDBACK_AGENT_PROMPT

FeedbackAgent = Agent(
    model=FEEDBACK_MODEL,  # Use gemini-2.5-flash for simple response synthesis
    name="feedback_agent",
    description="Aggregates feedback and generates final answers.",
    instruction=FEEDBACK_AGENT_PROMPT,
    output_key="final_response",  # State management: outputs to state.final_response
) 