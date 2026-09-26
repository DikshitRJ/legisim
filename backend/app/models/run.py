from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class SimulationRun(Base, UUIDMixin, TimestampMixin):
    __tablename__ = 'simulation_runs'

    notebook_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('notebooks.id', ondelete='CASCADE'))
    policy_text: Mapped[str | None] = mapped_column(Text)
    cohort_config: Mapped[Any | None] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String(50))
    progress: Mapped[int | None] = mapped_column(Integer, server_default=text("0"))

    # Relationships
    events: Mapped[list[RunEvent]] = relationship(back_populates="run", cascade="all, delete-orphan")
    summary: Mapped[RunSummary | None] = relationship(back_populates="run", cascade="all, delete-orphan", uselist=False)
    cohort_groups: Mapped[list[RunCohortGroup]] = relationship(back_populates="run", cascade="all, delete-orphan")
    state_data: Mapped[list[RunStateData]] = relationship(back_populates="run", cascade="all, delete-orphan")
    ripple_nodes: Mapped[list[RunRippleNode]] = relationship(back_populates="run", cascade="all, delete-orphan")
    ripple_edges: Mapped[list[RunRippleEdge]] = relationship(back_populates="run", cascade="all, delete-orphan")
    timeline_data: Mapped[list[RunTimelineData]] = relationship(back_populates="run", cascade="all, delete-orphan")
    chart_data: Mapped[list[RunChartData]] = relationship(back_populates="run", cascade="all, delete-orphan")
    report: Mapped[RunReport | None] = relationship(back_populates="run", cascade="all, delete-orphan", uselist=False)

    __table_args__ = (
        CheckConstraint("status IN ('loading', 'research', 'simulation', 'analysis', 'complete')", name='check_run_status'),
    )

class RunEvent(Base, UUIDMixin):
    __tablename__ = 'run_events'

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('simulation_runs.id', ondelete='CASCADE'))
    event_type: Mapped[str] = mapped_column(String(255))
    payload: Mapped[Any | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    run: Mapped[SimulationRun] = relationship(back_populates="events")

    __table_args__ = (
        Index('idx_run_events_run_id_created_at', 'run_id', 'created_at'),
    )

class RunSummary(Base, UUIDMixin):
    __tablename__ = 'run_summaries'

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('simulation_runs.id', ondelete='CASCADE'), unique=True)
    sections: Mapped[Any | None] = mapped_column(JSONB)
    metrics: Mapped[Any | None] = mapped_column(JSONB)

    run: Mapped[SimulationRun] = relationship(back_populates="summary")

class RunCohortGroup(Base, UUIDMixin):
    __tablename__ = 'run_cohort_groups'

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('simulation_runs.id', ondelete='CASCADE'))
    group_id: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    population: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    stance_support: Mapped[float | None] = mapped_column(Float)
    stance_neutral: Mapped[float | None] = mapped_column(Float)
    stance_oppose: Mapped[float | None] = mapped_column(Float)
    income_change: Mapped[float | None] = mapped_column(Float)
    behaviors: Mapped[Any | None] = mapped_column(JSONB)
    confidence: Mapped[str] = mapped_column(String(255))

    run: Mapped[SimulationRun] = relationship(back_populates="cohort_groups")

    __table_args__ = (
        Index('idx_run_cohort_groups_run_id', 'run_id'),
    )

class RunStateData(Base, UUIDMixin):
    __tablename__ = 'run_state_data'

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('simulation_runs.id', ondelete='CASCADE'))
    state_code: Mapped[str] = mapped_column(String(50))
    state_name: Mapped[str] = mapped_column(String(255))
    income_change: Mapped[float | None] = mapped_column(Float)
    inflation_impact: Mapped[float | None] = mapped_column(Float)
    acceptance: Mapped[float | None] = mapped_column(Float)
    jobs_affected: Mapped[int | None] = mapped_column(Integer)

    run: Mapped[SimulationRun] = relationship(back_populates="state_data")

    __table_args__ = (
        Index('idx_run_state_data_run_id_state_code', 'run_id', 'state_code'),
    )

class RunRippleNode(Base, UUIDMixin):
    __tablename__ = 'run_ripple_nodes'

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('simulation_runs.id', ondelete='CASCADE'))
    node_id: Mapped[str] = mapped_column(String(255))
    label: Mapped[str] = mapped_column(String(255))
    layer: Mapped[int] = mapped_column(Integer)
    domain: Mapped[str] = mapped_column(String(255))
    magnitude: Mapped[str] = mapped_column(String(255))
    confidence: Mapped[str] = mapped_column(String(255))
    kind: Mapped[str] = mapped_column(String(255))

    run: Mapped[SimulationRun] = relationship(back_populates="ripple_nodes")

    __table_args__ = (
        Index('idx_run_ripple_nodes_run_id', 'run_id'),
    )

class RunRippleEdge(Base, UUIDMixin):
    __tablename__ = 'run_ripple_edges'

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('simulation_runs.id', ondelete='CASCADE'))
    source_node: Mapped[str] = mapped_column(String(255))
    target_node: Mapped[str] = mapped_column(String(255))
    strength: Mapped[float] = mapped_column(Float)
    lag_months: Mapped[int] = mapped_column(Integer)
    mechanism: Mapped[str | None] = mapped_column(Text)

    run: Mapped[SimulationRun] = relationship(back_populates="ripple_edges")

    __table_args__ = (
        Index('idx_run_ripple_edges_run_id', 'run_id'),
    )

class RunTimelineData(Base, UUIDMixin):
    __tablename__ = 'run_timeline_data'

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('simulation_runs.id', ondelete='CASCADE'))
    month: Mapped[int] = mapped_column(Integer)
    label: Mapped[str] = mapped_column(String(255))
    income_change: Mapped[float | None] = mapped_column(Float)
    inflation_impact: Mapped[float | None] = mapped_column(Float)
    acceptance: Mapped[float | None] = mapped_column(Float)
    employment: Mapped[float | None] = mapped_column(Float)

    run: Mapped[SimulationRun] = relationship(back_populates="timeline_data")

    __table_args__ = (
        Index('idx_run_timeline_data_run_id_month', 'run_id', 'month'),
    )

class RunChartData(Base, UUIDMixin):
    __tablename__ = 'run_chart_data'

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('simulation_runs.id', ondelete='CASCADE'))
    chart_type: Mapped[str] = mapped_column(String(255))
    data_payload: Mapped[Any | None] = mapped_column(JSONB)

    run: Mapped[SimulationRun] = relationship(back_populates="chart_data")

    __table_args__ = (
        Index('idx_run_chart_data_run_id_chart_type', 'run_id', 'chart_type'),
    )

class RunReport(Base, UUIDMixin):
    __tablename__ = 'run_reports'

    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('simulation_runs.id', ondelete='CASCADE'), unique=True)
    markdown_content: Mapped[str | None] = mapped_column(Text)

    run: Mapped[SimulationRun] = relationship(back_populates="report")
