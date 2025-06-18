# feynmancraft_adk/schemas.py
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class Particle(BaseModel):
    name: str
    charge: float
    spin: float

class DiagramRequest(BaseModel):
    user_prompt: str
    style_hint: Optional[str] = None

class PlanStep(str, Enum):
    RETRIEVE_EXAMPLES = "retrieve_examples"
    GENERATE_TIKZ     = "generate_tikz"
    VALIDATE_TIKZ     = "validate_tikz"
    VALIDATE_PHYSICS  = "validate_physics"
    FEEDBACK          = "feedback"

class Plan(BaseModel):
    steps: List[PlanStep] = Field(default_factory=list)
    original_prompt: str
    physics_process: Optional[str] = None
    particles_involved: List[str] = Field(default_factory=list)

class TikzSnippet(BaseModel):
    code: str
    description: Optional[str] = None

class ValidationReport(BaseModel):
    ok: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    details: Optional[str] = None

# --- New Schemas for Physics Validation ---

class RuleValidationReport(BaseModel):
    """Report for a single physics rule validation."""
    rule_number: int
    title: str
    validation_type: str = Field(description="Either 'text' or 'computational'.")
    passed: bool
    pass_fail_reason: str = Field(description="Explanation of why the rule passed or failed.")

class PhysicsValidationReport(BaseModel):
    """A comprehensive report from the PhysicsValidatorAgent."""
    user_process: str
    validation_report: List[RuleValidationReport]
    overall_conclusion: str

class FinalAnswer(BaseModel):
    tikz: TikzSnippet
    physics_report: PhysicsValidationReport
    compile_report: ValidationReport
    summary: Optional[str] = None

class DiagramGenerationInput(BaseModel):
    user_prompt: str
    style_hint: Optional[str] = None
    examples: Optional[List[TikzSnippet]] = Field(default_factory=list)

class FeedbackAgentInput(BaseModel):
    generated_snippet: TikzSnippet
    physics_report: PhysicsValidationReport
    compile_report: ValidationReport

# NEW: Workflow State Management
class WorkflowState(BaseModel):
    """Central state object for agent-to-agent communication."""
    
    # Input
    user_request: Optional[str] = None
    style_hint: Optional[str] = None
    
    # Planning phase
    plan: Optional[Plan] = None
    
    # Knowledge retrieval phase  
    examples: Optional[List[TikzSnippet]] = Field(default_factory=list)
    search_metadata: Optional[dict] = None
    
    # Generation phase
    tikz_code: Optional[str] = None
    generation_metadata: Optional[dict] = None
    
    # Validation phases
    tikz_validation_report: Optional[ValidationReport] = None
    physics_validation_report: Optional[PhysicsValidationReport] = None
    
    # Final synthesis
    final_response: Optional[str] = None
    
    # System metadata
    workflow_step: Optional[str] = None
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class StateUpdate(BaseModel):
    """Represents an update to the workflow state from an agent."""
    agent_name: str
    output_key: str
    data: dict
    metadata: Optional[dict] = None 