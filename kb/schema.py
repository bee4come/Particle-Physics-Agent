from pydantic import BaseModel, Field
from typing import List, Optional

class FeynmanRecord(BaseModel):
    topic: str
    reaction: str
    particles: List[str]
    description: str
    tikz: str
    process_type: str
    source: Optional[str] = None
    embedding: Optional[List[float]] = Field(default=None, repr=False)
