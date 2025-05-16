# agents/tikz_feynman_agent.py
import google.generativeai as genai
import os
from typing import Optional # Added for type hinting

# Attempt to import KB components. Fail gracefully if they are not ready (e.g. during initial setup)
try:
    from kb.retriever import query_records_by_vector
    from kb.prompt import compose_prompt
    KB_ENABLED = True
    print("Knowledge base components (retriever, prompt) loaded successfully for TikzFeynmanAgent.")
except ImportError as e:
    print(f"Warning: Knowledge base components not found or import error: {e}. TikzFeynmanAgent will operate in zero-shot mode.")
    KB_ENABLED = False
    # Define dummy functions if KB is not enabled, so the agent can still be instantiated
    def query_records_by_vector(query_text: str, k: int = 3, search_k: int = -1): return []
    def compose_prompt(examples, user_description: str):
        # Fallback to the zero-shot prompt structure if KB/compose_prompt is not available
        # This is similar to the prompt used before KB integration.
        prompt_header = """You are a TikZ-Feynman diagram generator for LaTeX.
Ensure your output is **only** the LaTeX code **inside** the `\\feynmandiagram` environment, using **official** TikZ-Feynman syntax.
Include `[particle=...]` labels for incoming and outgoing particles.
Do not use custom macros like \\electron or \\photon.
Do not include \\begin{feynman} or \\vertex (as a standalone command).
Do not add any explanation. Just return the code.

Example format (content for \\feynmandiagram{{...}}):
\\feynmandiagram [horizontal=a to c] {{{{
  a [particle=e⁻] -- [fermion] b,
  b -- [fermion] c [particle=e⁻],
  b -- [photon] d [particle=γ]
}}}};
"""
        return (
            f"{prompt_header}\n\n"
            f"--- TASK ---\n"
            f"### User Description:\n{user_description}\n\n"
            f"### TikZ-Feynman Code (only the content for \\feynmandiagram{{...}}):\n"
        )


import re # For validation regex

