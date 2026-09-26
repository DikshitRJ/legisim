"""
JEV (Just Enough Verification) system schemas.
"""

from pydantic import BaseModel, Field
from typing import List

class PersonaInput(BaseModel):
    id: str
    text_representation: str

class EvalRequest(BaseModel):
    targeting_profile: str
    personas: List[PersonaInput]
    threshold: float = 0.5

class JEVPersonaScore(BaseModel):
    id: str
    score: float
    relevant: bool

class JEVEvalResponse(BaseModel):
    results: List[JEVPersonaScore]
    execution_time_ms: int

class TargetingProfile(BaseModel):
    policy_id: str = ""
    summary: str
    direct_impact_criteria: str
    indirect_impact_criteria: str
    geographic_focus: str
    economic_channels: List[str] = Field(default_factory=list)

__all__ = [
    "PersonaInput",
    "EvalRequest",
    "JEVPersonaScore",
    "JEVEvalResponse",
    "TargetingProfile",
]
