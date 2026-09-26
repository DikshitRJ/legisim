from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, cast

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return str(pwd_context.hash(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return bool(pwd_context.verify(plain_password, hashed_password))


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return str(encoded_jwt)


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decode a JWT token, returning the payload if valid."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return cast(dict[str, Any], payload)
    except JWTError:
        return None
