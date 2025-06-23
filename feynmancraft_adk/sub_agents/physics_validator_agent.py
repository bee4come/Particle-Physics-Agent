# Copyright 2024-2025 The FeynmanCraft ADK Project Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Physics Validator Agent for FeynmanCraft ADK.

This agent acts as a coordinator for physics validation. It receives a physics process,
finds relevant rules from a JSON database via semantic search, and orchestrates validation.
For rules requiring computation, it delegates to specialized tools.

Enhanced with ParticlePhysics MCP Server tools for comprehensive particle data validation.

This agent has been refactored to use the centralized tools module for all data loading,
embedding management, search functionality, and physics validation tools.
"""

import logging
from typing import Dict, List, Any

from google.adk.agents import Agent

from ..models import PHYSICS_VALIDATOR_MODEL
from .physics_validator_agent_prompt import PROMPT as PHYSICS_VALIDATOR_AGENT_PROMPT

# Import physics search functionality from tools
from ..tools.physics.search import (
    search_physics_rules,
    search_rules_by_particles,
    search_rules_by_process,
    validate_process_against_rules
)

# Import physics tools for enhanced particle validation
from ..tools.physics import (
    search_particle,
    get_particle_properties,
    validate_quantum_numbers,
    get_branching_fractions,
    compare_particles,
    convert_units,
    check_particle_properties,
)

# Import natural language physics parsing
from ..tools.physics.physics_tools import (
    parse_natural_language_physics
)

# Import MCP tools for comprehensive particle physics validation (external server)
from ..integrations.mcp import (
    search_particle_mcp,
    get_particle_properties_mcp,
    validate_quantum_numbers_mcp,
    get_branching_fractions_mcp,
    compare_particles_mcp,
    convert_units_mcp,
    check_particle_properties_mcp,
)

logger = logging.getLogger(__name__)


# --- Wrapper functions for agent tools ---

async def search_physics_rules_wrapper(query: str) -> List[Dict[str, Any]]:
    """
    Wrapper for search_physics_rules with default parameters.
    
    Args:
        query: Natural language query about physics rules
        
    Returns:
        List of relevant physics rules
    """
    try:
        return await search_physics_rules(query, top_k=5)
    except Exception as e:
        logger.error(f"Error in search_physics_rules_wrapper: {e}")
        return [{"error": f"Physics rules search failed: {str(e)}"}]


def search_rules_by_particles_wrapper(particles: str) -> List[Dict[str, Any]]:
    """
    Wrapper for searching rules by particles.
    
    Args:
        particles: Comma-separated list of particle names
        
    Returns:
        List of relevant physics rules
    """
    try:
        particle_list = [p.strip() for p in particles.split(',')]
        return search_rules_by_particles(particle_list, top_k=10)
    except Exception as e:
        logger.error(f"Error in search_rules_by_particles_wrapper: {e}")
        return [{"error": f"Particle rules search failed: {str(e)}"}]


def search_rules_by_process_wrapper(process_description: str) -> List[Dict[str, Any]]:
    """
    Wrapper for searching rules by process description.
    
    Args:
        process_description: Description of the physics process
        
    Returns:
        List of relevant physics rules
    """
    try:
        return search_rules_by_process(process_description, top_k=5)
    except Exception as e:
        logger.error(f"Error in search_rules_by_process_wrapper: {e}")
        return [{"error": f"Process rules search failed: {str(e)}"}]


def validate_process_wrapper(process_description: str, particles: str) -> Dict[str, Any]:
    """
    Wrapper for comprehensive process validation.
    
    Args:
        process_description: Description of the physics process
        particles: Comma-separated list of particles involved
        
    Returns:
        Validation result
    """
    try:
        particle_list = [p.strip() for p in particles.split(',')]
        return validate_process_against_rules(process_description, particle_list)
    except Exception as e:
        logger.error(f"Error in validate_process_wrapper: {e}")
        return {
            "process": process_description,
            "particles": particles,
            "error": str(e),
            "validation_status": "failed"
        }


def parse_natural_language_physics_wrapper(query: str) -> Dict[str, Any]:
    """
    Wrapper for parsing natural language physics queries.
    
    Args:
        query: Natural language physics query
        
    Returns:
        Parsed physics information
    """
    try:
        result = parse_natural_language_physics(query)
        return result
    except Exception as e:
        logger.error(f"Error in parse_natural_language_physics_wrapper: {e}")
        return {
            'status': 'error',
            'message': str(e),
            'original_query': query
        }


# --- MCP Tool Wrappers ---
# These wrappers handle async calls for MCP tools

async def search_particle_mcp_wrapper(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Wrapper for MCP particle search."""
    try:
        return await search_particle_mcp(query, max_results=max_results)
    except Exception as e:
        logger.error(f"MCP search_particle failed: {e}")
        return {"error": str(e), "status": "failed"}


