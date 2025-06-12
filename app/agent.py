# Copyright 2025 Google LLC
# Licensed under the Apache License, Version 2.0

"""
FeynmanCraft ADK Agent - TikZ Feynman Diagram Generator
Multi-agent system for generating TikZ Feynman diagrams from natural language descriptions.
"""

import sys
import os

# Add the parent directory to Python path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the orchestrator agent
from agents.orchestrator_agent import OrchestratorAgent

# Create the root agent instance as required by ADK
# This is the main entry point for the ADK framework
root_agent = OrchestratorAgent() 