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

"""
KB Retriever Agent for FeynmanCraft ADK.

This agent retrieves TikZ Feynman diagram examples from two sources:
1. A local JSON file with embeddings (for semantic search).
2. A Google BigQuery table with vector embeddings (for production-level semantic search).

This agent has been refactored to use the centralized tools module for
all data loading, embedding management, and search functionality.
"""

import logging
from typing import List, Dict, Any

from google.adk.agents import Agent

from ..models import KB_RETRIEVER_MODEL
from .kb_retriever_agent_prompt import PROMPT as KB_RETRIEVER_AGENT_PROMPT

# Import all search functionality from tools
from ..tools.kb.search import (
    search_local_tikz_examples,
    search_tikz_examples,
    search_tikz_examples_async
)

logger = logging.getLogger(__name__)


# --- Wrapper functions for agent tools (with defaults) ---

def search_tikz_examples_wrapper(query: str) -> List[Dict[str, Any]]:
    """
    Wrapper for search_tikz_examples with default parameters.
    
    Args:
        query: Natural language query about the Feynman diagram
        
    Returns:
        List of relevant TikZ examples
    """
    try:
        return search_tikz_examples(query, use_bigquery=False, k=5)
    except Exception as e:
        logger.error(f"Error in search_tikz_examples_wrapper: {e}")
        return [{"error": f"Search failed: {str(e)}"}]


async def search_local_tikz_examples_wrapper(query: str) -> List[Dict[str, Any]]:
    """
    Wrapper for search_local_tikz_examples with default parameters.
    
    Args:
        query: Natural language query about the Feynman diagram
        
    Returns:
        List of relevant TikZ examples from local KB
    """
    try:
        return await search_local_tikz_examples(query, top_k=5)
    except Exception as e:
        logger.error(f"Error in search_local_tikz_examples_wrapper: {e}")
        return [{"error": f"Local search failed: {str(e)}"}]


async def search_tikz_examples_async_wrapper(query: str) -> List[Dict[str, Any]]:
    """
    Async wrapper for unified TikZ examples search.
    
    Args:
        query: Natural language query about the Feynman diagram
        
    Returns:
        List of relevant TikZ examples
    """
    try:
        return await search_tikz_examples_async(query, use_bigquery=False, k=5)
    except Exception as e:
        logger.error(f"Error in search_tikz_examples_async_wrapper: {e}")
        return [{"error": f"Async search failed: {str(e)}"}]


# Removed BigQuery search functionality - using local KB only


# --- Agent Definition ---

KBRetrieverAgent = Agent(
    model=KB_RETRIEVER_MODEL,  # Use gemini-2.5-flash for simple retrieval tasks
    name="kb_retriever_agent",
    description="Retrieves relevant TikZ examples from local knowledge base using semantic/vector search. Uses centralized tools for all search operations.",
    instruction=KB_RETRIEVER_AGENT_PROMPT,
    output_key="examples",  # State management: outputs to state.examples
    tools=[
        # Primary search tools
        search_tikz_examples_wrapper,
        search_local_tikz_examples_wrapper,
        search_tikz_examples_async_wrapper,
    ],
)