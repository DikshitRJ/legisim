from __future__ import annotations

from typing import Any

from app.schemas.common import CamelModel


class CohortCategory(CamelModel):
    id: str
    number: str
    title: str
    options: list[str]


class PersonaDemographics(CamelModel):
    age: str
    income: str
    location: str
    education: str | None = None
    occupation: str | None = None
    region: str | None = None


class PersonaSchema(CamelModel):
    id: str
    demographics: PersonaDemographics
    assets_and_vulnerabilities: list[str]
    economic_dependency: list[str]


class PolicyInput(CamelModel):
    what_changes: str
    size_of_change: str
    change_type: str
    target_group: str
    geographic_coverage: str
    start_date: str | None = None
    rollout_phases: list[str] | None = None


class TargetingProfile(CamelModel):
    policy_id: str
    summary: str
    direct_impact_criteria: str
    indirect_impact_criteria: str
    geographic_focus: str
    economic_channels: list[str] | None = None


class JEVPersonaScore(CamelModel):
    id: str
    score: float
    relevant: bool


class JEVSelectionResult(CamelModel):
    policy_id: str
    threshold: float
    total_evaluated: int
    total_selected: int
    results: list[JEVPersonaScore]
    execution_time_ms: int


class HydratedPrompt(CamelModel):
    persona_id: str
    prompt_text: str


class CohortReactionCreate(CamelModel):
    cohort_id: str
    simulation_step: int
    stance_support: float
    stance_neutral: float
    stance_oppose: float
    behaviour_changes: list[dict[str, Any]]
    reasoning: str
    analogue_ids: list[str]
    confidence: float
