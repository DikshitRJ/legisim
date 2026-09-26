from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, decode_access_token, verify_password
from app.models.officer import Officer, OfficerSession


async def authenticate_officer(db: AsyncSession, officer_id: str, password: str) -> tuple[Officer, str]:
    """Authenticate an officer and create a session."""
    stmt = select(Officer).where(Officer.email == officer_id)
    result = await db.execute(stmt)
    officer = result.scalar_one_or_none()

    if not officer or not verify_password(password, officer.password_hash):
        raise UnauthorizedError("Invalid credentials")

    token = create_access_token(data={"sub": str(officer.id)})
    payload = decode_access_token(token)

    if payload is None:
        raise UnauthorizedError("Failed to generate token")

    expires_at = datetime.fromtimestamp(payload["exp"], tz=UTC)

    session = OfficerSession(officer_id=officer.id, token=token, expires_at=expires_at)
    db.add(session)
    await db.commit()

    return officer, token


async def logout_officer(db: AsyncSession, token: str) -> bool:
    """Log out an officer by invalidating their session."""
    stmt = select(OfficerSession).where(OfficerSession.token == token)
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()

    if session:
        await db.delete(session)
        await db.commit()

    return True


async def get_officer_by_token(db: AsyncSession, token: str) -> Officer | None:
    """Retrieve an officer by their active session token."""
    stmt = select(OfficerSession).where(
        OfficerSession.token == token,
        OfficerSession.expires_at > datetime.now(UTC)
    )
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()

    if not session:
        return None

    officer_stmt = select(Officer).where(Officer.id == session.officer_id)
    officer_result = await db.execute(officer_stmt)
    return officer_result.scalar_one_or_none()
