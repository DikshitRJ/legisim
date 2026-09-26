from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.cohort import (
    CohortCategory,
    CohortReactionCreate,
    HydratedPrompt,
    JEVSelectionResult,
    PersonaSchema,
    PolicyInput,
    TargetingProfile,
)
from app.schemas.common import CamelModel, SuccessResponse
from app.services import cohort_service

router = APIRouter()
categories_router = APIRouter()


@categories_router.get(
    "",
    response_model=list[CohortCategory],
    summary="Get cohort categories",
    operation_id="getCohortCategories"
)
async def get_categories() -> list[CohortCategory]:
    """Retrieve all available cohort categories for the simulation wizard."""
    return await cohort_service.get_cohort_categories()


@router.get(
    "/personas",
    response_model=list[PersonaSchema],
    summary="List baseline personas",
    operation_id="listPersonas"
)
async def list_personas(db: AsyncSession = Depends(get_db)) -> list[PersonaSchema]:
    """Retrieve all baseline personas."""
    return await cohort_service.list_personas(db)


@router.post(
    "/jev/targeting-profile",
    response_model=TargetingProfile,
    summary="Generate targeting profile",
    operation_id="generateTargetingProfile"
)
async def generate_targeting_profile(policy_input: PolicyInput) -> TargetingProfile:
    """Generate a targeting profile based on the policy input."""
    return await cohort_service.generate_targeting_profile(policy_input)


class JevSelectRequest(CamelModel):
    policy_id: str
    targeting_profile: TargetingProfile
    threshold: float = 0.65


@router.post(
    "/jev/select",
    response_model=JEVSelectionResult,
    summary="Run JEV Selection",
    operation_id="runJevSelection"
)
async def run_jev_selection(request: JevSelectRequest) -> JEVSelectionResult:
    """Run JEV selection to find relevant personas."""
    return await cohort_service.run_jev_selection(
        policy_id=request.policy_id,
        targeting_profile=request.targeting_profile,
        threshold=request.threshold
    )


class HydratePromptsRequest(CamelModel):
    persona_ids: list[str]
    local_context: str
    memory_summary: str


@router.post(
    "/prompts/hydrate",
    response_model=list[HydratedPrompt],
    summary="Hydrate Prompts",
    operation_id="hydratePrompts"
)
async def hydrate_prompts(request: HydratePromptsRequest) -> list[HydratedPrompt]:
    """Hydrate prompts for the specified personas."""
    return await cohort_service.hydrate_prompts(
        persona_ids=request.persona_ids,
        local_context=request.local_context,
        memory_summary=request.memory_summary
    )


@router.post(
    "/reactions",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Cohort Reactions",
    operation_id="submitCohortReactions"
)
async def submit_reactions(
    reactions: list[CohortReactionCreate],
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse:
    """Submit reactions from cohorts."""
    await cohort_service.submit_reactions(db, reactions)
    return SuccessResponse(success=True)
