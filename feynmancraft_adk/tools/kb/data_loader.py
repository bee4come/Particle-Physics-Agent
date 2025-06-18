"""
Data loading utilities for Knowledge Base.
"""

import json
import os
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_kb_data_path() -> str:
    """
    Get the path to the KB data file.
    
    Returns:
        Absolute path to feynman_kb.json
    """
    # Navigate from tools/kb to data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "..", "data", "feynman_kb.json")
    return os.path.normpath(data_path)


def load_kb_examples(path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Load KB examples from JSON file.
    
    Args:
        path: Optional custom path to KB file. If None, uses default path.
        
    Returns:
        List of KB examples
        
    Raises:
        FileNotFoundError: If the KB file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    if path is None:
        path = get_kb_data_path()
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Loaded {len(data)} KB examples from {path}")
            return data
    except FileNotFoundError:
        logger.error(f"KB file not found at {path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in KB file: {e}")
        raise


def validate_kb_data(examples: List[Dict[str, Any]]) -> List[str]:
    """
    Validate KB data format and content.
    
    Args:
        examples: List of KB examples to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    required_fields = ["id", "topic", "description", "tikz"]
    
    for i, example in enumerate(examples):
        # Check required fields
        for field in required_fields:
            if field not in example:
                errors.append(f"Example {i}: Missing required field '{field}'")
                
        # Validate field types
        if "id" in example and not isinstance(example["id"], (str, int)):
            errors.append(f"Example {i}: 'id' must be string or int")
            
        if "topic" in example and not isinstance(example["topic"], str):
            errors.append(f"Example {i}: 'topic' must be string")
            
        if "description" in example and not isinstance(example["description"], str):
            errors.append(f"Example {i}: 'description' must be string")
            
        if "tikz" in example and not isinstance(example["tikz"], str):
            errors.append(f"Example {i}: 'tikz' must be string")
            
        # Validate optional fields
        if "particles" in example and not isinstance(example["particles"], list):
            errors.append(f"Example {i}: 'particles' must be list")
            
        if "reaction" in example and not isinstance(example["reaction"], str):
            errors.append(f"Example {i}: 'reaction' must be string")
            
    return errors


def filter_kb_by_topic(examples: List[Dict[str, Any]], topic: str) -> List[Dict[str, Any]]:
    """
    Filter KB examples by topic.
    
    Args:
        examples: List of KB examples
        topic: Topic to filter by (case-insensitive)
        
    Returns:
        Filtered list of examples
    """
    topic_lower = topic.lower()
    return [
        example for example in examples
        if topic_lower in example.get("topic", "").lower()
    ]


def filter_kb_by_particles(examples: List[Dict[str, Any]], particles: List[str]) -> List[Dict[str, Any]]:
    """
    Filter KB examples by particles involved.
    
    Args:
        examples: List of KB examples
        particles: List of particle names to filter by
        
    Returns:
        Filtered list of examples containing any of the specified particles
    """
    particles_lower = [p.lower() for p in particles]
    filtered = []
    
    for example in examples:
        example_particles = example.get("particles", [])
        if isinstance(example_particles, list):
            example_particles_lower = [p.lower() for p in example_particles]
            if any(p in example_particles_lower for p in particles_lower):
                filtered.append(example)
                
    return filtered


def get_kb_stats(examples: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get statistics about the KB data.
    
    Args:
        examples: List of KB examples
        
    Returns:
        Dictionary with statistics
    """
    topics = {}
    particles = {}
    process_types = {}
    
    for example in examples:
        # Count topics
        topic = example.get("topic", "Unknown")
        topics[topic] = topics.get(topic, 0) + 1
        
        # Count particles
        for particle in example.get("particles", []):
            particles[particle] = particles.get(particle, 0) + 1
            
        # Count process types
        process_type = example.get("process_type", "Unknown")
        process_types[process_type] = process_types.get(process_type, 0) + 1
        
    return {
        "total_examples": len(examples),
        "topics": topics,
        "unique_topics": len(topics),
        "particles": particles,
        "unique_particles": len(particles),
        "process_types": process_types,
        "average_description_length": sum(len(e.get("description", "")) for e in examples) / len(examples) if examples else 0,
        "average_tikz_length": sum(len(e.get("tikz", "")) for e in examples) / len(examples) if examples else 0,
    }