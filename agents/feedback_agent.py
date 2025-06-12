from google.adk.agents import Agent
from google.adk.messages import JSONMessage
from feynmancraft_adk.schemas import TikzSnippet, ValidationReport, FinalAnswer
import json

class FeedbackAgent(Agent):
    """
    Aggregates validation results, generates user-friendly feedback,
    and constructs the FinalAnswer.
    """
    def __init__(self):
        super().__init__(name="FeedbackAgent")
        print(f"{self.name} initialized.")

    def run(self, message: JSONMessage) -> JSONMessage:
        """
        Generates feedback and the final answer based on inputs.
        The input message body is expected to be a dictionary containing:
        - "generated_tikz_snippet": dict (TikzSnippet model)
        - "physics_report": dict (ValidationReport model for physics)
        - "compile_report": dict (ValidationReport model for TikZ compilation)
        """
        print(f"{self.name} received input: {message.body}")
        
        try:
            input_data = message.body
            tikz_snippet_data = input_data.get("generated_tikz_snippet")
            physics_report_data = input_data.get("physics_report")
            compile_report_data = input_data.get("compile_report")

            if not all([tikz_snippet_data, physics_report_data, compile_report_data]):
                raise ValueError("Missing one or more required inputs: generated_tikz_snippet, physics_report, compile_report")

            # Reconstruct Pydantic models for easier handling and validation
            # TikzSnippet(**tikz_snippet_data) # Not strictly needed for FinalAnswer if already dict
            # physics_report = ValidationReport(**physics_report_data)
            # compile_report = ValidationReport(**compile_report_data)
            # FinalAnswer schema expects these as dicts, so we can pass them directly if they are already dicts.

        except Exception as e:
            error_final_answer = FinalAnswer(
                tikz=TikzSnippet(code="Error: Invalid input to FeedbackAgent", description=str(e)),
                physics_report=ValidationReport(ok=False, errors=[f"FeedbackAgent input error: {str(e)}"]),
                compile_report=ValidationReport(ok=False, errors=[f"FeedbackAgent input error: {str(e)}"])
            )
            print(f"{self.name} error processing input: {str(e)}")
            return JSONMessage(body=json.loads(error_final_answer.json()))

        # Construct FinalAnswer directly using the input dicts
        # The schemas for TikzSnippet and ValidationReport are compatible.
        final_answer_obj = FinalAnswer(
            tikz=tikz_snippet_data, # Expects a dict that matches TikzSnippet schema
            physics_report=physics_report_data, # Expects a dict that matches ValidationReport schema
            compile_report=compile_report_data  # Expects a dict that matches ValidationReport schema
        )
        
        # TODO: Add more sophisticated feedback generation here if needed,
        # e.g., natural language summary, confidence score, suggestions.
        # For now, FinalAnswer itself serves as the structured feedback.
        
        print(f"{self.name} constructed FinalAnswer: {final_answer_obj.dict()}")
        return JSONMessage(body=json.loads(final_answer_obj.json()))

if __name__ == '__main__':
    feedback_agent = FeedbackAgent()

    # Example successful input
    good_input_body = {
        "generated_tikz_snippet": {"code": "\\feynmandiagram{a->b};", "description": "Valid diagram"},
        "physics_report": {"ok": True, "errors": []},
        "compile_report": {"ok": True, "errors": []}
    }
    good_message = JSONMessage(body=good_input_body)
    output_good = feedback_agent.run(good_message)
    print(f"FeedbackAgent Output (Good): {json.dumps(output_good.body, indent=2)}")

    # Example input with errors
    bad_input_body = {
        "generated_tikz_snippet": {"code": "\\feynmandiagram{a-\\to b};", "description": "Diagram with error"},
        "physics_report": {"ok": True, "errors": []},
        "compile_report": {"ok": False, "errors": ["Missing } character"]}
    }
    bad_message = JSONMessage(body=bad_input_body)
    output_bad = feedback_agent.run(bad_message)
    print(f"FeedbackAgent Output (Bad): {json.dumps(output_bad.body, indent=2)}")

    # Example with missing input key
    missing_key_body = {
        "generated_tikz_snippet": {"code": "\\feynmandiagram{a->b};", "description": "Valid diagram"},
        "physics_report": {"ok": True, "errors": []}
        # compile_report is missing
    }
    missing_key_message = JSONMessage(body=missing_key_body)
    output_missing = feedback_agent.run(missing_key_message)
    print(f"FeedbackAgent Output (Missing Key): {json.dumps(output_missing.body, indent=2)}") 