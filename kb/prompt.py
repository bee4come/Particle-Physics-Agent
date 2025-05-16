# kb/prompt.py
from typing import List
from .schema import FeynmanRecord

def compose_prompt(examples: List[FeynmanRecord], user_description: str) -> str:
    """
    Composes a few-shot prompt using retrieved examples and the user's description.
    """
    if not isinstance(examples, list):
        # Handle cases where examples might not be a list, though type hinting suggests it.
        # Or raise an error. For now, treat as no examples.
        print("Warning: 'examples' provided to compose_prompt was not a list. Proceeding with no few-shot examples.")
        examples = []

    # Filter out examples that might be None or lack necessary attributes, just in case.
    valid_examples = [e for e in examples if isinstance(e, FeynmanRecord) and hasattr(e, 'reaction') and hasattr(e, 'tikz')]
    
    # Construct the few-shot examples part of the prompt
    # Using a slightly more robust way to access attributes, though Pydantic models should have them.
    shots_list = []
    for ex in valid_examples:
        reaction = getattr(ex, 'reaction', 'Unknown Reaction')
        tikz = getattr(ex, 'tikz', '# TikZ code not available')
        # Ensure tikz is a string and handle potential None values gracefully
        tikz_str = str(tikz) if tikz is not None else '# TikZ code not available'
        shots_list.append(f"### Example Reaction: {reaction}\n### Example TikZ Code:\n```latex\n{tikz_str}\n```")

    shots_string = "\n\n".join(shots_list)

    # Construct the final prompt
    # The user's example was: f"{shots}\n\n### USER\n{user_desc}\n### ANSWER\n"
    # Let's refine the instruction to the LLM slightly.
    
    prompt_header = """You are an expert TikZ-Feynman diagram generator for LaTeX.
Your goal is to produce clean, standard, and "publication-ready" TikZ-Feynman code snippets.

Follow these strict rules for the output:
1.  Generate **only** the LaTeX code that goes **inside** the `\\feynmandiagram{...}` environment. Do not include the `\\feynmandiagram{...}` command itself, only its content.
2.  Use **official** TikZ-Feynman syntax.
3.  **All connecting lines (edges) MUST have a style specification**, such as `[fermion]`, `[photon]`, `[gluon]`, `[boson]`, `[anti fermion]`, etc. Do not omit these.
4.  **Particle labels (`[particle=...]`) should be placed on the nodes** (the start/end points of lines), not on the edges.
5.  **Node Naming Convention (IMPORTANT):**
    *   Use `i#` for input particles (e.g., `i1`, `i2`).
    *   Use `v#` for internal vertices (e.g., `v1`, `v2`).
    *   Use `o#` for output particles (e.g., `o1`, `o2`).
    Maintain consistency (e.g., if an input `i1` connects to vertex `v1`, use these names).
6.  ❌ **DO NOT USE** custom macros like `\\electron` or `\\photon`.
7.  ❌ **DO NOT INCLUDE** `\\begin{feynman}` or `\\end{feynman}`.
8.  ❌ **DO NOT INCLUDE** `\\vertex` as a standalone command (vertices are defined by line connections).
9.  Provide no explanation, preamble, or markdown formatting. Just return the raw TikZ code for the diagram content.

Below are some examples of physics process descriptions and their corresponding TikZ-Feynman code content.
Use these examples to understand the style and level of detail required.
"""

    if shots_string:
        full_prompt = (
            f"{prompt_header}\n\n"
            f"--- EXAMPLES ---\n"
            f"{shots_string}\n\n"
            f"--- TASK ---\n"
            f"### User Description:\n{user_description}\n\n"
            f"### TikZ-Feynman Code (only the content for \\feynmandiagram{{...}}):\n"
        )
    else: # No valid examples, fall back to a zero-shot prompt with strong instructions
        full_prompt = (
            f"{prompt_header}\n\n"
            f"--- TASK ---\n"
            f"### User Description:\n{user_description}\n\n"
            f"### TikZ-Feynman Code (only the content for \\feynmandiagram{{...}}):\n"
        )
        
    return full_prompt

if __name__ == '__main__':
    # Example usage
    sample_examples = [
        FeynmanRecord(
            topic="QED", reaction="e- -> e- g", particles=["e-", "g"],
            description="Electron emits photon.", 
            tikz="\\feynmandiagram [horizontal=a to c] {\n  a [particle=e⁻] -- [fermion] b,\n  b -- [fermion] c [particle=e⁻],\n  b -- [photon] d [particle=γ],\n};",
            process_type="Emission"
        ),
        FeynmanRecord(
            topic="EW", reaction="Z -> nu nu_bar", particles=["Z", "nu", "nu_bar"],
            description="Z boson decays to neutrino anti-neutrino.",
            tikz="\\feynmandiagram [horizontal=a to b] {\n  a [particle=Z] -- [boson] b,\n  b -- [fermion] c [particle=ν],\n  b -- [anti fermion] d [particle=\\bar{ν}],\n};",
            process_type="Decay"
        )
    ]
    empty_examples = []
    
    user_desc_test = "A top quark decays into a W boson and a bottom quark."

    print("--- Prompt with examples ---")
    prompt1 = compose_prompt(sample_examples, user_desc_test)
    print(prompt1)

    print("\n--- Prompt without examples ---")
    prompt2 = compose_prompt(empty_examples, user_desc_test)
    print(prompt2)

    print("\n--- Prompt with None as examples ---")
    prompt3 = compose_prompt(None, user_desc_test) # type: ignore
    print(prompt3)
