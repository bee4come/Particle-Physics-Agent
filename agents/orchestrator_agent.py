# Copyright 2025 Google LLC
# Licensed under the Apache License, Version 2.0

"""
OrchestratorAgent - Main coordination agent for TikZ Feynman diagram generation
"""

from google.adk import Agent
from schemas import DiagramRequest, FinalAnswer, TikzSnippet, ValidationReport, PlanStep
import json


def generate_tikz_diagram(description: str) -> str:
    """
    Tool function to generate TikZ Feynman diagrams based on description
    
    Args:
        description: Natural language description of the physics process
        
    Returns:
        Generated TikZ code as a string
    """
    print(f"🔧 Generating TikZ diagram for: {description}")
    
    # Parse description for physics processes
    desc_lower = description.lower()
    
    if "annihilat" in desc_lower and ("electron" in desc_lower or "positron" in desc_lower) and "photon" in desc_lower:
        # Electron-positron annihilation to two photons
        tikz_code = """\\begin{tikzpicture}
  \\begin{feynman}
    \\vertex (a) {\\(e^-\\)};
    \\vertex [right=of a] (b);
    \\vertex [right=of b] (c) {\\(\\gamma\\)};
    \\vertex [below=of a] (d) {\\(e^+\\)};
    \\vertex [below=of c] (e) {\\(\\gamma\\)};
    \\diagram* {
      (a) -- [fermion] (b) -- [photon] (c),
      (d) -- [anti fermion] (b) -- [photon] (e)
    };
  \\end{feynman}
\\end{tikzpicture}"""
        
    elif "electron" in desc_lower and "photon" in desc_lower:
        # Electron emitting a photon (bremsstrahlung)
        tikz_code = """\\begin{tikzpicture}
  \\begin{feynman}
    \\vertex (a) {\\(e^-\\)};
    \\vertex [right=of a] (b);
    \\vertex [right=of b] (c) {\\(e^-\\)};
    \\vertex [above right=of b] (d) {\\(\\gamma\\)};
    \\diagram* {
      (a) -- [fermion] (b) -- [fermion] (c),
      (b) -- [photon] (d)
    };
  \\end{feynman}
\\end{tikzpicture}"""
        
    elif "muon" in desc_lower and "decay" in desc_lower:
        # Muon decay
        tikz_code = """\\begin{tikzpicture}
  \\begin{feynman}
    \\vertex (a) {\\(\\mu^-\\)};
    \\vertex [right=of a] (b);
    \\vertex [above right=of b] (c) {\\(\\nu_\\mu\\)};
    \\vertex [right=of b] (d) {\\(e^-\\)};
    \\vertex [below right=of b] (e) {\\(\\bar{\\nu}_e\\)};
    \\diagram* {
      (a) -- [fermion] (b),
      (b) -- [fermion] (c),
      (b) -- [fermion] (d),
      (b) -- [fermion] (e)
    };
  \\end{feynman}
\\end{tikzpicture}"""
        
    else:
        # Default simple fermion line
        tikz_code = """\\begin{tikzpicture}
  \\begin{feynman}
    \\vertex (a);
    \\vertex [right=of a] (b);
    \\diagram* {
      (a) -- [fermion] (b)
    };
  \\end{feynman}
\\end{tikzpicture}"""
    
    print(f"✅ Generated TikZ code successfully")
    return tikz_code


class OrchestratorAgent(Agent):
    """
    Main orchestrator agent that generates TikZ Feynman diagrams
    """

    def __init__(self):
        super().__init__(
            model="gemini-2.0-flash",
            name="OrchestratorAgent",
            description="Generates TikZ Feynman diagrams from natural language descriptions",
            instruction="""
            You are a specialized agent for generating TikZ Feynman diagrams.
            
            When a user describes a physics process, you should:
            1. Understand the physics described
            2. Use the generate_tikz_diagram tool to create the appropriate TikZ code
            3. Present the result in a clear, formatted way
            
            Always use the generate_tikz_diagram tool to create diagrams.
            Provide the complete TikZ code that users can directly use in their LaTeX documents.
            
            Be helpful and explain the physics process briefly when presenting the diagram.
            """,
            tools=[generate_tikz_diagram]
        )
        print(f"{self.name} initialized with ADK 1.2.1 and TikZ generation tool")


# For testing purposes
if __name__ == '__main__':
    print("OrchestratorAgent - Testing locally")
    
    agent = OrchestratorAgent()
    
    # Test with sample inputs
    test_inputs = [
        "electron positron annihilation to two photons",
        "electron emits a photon", 
        "muon decay",
        "simple fermion propagation"
    ]
    
    for test_input in test_inputs:
        print(f"\n{'='*50}")
        print(f"Testing: {test_input}")
        print('='*50)
        result = generate_tikz_diagram(test_input)
        print(f"Generated TikZ:\n{result}") 