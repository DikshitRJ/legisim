"""
Ripple engine schemas.
"""

from pydantic import BaseModel, Field
from enum import StrEnum

class DomainEnum(StrEnum):
    AGRICULTURE = "agriculture"
    MANUFACTURING = "manufacturing"
    SERVICES = "services"
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    INFRASTRUCTURE = "infrastructure"
    RETAIL = "retail"
    ENERGY = "energy"
    REAL_ESTATE = "real_estate"
    LOGISTICS = "logistics"
    PUBLIC_SECTOR = "public_sector"
    INFORMAL_SECTOR = "informal_sector"

class RippleNodeSchema(BaseModel):
    id: str
    domain: DomainEnum
    description: str
    impact_magnitude: float
    sentiment: float

class RippleEdgeSchema(BaseModel):
    source: str
    target: str
    relationship: str
    strength: float

__all__ = ["DomainEnum", "RippleNodeSchema", "RippleEdgeSchema"]
