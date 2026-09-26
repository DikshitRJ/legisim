"""
Cohort and Demographics schemas.
"""

from pydantic import BaseModel, Field
from typing import TypedDict, List, Dict, Any, Annotated

class Demographics(BaseModel):
    region: str
    age_band: str
    gender: str
    income_band: str
    occupation: str
    urban_rural: str
    education: str
    literacy: str

class SpendMix(BaseModel):
    food: float
    housing: float
    transport: float
    healthcare: float
    education: float
    other: float

class CohortCard(BaseModel):
    id: str
    demographics: Demographics
    spend_mix: SpendMix
    trust_in_govt: float
    ideological_lean: float
    agreeableness: float
    size: int
    weight: float

class BehaviourChange(BaseModel):
    description: str
    magnitude: float
    direction: int

class Stance(BaseModel):
    sentiment: str
    intensity: float
    rationale: str

class ReactionOutput(BaseModel):
    cohort_id: str
    behaviour_changes: List[BehaviourChange]
    stance: Stance
    public_acceptance: float
    confidence: float
    source: str

class CohortState(TypedDict, total=False):
    cohort_id: str
    policy_summary: str
    background_context: str
    reaction: ReactionOutput

__all__ = [
    "Demographics",
    "SpendMix",
    "CohortCard",
    "BehaviourChange",
    "Stance",
    "ReactionOutput",
    "CohortState"
]
