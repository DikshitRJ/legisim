"""Ripple Graph ORM models (standalone causal graph tables).

Defines RippleNode and RippleEdge tables per ripple/database.md spec.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class RippleNode(Base, UUIDMixin):
    """Causal node in the ripple graph for a simulation run."""

    __tablename__ = "ripple_node"

    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("simulation_runs.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    layer: Mapped[int] = mapped_column(Integer, nullable=False)
    domain: Mapped[str] = mapped_column(String(50), nullable=False)
    magnitude: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[str] = mapped_column(String(20), nullable=False)
    kind: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        Index("idx_ripple_node_run_id", "run_id"),
        Index("idx_ripple_node_domain", "domain"),
        Index("idx_ripple_node_layer", "layer"),
    )


class RippleEdge(Base, UUIDMixin):
    """Directed causal link between two ripple nodes."""

    __tablename__ = "ripple_edge"

    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("simulation_runs.id", ondelete="CASCADE"), nullable=False
    )
    source_node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("ripple_node.id", ondelete="CASCADE"), nullable=False
    )
    target_node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("ripple_node.id", ondelete="CASCADE"), nullable=False
    )
    strength: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    lag_months: Mapped[int] = mapped_column(Integer, nullable=False)
    mechanism: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    source_node: Mapped[RippleNode] = relationship("RippleNode", foreign_keys=[source_node_id])
    target_node: Mapped[RippleNode] = relationship("RippleNode", foreign_keys=[target_node_id])

    __table_args__ = (
        Index("idx_ripple_edge_run_id", "run_id"),
        Index("idx_ripple_edge_source_node_id", "source_node_id"),
        Index("idx_ripple_edge_target_node_id", "target_node_id"),
    )
