"""Notebook Pydantic Schemas.

Defines request and response schemas for the Notebooks domain,
adhering to the OpenAPI 3.0 specification.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import Field, field_validator

from app.schemas.common import CamelModel, SuccessResponse


class NotebookStatus(StrEnum):
    """Lifecycle status of a simulation notebook."""

    ACTIVE = "active"
    ARCHIVED = "archived"


class NotebookCreate(CamelModel):
    """Schema for creating a new notebook."""

    title: str = Field(..., description="Human-readable title of the notebook.")
    description: str = Field(..., description="Detailed description of the notebook.")


class NotebookUpdate(CamelModel):
    """Schema for updating notebook details."""

    title: str | None = Field(default=None, description="Updated title.")
    description: str | None = Field(default=None, description="Updated description.")


class NotebookResponse(CamelModel):
    """Schema representing a notebook response matching the OpenAPI Notebook model."""

    id: str = Field(..., description="Unique identifier for the notebook.")
    title: str = Field(..., description="Human-readable title of the notebook.")
    description: str = Field(..., description="Detailed description of the notebook.")
    sources: int = Field(default=0, description="Number of sources attached to the notebook.")
    modified_at: datetime = Field(..., description="ISO-8601 timestamp of last modification.")
    status: NotebookStatus = Field(..., description="Current lifecycle status.")

    @field_validator("id", mode="before")
    @classmethod
    def serialize_id(cls, v: Any) -> str:
        """Ensure UUID instances or other ID types are converted to strings."""
        if isinstance(v, uuid.UUID):
            return str(v)
        return str(v) if v is not None else ""

    @field_validator("sources", mode="before")
    @classmethod
    def serialize_sources(cls, v: Any) -> int:
        """Default sources to 0 if None."""
        return v if v is not None else 0

    @field_validator("description", mode="before")
    @classmethod
    def serialize_description(cls, v: Any) -> str:
        """Default description to empty string if None."""
        return v if v is not None else ""


# Alias matching OpenAPI schema name
Notebook = NotebookResponse

__all__ = [
    "Notebook",
    "NotebookCreate",
    "NotebookResponse",
    "NotebookStatus",
    "NotebookUpdate",
    "SuccessResponse",
]
