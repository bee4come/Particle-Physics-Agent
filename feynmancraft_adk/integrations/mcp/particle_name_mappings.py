"""
Particle Name Mappings for MCP Server

This module contains comprehensive mappings from common particle names
to the notation expected by the ParticlePhysics MCP Server.

The MCP server uses specific naming conventions:
- Leptons: e-, e+, mu-, mu+, tau-, tau+
- Quarks: u, d, c, s, t, b (and their antiparticles: ubar, dbar, etc.)
- Baryons: p (proton), n (neutron), pbar (antiproton), etc.
- Bosons: gamma (photon), g (gluon), W+, W-, Z, H (Higgs)
"""

from typing import Optional

# Comprehensive particle name mappings
PARTICLE_NAME_MAPPINGS = {
    # ===== LEPTONS =====
    # Electrons
    "electron": "e-",
    "positron": "e+",
    "antielectron": "e+",
    "e-": "e-",  # Already correct
    "e+": "e+",  # Already correct
    
    # Muons
    "muon": "mu-",
    "antimuon": "mu+",
    "mu-": "mu-",  # Already correct
    "mu+": "mu+",  # Already correct
    "muon-": "mu-",
    "muon+": "mu+",
    "μ": "mu-",  # Greek mu
    "μ-": "mu-",
    "μ+": "mu+",
    
    # Tau leptons
    "tau": "tau-",
    "antitau": "tau+",
    "tau lepton": "tau-",
    "antitau lepton": "tau+",
    "tau-": "tau-",  # Already correct
    "tau+": "tau+",  # Already correct
    "tauon": "tau-",
    "antitauon": "tau+",
    "τ": "tau-",  # Greek tau
    "τ-": "tau-",
    "τ+": "tau+",
    
    # ===== NEUTRINOS =====
    # Electron neutrinos
    "electron neutrino": "nu_e",
    "electron antineutrino": "nubar_e",
    "electron anti-neutrino": "nubar_e",
    "ve": "nu_e",
    "vebar": "nubar_e",
    "nu_e": "nu_e",  # Already correct
    "nu_e_bar": "nubar_e",  # Already correct
    "nue": "nu_e",  # Map old format to new
    "nuebar": "nubar_e",  # Map old format to new
    "ν_e": "nu_e",  # Greek nu
    "ν_ebar": "nubar_e",
    
    # Muon neutrinos
    "muon neutrino": "nu_mu",
    "muon antineutrino": "nubar_mu",
    "muon anti-neutrino": "nubar_mu",
    "vmu": "nu_mu",
    "vmubar": "nubar_mu",
    "nu_mu": "nu_mu",  # Already correct
    "nu_mu_bar": "nubar_mu",  # Already correct
    "numu": "nu_mu",  # Map old format to new
    "numubar": "nubar_mu",  # Map old format to new
    
    # Tau neutrinos
    "tau neutrino": "nu_tau",
    "tau antineutrino": "nubar_tau",
    "tau anti-neutrino": "nubar_tau",
    "vtau": "nu_tau",
    "vtaubar": "nubar_tau",
    "nu_tau": "nu_tau",  # Already correct
    "nu_tau_bar": "nubar_tau",  # Already correct
    "nutau": "nu_tau",  # Map old format to new
    "nutaubar": "nubar_tau",  # Map old format to new
    
    # ===== QUARKS =====
    # Up quarks
    "up": "u",
    "up quark": "u",
    "upquark": "u",
    "anti-up": "ubar",
    "antiup": "ubar",
    "anti-up quark": "ubar",
    "antip up quark": "ubar",
    "u": "u",  # Already correct
    "ubar": "ubar",  # Already correct
    
    # Down quarks
    "down": "d",
    "down quark": "d",
    "downquark": "d",
    "anti-down": "dbar",
    "antidown": "dbar",
    "anti-down quark": "dbar",
    "antidown quark": "dbar",
    "anti down quark": "dbar",
    "d": "d",  # Already correct
    "dbar": "dbar",  # Already correct
    
    # Charm quarks
    "charm": "c",
    "charm quark": "c",
    "charmquark": "c",
    "anti-charm": "cbar",
    "anticharm": "cbar",
    "anti-charm quark": "cbar",
    "anticharm quark": "cbar",
    "anti charm quark": "cbar",
    "c": "c",  # Already correct
    "cbar": "cbar",  # Already correct
    
    # Strange quarks
    "strange": "s",
    "strange quark": "s",
    "strangequark": "s",
    "anti-strange": "sbar",
    "antistrange": "sbar",
    "anti-strange quark": "sbar",
    "antistrange quark": "sbar",
    "anti strange quark": "sbar",
    "s": "s",  # Already correct
    "sbar": "sbar",  # Already correct
    
    # Top quarks
    "top": "t",
    "top quark": "t",
    "topquark": "t",
    "truth": "t",  # Alternative name
    "truth quark": "t",
    "anti-top": "tbar",
    "antitop": "tbar",
    "anti-top quark": "tbar",
    "antitop quark": "tbar",
    "anti top quark": "tbar",
    "t": "t",  # Already correct
    "tbar": "tbar",  # Already correct
    
    # Bottom quarks
    "bottom": "b",
    "bottom quark": "b",
    "bottomquark": "b",
    "beauty": "b",  # Alternative name
    "beauty quark": "b",
    "anti-bottom": "bbar",
    "antibottom": "bbar",
    "anti-bottom quark": "bbar",
    "antibottom quark": "bbar",
    "anti bottom quark": "bbar",
    "anti-beauty": "bbar",
    "antibeauty": "bbar",
    "anti-beauty quark": "bbar",
    "b": "b",  # Already correct
    "bbar": "bbar",  # Already correct
    
    # ===== BARYONS =====
    # Nucleons
    "proton": "p",
    "antiproton": "pbar",
    "anti-proton": "pbar",
    "p": "p",  # Already correct
    "pbar": "pbar",  # Already correct
    "p+": "p",
    "p-": "pbar",
    
    "neutron": "n",
    "antineutron": "nbar",
    "anti-neutron": "nbar",
    "n": "n",  # Already correct
    "nbar": "nbar",  # Already correct
    "n0": "n",
    
    # Lambda baryons
    "lambda": "Lambda0",
    "lambda0": "Lambda0",
    "antilambda": "Lambdabar0",
    "anti-lambda": "Lambdabar0",
    "Λ": "Lambda0",  # Greek Lambda
    "Λ0": "Lambda0",
    "λ": "Lambda0",  # Lowercase lambda (after normalization)
    "λ0": "Lambda0",
    
    # Sigma baryons
    "sigma+": "Sigma+",
    "sigma-": "Sigma-",
    "sigma0": "Sigma0",
    "antisigma+": "Sigmabar-",
    "antisigma-": "Sigmabar+",
    "antisigma0": "Sigmabar0",
    "Σ+": "Sigma+",  # Greek Sigma
    "Σ-": "Sigma-",
    "Σ0": "Sigma0",
    "σ+": "Sigma+",  # Lowercase sigma (after normalization)
    "σ-": "Sigma-",
    "σ0": "Sigma0",
    
    # Xi baryons
    "xi-": "Xi-",
    "xi0": "Xi0",
    "antixi-": "Xibar+",
    "antixi0": "Xibar0",
    
    # Omega baryons
    "omega-": "Omega-",
    "antiomega-": "Omegabar+",
    "Ω-": "Omega-",  # Greek Omega
    "Ω+": "Omegabar+",
    "ω-": "Omega-",  # Lowercase omega (after normalization)
    "ω+": "Omegabar+",
    
    # ===== GAUGE BOSONS =====
    # Photon
    "photon": "gamma",
    "gamma": "gamma",  # Already correct
    "γ": "gamma",
    
    # Gluon
    "gluon": "g",
    "g": "g",  # Already correct
    
    # W bosons
    "w boson": "W+",
    "w+ boson": "W+",
    "w- boson": "W-",
    "w+": "W+",
    "w-": "W-",
    "W+": "W+",  # Already correct
    "W-": "W-",  # Already correct
    "wboson": "W+",
    "w plus": "W+",
    "w minus": "W-",
    
    # Z boson
    "z boson": "Z0",
    "z0 boson": "Z0",
    "z": "Z0",
    "z0": "Z0",
    "Z": "Z0",  # Map to Z0
    "Z0": "Z0",  # Already correct
    "z zero": "Z0",
    "neutral z": "Z0",
    
    # Higgs boson
    "higgs": "H",
    "higgs boson": "H",
    "h": "H",
    "H": "H",  # Already correct
    "higgs0": "H",
    "h0": "H",
    
    # ===== MESONS =====
    # Pions
    "pion": "pi+",  # Default to positive
    "pion+": "pi+",
    "pion-": "pi-",
    "pion0": "pi0",
    "pi+": "pi+",  # Already correct
    "pi-": "pi-",  # Already correct
    "pi0": "pi0",  # Already correct
    "pi meson": "pi+",
    "charged pion": "pi+",
    "neutral pion": "pi0",
    "π": "pi+",  # Greek pi
    "π+": "pi+",
    "π-": "pi-",
    "π0": "pi0",
    
    # Kaons
    "kaon": "K+",  # Default to positive
    "kaon+": "K+",
    "kaon-": "K-",
    "kaon0": "K0",
    "antikaon0": "Kbar0",
    "K+": "K+",  # Already correct
    "K-": "K-",  # Already correct
    "K0": "K0",  # Already correct
    "K0bar": "Kbar0",  # Fixed notation
    "k meson": "K+",
    "k+": "K+",
    "k-": "K-",
    "k0": "K0",
    
    # D mesons
    "d meson": "D+",
    "d+": "D+",
    "d-": "D-",
    "d0": "D0",
    "D+": "D+",  # Already correct
    "D-": "D-",  # Already correct
    "D0": "D0",  # Already correct
    
    # B mesons
    "b meson": "B+",
    "b+": "B+",
    "b-": "B-",
    "b0": "B0",
    "B+": "B+",  # Already correct
    "B-": "B-",  # Already correct
    "B0": "B0",  # Already correct
    
    # Eta mesons
    "eta": "eta",
    "eta prime": "eta^'(958)0",
    "etaprime": "eta^'(958)0",
    "η": "eta",
    "η'": "eta^'(958)0",
    
    # Rho mesons
    "rho": "rho(770)+",
    "rho+": "rho(770)+",
    "rho-": "rho(770)-",
    "rho0": "rho(770)0",
    "ρ": "rho(770)+",
    "ρ+": "rho(770)+",
    "ρ-": "rho(770)-",
    "ρ0": "rho(770)0",
    
    # J/psi
    "jpsi": "J/psi(1S)",
    "j/psi": "J/psi(1S)",
    "J/psi": "J/psi(1S)",  # Updated
    "charmonium": "J/psi(1S)",
    
    # Upsilon
    "upsilon": "Upsilon(1S)",
    "bottomonium": "Upsilon(1S)",
    "Υ": "Upsilon(1S)",
}

