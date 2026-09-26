"""Pydantic V2 Schemas for the Ripple Graph Domain.

Defines schemas matching the ripple/openapi.yaml specification for causal graph
nodes, directed transmission edges, and full graph query responses.
"""

from __future__ import annotations

from typing import Literal

from app.schemas.run import (
    EvidenceKind,
    RippleEdge,
    RippleGraph,
    RippleGraphResponse,
    RippleNode,
)

# Standard causal domains per ripple/openapi.yaml
RippleDomain = Literal[
    "policy",
    "transport",
    "agriculture",
    "business",
    "consumer",
    "income",
    "economy",
    "social",
    "political",
    "fiscal",
    "health",
    "education",
    "energy",
    "employment",
]

ConfidenceLevel = Literal["High", "Medium", "Low", "high", "medium", "low"]

__all__: list[str] = [
    "RippleDomain",
    "ConfidenceLevel",
    "EvidenceKind",
    "RippleNode",
    "RippleEdge",
    "RippleGraph",
    "RippleGraphResponse",
]
