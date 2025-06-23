"""
MCP (Model Context Protocol) Integration Module
Contains ParticlePhysics MCP Server client for external server communication
"""

from .mcp_client import (
    ParticlePhysicsMCPClient,
    get_mcp_client,
    search_particle_mcp,
    get_particle_properties_mcp,
    validate_quantum_numbers_mcp,
    get_branching_fractions_mcp,
    compare_particles_mcp,
    convert_units_mcp,
    check_particle_properties_mcp
)

from .particle_name_mappings import (
    PARTICLE_NAME_MAPPINGS,
    BASIC_MAPPINGS,
    normalize_particle_name,
    get_antiparticle_name
)

__all__ = [
    # MCP Client
    'ParticlePhysicsMCPClient',
    'get_mcp_client',
    'search_particle_mcp',
    'get_particle_properties_mcp', 
    'validate_quantum_numbers_mcp',
    'get_branching_fractions_mcp',
    'compare_particles_mcp',
    'convert_units_mcp',
    'check_particle_properties_mcp',
    
    # Particle Name Mappings
    'PARTICLE_NAME_MAPPINGS',
    'BASIC_MAPPINGS',
    'normalize_particle_name',
    'get_antiparticle_name'
] 