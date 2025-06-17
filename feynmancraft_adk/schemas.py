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

class TikzSnippet(BaseModel):
    code: str
    description: Optional[str]

class ValidationReport(BaseModel):
    ok: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

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

class DiagramGenerationInput(BaseModel):
    user_prompt: str
    style_hint: Optional[str] = None
    examples: Optional[List[TikzSnippet]] = Field(default_factory=list)

class FeedbackAgentInput(BaseModel):
    generated_snippet: TikzSnippet
    physics_report: PhysicsValidationReport
    compile_report: ValidationReport 