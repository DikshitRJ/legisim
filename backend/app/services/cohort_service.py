from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cohort import CohortReaction
from app.models.cohort import Persona as PersonaModel
from app.schemas.cohort import (
    CohortCategory,
    CohortReactionCreate,
    HydratedPrompt,
    JEVPersonaScore,
    JEVSelectionResult,
    PersonaDemographics,
    PersonaSchema,
    PolicyInput,
    TargetingProfile,
)


async def list_personas(db: AsyncSession) -> list[PersonaSchema]:
    """Query all personas from DB and map to PersonaSchema with nested demographics."""
    result = await db.execute(select(PersonaModel))
    personas_db = result.scalars().all()

    personas_schema = []
    for p in personas_db:
        demo = PersonaDemographics(
            age=p.age,
            income=p.income,
            location=p.location,
            education=p.education,
            occupation=p.occupation,
            region=p.region
        )
        p_schema = PersonaSchema(
            id=p.id,
            demographics=demo,
            assets_and_vulnerabilities=p.assets_and_vulnerabilities or [],
            economic_dependency=p.economic_dependency or []
        )
        personas_schema.append(p_schema)

    return personas_schema

async def get_cohort_categories() -> list[CohortCategory]:
    """Return hardcoded categories for the simulation wizard."""
    return [
        CohortCategory(
            id="cat-1",
            number="01",
            title="Income Group",
            options=["Low Income", "Middle Income", "High Income"]
        ),
        CohortCategory(
            id="cat-2",
            number="02",
            title="Region",
            options=["North", "South", "East", "West"]
        )
    ]

async def generate_targeting_profile(policy_input: PolicyInput) -> TargetingProfile:
    """STUB: return mock targeting profile."""
    return TargetingProfile(
        policy_id="mock-policy-123",
        summary=f"Targeting profile for {policy_input.what_changes}",
        direct_impact_criteria="Individuals directly affected by the policy.",
        indirect_impact_criteria="Businesses and families indirectly affected.",
        geographic_focus=policy_input.geographic_coverage,
        economic_channels=["Taxation", "Subsidies"]
    )

async def run_jev_selection(policy_id: str, targeting_profile: TargetingProfile, threshold: float) -> JEVSelectionResult:
    """STUB: return mock selection result."""
    return JEVSelectionResult(
        policy_id=policy_id,
        threshold=threshold,
        total_evaluated=100,
        total_selected=2,
        results=[
            JEVPersonaScore(id="persona-1", score=0.85, relevant=True),
            JEVPersonaScore(id="persona-2", score=0.72, relevant=True)
        ],
        execution_time_ms=1250
    )

async def hydrate_prompts(persona_ids: list[str], local_context: str, memory_summary: str) -> list[HydratedPrompt]:
    """STUB: hydrate prompts for given personas."""
    return [
        HydratedPrompt(
            persona_id=pid,
            prompt_text=f"Act as persona {pid} considering {local_context} with memory {memory_summary}."
        )
        for pid in persona_ids
    ]

async def submit_reactions(db: AsyncSession, reactions: list[CohortReactionCreate]) -> None:
    """Save cohort reactions to DB."""
    for reaction in reactions:
        db_reaction = CohortReaction(
            id=str(uuid.uuid4()),
            cohort_id=reaction.cohort_id,
            simulation_step=reaction.simulation_step,
            stance_support=reaction.stance_support,
            stance_neutral=reaction.stance_neutral,
            stance_oppose=reaction.stance_oppose,
            behaviour_changes=reaction.behaviour_changes,
            reasoning=reaction.reasoning,
            analogue_ids=reaction.analogue_ids,
            confidence=reaction.confidence
        )
        db.add(db_reaction)
    await db.commit()