# Simplified mappings for specific use cases
BASIC_MAPPINGS = {
    # Most common particles
    "electron": "e-",
    "positron": "e+",
    "muon": "mu-",
    "antimuon": "mu+",
    "proton": "p",
    "antiproton": "pbar",
    "neutron": "n",
    "antineutron": "nbar",
    "photon": "gamma",
    "up": "u",
    "down": "d",
    "up quark": "u",
    "down quark": "d",
}


def normalize_particle_name(name: str, use_basic: bool = False) -> str:
    """
    Normalize a particle name to MCP server notation.
    
    Args:
        name: The particle name to normalize
        use_basic: If True, only use basic mappings (faster but less comprehensive)
        
    Returns:
        The normalized particle name, or the original if no mapping found
    """
    # Normalize the input
    normalized = name.lower().strip()
    
    # Choose mapping dictionary
    mappings = BASIC_MAPPINGS if use_basic else PARTICLE_NAME_MAPPINGS
    
    # Return mapped name or original
    return mappings.get(normalized, name)


def get_antiparticle_name(particle: str) -> Optional[str]:
    """
    Get the antiparticle name for a given particle.
    
    Args:
        particle: The particle name (in MCP notation)
        
    Returns:
        The antiparticle name, or None if not applicable
    """
    antiparticle_map = {
        # Leptons
        "e-": "e+",
        "e+": "e-",
        "mu-": "mu+",
        "mu+": "mu-",
        "tau-": "tau+",
        "tau+": "tau-",
        
        # Neutrinos
        "nu_e": "nubar_e",
        "nubar_e": "nu_e",
        "nu_mu": "nubar_mu",
        "nubar_mu": "nu_mu",
        "nu_tau": "nubar_tau",
        "nubar_tau": "nu_tau",
        
        # Quarks
        "u": "ubar",
        "ubar": "u",
        "d": "dbar",
        "dbar": "d",
        "c": "cbar",
        "cbar": "c",
        "s": "sbar",
        "sbar": "s",
        "t": "tbar",
        "tbar": "t",
        "b": "bbar",
        "bbar": "b",
        
        # Baryons
        "p": "pbar",
        "pbar": "p",
        "n": "nbar",
        "nbar": "n",
        
        # W bosons
        "W+": "W-",
        "W-": "W+",
        
        # Mesons
        "pi+": "pi-",
        "pi-": "pi+",
        "K+": "K-",
        "K-": "K+",
        "D+": "D-",
        "D-": "D+",
        "B+": "B-",
        "B-": "B+",
    }
    
    return antiparticle_map.get(particle)


# Export all mappings and functions
__all__ = [
    'PARTICLE_NAME_MAPPINGS',
    'BASIC_MAPPINGS',
    'normalize_particle_name',
    'get_antiparticle_name'
] 