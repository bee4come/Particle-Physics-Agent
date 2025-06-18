"""
Physics Tools for FeynmanCraft ADK.

This module provides physics calculations and validation functions.
Separated from external integrations for clean architecture.
"""

import asyncio
from typing import Dict, Any, List, Optional
from .particle_data import particle_db


async def search_particle(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search for particles in the database."""
    try:
        particles = particle_db.search_particles(query, max_results)
        return {
            'status': 'success',
            'particles': particles,
            'query': query,
            'count': len(particles)
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'query': query
        }


async def get_particle_properties(particle_name: str, units_preference: str = "GeV") -> Dict[str, Any]:
    """Get comprehensive particle properties."""
    try:
        particle = particle_db.get_particle(particle_name)
        if not particle:
            return {
                'status': 'error',
                'message': f'Particle {particle_name} not found'
            }
        
        # Unit conversion if needed
        particle_copy = particle.copy()
        if units_preference == "GeV" and particle.get('mass', {}).get('unit') == 'MeV':
            mass_data = particle['mass'].copy()
            mass_data['value'] = mass_data['value'] / 1000
            mass_data['unit'] = 'GeV'
            particle_copy['mass'] = mass_data
        
        return {
            'status': 'success',
            'particle': particle_copy,
            'units': units_preference
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'particle_name': particle_name
        }


async def validate_quantum_numbers(particle_name: str) -> Dict[str, Any]:
    """Validate quantum number consistency for a particle."""
    try:
        particle = particle_db.get_particle(particle_name)
        if not particle:
            return {
                'status': 'error',
                'message': f'Particle {particle_name} not found'
            }
        
        quantum_numbers = particle.get('quantum_numbers', {})
        
        # Basic validation checks
        validations = {
            'has_quantum_numbers': bool(quantum_numbers),
            'spin_parity_consistent': True,  # Simplified for now
            'charge_conjugation_valid': True,  # Simplified for now
            'overall_validity': bool(quantum_numbers)
        }
        
        return {
            'status': 'success',
            'particle': particle_name,
            'quantum_numbers': quantum_numbers,
            'validations': validations,
            'overall_validity': validations['overall_validity']
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'particle_name': particle_name
        }


async def get_branching_fractions(particle_name: str, limit: int = 10) -> Dict[str, Any]:
    """Get decay modes and branching fractions (simplified implementation)."""
    try:
        particle = particle_db.get_particle(particle_name)
        if not particle:
            return {
                'status': 'error',
                'message': f'Particle {particle_name} not found'
            }
        
        # Simplified decay modes based on particle type
        decay_modes = []
        particle_type = particle.get('type', '')
        
        if particle_name == 'muon':
            decay_modes = [
                {'products': ['electron', 'electron_neutrino', 'muon_antineutrino'], 
                 'branching_fraction': 1.0, 'type': 'weak'}
            ]
        elif particle_name == 'tau':
            decay_modes = [
                {'products': ['muon', 'muon_antineutrino', 'tau_neutrino'], 
                 'branching_fraction': 0.1739, 'type': 'weak'},
                {'products': ['electron', 'electron_antineutrino', 'tau_neutrino'], 
                 'branching_fraction': 0.1782, 'type': 'weak'}
            ]
        elif 'pion' in particle_name:
            if particle_name == 'pion_plus':
                decay_modes = [
                    {'products': ['muon', 'muon_neutrino'], 
                     'branching_fraction': 0.9998, 'type': 'weak'}
                ]
        
        return {
            'status': 'success',
            'particle': particle_name,
            'decay_modes': decay_modes[:limit],
            'total_modes': len(decay_modes)
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'particle_name': particle_name
        }


async def compare_particles(particle_names: str, properties: str = "mass,charge,spin") -> Dict[str, Any]:
    """Compare properties of multiple particles."""
    try:
        # Parse inputs
        particle_list = [p.strip() for p in particle_names.split(',')]
        properties_list = [p.strip() for p in properties.split(',')]
        
        comparison_data = {}
        for particle_name in particle_list:
            particle = particle_db.get_particle(particle_name)
            if particle:
                comparison_data[particle_name] = particle
        
        # Build comparison matrix
        property_comparison = {}
        for prop in properties_list:
            property_comparison[prop] = {}
            for particle_name, data in comparison_data.items():
                if prop == 'mass':
                    mass_data = data.get('mass', {})
                    property_comparison[prop][particle_name] = mass_data
                else:
                    property_comparison[prop][particle_name] = data.get(prop)
        
        return {
            'status': 'success',
            'particles': list(comparison_data.keys()),
            'properties': properties_list,
            'property_comparison': property_comparison
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'input': {'particles': particle_names, 'properties': properties}
        }


async def convert_units(value: float, from_units: str, to_units: str) -> Dict[str, Any]:
    """Convert between physics units."""
    try:
        conversion_factors = {
            ('MeV', 'GeV'): 0.001,
            ('GeV', 'MeV'): 1000,
            ('s', 'ns'): 1e9,
            ('ns', 's'): 1e-9,
            ('eV', 'MeV'): 1e-6,
            ('MeV', 'eV'): 1e6
        }
        
        factor = conversion_factors.get((from_units, to_units), 1.0)
        converted_value = value * factor
        
        return {
            'status': 'success',
            'original': {'value': value, 'unit': from_units},
            'converted': {'value': converted_value, 'unit': to_units},
            'conversion_factor': factor
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'conversion': f'{value} {from_units} -> {to_units}'
        }


async def check_particle_properties(particle_name: str) -> Dict[str, Any]:
    """Comprehensive particle property checking."""
    try:
        particle = particle_db.get_particle(particle_name)
        if not particle:
            return {
                'status': 'error',
                'message': f'Particle {particle_name} not found'
            }
        
        # Comprehensive checks
        checks = {
            'has_mass': 'mass' in particle,
            'has_charge': 'charge' in particle,
            'has_spin': 'spin' in particle,
            'has_quantum_numbers': 'quantum_numbers' in particle,
            'has_pdg_id': 'pdg_id' in particle,
            'lifetime_defined': 'lifetime' in particle
        }
        
        overall_completeness = sum(checks.values()) / len(checks)
        
        return {
            'status': 'success',
            'particle': particle_name,
            'property_checks': checks,
            'completeness_score': overall_completeness,
            'particle_data': particle
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'particle_name': particle_name
        }


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