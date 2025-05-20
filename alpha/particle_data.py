"""
Provides physical property data for common particles
"""

PARTICLE_DATABASE = {
    # Leptons
    "e-": {"name": "Electron", "symbol": "e^-", "charge": -1, "spin": 0.5, "mass_gev": 0.000511, "type": "lepton"},
    "e+": {"name": "Positron", "symbol": "e^+", "charge": 1, "spin": 0.5, "mass_gev": 0.000511, "type": "lepton"},
    "mu-": {"name": "Muon", "symbol": "\\mu^-", "charge": -1, "spin": 0.5, "mass_gev": 0.10566, "type": "lepton"},
    "mu+": {"name": "Anti-muon", "symbol": "\\mu^+", "charge": 1, "spin": 0.5, "mass_gev": 0.10566, "type": "lepton"},
    "tau-": {"name": "Tau", "symbol": "\\tau^-", "charge": -1, "spin": 0.5, "mass_gev": 1.7768, "type": "lepton"},
    "tau+": {"name": "Anti-tau", "symbol": "\\tau^+", "charge": 1, "spin": 0.5, "mass_gev": 1.7768, "type": "lepton"},
    "ve": {"name": "Electron neutrino", "symbol": "\\nu_e", "charge": 0, "spin": 0.5, "mass_gev": 0, "type": "lepton"},
    "vmu": {"name": "Muon neutrino", "symbol": "\\nu_{\\mu}", "charge": 0, "spin": 0.5, "mass_gev": 0, "type": "lepton"},
    "vtau": {"name": "Tau neutrino", "symbol": "\\nu_{\\tau}", "charge": 0, "spin": 0.5, "mass_gev": 0, "type": "lepton"},
    "ve_bar": {"name": "Electron antineutrino", "symbol": "\\bar{\\nu}_e", "charge": 0, "spin": 0.5, "mass_gev": 0, "type": "lepton"},
    "vmu_bar": {"name": "Muon antineutrino", "symbol": "\\bar{\\nu}_{\\mu}", "charge": 0, "spin": 0.5, "mass_gev": 0, "type": "lepton"},
    "vtau_bar": {"name": "Tau antineutrino", "symbol": "\\bar{\\nu}_{\\tau}", "charge": 0, "spin": 0.5, "mass_gev": 0, "type": "lepton"},
    
    # Quarks
    "u": {"name": "Up quark", "symbol": "u", "charge": 2/3, "spin": 0.5, "mass_gev": 0.0022, "type": "quark"},
    "d": {"name": "Down quark", "symbol": "d", "charge": -1/3, "spin": 0.5, "mass_gev": 0.0047, "type": "quark"},
    "c": {"name": "Charm quark", "symbol": "c", "charge": 2/3, "spin": 0.5, "mass_gev": 1.27, "type": "quark"},
    "s": {"name": "Strange quark", "symbol": "s", "charge": -1/3, "spin": 0.5, "mass_gev": 0.095, "type": "quark"},
    "t": {"name": "Top quark", "symbol": "t", "charge": 2/3, "spin": 0.5, "mass_gev": 172.76, "type": "quark"},
    "b": {"name": "Bottom quark", "symbol": "b", "charge": -1/3, "spin": 0.5, "mass_gev": 4.18, "type": "quark"},
    "u_bar": {"name": "Anti-up quark", "symbol": "\\bar{u}", "charge": -2/3, "spin": 0.5, "mass_gev": 0.0022, "type": "quark"},
    "d_bar": {"name": "Anti-down quark", "symbol": "\\bar{d}", "charge": 1/3, "spin": 0.5, "mass_gev": 0.0047, "type": "quark"},
    "c_bar": {"name": "Anti-charm quark", "symbol": "\\bar{c}", "charge": -2/3, "spin": 0.5, "mass_gev": 1.27, "type": "quark"},
    "s_bar": {"name": "Anti-strange quark", "symbol": "\\bar{s}", "charge": 1/3, "spin": 0.5, "mass_gev": 0.095, "type": "quark"},
    "t_bar": {"name": "Anti-top quark", "symbol": "\\bar{t}", "charge": -2/3, "spin": 0.5, "mass_gev": 172.76, "type": "quark"},
    "b_bar": {"name": "Anti-bottom quark", "symbol": "\\bar{b}", "charge": 1/3, "spin": 0.5, "mass_gev": 4.18, "type": "quark"},
    
    # Gauge bosons
    "gamma": {"name": "Photon", "symbol": "\\gamma", "charge": 0, "spin": 1, "mass_gev": 0, "type": "boson"},
    "g": {"name": "Gluon", "symbol": "g", "charge": 0, "spin": 1, "mass_gev": 0, "type": "boson"},
    "W+": {"name": "W+ boson", "symbol": "W^+", "charge": 1, "spin": 1, "mass_gev": 80.377, "type": "boson"},
    "W-": {"name": "W- boson", "symbol": "W^-", "charge": -1, "spin": 1, "mass_gev": 80.377, "type": "boson"},
    "Z": {"name": "Z boson", "symbol": "Z^0", "charge": 0, "spin": 1, "mass_gev": 91.1876, "type": "boson"},
    "H": {"name": "Higgs boson", "symbol": "H", "charge": 0, "spin": 0, "mass_gev": 125.25, "type": "boson"},
    
    # Mesons
    "pi+": {"name": "π+ meson", "symbol": "\\pi^+", "charge": 1, "spin": 0, "mass_gev": 0.13957, "type": "meson"},
    "pi-": {"name": "π- meson", "symbol": "\\pi^-", "charge": -1, "spin": 0, "mass_gev": 0.13957, "type": "meson"},
    "pi0": {"name": "π0 meson", "symbol": "\\pi^0", "charge": 0, "spin": 0, "mass_gev": 0.13498, "type": "meson"},
    "K+": {"name": "K+ meson", "symbol": "K^+", "charge": 1, "spin": 0, "mass_gev": 0.49368, "type": "meson"},
    "K-": {"name": "K- meson", "symbol": "K^-", "charge": -1, "spin": 0, "mass_gev": 0.49368, "type": "meson"},
    "K0": {"name": "K0 meson", "symbol": "K^0", "charge": 0, "spin": 0, "mass_gev": 0.49761, "type": "meson"},
    
    # Baryons
    "p": {"name": "Proton", "symbol": "p", "charge": 1, "spin": 0.5, "mass_gev": 0.93827, "type": "baryon"},
    "n": {"name": "Neutron", "symbol": "n", "charge": 0, "spin": 0.5, "mass_gev": 0.93956, "type": "baryon"},
    "p_bar": {"name": "Antiproton", "symbol": "\\bar{p}", "charge": -1, "spin": 0.5, "mass_gev": 0.93827, "type": "baryon"},
    "n_bar": {"name": "Antineutron", "symbol": "\\bar{n}", "charge": 0, "spin": 0.5, "mass_gev": 0.93956, "type": "baryon"},
}

