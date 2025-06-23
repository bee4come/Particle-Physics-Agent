# feynmancraft-adk/agents/prompt_utils.py
from typing import List, Optional
from ..schemas import TikzSnippet # Adjusted import for schemas

def compose_prompt(base_prompt: str, user_prompt: str, examples: Optional[List[TikzSnippet]] = None, style_hint: Optional[str] = None) -> str:
    """
    Appends formatted examples and the user's task to a base prompt.
    The base_prompt is expected to contain the main instructions and formatting rules.
    """
    if examples is None:
        examples = []

    valid_examples = [e for e in examples if isinstance(e, TikzSnippet) and hasattr(e, 'code')]
    
    shots_list = []
    for ex in valid_examples:
        example_context = ex.description or "Example Diagram Snippet"
        tikz_str = str(ex.code) if ex.code is not None else '# TikZ code not available'
        # Using a slightly different formatting to clearly delineate examples
        shots_list.append(f"### Example Context: {example_context}\n### Example TikZ-Feynman Code (content for '\\feynmandiagram[...]'):\n```latex\n{tikz_str}\n```")

    shots_string = "\n\n".join(shots_list)
    
    # Construct the final part of the prompt to be appended
    task_section = f"### User Description:\n{user_prompt}\n"
    if style_hint:
        task_section += f"### Style Hint:\n{style_hint}\n"
    task_section += "\n### TikZ-Feynman Code (only the content for '\\feynmandiagram[...]'):\n"

    if shots_string:
        full_prompt = (
            f"{base_prompt}\n\n"
            f"--- EXAMPLES ---\n"
            f"{shots_string}\n\n"
            f"--- TASK ---\n"
            f"{task_section}"
        )
    else: 
        full_prompt = (
            f"{base_prompt}\n\n"
            f"--- TASK ---\n"
            f"{task_section}"
        )
        
    return full_prompt

if __name__ == '__main__':
    import sys
    from pathlib import Path
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Import schemas after path adjustment
    try:
        from schemas import TikzSnippet
    except ImportError as e:
        print(f"Local test: Error importing schemas: {e}")
        sys.exit(1)

    # Example base prompt (simulating what would be imported)
    test_base_prompt = "You are a TikZ generator. Follow these rules...\nBelow are examples and your task:"

    sample_tikz_examples = [
        TikzSnippet(code="a [particle=e⁻] -- [fermion] b; b -- [photon] d;", description="Electron emits photon"),
    ]
    user_desc_test_case = "A top quark decays."
    
    print("--- Testing compose_prompt with examples ---")
    prompt_with_examples = compose_prompt(test_base_prompt, user_desc_test_case, examples=sample_tikz_examples, style_hint="modern")
    print(prompt_with_examples)

    print("\n--- Testing compose_prompt without examples ---")
    prompt_without_examples = compose_prompt(test_base_prompt, user_desc_test_case, style_hint="classic")
    print(prompt_without_examples)
