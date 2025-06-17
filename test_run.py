#!/usr/bin/env python
"""Test running the FeynmanCraft ADK agent directly."""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feynmancraft_adk.agent import root_agent

def test_agent():
    """Test the agent with a simple request."""
    # Simple test request
    test_input = "Generate a Feynman diagram for electron-positron annihilation to two photons"
    
    print(f"Testing with input: {test_input}")
    print("-" * 50)
    
    try:
        # Get the agent's response
        response = root_agent.get_response(test_input)
        print("Response:", response)
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_agent()