# Particle name aliases
PARTICLE_ALIASES = {
    # Symbol aliases
    "electron": "e-",
    "positron": "e+",
    "muon": "mu-",
    "anti-muon": "mu+",
    "tau": "tau-",
    "anti-tau": "tau+",
    "photon": "gamma",
    "gluon": "g",
    "higgs": "H",
    "proton": "p",
    "neutron": "n",
    "antiproton": "p_bar",
    "antineutron": "n_bar",
    
    # Chinese aliases (keeping for compatibility)
    "电子": "e-",
    "正电子": "e+",
    "μ子": "mu-",
    "反μ子": "mu+",
    "τ子": "tau-",
    "反τ子": "tau+",
    "光子": "gamma",
    "胶子": "g",
    "希格斯玻色子": "H",
    "质子": "p",
    "中子": "n",
    "反质子": "p_bar",
    "反中子": "n_bar",
    
    # Symbol shortcuts
    "e-": "e-",
    "e+": "e+",
    "μ-": "mu-",
    "μ+": "mu+",
    "τ-": "tau-",
    "τ+": "tau+",
    "γ": "gamma",
}

# Define interaction rules
INTERACTION_RULES = [
    # Electromagnetic interaction
    {
        "name": "Electromagnetic Interaction",
        "particles": ["gamma"],
        "description": "Force transmitted by photon exchange, affects all charged particles"
    },
    # Weak interaction
    {
        "name": "Weak Interaction",
        "particles": ["W+", "W-", "Z"],
        "description": "Force transmitted by W and Z bosons, affects all fermions"
    },
    # Strong interaction
    {
        "name": "Strong Interaction",
        "particles": ["g"],
        "description": "Force transmitted by gluons, affects all quarks and hadrons"
    },
    # Higgs interaction
    {
        "name": "Higgs Interaction",
        "particles": ["H"],
        "description": "Interaction related to mass, the Higgs boson gives mass to fundamental particles"
    }
]

