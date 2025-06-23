from google.adk.agents import Agent

# Import specialized model for complex planning tasks
from ..models import PLANNER_MODEL
from .planner_agent_prompt import PROMPT as PLANNER_AGENT_PROMPT

PlannerAgent = Agent(
    model=PLANNER_MODEL,  # Use gemini-2.5-pro for complex reasoning
    name="planner_agent",
    description="Parses user prompt into a comprehensive execution plan with validation-correction loop support.",
    instruction=PLANNER_AGENT_PROMPT,
    output_key="plan",  # State management: outputs to state.plan
)

if __name__ == '__main__':
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from schemas import DiagramRequest # Re-import after path change
        print("Local test: schemas imported successfully.")
    except ImportError as e:
        print(f"Local test import error for schemas: {e}.")
        sys.exit(1)
    
    print("Conceptual local test for PlannerAgent (ADK 1.x compliant style):")
    try:
        print(f"PlannerAgent definition created: {PlannerAgent.name}")
        print(f"Output key: {PlannerAgent.output_key}")
        
        sample_request_data = DiagramRequest(user_prompt="e+ e- to Z gamma")
        print(f"Sample request for run(): {sample_request_data.model_dump_json(indent=2)}")
        
        print("PlannerAgent configured for state-based communication.")
        print("Local test conceptually finished.")

    except Exception as e:
        print(f"Error during local conceptual test: {e}")
        import traceback
        traceback.print_exc() 