# ADK App Entry Point
# This file exposes the root_agent for the ADK framework

# Import all necessary components
import os
import sys

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main orchestrator agent
from agents.orchestrator_agent import OrchestratorAgent

# Create the root agent instance
root_agent = OrchestratorAgent()

# ADK Application Package 