async def get_particle_properties_mcp_wrapper(particle_name: str, units_preference: str = "GeV") -> Dict[str, Any]:
    """Wrapper for MCP particle properties."""
    try:
        return await get_particle_properties_mcp(particle_name, units_preference=units_preference)
    except Exception as e:
        logger.error(f"MCP get_particle_properties failed: {e}")
        return {"error": str(e), "status": "failed"}


async def validate_quantum_numbers_mcp_wrapper(particle_name: str) -> Dict[str, Any]:
    """Wrapper for MCP quantum number validation."""
    try:
        return await validate_quantum_numbers_mcp(particle_name)
    except Exception as e:
        logger.error(f"MCP validate_quantum_numbers failed: {e}")
        return {"error": str(e), "status": "failed"}


async def get_branching_fractions_mcp_wrapper(particle_name: str, limit: int = 10) -> Dict[str, Any]:
    """Wrapper for MCP branching fractions."""
    try:
        return await get_branching_fractions_mcp(particle_name, limit=limit)
    except Exception as e:
        logger.error(f"MCP get_branching_fractions failed: {e}")
        return {"error": str(e), "status": "failed"}


async def compare_particles_mcp_wrapper(particle_names: str, properties: str = "mass,charge,spin") -> Dict[str, Any]:
    """Wrapper for MCP particle comparison."""
    try:
        particle_list = [p.strip() for p in particle_names.split(',')]
        properties_list = [p.strip() for p in properties.split(',')]
        return await compare_particles_mcp(particle_list, properties=properties_list)
    except Exception as e:
        logger.error(f"MCP compare_particles failed: {e}")
        return {"error": str(e), "status": "failed"}


async def convert_units_mcp_wrapper(value: float, from_units: str, to_units: str) -> Dict[str, Any]:
    """Wrapper for MCP unit conversion."""
    try:
        return await convert_units_mcp(value, from_units, to_units)
    except Exception as e:
        logger.error(f"MCP convert_units failed: {e}")
        return {"error": str(e), "status": "failed"}


async def check_particle_properties_mcp_wrapper(particle_name: str) -> Dict[str, Any]:
    """Wrapper for MCP particle property check."""
    try:
        return await check_particle_properties_mcp(particle_name)
    except Exception as e:
        logger.error(f"MCP check_particle_properties failed: {e}")
        return {"error": str(e), "status": "failed"}


# --- Agent Definition ---

PhysicsValidatorAgent = Agent(
    model=PHYSICS_VALIDATOR_MODEL,  # Use gemini-2.5-pro for complex physics validation
    name="physics_validator_agent",
    description="Validates physics processes using comprehensive particle physics tools, MCP tools, and natural language processing. Uses centralized tools for all validation operations.",
    instruction=PHYSICS_VALIDATOR_AGENT_PROMPT,
    output_key="physics_validation_report",  # State management: outputs to state.physics_validation_report
    tools=[
        # Physics rules search tools
        search_physics_rules_wrapper,
        search_rules_by_particles_wrapper,
        search_rules_by_process_wrapper,
        validate_process_wrapper,
        
        # Internal physics tools (these already use MCP internally)
        search_particle,
        get_particle_properties,
        validate_quantum_numbers,
        get_branching_fractions,
        compare_particles,
        convert_units,
        check_particle_properties,
        
        # MCP physics tools with proper wrappers
        search_particle_mcp_wrapper,
        get_particle_properties_mcp_wrapper,
        validate_quantum_numbers_mcp_wrapper,
        get_branching_fractions_mcp_wrapper,
        compare_particles_mcp_wrapper,
        convert_units_mcp_wrapper,
        check_particle_properties_mcp_wrapper,
        
        # Natural language processing tools
        parse_natural_language_physics_wrapper,
    ],
)