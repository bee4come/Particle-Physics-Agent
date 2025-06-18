"""
Particle Physics Database for FeynmanCraft ADK.

This module contains comprehensive particle data based on PDG (Particle Data Group) standards.
Provides particle properties, quantum numbers, masses, lifetimes, and decay information.
"""

from typing import Dict, Any, List, Optional


class ParticleDatabase:
    """Comprehensive particle physics database."""
    
    def __init__(self):
        """Initialize the particle database."""
        self._particle_db = self._init_particle_database()
    
    def _init_particle_database(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive particle database with PDG data."""
        return {
            'electron': {
                'name': 'electron', 'symbol': 'e-', 'pdg_id': 11,
                'alt_names': ['e-', 'e minus', 'beta minus'],
                'mass': {'value': 0.5109989461, 'unit': 'MeV', 'uncertainty': 0.0000000031},
                'charge': -1, 'spin': 0.5, 'type': 'lepton', 'generation': 1,
                'lifetime': 'stable', 
                'quantum_numbers': {'J': 0.5, 'P': 1, 'C': -1, 'lepton_number': 1}
            },
            'positron': {
                'name': 'positron', 'symbol': 'e+', 'pdg_id': -11,
                'alt_names': ['e+', 'e plus', 'beta plus', 'antielectron'],
                'mass': {'value': 0.5109989461, 'unit': 'MeV', 'uncertainty': 0.0000000031},
                'charge': 1, 'spin': 0.5, 'type': 'lepton', 'generation': 1,
                'lifetime': 'stable',
                'quantum_numbers': {'J': 0.5, 'P': 1, 'C': -1, 'lepton_number': -1}
            },
            'muon': {
                'name': 'muon', 'symbol': 'μ-', 'pdg_id': 13,
                'alt_names': ['mu-', 'mu minus', 'muon minus'],
                'mass': {'value': 105.6583745, 'unit': 'MeV', 'uncertainty': 0.0000024},
                'charge': -1, 'spin': 0.5, 'type': 'lepton', 'generation': 2,
                'lifetime': {'value': 2.1969811e-6, 'unit': 's', 'uncertainty': 0.0000022e-6},
                'quantum_numbers': {'J': 0.5, 'P': 1, 'C': -1, 'lepton_number': 1}
            },
            'antimuon': {
                'name': 'antimuon', 'symbol': 'μ+', 'pdg_id': -13,
                'alt_names': ['mu+', 'mu plus', 'muon plus'],
                'mass': {'value': 105.6583745, 'unit': 'MeV', 'uncertainty': 0.0000024},
                'charge': 1, 'spin': 0.5, 'type': 'lepton', 'generation': 2,
                'lifetime': {'value': 2.1969811e-6, 'unit': 's', 'uncertainty': 0.0000022e-6},
                'quantum_numbers': {'J': 0.5, 'P': 1, 'C': -1, 'lepton_number': -1}
            },
            'tau': {
                'name': 'tau', 'symbol': 'τ-', 'pdg_id': 15,
                'alt_names': ['tau-', 'tau minus', 'tauon'],
                'mass': {'value': 1776.86, 'unit': 'MeV', 'uncertainty': 0.12},
                'charge': -1, 'spin': 0.5, 'type': 'lepton', 'generation': 3,
                'lifetime': {'value': 2.903e-13, 'unit': 's', 'uncertainty': 0.005e-13},
                'quantum_numbers': {'J': 0.5, 'P': 1, 'C': -1, 'lepton_number': 1}
            },
            'proton': {
                'name': 'proton', 'symbol': 'p', 'pdg_id': 2212,
                'alt_names': ['p+', 'hydrogen nucleus'],
                'mass': {'value': 938.2720813, 'unit': 'MeV', 'uncertainty': 0.0000058},
                'charge': 1, 'spin': 0.5, 'type': 'baryon', 'quark_content': 'uud',
                'lifetime': 'stable',
                'quantum_numbers': {'J': 0.5, 'P': 1, 'I': 0.5, 'baryon_number': 1}
            },
            'neutron': {
                'name': 'neutron', 'symbol': 'n', 'pdg_id': 2112,
                'alt_names': ['n0', 'neutron'],
                'mass': {'value': 939.5654133, 'unit': 'MeV', 'uncertainty': 0.0000058},
                'charge': 0, 'spin': 0.5, 'type': 'baryon', 'quark_content': 'udd',
                'lifetime': {'value': 879.4, 'unit': 's', 'uncertainty': 0.6},
                'quantum_numbers': {'J': 0.5, 'P': 1, 'I': 0.5, 'baryon_number': 1}
            },
            'photon': {
                'name': 'photon', 'symbol': 'γ', 'pdg_id': 22,
                'alt_names': ['gamma', 'light', 'electromagnetic radiation'],
                'mass': {'value': 0, 'unit': 'MeV', 'uncertainty': 0},
                'charge': 0, 'spin': 1, 'type': 'boson', 'force': 'electromagnetic',
                'lifetime': 'stable',
                'quantum_numbers': {'J': 1, 'P': -1, 'C': -1}
            },
            'pion_plus': {
                'name': 'pion_plus', 'symbol': 'π+', 'pdg_id': 211,
                'alt_names': ['pi+', 'pion plus'],
                'mass': {'value': 139.57039, 'unit': 'MeV', 'uncertainty': 0.00018},
                'charge': 1, 'spin': 0, 'type': 'meson', 'quark_content': 'ud̄',
                'lifetime': {'value': 2.6033e-8, 'unit': 's', 'uncertainty': 0.0005e-8},
                'quantum_numbers': {'J': 0, 'P': -1, 'I': 1}
            },
            'pion_minus': {
                'name': 'pion_minus', 'symbol': 'π-', 'pdg_id': -211,
                'alt_names': ['pi-', 'pion minus'],
                'mass': {'value': 139.57039, 'unit': 'MeV', 'uncertainty': 0.00018},
                'charge': -1, 'spin': 0, 'type': 'meson', 'quark_content': 'dū',
                'lifetime': {'value': 2.6033e-8, 'unit': 's', 'uncertainty': 0.0005e-8},
                'quantum_numbers': {'J': 0, 'P': -1, 'I': 1}
            },
            'w_boson': {
                'name': 'w_boson', 'symbol': 'W±', 'pdg_id': 24,
                'alt_names': ['W boson', 'W plus', 'W minus', 'weak boson'],
                'mass': {'value': 80377, 'unit': 'MeV', 'uncertainty': 12},
                'charge': '±1', 'spin': 1, 'type': 'boson', 'force': 'weak',
                'lifetime': {'value': 3.156e-25, 'unit': 's'},
                'quantum_numbers': {'J': 1, 'P': -1}
            },
            'z_boson': {
                'name': 'z_boson', 'symbol': 'Z⁰', 'pdg_id': 23,
                'alt_names': ['Z boson', 'Z zero', 'neutral weak boson'],
                'mass': {'value': 91187.6, 'unit': 'MeV', 'uncertainty': 2.1},
                'charge': 0, 'spin': 1, 'type': 'boson', 'force': 'weak',
                'lifetime': {'value': 2.64e-25, 'unit': 's'},
                'quantum_numbers': {'J': 1, 'P': -1}
            }
        }
    
    def get_particle(self, query: str) -> Optional[Dict[str, Any]]:
        """Get particle by name, symbol, or PDG ID."""
        query_lower = query.lower().strip()
        
        # Direct name match
        if query_lower in self._particle_db:
            return self._particle_db[query_lower]
        
        # Search by symbol, alt_names, or PDG ID
        for particle_data in self._particle_db.values():
            # Symbol match
            if particle_data.get('symbol', '').lower() == query_lower:
                return particle_data
            
            # Alt names match
            alt_names = particle_data.get('alt_names', [])
            if any(alt.lower() == query_lower for alt in alt_names):
                return particle_data
            
            # PDG ID match
            try:
                query_pdg = int(query)
                if particle_data.get('pdg_id') == query_pdg:
                    return particle_data
            except ValueError:
                pass
        
        return None
    
    def search_particles(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search particles with fuzzy matching."""
        query_lower = query.lower().strip()
        results = []
        
        # Exact matches first
        exact_match = self.get_particle(query)
        if exact_match:
            results.append(exact_match)
        
        # Fuzzy matches for remaining slots
        for particle_data in self._particle_db.values():
            if len(results) >= max_results:
                break
            
            if exact_match and particle_data == exact_match:
                continue
            
            # Check if query is substring of name or alt names
            if (query_lower in particle_data['name'].lower() or
                any(query_lower in alt.lower() for alt in particle_data.get('alt_names', []))):
                results.append(particle_data)
        
        return results[:max_results]
    
    def list_particles(self, particle_type: str = "all", charge_filter: str = "all") -> List[Dict[str, Any]]:
        """List particles with filtering options."""
        particles = list(self._particle_db.values())
        
        # Filter by type
        if particle_type != "all":
            particles = [p for p in particles if p.get('type') == particle_type]
        
        # Filter by charge
        if charge_filter == "neutral":
            particles = [p for p in particles if p.get('charge') == 0]
        elif charge_filter == "positive":
            particles = [p for p in particles if p.get('charge', 0) > 0]
        elif charge_filter == "negative":
            particles = [p for p in particles if p.get('charge', 0) < 0]
        
        return particles


# Global particle database instance
particle_db = ParticleDatabase() 