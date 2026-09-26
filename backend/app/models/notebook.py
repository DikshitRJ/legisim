"""Notebook and NotebookSession ORM models for the Notebooks domain.

Defines the notebooks and sessions tables per notebooks/database.md spec.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class Notebook(Base, UUIDMixin):
    """High-level notebook metadata container for simulation configurations."""

    __tablename__ = "notebooks"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    sources: Mapped[int | None] = mapped_column(Integer, server_default=text("0"))
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    sessions: Mapped[list[NotebookSession]] = relationship(
        "NotebookSession", back_populates="notebook", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("status IN ('active', 'archived')", name="check_notebook_status"),
        Index("idx_notebooks_status", "status"),
    )


class NotebookSession(Base, UUIDMixin):
    """Individual simulation or user session associated with a notebook."""

    __tablename__ = "sessions"

    notebook_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("notebooks.id", ondelete="CASCADE")
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    notebook: Mapped[Notebook] = relationship("Notebook", back_populates="sessions")

    __table_args__ = (
        CheckConstraint("status IN ('active', 'ended')", name="check_session_status"),
        Index("idx_sessions_notebook_id", "notebook_id"),
    )
