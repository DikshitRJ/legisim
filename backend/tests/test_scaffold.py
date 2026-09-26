"""Tests for LegiSim backend scaffold infrastructure."""

from __future__ import annotations

import pytest
from httpx import AsyncClient
from pydantic import Field

from app.config import Settings, settings
from app.core.exceptions import (
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)
from app.models.base import Base, TimestampMixin, UUIDMixin
from app.schemas.common import (
    CamelModel,
    ErrorResponse,
    HealthResponse,
    PaginatedResponse,
    SuccessResponse,
)


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client: AsyncClient) -> None:
    """Test that the /api/health endpoint returns 200 OK and valid health payload."""
    response = await async_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["environment"] == settings.ENVIRONMENT
    assert "version" in data


def test_settings_defaults() -> None:
    """Test default values of application Settings."""
    cfg = Settings()
    assert cfg.ENVIRONMENT in ["development", "production", "testing"]
    assert cfg.DOMAIN == "localhost"
    assert "postgresql+asyncpg://" in cfg.DATABASE_URL
    assert "redis://" in cfg.REDIS_URL
    assert cfg.S3_ENDPOINT == "localhost:9000"
    assert cfg.JWT_ALGORITHM == "HS256"


def test_common_schemas_camel_case() -> None:
    """Test that CamelModel correctly serializes snake_case attributes to camelCase."""

    class ExampleSchema(CamelModel):
        first_name: str
        is_active: bool
        total_score: float = Field(default=0.0)

    obj = ExampleSchema(first_name="Jane", is_active=True, total_score=99.5)
    serialized = obj.model_dump(by_alias=True)

    assert "firstName" in serialized
    assert serialized["firstName"] == "Jane"
    assert "isActive" in serialized
    assert serialized["isActive"] is True
    assert "totalScore" in serialized
    assert serialized["totalScore"] == 99.5

    success = SuccessResponse(success=True)
    assert success.success is True

    error = ErrorResponse(message="Sample error")
    assert error.message == "Sample error"

    health = HealthResponse(status="healthy", environment="development", version="0.1.0")
    assert health.status == "healthy"

    paginated = PaginatedResponse[str](
        items=["item1", "item2"],
        total=2,
        page=1,
        page_size=10,
        has_more=False,
    )
    assert paginated.total == 2
    assert paginated.page_size == 10
    paginated_dump = paginated.model_dump(by_alias=True)
    assert "pageSize" in paginated_dump
    assert "hasMore" in paginated_dump


def test_custom_http_exceptions() -> None:
    """Test custom exception classes have correct status codes and default details."""
    exc_404 = NotFoundError("Item not found")
    assert exc_404.status_code == 404
    assert exc_404.detail == "Item not found"

    exc_403 = ForbiddenError()
    assert exc_403.status_code == 403

    exc_400 = BadRequestError()
    assert exc_400.status_code == 400

    exc_409 = ConflictError()
    assert exc_409.status_code == 409

    exc_401 = UnauthorizedError()
    assert exc_401.status_code == 401


def test_models_base_and_mixins() -> None:
    """Test SQLAlchemy base metadata and mixin attributes."""
    assert hasattr(Base, "metadata")
    assert hasattr(UUIDMixin, "id")
    assert hasattr(TimestampMixin, "created_at")
    assert hasattr(TimestampMixin, "updated_at")
