"""
Physics utilities for FeynmanCraft ADK.

This module provides physics calculations, particle data, and validation tools.
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

__all__ = [
    'particle_db',
    'ParticleDatabase',
    'search_particle',
    'get_particle_properties',
    'validate_quantum_numbers',
    'get_branching_fractions',
    'compare_particles',
    'convert_units',
    'check_particle_properties'
] 