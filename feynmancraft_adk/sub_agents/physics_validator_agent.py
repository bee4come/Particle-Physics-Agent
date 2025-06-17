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
Physics Validator Agent for FeynmanCraft ADK.

This agent acts as a coordinator. It receives a physics process, finds
relevant rules from a JSON database via semantic search, and orchestrates validation.
For rules requiring computation, it delegates to a specialized CodeAgent.
"""

import json
import os
import asyncio
from typing import Dict, List, Any

from google.adk.agents import Agent
import numpy as np

# Note: language_models import moved to where it's used
# to avoid import errors when the module is not available

from .. import MODEL

# --- Globals for Physics Rules and Embeddings Cache ---
PHYSICS_RULES: List[Dict[str, Any]] = []
RULE_EMBEDDINGS_CACHE: Dict[int, List[float]] = {}
MODEL_NAME = "text-embedding-004"

# --- Physics Rules Loading & Embedding ---

def load_physics_rules() -> None:
    """Loads physics rules from pprules.json and populates the global variable."""
    global PHYSICS_RULES
    if PHYSICS_RULES:
        return

    try:
        rules_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "pprules.json"
        )
        with open(rules_path, "r", encoding="utf-8") as f:
            rules_data = json.load(f)
        PHYSICS_RULES = rules_data.get("rules", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading physics rules: {e}")
        PHYSICS_RULES = []

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

async def _embed_and_cache_rules() -> None:
    """Generates and caches embeddings for all physics rules."""
    global RULE_EMBEDDINGS_CACHE
    if RULE_EMBEDDINGS_CACHE:
        return

    print("Generating and caching embeddings for physics rules...")
    
    try:
        for rule in PHYSICS_RULES:
            rule_content = rule.get("content", "")
            if rule_content:
                embedding = await _get_embedding(rule_content)
                if embedding:
                    RULE_EMBEDDINGS_CACHE[rule["rule_number"]] = embedding
        
        print(f"Cached embeddings for {len(RULE_EMBEDDINGS_CACHE)} rules.")
    except Exception as e:
        print(f"Could not generate rule embeddings: {e}")

def _cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Computes cosine similarity between two vectors."""
    vec1 = np.array(v1)
    vec2 = np.array(v2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if norm_product == 0:
        return 0.0
    return np.dot(vec1, vec2) / norm_product

async def search_physics_rules(query: str, top_k: int) -> List[Dict[str, Any]]:
    """Finds the most relevant physics rules for a query using semantic search."""
    load_physics_rules()
    await _embed_and_cache_rules()

    if not PHYSICS_RULES or not RULE_EMBEDDINGS_CACHE:
        return [{"error": "Physics rules or embeddings are not available."}]

    try:
        query_embedding = await _get_embedding(query)
    except Exception as e:
        return [{"error": f"Failed to get query embedding: {e}"}]

    similarities = []
    for rule in PHYSICS_RULES:
        rule_number = rule["rule_number"]
        if rule_number in RULE_EMBEDDINGS_CACHE:
            sim = _cosine_similarity(query_embedding, RULE_EMBEDDINGS_CACHE[rule_number])
            similarities.append((sim, rule))

    similarities.sort(key=lambda x: x[0], reverse=True)
    return [rule for sim, rule in similarities[:top_k]]

# --- Wrapper function for agent tool ---

async def search_physics_rules_wrapper(query: str) -> List[Dict[str, Any]]:
    """Wrapper for search_physics_rules with default parameters."""
    return await search_physics_rules(query, top_k=5)

# --- Agent Definition ---

PhysicsValidatorAgent = Agent(
    name="physics_validator_agent",
    model=MODEL,
    description=(
        "Validates a physics process against a database of rules via semantic search. "
        "Coordinates with a CodeAgent for computational checks."
    ),
    instruction="""You are a Physics Validator Agent, an expert in particle physics.
Your primary function is to validate a given physics process by retrieving relevant rules and applying them.

**Your Workflow:**

1.  **Analyze User Input**: You will receive a physics process description (e.g., "muon-antimuon annihilation").

2.  **Search for Relevant Rules**: Your first and most crucial step is to **call the `search_physics_rules` tool**. Use the user's process description as the `query`. This tool will perform a semantic search and return the most relevant rules from the knowledge base.

3.  **Process Each Retrieved Rule**: For each rule returned by the search tool, perform one of the following actions:

    a.  **Text-Based Validation (if `needs_code` is `false` or absent)**:
        -   Read the rule's `content`. Based on your expert knowledge, determine if the user's process **obeys or violates** this rule and formulate a concise `pass_fail_reason`.

    b.  **Computational Validation (if `needs_code` is `true`)**:
        -   Examine the rule's `code_spec`. From the user's input, extract numerical values for the required `inputs`.
        -   For now, use your physics knowledge to estimate the result since direct code execution is complex.
        -   Formulate a `pass_fail_reason` that includes the inputs used and estimated result.

4.  **Synthesize and Report**:
    -   Aggregate the validation results for all retrieved rules into a `validation_report`.
    -   Provide a final `overall_conclusion`.
    -   **CRITICAL**: Structure your final output as a single JSON object.

5.  **Transfer Back**: After completing the validation and providing your JSON report, immediately transfer control back to the root_agent by calling transfer_to_agent with agent_name="root_agent". Do not wait for further input.
""",
    tools=[search_physics_rules_wrapper],
)

# Load the rules when the module is imported to be ready for embedding.
load_physics_rules() 