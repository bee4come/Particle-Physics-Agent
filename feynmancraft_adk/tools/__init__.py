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
Tools module for FeynmanCraft ADK.

This module provides a unified interface for all tools used by the agents,
organized into categories:
- KB (Knowledge Base): Embedding, search, and retrieval tools
- Physics: Particle data and physics validation tools
- Integrations: Third-party integrations like MCP
"""

# Knowledge Base tools
from .kb import (
    # Embedding utilities
    get_embedding,
    embed_and_cache,
    cosine_similarity,
    find_similar_texts,
    # KB tool classes
    LocalKBTool,
)

# KB data loading and management
from .kb.data_loader import (
    load_kb_examples,
    get_kb_data_path,
    validate_kb_data,
    filter_kb_by_topic,
    filter_kb_by_particles,
    get_kb_stats,
)

from .kb.embedding_manager import (
    KBEmbeddingManager,
    embed_and_cache_kb,
    get_kb_manager,
)

# KB search tools
from .kb.search import (
    search_local_tikz_examples,
    search_tikz_examples,
    search_tikz_examples_async,
    rank_results,
    filter_results_by_confidence,
)

# Physics tools
from .physics import (
    # Particle data tools
    search_particle,
    get_particle_properties,
    validate_quantum_numbers,
    get_branching_fractions,
    compare_particles,
    convert_units,
    check_particle_properties,
)

# Physics data loading and management
from .physics.data_loader import (
    load_physics_rules,
    get_rules_data_path,
    validate_rules_data,
    filter_rules_by_category,
    filter_rules_by_particles as filter_physics_rules_by_particles,
    search_rules_by_keyword,
    get_rule_by_number,
    get_rules_stats,
    create_rule_index,
)

from .physics.embedding_manager import (
    RulesEmbeddingManager,
    embed_and_cache_rules,
    get_rules_manager,
)

# Physics search tools
from .physics.search import (
    search_physics_rules,
    filter_rules_by_type,
    rank_rules,
    search_rules_by_particles,
    search_rules_by_process,
    get_conservation_rules,
    validate_process_against_rules,
)

# Natural language physics parsing
from .physics.physics_tools import (
    parse_natural_language_physics,
)

# MCP integration tools
from .integrations import (
    search_particle_mcp,
    get_particle_properties_mcp,
    validate_quantum_numbers_mcp,
    get_branching_fractions_mcp,
    compare_particles_mcp,
    convert_units_mcp,
    check_particle_properties_mcp,
)

# LaTeX compilation tools removed - using prompt-based validation

__all__ = [
    # KB embedding utilities
    "get_embedding",
    "embed_and_cache",
    "cosine_similarity",
    "find_similar_texts",
    "LocalKBTool",
    
    # KB data loading and management
    "load_kb_examples",
    "get_kb_data_path",
    "validate_kb_data",
    "filter_kb_by_topic",
    "filter_kb_by_particles",
    "get_kb_stats",
    "KBEmbeddingManager",
    "embed_and_cache_kb",
    "get_kb_manager",
    
    # KB search tools
    "search_local_tikz_examples",
    "search_tikz_examples",
    "search_tikz_examples_async",
    "rank_results",
    "filter_results_by_confidence",
    
    # Physics particle tools
    "search_particle",
    "get_particle_properties",
    "validate_quantum_numbers",
    "get_branching_fractions",
    "compare_particles",
    "convert_units",
    "check_particle_properties",
    
    # Physics data loading and management
    "load_physics_rules",
    "get_rules_data_path",
    "validate_rules_data",
    "filter_rules_by_category",
    "filter_physics_rules_by_particles",
    "search_rules_by_keyword",
    "get_rule_by_number",
    "get_rules_stats",
    "create_rule_index",
    "RulesEmbeddingManager",
    "embed_and_cache_rules",
    "get_rules_manager",
    
    # Physics search tools
    "search_physics_rules",
    "filter_rules_by_type",
    "rank_rules",
    "search_rules_by_particles",
    "search_rules_by_process",
    "get_conservation_rules",
    "validate_process_against_rules",
    
    # Natural language processing
    "parse_natural_language_physics",
    
    # MCP integration tools
    "search_particle_mcp",
    "get_particle_properties_mcp",
    "validate_quantum_numbers_mcp",
    "get_branching_fractions_mcp",
    "compare_particles_mcp",
    "convert_units_mcp",
    "check_particle_properties_mcp",
    
]