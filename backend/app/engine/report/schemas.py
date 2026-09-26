"""
Report generation schemas.
"""

from pydantic import BaseModel, Field
from enum import StrEnum
from typing import List

class ClaimSource(StrEnum):
    MEASURED = "measured"
    MODELLED = "modelled"
    JUDGED = "judged"

class SectionID(StrEnum):
    EXECUTIVE_SUMMARY = "executive_summary"
    POLICY_OVERVIEW = "policy_overview"
    ECONOMIC_IMPACT = "economic_impact"
    SOCIAL_IMPACT = "social_impact"
    REGIONAL_IMPACT = "regional_impact"
    IMPLEMENTATION_RISKS = "implementation_risks"
    RECOMMENDATIONS = "recommendations"
    METHODOLOGY = "methodology"

class PersonaSpotlight(BaseModel):
    cohort_id: str
    story: str = Field(..., max_length=500)

class ImpactItem(BaseModel):
    metric_name: str
    value: float
    description: str

class ReportClaim(BaseModel):
    claim_id: str = Field(..., pattern=r"^claim_\d{2,3}$")
    statement: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    source: ClaimSource

class ReportSection(BaseModel):
    section_id: SectionID
    title: str
    content: str
    claims: List[ReportClaim] = Field(default_factory=list)
    impacts: List[ImpactItem] = Field(default_factory=list)
    spotlights: List[PersonaSpotlight] = Field(default_factory=list)

class FullReport(BaseModel):
    title: str
    sections: List[ReportSection] = Field(..., min_length=8, max_length=8)

__all__ = [
    "ClaimSource",
    "SectionID",
    "PersonaSpotlight",
    "ImpactItem",
    "ReportClaim",
    "ReportSection",
    "FullReport"
]
