"""
Data loading utilities for Physics Rules.
"""

import json
import os
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_rules_data_path() -> str:
    """
    Get the path to the physics rules data file.
    
    Returns:
        Absolute path to pprules.json
    """
    # Navigate from tools/physics to data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "..", "data", "pprules.json")
    return os.path.normpath(data_path)


def load_physics_rules(path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Load physics rules from JSON file.
    
    Args:
        path: Optional custom path to rules file. If None, uses default path.
        
    Returns:
        List of physics rules
        
    Raises:
        FileNotFoundError: If the rules file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    if path is None:
        path = get_rules_data_path()
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            rules = data.get("rules", [])
            logger.info(f"Loaded {len(rules)} physics rules from {path}")
            return rules
    except FileNotFoundError:
        logger.error(f"Physics rules file not found at {path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in physics rules file: {e}")
        raise


def validate_rules_data(rules: List[Dict[str, Any]]) -> List[str]:
    """
    Validate physics rules data format and content.
    
    Args:
        rules: List of physics rules to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    required_fields = ["rule_number", "content"]
    
    for i, rule in enumerate(rules):
        # Check required fields
        for field in required_fields:
            if field not in rule:
                errors.append(f"Rule {i}: Missing required field '{field}'")
                
        # Validate field types
        if "rule_number" in rule and not isinstance(rule["rule_number"], (str, int)):
            errors.append(f"Rule {i}: 'rule_number' must be string or int")
            
        if "content" in rule and not isinstance(rule["content"], str):
            errors.append(f"Rule {i}: 'content' must be string")
            
        # Validate optional fields
        if "category" in rule and not isinstance(rule["category"], str):
            errors.append(f"Rule {i}: 'category' must be string")
            
        if "description" in rule and not isinstance(rule["description"], str):
            errors.append(f"Rule {i}: 'description' must be string")
            
        if "examples" in rule and not isinstance(rule["examples"], list):
            errors.append(f"Rule {i}: 'examples' must be list")
            
        if "particles" in rule and not isinstance(rule["particles"], list):
            errors.append(f"Rule {i}: 'particles' must be list")
            
    return errors


def filter_rules_by_category(rules: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
    """
    Filter physics rules by category.
    
    Args:
        rules: List of physics rules
        category: Category to filter by (case-insensitive)
        
    Returns:
        Filtered list of rules
    """
    category_lower = category.lower()
    return [
        rule for rule in rules
        if category_lower in rule.get("category", "").lower()
    ]


def filter_rules_by_particles(rules: List[Dict[str, Any]], particles: List[str]) -> List[Dict[str, Any]]:
    """
    Filter physics rules by particles involved.
    
    Args:
        rules: List of physics rules
        particles: List of particle names to filter by
        
    Returns:
        Filtered list of rules involving any of the specified particles
    """
    particles_lower = [p.lower() for p in particles]
    filtered = []
    
    for rule in rules:
        rule_particles = rule.get("particles", [])
        rule_content = rule.get("content", "").lower()
        
        # Check if particles are mentioned in content or particles list
        match_found = False
        
        # Check particles list
        if isinstance(rule_particles, list):
            rule_particles_lower = [p.lower() for p in rule_particles]
            if any(p in rule_particles_lower for p in particles_lower):
                match_found = True
        
        # Check content
        if not match_found:
            if any(p in rule_content for p in particles_lower):
                match_found = True
                
        if match_found:
            filtered.append(rule)
                
    return filtered


def search_rules_by_keyword(rules: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
    """
    Search rules by keyword in content, description, or category.
    
    Args:
        rules: List of physics rules
        keyword: Keyword to search for (case-insensitive)
        
    Returns:
        List of matching rules
    """
    keyword_lower = keyword.lower()
    matching_rules = []
    
    for rule in rules:
        # Search in content
        content = rule.get("content", "").lower()
        description = rule.get("description", "").lower()
        category = rule.get("category", "").lower()
        
        if (keyword_lower in content or 
            keyword_lower in description or 
            keyword_lower in category):
            matching_rules.append(rule)
            
    return matching_rules


def get_rule_by_number(rules: List[Dict[str, Any]], rule_number: Any) -> Optional[Dict[str, Any]]:
    """
    Get a specific rule by its rule number.
    
    Args:
        rules: List of physics rules
        rule_number: Rule number to find
        
    Returns:
        Rule dictionary or None if not found
    """
    for rule in rules:
        if str(rule.get("rule_number")) == str(rule_number):
            return rule
    return None


def get_rules_stats(rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get statistics about the physics rules data.
    
    Args:
        rules: List of physics rules
        
    Returns:
        Dictionary with statistics
    """
    categories = {}
    particles = {}
    rule_types = {}
    content_lengths = []
    
    for rule in rules:
        # Count categories
        category = rule.get("category", "Unknown")
        categories[category] = categories.get(category, 0) + 1
        
        # Count particles
        for particle in rule.get("particles", []):
            particles[particle] = particles.get(particle, 0) + 1
            
        # Count rule types (based on keywords in content)
        content = rule.get("content", "").lower()
        if "conservation" in content:
            rule_types["conservation"] = rule_types.get("conservation", 0) + 1
        if "decay" in content:
            rule_types["decay"] = rule_types.get("decay", 0) + 1
        if "interaction" in content:
            rule_types["interaction"] = rule_types.get("interaction", 0) + 1
        if "symmetry" in content:
            rule_types["symmetry"] = rule_types.get("symmetry", 0) + 1
            
        # Track content lengths
        content_lengths.append(len(rule.get("content", "")))
        
    avg_content_length = sum(content_lengths) / len(content_lengths) if content_lengths else 0
        
    return {
        "total_rules": len(rules),
        "categories": categories,
        "unique_categories": len(categories),
        "particles": particles,
        "unique_particles": len(particles),
        "rule_types": rule_types,
        "average_content_length": avg_content_length,
        "min_content_length": min(content_lengths) if content_lengths else 0,
        "max_content_length": max(content_lengths) if content_lengths else 0,
    }


def create_rule_index(rules: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Create an index of rules by rule number for fast lookup.
    
    Args:
        rules: List of physics rules
        
    Returns:
        Dictionary mapping rule numbers to rule data
    """
    index = {}
    for rule in rules:
        rule_number = str(rule.get("rule_number", ""))
        if rule_number:
            index[rule_number] = rule
    return index