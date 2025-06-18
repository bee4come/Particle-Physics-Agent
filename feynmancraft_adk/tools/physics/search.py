"""
Physics rules search tools.
"""

import asyncio
from typing import List, Dict, Any, Optional
import logging

from .embedding_manager import get_rules_manager
from ..kb.embeddings import get_embedding, cosine_similarity

logger = logging.getLogger(__name__)


async def search_physics_rules(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Perform semantic search for physics rules.
    
    Args:
        query: Natural language query about physics rules
        top_k: Number of top results to return
        
    Returns:
        List of relevant physics rules sorted by similarity
    """
    try:
        # Get rules manager and ensure it's initialized
        manager = get_rules_manager()
        await manager.initialize()
        
        if not manager.physics_rules or not manager.embeddings_cache:
            return [{"error": "Physics rules or embeddings are not available."}]
        
        # Get query embedding
        query_embedding = await asyncio.to_thread(
            get_embedding, 
            query, 
            manager.model_name
        )
        
        if not query_embedding:
            return [{"error": "Failed to get query embedding"}]
        
        # Calculate similarities
        similarities = []
        for rule in manager.physics_rules:
            rule_number = rule.get("rule_number")
            if rule_number in manager.embeddings_cache:
                rule_embedding = manager.embeddings_cache[rule_number]
                similarity = cosine_similarity(query_embedding, rule_embedding)
                similarities.append((similarity, rule))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for similarity, rule in similarities[:top_k]:
            result = rule.copy()
            result["similarity_score"] = similarity
            results.append(result)
            
        logger.info(f"Found {len(results)} physics rules for query: {query[:50]}...")
        return results
        
    except Exception as e:
        logger.error(f"Error in physics rules search: {e}")
        return [{"error": f"Search failed: {str(e)}"}]


def filter_rules_by_type(rules: List[Dict[str, Any]], rule_type: str) -> List[Dict[str, Any]]:
    """
    Filter rules by type based on content analysis.
    
    Args:
        rules: List of physics rules
        rule_type: Type of rule to filter for
        
    Returns:
        Filtered rules
    """
    rule_type_lower = rule_type.lower()
    type_keywords = {
        'conservation': ['conservation', 'conserved', 'preserve'],
        'decay': ['decay', 'decays', 'lifetime'],
        'interaction': ['interaction', 'force', 'coupling'],
        'symmetry': ['symmetry', 'symmetric', 'invariant'],
        'quantum_numbers': ['quantum number', 'charge', 'spin', 'isospin'],
        'kinematics': ['momentum', 'energy', 'mass', 'velocity'],
        'selection_rules': ['forbidden', 'allowed', 'selection rule']
    }
    
    keywords = type_keywords.get(rule_type_lower, [rule_type_lower])
    
    filtered_rules = []
    for rule in rules:
        content = rule.get("content", "").lower()
        category = rule.get("category", "").lower()
        
        if any(keyword in content or keyword in category for keyword in keywords):
            filtered_rules.append(rule)
            
    return filtered_rules


def rank_rules(rules: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Re-rank physics rules based on additional criteria.
    
    Args:
        rules: List of physics rules with similarity scores
        query: Original query
        
    Returns:
        Re-ranked rules
    """
    query_lower = query.lower()
    query_words = query_lower.split()
    
    for rule in rules:
        score = rule.get("similarity_score", 0.0)
        content = rule.get("content", "").lower()
        category = rule.get("category", "").lower()
        
        # Boost rules with exact query word matches in content
        word_matches = sum(1 for word in query_words if word in content)
        score += word_matches * 0.1
        
        # Boost rules with category matches
        if any(word in category for word in query_words):
            score += 0.15
            
        # Boost conservation rules for conservation queries
        if "conservation" in query_lower and "conservation" in content:
            score += 0.2
            
        # Boost decay rules for decay queries
        if "decay" in query_lower and "decay" in content:
            score += 0.2
            
        # Boost interaction rules for interaction queries
        if "interaction" in query_lower and "interaction" in content:
            score += 0.2
            
        rule["final_score"] = score
    
    # Sort by final score
    rules.sort(key=lambda x: x.get("final_score", 0), reverse=True)
    return rules


def search_rules_by_particles(particles: List[str], top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Search for physics rules involving specific particles.
    
    Args:
        particles: List of particle names to search for
        top_k: Maximum number of results to return
        
    Returns:
        List of relevant physics rules
    """
    try:
        manager = get_rules_manager()
        
        # Simple text-based search for particles in rule content
        particles_lower = [p.lower() for p in particles]
        matching_rules = []
        
        for rule in manager.physics_rules:
            content = rule.get("content", "").lower()
            rule_particles = rule.get("particles", [])
            
            # Check if any particle is mentioned in content
            content_match = any(particle in content for particle in particles_lower)
            
            # Check if any particle is in the particles list
            particles_match = False
            if isinstance(rule_particles, list):
                rule_particles_lower = [p.lower() for p in rule_particles]
                particles_match = any(p in rule_particles_lower for p in particles_lower)
            
            if content_match or particles_match:
                # Calculate relevance score
                score = 0.0
                for particle in particles_lower:
                    if particle in content:
                        score += content.count(particle) * 0.3
                    if isinstance(rule_particles, list) and particle in [p.lower() for p in rule_particles]:
                        score += 0.5
                
                rule_copy = rule.copy()
                rule_copy["relevance_score"] = score
                matching_rules.append(rule_copy)
        
        # Sort by relevance score
        matching_rules.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        logger.info(f"Found {len(matching_rules)} rules for particles: {particles}")
        return matching_rules[:top_k]
        
    except Exception as e:
        logger.error(f"Error searching rules by particles: {e}")
        return []


def search_rules_by_process(process_description: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for physics rules relevant to a specific process.
    
    Args:
        process_description: Description of the physics process
        top_k: Number of top results to return
        
    Returns:
        List of relevant physics rules
    """
    # Extract key terms from the process description
    process_lower = process_description.lower()
    key_terms = []
    
    # Physics process types
    if "decay" in process_lower:
        key_terms.extend(["decay", "lifetime", "branching"])
    if "scattering" in process_lower:
        key_terms.extend(["scattering", "cross section", "interaction"])
    if "annihilation" in process_lower:
        key_terms.extend(["annihilation", "antiparticle"])
    if "production" in process_lower:
        key_terms.extend(["production", "creation"])
    if "collision" in process_lower:
        key_terms.extend(["collision", "scattering"])
        
    # Conservation laws
    if any(word in process_lower for word in ["energy", "momentum", "charge", "conservation"]):
        key_terms.extend(["conservation", "conserved"])
        
    try:
        manager = get_rules_manager()
        matching_rules = []
        
        for rule in manager.physics_rules:
            content = rule.get("content", "").lower()
            category = rule.get("category", "").lower()
            
            # Calculate relevance score
            score = 0.0
            
            # Check for key terms
            for term in key_terms:
                if term in content:
                    score += 0.4
                if term in category:
                    score += 0.3
                    
            # Check for exact phrase matches
            if any(phrase in content for phrase in process_lower.split() if len(phrase) > 3):
                score += 0.5
                
            if score > 0:
                rule_copy = rule.copy()
                rule_copy["process_relevance_score"] = score
                matching_rules.append(rule_copy)
        
        # Sort by relevance score
        matching_rules.sort(key=lambda x: x.get("process_relevance_score", 0), reverse=True)
        
        logger.info(f"Found {len(matching_rules)} rules for process: {process_description[:50]}...")
        return matching_rules[:top_k]
        
    except Exception as e:
        logger.error(f"Error searching rules by process: {e}")
        return []


def get_conservation_rules() -> List[Dict[str, Any]]:
    """
    Get all conservation-related physics rules.
    
    Returns:
        List of conservation rules
    """
    try:
        manager = get_rules_manager()
        conservation_rules = []
        
        for rule in manager.physics_rules:
            content = rule.get("content", "").lower()
            category = rule.get("category", "").lower()
            
            if ("conservation" in content or "conserved" in content or 
                "conservation" in category):
                conservation_rules.append(rule)
                
        logger.info(f"Found {len(conservation_rules)} conservation rules")
        return conservation_rules
        
    except Exception as e:
        logger.error(f"Error getting conservation rules: {e}")
        return []


def validate_process_against_rules(
    process_description: str, 
    particles_involved: List[str]
) -> Dict[str, Any]:
    """
    Validate a physics process against relevant rules.
    
    Args:
        process_description: Description of the process
        particles_involved: List of particles in the process
        
    Returns:
        Validation result with applicable rules and violations
    """
    try:
        # Get relevant rules
        process_rules = search_rules_by_process(process_description, top_k=10)
        particle_rules = search_rules_by_particles(particles_involved, top_k=10)
        conservation_rules = get_conservation_rules()
        
        # Combine and deduplicate rules
        all_rules = {}
        for rule in process_rules + particle_rules + conservation_rules:
            rule_number = rule.get("rule_number")
            if rule_number:
                all_rules[rule_number] = rule
        
        applicable_rules = list(all_rules.values())
        
        # Basic validation logic would go here
        # For now, return the applicable rules
        validation_result = {
            "process": process_description,
            "particles": particles_involved,
            "applicable_rules": applicable_rules,
            "total_rules_checked": len(applicable_rules),
            "validation_status": "rules_identified",
            "violations": [],  # Would be populated by actual validation logic
            "recommendations": []
        }
        
        return validation_result
        
    except Exception as e:
        logger.error(f"Error validating process: {e}")
        return {
            "process": process_description,
            "particles": particles_involved,
            "error": str(e),
            "validation_status": "failed"
        }