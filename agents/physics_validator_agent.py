from google.adk.agents import Agent
from google.adk.messages import JSONMessage
from feynmancraft_adk.schemas import ValidationReport, TikzSnippet # Assuming input might be TikzSnippet
from feyncore.physics.physics_validator import PhysicsValidator as CorePhysicsValidator
import json

class PhysicsValidatorAgent(Agent):
    """
    Validates the physical correctness of a Feynman diagram description or generated code.
    This version calls the feyncore.physics.physics_validator placeholder.
    """
    def __init__(self, particle_data_source: str = None):
        super().__init__(name="PhysicsValidatorAgent")
        # Initialize the core physics validation logic from feyncore
        # The particle_data_source would be the path to actual particle data file/db
        # For the placeholder, it's just illustrative.
        self.core_validator = CorePhysicsValidator(particle_data_source="path/to/particle_data.json")
        print(f"{self.name} initialized.")

    def run(self, message: JSONMessage) -> JSONMessage:
        """
        Validates the physics of the diagram based on the input message.

        Args:
            message: JSONMessage containing information about the diagram.
                     The body could be a TikzSnippet or a more structured representation.

        Returns:
            JSONMessage with a body containing a ValidationReport.
        """
        print(f"{self.name} received input: {message.body}")
        
        # Try to parse as TikzSnippet to get a description or code for context
        # This is a placeholder for how the agent might extract relevant info.
        # A more robust implementation would expect a defined input schema.
        diagram_info_for_core_validator = {}
        try:
            snippet = TikzSnippet(**message.body)
            diagram_info_for_core_validator = {
                "description": snippet.description,
                "tikz_code": snippet.code
                # Potentially parse particles from description or code if needed by core_validator
            }
            print(f"{self.name} parsed input as TikzSnippet.")
        except Exception:
            # If not a TikzSnippet, maybe it's another structure or just a general dict
            diagram_info_for_core_validator = message.body
            print(f"{self.name} could not parse input as TikzSnippet, using raw body for core validator.")

        # Use the core validator (currently a placeholder)
        # The core_validator.check_conservation_laws expects a dict `diagram_info`
        core_validation_results = self.core_validator.check_conservation_laws(diagram_info=diagram_info_for_core_validator)

        # Create ValidationReport based on the results from the core validator
        # The placeholder core_validator returns a dict like:
        # {"charge_conserved": "Not implemented", ..., "errors": ["Physics validation logic not yet implemented."]}
        
        is_ok_core = not bool(core_validation_results.get("errors"))
        errors_from_core = core_validation_results.get("errors", [])
        
        # Add more details from core_validation_results to errors if needed
        if not is_ok_core and not errors_from_core:
             errors_from_core.append("Core physics validator indicated failure without specific errors.")
        elif is_ok_core and errors_from_core: # Should not happen if logic is consistent
            is_ok_core = False # If there are errors, it's not okay

        report = ValidationReport(ok=is_ok_core, errors=errors_from_core)
        
        print(f"{self.name} generated report: {report.dict()}")
        return JSONMessage(body=json.loads(report.json()))

if __name__ == '__main__':
    # This is for local testing of the agent if needed
    physics_agent = PhysicsValidatorAgent()
    
    # Test with a TikzSnippet-like input
    test_diagram_body = {
        "code": "\\feynmandiagram{e- -> e- g}",
        "description": "Electron emitting a gluon (incorrect for QED)"
    }
    test_message = JSONMessage(body=test_diagram_body)
    output = physics_agent.run(test_message)
    print(f"PhysicsValidatorAgent output (TikzSnippet input): {json.dumps(output.body, indent=2)}")

    # Test with a more generic dict input
    generic_input_body = {
        "process_description": "muon decay to electron, electron antineutrino, muon neutrino",
        "incoming_particles": [{"name": "mu-"}],
        "outgoing_particles": [{"name": "e-"}, {"name": "anti-nu_e"}, {"name": "nu_mu"}]
    }
    generic_message = JSONMessage(body=generic_input_body)
    output_generic = physics_agent.run(generic_message)
    print(f"PhysicsValidatorAgent output (Generic input): {json.dumps(output_generic.body, indent=2)}") 