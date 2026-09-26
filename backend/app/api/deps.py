from __future__ import annotations

from typing import Any

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import UnauthorizedError
from app.models.officer import Officer
from app.services.auth_service import get_officer_by_token
from app.services.s3_service import S3Service

security = HTTPBearer()


def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extract token from HTTP Bearer auth."""
    return credentials.credentials


async def get_current_user(
    token: str = Depends(get_token),
    db: AsyncSession = Depends(get_db),
) -> Officer:
    """Retrieve the currently authenticated officer based on token."""
    officer = await get_officer_by_token(db, token)
    if not officer:
        raise UnauthorizedError("Invalid or expired token")
    return officer


def get_redis(request: Request) -> Any | None:
    """Get Redis connection from application state."""
    return getattr(request.app.state, "redis", None)


def get_s3(request: Request) -> Any | None:
    """Get S3 session from application state."""
    return getattr(request.app.state, "s3_session", None)


def get_s3_service(request: Request) -> S3Service:
    """Get S3Service instance initialized with the application S3 session."""
    session = getattr(request.app.state, "s3_session", None)
    return S3Service(session=session)


# Re-export get_db
__all__ = [
    "S3Service",
    "get_current_user",
    "get_db",
    "get_redis",
    "get_s3",
    "get_s3_service",
    "get_token",
]

