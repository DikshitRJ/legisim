from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class Persona(Base):
    __tablename__ = 'personas'

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    age: Mapped[str] = mapped_column(String(255))
    income: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))
    education: Mapped[str] = mapped_column(String(255))
    occupation: Mapped[str] = mapped_column(String(255))
    region: Mapped[str] = mapped_column(String(255))
    assets_and_vulnerabilities: Mapped[Any | None] = mapped_column(JSONB)
    economic_dependency: Mapped[Any | None] = mapped_column(JSONB)

class CohortCard(Base):
    __tablename__ = 'cohort_cards'

    cohort_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    weight: Mapped[int] = mapped_column(Integer)
    region: Mapped[str] = mapped_column(String(255))
    urban_rural: Mapped[str] = mapped_column(String(255))
    income_band: Mapped[str] = mapped_column(String(255))
    occupation: Mapped[str] = mapped_column(String(255))
    age_band: Mapped[str] = mapped_column(String(255))
    education: Mapped[str] = mapped_column(String(255))
    spend_mix: Mapped[Any | None] = mapped_column(JSONB)
    trust_in_govt: Mapped[float | None] = mapped_column(Float)
    agreeableness_lean: Mapped[float | None] = mapped_column(Float)
    assets_and_vulnerabilities: Mapped[Any | None] = mapped_column(JSONB)
    economic_dependency: Mapped[Any | None] = mapped_column(JSONB)

class TargetingProfile(Base, UUIDMixin):
    __tablename__ = 'targeting_profiles'

    policy_id: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str | None] = mapped_column(Text)
    direct_impact_criteria: Mapped[str | None] = mapped_column(Text)
    indirect_impact_criteria: Mapped[str | None] = mapped_column(Text)
    geographic_focus: Mapped[str | None] = mapped_column(Text)
    economic_channels: Mapped[Any | None] = mapped_column(JSONB)

class JEVSelectionResult(Base, UUIDMixin):
    __tablename__ = 'jev_selection_results'

    targeting_profile_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('targeting_profiles.id', ondelete='CASCADE'))
    policy_id: Mapped[str] = mapped_column(String(255))
    threshold: Mapped[float | None] = mapped_column(Float)
    total_evaluated: Mapped[int | None] = mapped_column(Integer)
    total_selected: Mapped[int | None] = mapped_column(Integer)
    execution_time_ms: Mapped[int | None] = mapped_column(Integer)
    results: Mapped[Any | None] = mapped_column(JSONB)

class CohortReaction(Base, UUIDMixin):
    __tablename__ = 'cohort_reactions'

    cohort_id: Mapped[str] = mapped_column(String(255), ForeignKey('cohort_cards.cohort_id', ondelete='CASCADE'))
    simulation_step: Mapped[int] = mapped_column(Integer)
    stance_support: Mapped[float | None] = mapped_column(Float)
    stance_neutral: Mapped[float | None] = mapped_column(Float)
    stance_oppose: Mapped[float | None] = mapped_column(Float)
    behaviour_changes: Mapped[Any | None] = mapped_column(JSONB)
    reasoning: Mapped[str | None] = mapped_column(Text)
    analogue_ids: Mapped[Any | None] = mapped_column(JSONB)
    confidence: Mapped[float | None] = mapped_column(Float)
