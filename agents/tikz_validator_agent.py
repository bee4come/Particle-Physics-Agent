from google.adk.agents import Agent
from google.adk.messages import JSONMessage
from feynmancraft_adk.schemas import TikzSnippet, ValidationReport
from feyncore.compilation.compiler import compile_tikz_code # Import the actual compiler
import json
# from google.adk.models import Model # If LLM is used for log analysis, as in legacy

class TikZValidatorAgent(Agent):
    """
    Validates the generated TikZ code by attempting to compile it using LaTeX.
    Checks for syntax errors and other compilation issues.
    Based on legacy: tikz-hunter/agents/validator_agent.py (specifically its compilation part)
    and uses feyncore.compilation.compiler.
    """
    def __init__(self, latex_executable: str = "pdflatex"):
        super().__init__(name="TikZValidatorAgent")
        self.latex_executable = latex_executable
        # self.model_for_log_analysis = Model(...) # If LLM log analysis is retained
        print(f"{self.name} initialized with LaTeX executable: {self.latex_executable}.")

    def run(self, message: JSONMessage) -> JSONMessage:
        print(f"{self.name} received input: {message.body}")
        try:
            snippet = TikzSnippet(**message.body)
        except Exception as e:
            error_report = ValidationReport(
                ok=False,
                errors=[f"Input message body is not a valid TikzSnippet: {str(e)}"]
            )
            print(f"{self.name} generated error report due to invalid input: {error_report.dict()}")
            return JSONMessage(body=json.loads(error_report.json()))

        # Call the actual compiler function from feyncore
        success, log, pdf_bytes = compile_tikz_code(
            tikz_code=snippet.code,
            latex_executable=self.latex_executable
        )

        errors = []
        if not success:
            # Populate errors from the log if compilation failed
            # For simplicity, we can add a snippet of the log or specific error messages.
            # A more sophisticated error parsing can be added later.
            log_snippet = log.strip()[-1000:] # Get last 1000 chars of log as a sample
            errors.append(f"Compilation failed. Log snippet: ... {log_snippet}")
            # You could try to parse common errors as before:
            if "Undefined control sequence" in log:
                errors.append("Potential missing package or macro (Undefined control sequence).")
            if "Missing" in log:
                errors.append("Potential syntax error (Missing character/command).")
            # Add more specific error parsing if needed
        
        report = ValidationReport(ok=success, errors=errors)
        print(f"{self.name} generated report: {report.dict()}")
        # The ADK message body should be a JSON-serializable dict.
        # report.json() returns a JSON string, so use json.loads() or report.dict().
        return JSONMessage(body=json.loads(report.json()))

if __name__ == '__main__':
    # This is for local testing of the agent if needed
    validator = TikZValidatorAgent()
    
    # Test case 1: Valid TikZ code
    valid_tikz_body = {
        "code": "\\begin{tikzpicture}\\node{Hello World};\\end{tikzpicture}",
        "description": "A simple valid diagram"
    }
    valid_message = JSONMessage(body=valid_tikz_body)
    output_valid = validator.run(valid_message)
    print(f"Validation (Valid Code): {json.dumps(output_valid.body, indent=2)}")
    # To see the PDF, you'd need to get it from the compile_tikz_code function, 
    # which is not directly returned by this agent's run method in this structure.
    # The agent focuses on the validation report.

    # Test case 2: Invalid TikZ code (syntax error)
    invalid_tikz_body = {
        "code": "\\begin{tikzpicture}\\node{Missing Brace;\\end{tikzpicture}", 
        "description": "A diagram with syntax error"
    }
    invalid_message = JSONMessage(body=invalid_tikz_body)
    output_invalid = validator.run(invalid_message)
    print(f"Validation (Invalid Code): {json.dumps(output_invalid.body, indent=2)}")

    # Test case 3: Input that is not a TikzSnippet
    malformed_input_body = {"text": "this is not a tikz snippet"}
    malformed_message = JSONMessage(body=malformed_input_body)
    output_malformed = validator.run(malformed_message)
    print(f"Validation (Malformed Input): {json.dumps(output_malformed.body, indent=2)}")
    # print(f"Log for invalid: \n{output_invalid['log']}") 