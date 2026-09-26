"""Officer and OfficerSession ORM models for the Auth domain.

Defines the officers and officer_sessions tables per auth/database.md spec.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Officer(Base, UUIDMixin, TimestampMixin):
    """Officer (user) credentials and profile."""

    __tablename__ = "officers"

    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), server_default=text("'officer'"))

    sessions: Mapped[list[OfficerSession]] = relationship(
        "OfficerSession", back_populates="officer", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("idx_officers_email", "email"),)


class OfficerSession(Base, UUIDMixin):
    """Active login session with authentication token."""

    __tablename__ = "officer_sessions"

    officer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("officers.id", ondelete="CASCADE")
    )
    token: Mapped[str] = mapped_column(String(512), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    officer: Mapped[Officer] = relationship("Officer", back_populates="sessions")

    __table_args__ = (
        Index("idx_officer_sessions_token", "token"),
        Index("idx_officer_sessions_officer_id", "officer_id"),
    )