# Specific interaction processes
INTERACTION_PROCESSES = [
    {
        "name": "Electron-Positron Annihilation",
        "particles": ["e-", "e+"],
        "products": ["gamma", "gamma"],
        "equation": "e^- + e^+ \\to \\gamma + \\gamma",
        "description": "Electron and positron annihilate to produce two photons"
    },
    {
        "name": "Electron-Electron Scattering",
        "particles": ["e-", "e-"],
        "products": ["e-", "e-"],
        "equation": "e^- + e^- \\to e^- + e^-",
        "description": "Electrons scatter via virtual photon exchange"
    },
    {
        "name": "Compton Scattering",
        "particles": ["gamma", "e-"],
        "products": ["gamma", "e-"],
        "equation": "\\gamma + e^- \\to \\gamma + e^-",
        "description": "Photon scatters off an electron, losing energy"
    },
    {
        "name": "Neutral Current Weak Interaction",
        "particles": ["Z", "e-"],
        "products": ["Z", "e-"],
        "equation": "Z + e^- \\to Z + e^-",
        "description": "Weak interaction mediated by Z boson, preserving particle flavors"
    },
    {
        "name": "Charged Current Weak Interaction",
        "particles": ["W+", "e-"],
        "products": ["ve", "W-"],
        "equation": "W^+ + e^- \\to \\nu_e + W^-",
        "description": "Weak interaction mediated by W boson, changing particle flavors"
    },
    {
        "name": "W Boson Decay",
        "particles": ["W+"],
        "products": ["e+", "ve"],
        "equation": "W^+ \\to e^+ + \\nu_e",
        "description": "W+ boson decays into positron and electron neutrino"
    },
    {
        "name": "Z Boson Decay",
        "particles": ["Z"],
        "products": ["e-", "e+"],
        "equation": "Z \\to e^- + e^+",
        "description": "Z boson decays into electron-positron pair"
    },
    {
        "name": "Muon Decay",
        "particles": ["mu-"],
        "products": ["e-", "ve", "vmu_bar"],
        "equation": "\\mu^- \\to e^- + \\nu_e + \\bar{\\nu}_{\\mu}",
        "description": "Muon decays into electron, electron neutrino and muon antineutrino"
    },
    {
        "name": "Tau Decay",
        "particles": ["tau-"],
        "products": ["e-", "ve", "vtau_bar"],
        "equation": "\\tau^- \\to e^- + \\nu_e + \\bar{\\nu}_{\\tau}",
        "description": "Tau lepton decays into electron, electron neutrino and tau antineutrino"
    },
    {
        "name": "Higgs Decay to Photon Pair",
        "particles": ["H"],
        "products": ["gamma", "gamma"],
        "equation": "H \\to \\gamma + \\gamma",
        "description": "Higgs boson decays into two photons via loop effects"
    },
    {
        "name": "Higgs Decay to Z Boson Pair",
        "particles": ["H"],
        "products": ["Z", "Z"],
        "equation": "H \\to Z + Z",
        "description": "Higgs boson decays into two Z bosons"
    },
    {
        "name": "Higgs Decay to W Boson Pair",
        "particles": ["H"],
        "products": ["W+", "W-"],
        "equation": "H \\to W^+ + W^-",
        "description": "Higgs boson decays into W+ and W- boson pair"
    },
    {
        "name": "Hadronization",
        "particles": ["u", "u_bar"],
        "products": ["g", "g"],
        "equation": "u + \\bar{u} \\to g + g",
        "description": "Quark-antiquark pair annihilation producing gluons"
    },
    {
        "name": "Quark Flavor Change",
        "particles": ["u", "W-"],
        "products": ["d", "W-"],
        "equation": "u + W^- \\to d + W^-",
        "description": "Up quark transforms to down quark via weak interaction"
    }
]

