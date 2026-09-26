"""
Critic evaluation schemas.
"""

from pydantic import BaseModel
from typing import List

class EvidenceMapping(BaseModel):
    claim_id: str
    supporting_evidence: List[str]
    contradicting_evidence: List[str]

class CriticFeedback(BaseModel):
    overall_score: float
    major_flaws: List[str]
    evidence_mappings: List[EvidenceMapping]
    suggested_improvements: List[str]
    is_approved: bool

__all__ = ["EvidenceMapping", "CriticFeedback"]
