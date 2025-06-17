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
"""

import json
import os
import asyncio
import logging
from typing import List, Dict, Any

from google.adk.agents import Agent
from google.cloud import aiplatform
from google.cloud import bigquery
import numpy as np

from .. import MODEL
from .kb_retriever_agent_prompt import PROMPT as KB_RETRIEVER_AGENT_PROMPT

logger = logging.getLogger(__name__)

# --- Globals for KB Examples and Embeddings Cache ---
KB_EXAMPLES: List[Dict[str, Any]] = []
KB_EMBEDDINGS_CACHE: Dict[int, List[float]] = {}  # Use index as key
MODEL_NAME = "text-embedding-004"


def _cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Computes cosine similarity between two vectors."""
    vec1 = np.array(v1)
    vec2 = np.array(v2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if norm_product == 0:
        return 0.0
    return np.dot(vec1, vec2) / norm_product

def load_kb_examples() -> None:
    """Loads KB examples from feynman_kb.json and populates the global variable."""
    global KB_EXAMPLES
    if KB_EXAMPLES:
        return
    try:
        examples_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "feynman_kb.json"
        )
        with open(examples_path, "r", encoding="utf-8") as f:
            KB_EXAMPLES = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading KB examples: {e}")
        KB_EXAMPLES = []

async def _get_embedding(text: str) -> List[float]:
    """Generates an embedding for a given text using Gemini API."""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found")
        
        genai.configure(api_key=api_key)
        
        def get_sync_embedding():
            response = genai.embed_content(
                model=f"models/{MODEL_NAME}",
                content=text,
                task_type="RETRIEVAL_DOCUMENT"
            )
            return response.get("embedding")
        
        embedding = await asyncio.to_thread(get_sync_embedding)
        return embedding if embedding else []
        
    except Exception as e:
        print(f"Failed to get embedding: {e}")
        return []

async def _embed_and_cache_kb() -> None:
    """Generates and caches embeddings for all KB examples."""
    global KB_EMBEDDINGS_CACHE
    if KB_EMBEDDINGS_CACHE:
        return

    load_kb_examples()
    print("Generating and caching embeddings for KB examples...")
    
    try:
        for i, example in enumerate(KB_EXAMPLES):
            text_to_embed = f"{example.get('topic', '')}: {example.get('description', '')}"
            embedding = await _get_embedding(text_to_embed)
            if embedding:
                KB_EMBEDDINGS_CACHE[i] = embedding
        
        print(f"Cached embeddings for {len(KB_EMBEDDINGS_CACHE)} KB examples.")
    except Exception as e:
        print(f"Could not generate KB embeddings: {e}")

# --- Tool for Local JSON Search (now with embeddings) ---

async def search_local_tikz_examples(query: str, top_k: int) -> List[Dict[str, Any]]:
    """
    Performs a semantic search for TikZ examples in a local JSON file.
    """
    await _embed_and_cache_kb()

    if not KB_EXAMPLES or not KB_EMBEDDINGS_CACHE:
        return [{"error": "KB examples or embeddings are not available."}]

    try:
        query_embedding = await _get_embedding(query)
    except Exception as e:
        return [{"error": f"Failed to get query embedding: {e}"}]

    similarities = []
    for i, example in enumerate(KB_EXAMPLES):
        if i in KB_EMBEDDINGS_CACHE:
            sim = _cosine_similarity(query_embedding, KB_EMBEDDINGS_CACHE[i])
            similarities.append((sim, example))

    similarities.sort(key=lambda x: x[0], reverse=True)
    return [example for sim, example in similarities[:top_k]]

# --- Unified KB Search Tool ---

def search_tikz_examples(query: str, use_bigquery: bool, k: int) -> List[Dict[str, Any]]:
    """
    Performs a search for TikZ examples using either BigQuery or local KB.
    
    Args:
        query: Natural language query about the Feynman diagram
        use_bigquery: Whether to try BigQuery first (default: True)
        k: Number of results to return
        
    Returns:
        List of relevant TikZ examples
    """
    results = []
    
    # Try BigQuery first if requested
    if use_bigquery:
        try:
            from ..tools.bigquery_kb_tool import BigQueryKBTool
            
            logger.info("Attempting BigQuery search...")
            kb_tool = BigQueryKBTool()
            results = kb_tool.semantic_search(query)
            
            if results:
                logger.info(f"Found {len(results)} results from BigQuery")
                # Format results
                formatted_results = []
                for result in results:
                    formatted_results.append({
                        "id": result.get("id", ""),
                        "topic": result.get("topic", ""),
                        "reaction": result.get("reaction", ""),
                        "particles": result.get("particles", []),
                        "description": result.get("description", ""),
                        "tikz": result.get("tikz", ""),
                        "source": result.get("source", ""),
                        "process_type": result.get("process_type", ""),
                        "relevance_score": result.get("relevance_score", 0),
                        "source_type": "bigquery"
                    })
                return formatted_results[:k]
                
        except Exception as e:
            logger.warning(f"BigQuery search failed: {e}")
            logger.info("Falling back to local search...")
    
    # Fall back to local search
    try:
        from ..tools.local_kb_tool import LocalKBTool
        
        logger.info("Using local KB search...")
        local_tool = LocalKBTool()
        
        # Try vector search first
        results = local_tool.hybrid_search(query, k=k)
        
        if results:
            logger.info(f"Found {len(results)} results from local KB")
            # Add source type
            for result in results:
                result["source_type"] = "local"
            return results
        else:
            logger.warning("No results found in local KB")
            
    except Exception as e:
        logger.error(f"Local search also failed: {e}")
    
    # If all fails, return empty list
    return []

# --- Wrapper functions for agent tools (with defaults) ---

def search_tikz_examples_wrapper(query: str) -> List[Dict[str, Any]]:
    """Wrapper for search_tikz_examples with default parameters."""
    return search_tikz_examples(query, use_bigquery=False, k=5)

async def search_local_tikz_examples_wrapper(query: str) -> List[Dict[str, Any]]:
    """Wrapper for search_local_tikz_examples with default parameters."""
    return await search_local_tikz_examples(query, top_k=5)

# --- Agent Definition ---

KBRetrieverAgent = Agent(
    model=MODEL,
    name="kb_retriever_agent",
    description="Retrieves relevant TikZ examples from BigQuery or local knowledge base using semantic/vector search.",
    instruction=KB_RETRIEVER_AGENT_PROMPT,
    tools=[
        search_tikz_examples_wrapper,
        search_local_tikz_examples_wrapper,
    ],
) 