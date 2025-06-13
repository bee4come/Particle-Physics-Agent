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

"""KB Retriever Agent for FeynmanCraft ADK."""

from google.adk.agents import Agent

from .. import MODEL
from .kb_retriever_agent_prompt import PROMPT as KB_RETRIEVER_AGENT_PROMPT

KBRetrieverAgent = Agent(
    model=MODEL,
    name="kb_retriever_agent",
    description="Retrieves relevant TikZ examples from knowledge base.",
    instruction=KB_RETRIEVER_AGENT_PROMPT,
) 