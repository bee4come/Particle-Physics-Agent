"""
Physics Tools for FeynmanCraft ADK.

This module provides physics calculations and validation functions using the ParticlePhysics MCP Server.
All particle data comes from the external MCP server.
"""

import asyncio
from typing import Dict, Any, List, Optional
from ...integrations.mcp import (
    search_particle_mcp,
    get_particle_properties_mcp,
    validate_quantum_numbers_mcp,
    get_branching_fractions_mcp,
    compare_particles_mcp,
    convert_units_mcp,
    check_particle_properties_mcp
)


async def search_particle(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search for particles using MCP server."""
    return await search_particle_mcp(query, max_results=max_results)


async def get_particle_properties(particle_name: str, units_preference: str = "GeV") -> Dict[str, Any]:
    """Get comprehensive particle properties from MCP server."""
    return await get_particle_properties_mcp(particle_name, units_preference=units_preference)


async def validate_quantum_numbers(particle_name: str) -> Dict[str, Any]:
    """Validate quantum number consistency using MCP server."""
    return await validate_quantum_numbers_mcp(particle_name)


async def get_branching_fractions(particle_name: str, limit: int = 10) -> Dict[str, Any]:
    """Get decay modes and branching fractions from MCP server."""
    return await get_branching_fractions_mcp(particle_name, limit=limit)


async def compare_particles(particle_names: str, properties: str = "mass,charge,spin") -> Dict[str, Any]:
    """Compare properties of multiple particles using MCP server."""
    # Convert comma-separated string to list
    particle_list = [p.strip() for p in particle_names.split(',')]
    properties_list = [p.strip() for p in properties.split(',')]
    return await compare_particles_mcp(particle_list, properties=properties_list)


async def convert_units(value: float, from_units: str, to_units: str) -> Dict[str, Any]:
    """Convert between physics units using MCP server."""
    return await convert_units_mcp(value, from_units, to_units)


async def check_particle_properties(particle_name: str) -> Dict[str, Any]:
    """Comprehensive particle property checking using MCP server."""
    return await check_particle_properties_mcp(particle_name)


def parse_natural_language_physics(query: str) -> Dict[str, Any]:
    """Parse natural language physics queries and convert to standard notation."""
    import re
    
    query_lower = query.lower().strip()
    
    # Dictionary of common patterns and their physics interpretations
    patterns = {
        # Quark combinations - handle both "upquark" and "up quark" variations
        r'two\s+(?:up\s*quarks?|upquarks?)\s+and\s+one\s+(?:down\s*quarks?|downquarks?)': {
            'particles': ['up', 'up', 'down'],
            'quark_composition': 'uud',
            'result': 'proton',
            'physics_process': 'quark binding via strong force',
            'description': 'Two up quarks and one down quark form a proton (uud composition)',
            'educational_note': 'This is the quark structure of a proton, bound by the strong nuclear force'
        },
        r'two\s+(?:down\s*quarks?|downquarks?)\s+and\s+one\s+(?:up\s*quarks?|upquarks?)': {
            'particles': ['down', 'down', 'up'],
            'quark_composition': 'ddu',
            'result': 'neutron',
            'physics_process': 'quark binding via strong force',
            'description': 'Two down quarks and one up quark form a neutron (ddu composition)',
            'educational_note': 'This is the quark structure of a neutron, bound by the strong nuclear force'
        },
        r'electron\s+and\s+positron\s+collide|electron.*positron.*annihilation': {
            'particles': ['electron', 'positron'],
            'physics_process': 'electron-positron annihilation',
            'result': 'photons',
            'description': 'Electron-positron annihilation produces photons',
            'notation': 'e⁻ + e⁺ → γγ'
        },
        r'muon\s+decay': {
            'particles': ['muon'],
            'physics_process': 'muon decay',
            'result': ['electron', 'electron antineutrino', 'muon neutrino'],
            'description': 'Muon decay via weak interaction',
            'notation': 'μ⁻ → e⁻ + ν̄ₑ + νμ'
        },
        r'what\s+happens?\s+(?:if|when).*three\s+quarks?': {
            'particles': ['quark', 'quark', 'quark'],
            'physics_process': 'baryon formation',
            'result': 'baryon',
            'description': 'Three quarks form a baryon (proton, neutron, etc.)',
            'educational_note': 'Baryons are hadrons composed of three quarks'
        },
        r'what\s+happens?\s+(?:if|when).*(?:quark.*antiquark|antiquark.*quark)': {
            'particles': ['quark', 'antiquark'],
            'physics_process': 'meson formation',
            'result': 'meson',
            'description': 'A quark and antiquark form a meson',
            'educational_note': 'Mesons are hadrons composed of a quark-antiquark pair'
        },
        # More flexible patterns for common issues
        r'(?:two|2)\s*(?:down\s*quarks?|downquarks?)\s+and\s+(?:one|1)\s*(?:electron|elctron)': {
            'particles': ['down', 'down', 'electron'],
            'physics_process': 'unphysical combination',
            'result': 'impossible bound state',
            'description': 'Two down quarks and an electron cannot form a stable bound state',
            'educational_note': 'Quarks form bound states with other quarks (baryons, mesons), not with electrons. Electrons interact electromagnetically, not via the strong force.'
        }
    }
    
    # Check each pattern
    for pattern, interpretation in patterns.items():
        if re.search(pattern, query_lower):
            return {
                'status': 'success',
                'original_query': query,
                'physics_interpretation': interpretation,
                'suggested_process': interpretation.get('physics_process', 'unknown'),
                'educational_context': interpretation.get('educational_note', ''),
                'standard_notation': interpretation.get('notation', ''),
                'can_generate_diagram': interpretation.get('physics_process') not in ['unphysical combination']
            }
    
    # If no specific pattern matches, try to extract particle names
    particle_names = []
    common_particles = [
        'electron', 'positron', 'muon', 'photon', 'proton', 'neutron',
        'up quark', 'upquark', 'down quark', 'downquark', 'strange quark', 'charm quark', 'bottom quark', 'top quark',
        'neutrino', 'antineutrino', 'w boson', 'z boson', 'higgs', 'gluon'
    ]
    
    for particle in common_particles:
        if particle in query_lower:
            particle_names.append(particle)
    
    if particle_names:
        return {
            'status': 'partial',
            'original_query': query,
            'identified_particles': particle_names,
            'suggestion': f'Could you specify what interaction or process involving {", ".join(particle_names)} you want to see?',
            'educational_context': 'Try asking about specific processes like decay, annihilation, or collision',
            'can_generate_diagram': False
        }
    
    # Fallback for unrecognized queries
    return {
        'status': 'unclear',
        'original_query': query,
        'suggestion': 'Could you rephrase your physics question? For example: "electron-positron annihilation" or "muon decay"',
        'educational_context': 'FeynmanCraft can generate diagrams for particle interactions, decays, and collisions',
        'examples': [
            'electron and positron annihilation',
            'muon decay',
            'two up quarks and one down quark',
            'Higgs decay to W bosons'
        ],
        'can_generate_diagram': False
    } 