from google.adk.agents import Agent
from google.adk.messages import JSONMessage
from google.adk.models import Model # Removed GeminiModel, Model is general
from feynmancraft_adk.schemas import TikzSnippet # DiagramRequest removed as it's part of message.body
import json
import textwrap 

class DiagramGeneratorAgent(Agent):
    """
    Generates TikZ code for Feynman diagrams using a Generative AI model (Gemini).
    It takes a natural language description and few-shot examples as input.
    Aims to use model's function calling to return structured TikzSnippet.
    """
    def __init__(self, model_id: str = "gemini-1.5-pro-latest"):
        super().__init__(name="DiagramGeneratorAgent")
        self.model = Model(model_id=model_id)
        print(f"{self.name} initialized with model: {self.model.model_id}.")

    def run(self, message: JSONMessage) -> JSONMessage:
        print(f"{self.name} received input: {message.body}")
        try:
            input_data = message.body
            user_prompt = input_data.get("user_prompt")
            if not user_prompt:
                raise ValueError("user_prompt is required in the input message body.")
            
            examples = input_data.get("examples", []) 
            style_hint = input_data.get("style_hint")

        except Exception as e:
            error_snippet = TikzSnippet(
                code="% Error: Invalid input to DiagramGeneratorAgent", 
                description=str(e)
            )
            print(f"{self.name} error processing input: {str(e)}")
            return JSONMessage(body=json.loads(error_snippet.json()))

        try:
            # Prompt for structured JSON output (TikzSnippet schema)
            structured_prompt_lines = [
                "You are an expert in particle physics and LaTeX using the TikZ and feynmandiagram packages.",
                "Your task is to generate a valid TikZ code snippet for a Feynman diagram based on the user's description, AND a brief text description of the generated diagram.",
                "You MUST output a single, valid JSON object that strictly conforms to the following Pydantic model schema:",
                '{\"code\": \"string (the TikZ code)\", \"description\": \"string (your brief text description)\"}',
                "Ensure the TikZ code is complete and compilable. Do not include any other text, explanations, or markdown formatting outside of this JSON object."
            ]
            if style_hint:
                structured_prompt_lines.append(f"\nStyle Hint: {style_hint}")
            
            structured_prompt_lines.append(f"\nUser's Diagram Description:\n{user_prompt}\n")
            
            if examples and len(examples) > 0:
                structured_prompt_lines.append("Examples of TikZ code and descriptions (for context, your output should still be a single JSON object as specified above):")
                for i, example in enumerate(examples):
                    ex_code = example.get("code", "")
                    ex_desc = example.get("description", "(no description provided)")
                    example_text = f"Example {i+1}:\nDescription: {ex_desc}\nTikZ Code:\n{ex_code}\n"
                    structured_prompt_lines.append(example_text)
            structured_prompt_lines.append("\nNow, generate the JSON output with 'code' and 'description' keys based on the user's diagram description.")
            
            final_prompt_for_structured_output = "\n".join(structured_prompt_lines)
            print(f"{self.name} final prompt for structured output (first 1000 chars):\n{final_prompt_for_structured_output[:1000]}...")
            print(f"(Prompt length: {len(final_prompt_for_structured_output)})")

            generated_data = self.model.generate(
                prompt=final_prompt_for_structured_output,
                output_schema=TikzSnippet 
            )
            
            if not isinstance(generated_data, TikzSnippet):
                print(f"{self.name} Warning: Model did not return a TikzSnippet instance directly. Got: {type(generated_data)}. Content: {str(generated_data)[:500]}...")
                if isinstance(generated_data, dict):
                    snippet = TikzSnippet(**generated_data)
                elif isinstance(generated_data, str): 
                    try:
                        data_dict = json.loads(generated_data)
                        snippet = TikzSnippet(**data_dict)
                    except json.JSONDecodeError:
                        snippet = TikzSnippet(code=generated_data, description=f"Generated diagram for: {user_prompt} (description from LLM not structured or parsing failed)")
                else:
                    raise TypeError(f"Model returned an unexpected type: {type(generated_data)}. Content: {str(generated_data)[:500]}...")
            else:
                snippet = generated_data

            print(f"{self.name} successfully generated TikZ snippet: {snippet.dict()}")
            return JSONMessage(body=json.loads(snippet.json()))

        except Exception as e:
            print(f"{self.name} error during LLM call or processing: {str(e)}")
            error_snippet = TikzSnippet(
                code=f"% Error during TikZ generation for: {user_prompt}\n% {str(e)}",
                description=f"Failed to generate diagram: {str(e)}"
            )
            return JSONMessage(body=json.loads(error_snippet.json()))

if __name__ == '__main__':
    import os
    if not os.getenv("GOOGLE_API_KEY"):
        print("WARNING: GOOGLE_API_KEY not set. LLM call will likely fail.")
        print("Skipping DiagramGeneratorAgent live test.")
    else:
        print("Found GOOGLE_API_KEY. Proceeding with DiagramGeneratorAgent test...")
        generator = DiagramGeneratorAgent()
        
        sample_input_body = {
            "user_prompt": "electron-positron annihilation into two photons",
            "style_hint": "Use simple lines, label particles clearly.",
            "examples": [
                {
                    "code": textwrap.dedent(r"""
                    \begin{tikzpicture}
                      \begin{feynman}
                        \vertex (a) {$e^-$};
                        \vertex [right=of a] (b);
                        \vertex [right=of b] (c) {$e^-$};
                        \vertex [above=of b] (d) {$\gamma$};
                        \diagram* {
                          (a) -- (b) -- (c),
                          (b) -- (d),
                        };
                      \end{feynman}
                    \end{tikzpicture}
                    """).strip(), 
                    "description": "Electron emitting a photon"
                }
            ]
        }
        sample_message = JSONMessage(body=sample_input_body)
        
        print("\n--- Running DiagramGeneratorAgent Test --- ")
        output_message = generator.run(sample_message)
        print("--- DiagramGeneratorAgent Test Complete ---")
        
        if output_message and output_message.body:
            print(f"\nDiagramGeneratorAgent Raw Output Body: {json.dumps(output_message.body, indent=2)}")
            try:
                final_snippet = TikzSnippet(**output_message.body)
                print(f"\nSuccessfully Parsed TikzSnippet:")
                print(f"  Description: {final_snippet.description}")
                print(f"  Code:\n{final_snippet.code}")
            except Exception as e:
                print(f"\nError parsing output body as TikzSnippet: {e}")
        else:
            print("\nDiagramGeneratorAgent produced no output or empty body.") 