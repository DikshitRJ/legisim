"""Pydantic V2 Schemas for Scenario Comparison.

Defines request and response schemas for multi-run comparative scenario analysis.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from app.schemas.common import CamelModel


class CompareRequest(CamelModel):
    """Request payload to compare multiple simulation runs side-by-side."""

    run_ids: list[str] = Field(
        ...,
        min_length=1,
        description="List of simulation run IDs to compare",
    )


class CompareResponse(CamelModel):
    """Response containing side-by-side comparison metrics for simulation runs."""

    comparison: dict[str, Any] = Field(
        default_factory=dict,
        description="Comparative analysis matrix and delta metrics",
    )


__all__: list[str] = [
    "CompareRequest",
    "CompareResponse",
]
