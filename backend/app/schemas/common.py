"""Common Pydantic Schemas and Base Models.

Defines reusable base schemas, camelCase alias generators, and standardized
success and error response schemas across the API domains.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Base Pydantic model with automatic snake_case to camelCase aliasing.

    Enables ORM attribute reading and serialization using camelCase keys
    matching the OpenAPI 3.0 specifications.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class SuccessResponse(CamelModel):
    """Standard success acknowledgment response."""

    success: bool = True


class ErrorResponse(CamelModel):
    """Standard error response payload."""

    message: str


class HealthResponse(CamelModel):
    """Service health status response."""

    status: str
    environment: str
    version: str


class PaginatedResponse[T](CamelModel):
    """Generic wrapper for paginated result collections."""

    items: list[T]
    total: int
    page: int
    page_size: int
    has_more: bool
