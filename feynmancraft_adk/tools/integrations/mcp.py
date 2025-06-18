"""
MCP Integration Tools for FeynmanCraft ADK
Uses external ParticlePhysics MCP Server at https://github.com/uzerone/ParticlePhysics-MCP-Server
"""

# Import from the proper MCP client
from ...integrations.mcp import (
    search_particle_mcp,
    get_particle_properties_mcp,
    validate_quantum_numbers_mcp,
    get_branching_fractions_mcp,
    compare_particles_mcp,
    convert_units_mcp,
    check_particle_properties_mcp
)

# Re-export for tools usage
__all__ = [
    'search_particle_mcp',
    'get_particle_properties_mcp',
    'validate_quantum_numbers_mcp', 
    'get_branching_fractions_mcp',
    'compare_particles_mcp',
    'convert_units_mcp',
    'check_particle_properties_mcp'
] 