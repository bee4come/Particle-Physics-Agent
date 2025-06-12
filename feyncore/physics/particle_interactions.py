import pdg
from typing import Dict, List, Union, Tuple
import re

def get_particles_from_pdg(particle_names: List[str]) -> List[Dict]:
    """
    Query multiple particles from PDG API
    
    Args:
        particle_names: List of particle names or symbols to search
        
    Returns:
        List of particle dictionaries with properties
    """
    api = pdg.connect()  # 连接到 PDG 数据库
    results = []
    
    for name in particle_names:
        try:
            # 尝试通过名称查找粒子
            particles = api.get_particles_by_name(name, case_sensitive=False)
            if particles:
                # 获取第一个匹配项
                particle = particles[0]
                
                # 获取粒子的详细属性
                properties = {}
                for prop in particle.properties():
                    props_dict = prop.summary().as_dict()
                    data_type = prop.data_type
                    properties[data_type] = props_dict
                
                # 格式化信息
                result = {
                    "name": particle.name,
                    "pdg_id": particle.pdgid,
                    "symbol": particle.latex_name,
                    "mass_gev": properties.get("M", {}).get("value"),
                    "charge": properties.get("Q", {}).get("value"),
                    "spin": properties.get("J", {}).get("value"),
                    "lifetime_s": properties.get("tau", {}).get("value"),
                    "raw_data": properties  # 存储原始数据以供其他信息使用
                }
                results.append(result)
            else:
                print(f"警告: 未找到与'{name}'匹配的粒子")
        except Exception as e:
            print(f"查询粒子'{name}'时出错: {str(e)}")
    
    return results

def identify_interaction_type(particles: List[Dict]) -> List[str]:
    """
    Identify possible interaction types between particles
    
    Args:
        particles: List of particle dictionaries with properties
        
    Returns:
        List of possible interaction descriptions
    """
    interactions = []
    
    # Extract particle types and properties
    leptons = [p for p in particles if is_lepton(p)]
    quarks = [p for p in particles if is_quark(p)]
    bosons = [p for p in particles if is_boson(p)]
    
    # Check for specific interactions based on particle combinations
    if any(p.get('symbol') == 'γ' or p.get('name', '').lower() == 'photon' for p in particles):
        interactions.append("电磁相互作用")
    
    if any(p.get('symbol') in ['W+', 'W-', 'Z'] for p in particles):
        interactions.append("弱相互作用")
        
    if any(p.get('symbol') == 'g' or p.get('name', '').lower() == 'gluon' for p in particles):
        interactions.append("强相互作用")
        
    if any(p.get('symbol') == 'H' or p.get('name', '').lower() == 'higgs' for p in particles):
        interactions.append("希格斯相互作用")
    
    # Identify specific processes based on particle combinations
    process = identify_process(particles)
    if process:
        interactions.append(process)
    
    return interactions

def is_lepton(particle: Dict) -> bool:
    """Determine if a particle is a lepton"""
    lepton_names = ['electron', 'muon', 'tau', 'neutrino', 'e-', 'e+', 'μ-', 'μ+', 'τ-', 'τ+']
    name = particle.get('name', '').lower()
    symbol = particle.get('symbol', '')
    
    return any(lep in name for lep in lepton_names) or symbol in ['e-', 'e+', 'μ-', 'μ+', 'τ-', 'τ+', 'ν_e', 'ν_μ', 'ν_τ']

def is_quark(particle: Dict) -> bool:
    """Determine if a particle is a quark"""
    quark_names = ['quark', 'up', 'down', 'charm', 'strange', 'top', 'bottom', 'u', 'd', 'c', 's', 't', 'b']
    name = particle.get('name', '').lower()
    symbol = particle.get('symbol', '')
    
    return 'quark' in name or symbol in ['u', 'd', 'c', 's', 't', 'b']

def is_boson(particle: Dict) -> bool:
    """Determine if a particle is a boson"""
    spin = particle.get('spin')
    return spin is not None and int(spin) == spin  # Integer spin means boson

def identify_process(particles: List[Dict]) -> str:
    """Identify specific physical process based on particle combination"""
    symbols = [p.get('symbol', '') for p in particles]
    names = [p.get('name', '').lower() for p in particles]
    
    # Basic decay processes
    if 'W+' in symbols and 'e+' in symbols and 'ν_e' in symbols:
        return "W+ → e+ + ν_e (W玻色子衰变)"
    
    if 'Z' in symbols and 'e+' in symbols and 'e-' in symbols:
        return "Z → e+ + e- (Z玻色子衰变)"
    
    if 'H' in symbols and 'γ' in symbols and symbols.count('γ') >= 2:
        return "H → γγ (希格斯到光子衰变)"
    
    if 'μ-' in symbols and 'e-' in symbols and 'ν_μ' in symbols:
        return "μ- → e- + ν_e + ν_μ (缪子衰变)"
    
    # If no specific process identified, return empty
    return ""

def find_particle_interactions(particle_names: List[str]) -> Dict:
    """
    Find interactions between given particles using PDG data
    
    Args:
        particle_names: List of particle names to check
        
    Returns:
        Dictionary with interaction details
    """
    # Get particle data
    particles = get_particles_from_pdg(particle_names)
    
    if len(particles) < 2:
        return {
            "status": "错误",
            "message": "需要至少两个有效的粒子来检查相互作用"
        }
    
    # Identify interaction types
    interactions = identify_interaction_type(particles)
    
    # Create result
    result = {
        "status": "成功" if interactions else "未找到",
        "particles": [{
            "name": p.get("name"),
            "symbol": p.get("symbol"),
            "charge": p.get("charge"),
            "spin": p.get("spin"),
            "mass_gev": p.get("mass_gev")
        } for p in particles],
        "interactions": interactions
    }
    
    return result 