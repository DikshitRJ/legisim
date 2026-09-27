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
    """Return comprehensive categories for the simulation questionnaire wizard.

    These categories capture the key socio-economic dimensions needed to
    define the population cohorts that will react to the simulated policy.
    """
    return [
        CohortCategory(
            id="cat-income",
            number="01",
            title="Household Income (Annual)",
            options=[
                "Below ₹1 lakh",
                "₹1–3 lakh",
                "₹3–6 lakh",
                "₹6–10 lakh",
                "₹10–25 lakh",
                "Above ₹25 lakh",
            ],
        ),
        CohortCategory(
            id="cat-occupation",
            number="02",
            title="Occupation / Sector",
            options=[
                "Agriculture & Farming",
                "Daily Wage / Informal Labour",
                "Manufacturing & Factory Worker",
                "Small Business / Self-Employed",
                "Private Sector Employee",
                "Government / PSU Employee",
                "Healthcare Worker",
                "Student",
                "Homemaker",
                "Retired / Senior Citizen",
            ],
        ),
        CohortCategory(
            id="cat-region",
            number="03",
            title="Region / State",
            options=[
                "North India (Delhi, UP, Haryana, Punjab, Himachal, J&K)",
                "South India (TN, Karnataka, Kerala, AP, Telangana)",
                "East India (WB, Bihar, Jharkhand, Odisha, NE States)",
                "West India (Maharashtra, Gujarat, Rajasthan, Goa)",
                "Central India (MP, Chhattisgarh)",
                "North-East (Assam, Meghalaya, Manipur, Tripura, etc.)",
            ],
        ),
        CohortCategory(
            id="cat-family",
            number="04",
            title="Family Size",
            options=[
                "Single / No dependants",
                "Nuclear family (2–4 members)",
                "Medium family (5–6 members)",
                "Large / Joint family (7+ members)",
            ],
        ),
        CohortCategory(
            id="cat-age",
            number="05",
            title="Age Group",
            options=[
                "18–25 (Youth)",
                "26–35 (Young Adult)",
                "36–50 (Middle-Aged)",
                "51–60 (Pre-Retirement)",
                "60+ (Senior Citizen)",
            ],
        ),
        CohortCategory(
            id="cat-education",
            number="06",
            title="Education Level",
            options=[
                "No formal schooling",
                "Primary (up to Class 8)",
                "Secondary (Class 9–12)",
                "Graduate (BA / BSc / BCom / etc.)",
                "Post-Graduate / Professional Degree",
            ],
        ),
        CohortCategory(
            id="cat-location",
            number="07",
            title="Urban / Rural",
            options=[
                "Metro city (population > 10 lakh)",
                "Tier-2 / Tier-3 city",
                "Semi-urban / Town",
                "Rural / Village",
            ],
        ),
        CohortCategory(
            id="cat-gender",
            number="08",
            title="Gender",
            options=[
                "Male",
                "Female",
                "Non-binary / Third gender",
            ],
        ),
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