class TikzFeynmanAgent:
    def __init__(self, api_key: str = None, model_name: str = None, use_kb: bool = True, num_examples_from_kb: int = 3, max_retries: int = 1):
        resolved_api_key = api_key if api_key else os.getenv("GOOGLE_API_KEY")
        # Use GEMINI_MODEL_NAME for the generative agent, not GEMINI_EMBEDDING_MODEL_NAME
        default_generative_model = "gemini-1.5-pro-latest" # Or another suitable generative model
        resolved_model_name = model_name if model_name else os.getenv("GEMINI_MODEL_NAME", default_generative_model)


        if not resolved_api_key:
            raise ValueError("Google API Key not provided or found in environment variables (GOOGLE_API_KEY).")
        
        # Configure genai globally. This is used by genai.GenerativeModel and also by kb.embedding if it uses genai.embed_content
        genai.configure(api_key=resolved_api_key)
        
        self.model = genai.GenerativeModel(resolved_model_name)
        self.use_kb = KB_ENABLED and use_kb # KB can only be used if components loaded and user wants to use it
        self.num_examples_from_kb = num_examples_from_kb
        self.max_retries = max_retries
        print(f"TikzFeynmanAgent initialized with model: {resolved_model_name}. Knowledge Base enabled: {self.use_kb}. Max retries: {self.max_retries}")

    def _validate_tikz_code(self, tikz_code: str) -> bool:
        """
        Validates the generated TikZ code for essential styles.
        Checks for the presence of [fermion], [photon], [boson], [gluon], or [ghost].
        """
        # Regex to find common particle lines. This can be expanded.
        # It looks for patterns like "-- [fermion]", "-- [photon]", etc.
        # Allows for optional spaces around the brackets and inside.
        # Also checks for particle labels like [particle=...]
        required_styles = [
            r"\[\s*fermion\s*\]",
            r"\[\s*photon\s*\]",
            r"\[\s*boson\s*\]",
            r"\[\s*gluon\s*\]",
            r"\[\s*ghost\s*\]",
            # It's also good to ensure particle labels are present for external lines,
            # but the core styles above are more critical for the diagram structure itself.
            # r"\[\s*particle\s*=\s*.*?\s*\]" # This might be too strict if not all diagrams need it.
        ]
        # Check if at least one of the required styles is present.
        # This is a basic check; more sophisticated parsing might be needed for complex rules.
        for style_pattern in required_styles:
            if re.search(style_pattern, tikz_code):
                print(f"Validation: Found style matching '{style_pattern}' in generated code.")
                return True
        
        print("Validation: No essential TikZ-Feynman styles (e.g., [fermion], [photon]) found in the generated code.")
        return False

    def generate_tikz_code(self, description: str) -> str:
        examples = []
        if self.use_kb:
            print(f"Attempting to retrieve {self.num_examples_from_kb} examples from KB for description: \"{description[:50]}...\"")
            try:
                examples = query_records_by_vector(description, k=self.num_examples_from_kb)
                if examples:
                    print(f"Retrieved {len(examples)} examples from KB.")
                else:
                    print("No examples retrieved from KB.")
            except Exception as e:
                print(f"Error retrieving examples from KB: {e}. Proceeding in zero-shot mode.")
                examples = []
        
        # compose_prompt will handle empty examples list and generate a zero-shot prompt if needed.
        # The prompt from kb.prompt already contains detailed instructions.
        prompt = compose_prompt(examples, description)
        
        # The old hardcoded prompt for reference (now handled by compose_prompt):
        # prompt = f"""You are a TikZ-Feynman diagram generator for LaTeX.
        # Given the physics description:
        # "{description}"
        # Generate **only** LaTeX code **inside** the `\\feynmandiagram` environment, using **official** TikZ-Feynman syntax.
        # Do not use custom macros like \\electron or \\photon.
        # Use only the default TikZ-Feynman commands like:
        # - fermion, photon, boson, vertex, anti fermion, etc.
        # - Include `[particle=...]` labels for incoming and outgoing particles where appropriate for clarity (e.g., `a [particle=e⁻]`, `c [particle=e⁻]`, `d [particle=γ]`).
        # Your output must be in this format (example with particle labels):
        # \\feynmandiagram [horizontal=a to c] {{{{
        #   a [particle=e⁻] -- [fermion] b,
        #   b -- [fermion] c [particle=e⁻],
        #   b -- [photon] d [particle=γ]
        # }}}};
        # Do not include \\begin{{feynman}} or \\vertex (as a standalone command).
        # Do not add any explanation.
        # Just return the code."""
        # Note: Escaped curly braces for f-string: {{{{ and }}}}

        generated_code = ""
        for attempt in range(self.max_retries + 1): # Initial attempt + retries
            print(f"Generation attempt {attempt + 1}/{self.max_retries + 1}")
            try:
                # Set temperature to 0.0 for deterministic and consistent output
                generation_config = genai.types.GenerationConfig(temperature=0.0)
                # Consider adding safety_settings if needed
                # safety_settings=[
                #     {
                #         "category": "HARM_CATEGORY_HARASSMENT",
                #         "threshold": "BLOCK_NONE",
                #     },
                #     # ... other categories
                # ]
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config
                    # safety_settings=safety_settings 
                )
                
                if response.parts:
                    generated_code = response.text.strip()
                    print("Code generated. Validating...")
                    if self._validate_tikz_code(generated_code):
                        print("Validation successful.")
                        return generated_code
                    else:
                        print(f"Validation failed for attempt {attempt + 1}.")
                        if attempt < self.max_retries:
                            print("Retrying...")
                        else:
                            print("Max retries reached. Returning last generated code despite validation failure.")
                            return generated_code # Or a specific error message / fallback
                else:
                    # Fallback or error handling if response.text is not available as expected
                    if response.prompt_feedback and response.prompt_feedback.block_reason:
                        error_message = f"Generation failed due to: {response.prompt_feedback.block_reason_message}"
                        print(error_message)
                        if attempt == self.max_retries: return error_message # Return error on last attempt
                    else:
                        error_message = "Error: No content generated. The prompt might have been blocked or an unknown error occurred."
                        print(error_message)
                        if attempt == self.max_retries: return error_message # Return error on last attempt
                    
                    if attempt == self.max_retries: # If it's the last attempt and it failed to produce parts
                        return generated_code if generated_code else error_message # Return whatever was last generated or the error

            except Exception as e:
                # Handle potential API errors or other exceptions
                print(f"An error occurred during generation attempt {attempt + 1}: {str(e)}")
                if attempt == self.max_retries:
                    return f"An error occurred after {self.max_retries + 1} attempts: {str(e)}"
        
        return generated_code # Should be unreachable if logic is correct, but as a fallback.

if __name__ == '__main__':
    # This is a simple test block.
    # In a real scenario, you'd get the API key securely (e.g., environment variable)
    # and the description from user input or another source.
    
    # The main CLI script (run_agent_cli.py) is now the primary way to test.
    # This __main__ block can be simplified or removed if CLI is preferred for testing.
    print("This is the TikzFeynmanAgent module. To run, use run_agent_cli.py or import this class.")
    # Example of direct instantiation (requires GOOGLE_API_KEY and optionally GEMINI_MODEL_NAME to be set in env):
    # from dotenv import load_dotenv
    # load_dotenv() # Load .env file if you want to test this module directly
    # if os.getenv("GOOGLE_API_KEY"):
    #     try:
    #         agent = TikzFeynmanAgent() # Will use env variables
    #         test_description = "An electron emits a photon and continues as an electron."
    #         print(f"Testing agent with: \"{test_description}\"")
    #         tikz_code = agent.generate_tikz_code(test_description)
    #         print("\nGenerated TikZ Code:")
    #         print(tikz_code)
    #     except ValueError as e:
    #         print(f"Error during direct test: {e}")
    # else:
    #     print("GOOGLE_API_KEY not set in environment. Skipping direct test of agent module.")
