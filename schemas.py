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

class TikzSnippet(BaseModel):
    code: str
    description: Optional[str]

class ValidationReport(BaseModel):
    ok: bool
    errors: List[str] = Field(default_factory=list)

class FinalAnswer(BaseModel):
    tikz: TikzSnippet
    physics_report: ValidationReport
    compile_report: ValidationReport 