# TikZ Feynman diagram definitions
TIKZ_FEYNMAN_DIAGRAMS = {
    "Electron-Positron Annihilation": """
    % Modern approach using feynmandiagram
    \\feynmandiagram [horizontal=a to b] {
      i1 [particle=$e^-$] -- [fermion] a -- [fermion] i2 [particle=$e^+$],
      a -- [photon] b,
      f1 [particle=$\\gamma$] -- [photon] b -- [photon] f2 [particle=$\\gamma$],
    };
    
    % Traditional vertex approach as fallback
    % \\vertex (a) at (-1,1) {$e^-$};
    % \\vertex (b) at (-1,-1) {$e^+$};
    % \\vertex (c) at (0,0);
    % \\vertex (d) at (1,1) {$\\gamma$};
    % \\vertex (e) at (1,-1) {$\\gamma$};
    % 
    % \\diagram {
    %   (a) -- [fermion] (c),
    %   (b) -- [anti fermion] (c),
    %   (c) -- [boson] (d),
    %   (c) -- [boson] (e)
    % };
    """,
    
    "Electron-Electron Scattering": """
    % Modern approach using feynmandiagram
    \\feynmandiagram [horizontal=i1 to f1] {
      i1 [particle=$e^-$] -- [fermion] a -- [fermion] f1 [particle=$e^-$],
      i2 [particle=$e^-$] -- [fermion] b -- [fermion] f2 [particle=$e^-$],
      a -- [photon, edge label=$\\gamma$] b,
    };
    """,
    
    "Compton Scattering": """
    % Modern approach using feynmandiagram
    \\feynmandiagram [layered layout, horizontal=a to b] {
      i1 [particle=$\\gamma$] -- [photon] a -- [photon] f1 [particle=$\\gamma$],
      i2 [particle=$e^-$] -- [fermion] a -- [fermion] f2 [particle=$e^-$], 
    };
    """,
    
    "Neutral Current Weak Interaction": """
    \\vertex (a) at (-1.5,1) {$e^-$};
    \\vertex (b) at (-1.5,-1) {$Z^0$};
    \\vertex (c) at (0,1);
    \\vertex (d) at (0,-1);
    \\vertex (e) at (1.5,1) {$e^-$};
    \\vertex (f) at (1.5,-1) {$Z^0$};
    
    \\diagram {
      (a) -- [fermion] (c),
      (b) -- [boson] (d),
      (c) -- [fermion] (e),
      (d) -- [boson] (f),
      (c) -- [fermion, edge label=$\\nu$] (d)
    };""",
    
    "Charged Current Weak Interaction": """
    \\vertex (a) at (-1.5,1) {$e^-$};
    \\vertex (b) at (-1.5,-1) {$W^+$};
    \\vertex (c) at (0,0);
    \\vertex (e) at (1.5,1) {$\\nu_e$};
    \\vertex (f) at (1.5,-1) {$W^-$};
    
    \\diagram {
      (a) -- [fermion] (c) -- [fermion] (e),
      (b) -- [boson] (c) -- [boson] (f),
    };""",
    
    "W Boson Decay": """
    \\vertex (a) at (-1.5,0) {$W^+$};
    \\vertex (b) at (0,0);
    \\vertex (c) at (1.5,1) {$e^+$};
    \\vertex (d) at (1.5,-1) {$\\nu_e$};
    
    \\diagram {
      (a) -- [boson] (b),
      (b) -- [anti fermion] (c),
      (b) -- [fermion] (d)
    };""",
    
    "Z Boson Decay": """
    % Modern approach with spring layout
    \\feynmandiagram [vertical=a to b] {
      a [particle=$Z^0$] -- [boson] b,
      b -- [fermion] f1 [particle=$e^-$],
      b -- [anti fermion] f2 [particle=$e^+$],
    };
    """,
    
    "Muon Decay": """
    \\vertex (a) at (-1.5,0) {$\\mu^-$};
    \\vertex (b) at (0,0);
    \\vertex (c) at (1,0);
    \\vertex (d) at (2,1) {$e^-$};
    \\vertex (e) at (2,0) {$\\bar{\\nu}_{\\mu}$};
    \\vertex (f) at (2,-1) {$\\nu_e$};
    
    \\diagram {
      (a) -- [fermion] (b),
      (b) -- [fermion] (c),
      (c) -- [fermion] (d),
      (c) -- [anti fermion] (e),
      (b) -- [fermion] (f),
      (b) -- [boson, edge label=$W^-$] (c)
    };""",
    
    "Higgs Decay to Photon Pair": """
    % Modern approach with momentum arrows
    \\feynmandiagram [horizontal=a to b] {
      a [particle=$H$] -- [scalar, momentum=$p_H$] b,
      b -- [photon, momentum'=$k_1$] f1 [particle=$\\gamma$],
      b -- [photon, momentum'=$k_2$] f2 [particle=$\\gamma$],
    };
    """,
    
    # Default diagram with modern approach
    "DEFAULT": """
    % Modern approach with automatic layout
    \\feynmandiagram {
      i [particle=$in$] -- [fermion] a,
      a -- [fermion] f1 [particle=$out_1$],
      a -- [fermion] f2 [particle=$out_2$],
    };
    
    % Traditional approach as fallback
    % \\vertex (a) at (-1,0);
    % \\vertex (b) at (0,0);
    % \\vertex (c) at (1,1);
    % \\vertex (d) at (1,-1);
    % 
    % \\diagram {
    %   (a) -- [fermion] (b),
    %   (b) -- [fermion] (c),
    %   (b) -- [fermion] (d)
    % };
    """
}

