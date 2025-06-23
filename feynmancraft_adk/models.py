"""Model configurations for different agents."""

from .shared_libraries.config import get_model_for_agent

# Complex agents use gemini-2.5-pro for better reasoning
PLANNER_MODEL = get_model_for_agent("planner")
GENERATOR_MODEL = get_model_for_agent("generator") 
PHYSICS_VALIDATOR_MODEL = get_model_for_agent("physics_validator")

# Simple agents use gemini-2.5-flash for speed
KB_RETRIEVER_MODEL = get_model_for_agent("kb_retriever")
TIKZ_VALIDATOR_MODEL = get_model_for_agent("tikz_validator")
FEEDBACK_MODEL = get_model_for_agent("feedback")

# Default model
DEFAULT_MODEL = get_model_for_agent("default")