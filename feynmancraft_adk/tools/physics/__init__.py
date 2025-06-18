"""
Physics Tools Module for FeynmanCraft ADK

This module provides physics validation and calculation tools using the ParticlePhysics MCP Server.
All particle data comes from the external MCP server.
"""

from .physics_tools import (
    search_particle,
    get_particle_properties,
    validate_quantum_numbers,
    get_branching_fractions,
    compare_particles,
    convert_units,
    check_particle_properties,
    parse_natural_language_physics
)
from .search import (
    search_physics_rules,
    filter_rules_by_type,
    rank_rules,
    search_rules_by_particles,
    search_rules_by_process,
    get_conservation_rules,
    validate_process_against_rules
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
    create_rule_index
)
from .embedding_manager import (
    RulesEmbeddingManager,
    get_rules_manager
)

__all__ = [
    # Core physics tools (using MCP)
    'search_particle',
    'get_particle_properties',
    'validate_quantum_numbers',
    'get_branching_fractions',
    'compare_particles',
    'convert_units',
    'check_particle_properties',
    'parse_natural_language_physics',
    
    # Rules search
    'search_physics_rules',
    'filter_rules_by_type',
    'rank_rules',
    'search_rules_by_particles',
    'search_rules_by_process',
    'get_conservation_rules',
    'validate_process_against_rules',
    
    # Data loading
    'load_physics_rules',
    'get_rules_data_path',
    'validate_rules_data',
    'filter_rules_by_category',
    'filter_rules_by_particles',
    'search_rules_by_keyword',
    'get_rule_by_number',
    'get_rules_stats',
    'create_rule_index',
    
    # Embedding management
    'RulesEmbeddingManager',
    'get_rules_manager'
]