def get_particle_by_name_or_alias(particle_name: str):
    """
    Get particle data by name or alias
    
    Args:
        particle_name: Particle name or alias
        
    Returns:
        Particle data dictionary or None
    """
    # Normalize name
    name_lower = particle_name.lower()
    
    # Direct lookup
    if particle_name in PARTICLE_DATABASE:
        particle = PARTICLE_DATABASE[particle_name].copy()
        particle["id"] = particle_name
        return particle
        
    # Lookup by alias    
    if name_lower in PARTICLE_ALIASES:
        particle_id = PARTICLE_ALIASES[name_lower]
        if particle_id in PARTICLE_DATABASE:
            particle = PARTICLE_DATABASE[particle_id].copy()
            particle["id"] = particle_id
            return particle
    
    return None

def find_interactions(particle_ids):
    """
    Find interactions between particles
    
    Args:
        particle_ids: List of particle IDs
        
    Returns:
        List of interaction information
    """
    interactions = []
    
    # Check fundamental interactions
    for rule in INTERACTION_RULES:
        rule_particles = set(rule["particles"])
        if any(p in particle_ids for p in rule_particles):
            interactions.append({
                "name": rule["name"],
                "description": rule["description"],
                "type": "fundamental"
            })
    
    # Check specific processes
    for process in INTERACTION_PROCESSES:
        process_particles = set(process["particles"])
        if process_particles.issubset(set(particle_ids)) or len(process_particles & set(particle_ids)) >= 1:
            # Copy all process information
            process_info = process.copy()
            process_info["type"] = "process"
            interactions.append(process_info)
    
    return interactions 