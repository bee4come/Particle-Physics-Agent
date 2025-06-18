"""
Physics utilities for FeynmanCraft ADK.

This module provides physics calculations, particle data, validation tools,
rules-based validation, embedding-based search, and comprehensive data management.
"""

from .particle_data import particle_db, ParticleDatabase
from .physics_tools import (
    search_particle,
    get_particle_properties,
    validate_quantum_numbers,
    get_branching_fractions,
    compare_particles,
    convert_units,
    check_particle_properties
)

from .data_loader import (
    load_physics_rules,
    get_rules_data_path,
    validate_rules_data,
    filter_rules_by_category,
    filter_rules_by_particles,
    search_rules_by_keyword,
    get_rule_by_number,
    get_rules_stats,
    create_rule_index,
)

from .embedding_manager import (
    RulesEmbeddingManager,
    embed_and_cache_rules,
    get_rules_manager,
)

from .search import (
    search_physics_rules,
    filter_rules_by_type,
    rank_rules,
    search_rules_by_particles,
    search_rules_by_process,
    get_conservation_rules,
    validate_process_against_rules,
)

__all__ = [
    # Core particle physics tools
    'particle_db',
    'ParticleDatabase',
    'search_particle',
    'get_particle_properties',
    'validate_quantum_numbers',
    'get_branching_fractions',
    'compare_particles',
    'convert_units',
    'check_particle_properties',
    
    # Rules data loading and management
    'load_physics_rules',
    'get_rules_data_path',
    'validate_rules_data',
    'filter_rules_by_category',
    'filter_rules_by_particles',
    'search_rules_by_keyword',
    'get_rule_by_number',
    'get_rules_stats',
    'create_rule_index',
    
    # Rules embedding management
    'RulesEmbeddingManager',
    'embed_and_cache_rules',
    'get_rules_manager',
    
    # Rules search tools
    'search_physics_rules',
    'filter_rules_by_type',
    'rank_rules',
    'search_rules_by_particles',
    'search_rules_by_process',
    'get_conservation_rules',
    'validate_process_against_rules',
]