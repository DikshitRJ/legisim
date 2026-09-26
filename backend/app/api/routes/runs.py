from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.schemas.run import (
    ChatRequest,
    ChatResponse,
    CohortGroup,
    DataCubeResponse,
    ReportResponse,
    ResumeRequest,
    RippleGraph,
    RunDashboard,
    RunEventResponse,
    RunStartRequest,
    RunStartResponse,
    RunStatus,
    RunSummary,
    StateData,
    TimelineDataPoint,
)
from app.services import run_service
from app.services.export_service import export_run as export_run_service

router = APIRouter()

@router.post("/", response_model=RunStartResponse)
async def create_run(
    request: RunStartRequest,
    notebook_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    run = await run_service.create_run(db, notebook_id, request.policy_text, request.cohorts)
    return RunStartResponse(run_id=str(run.id), status=run.status)

@router.get("/{run_id}/status", response_model=RunStatus)
async def get_run_status(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await run_service.get_run_status(db, run_id)

@router.get("/{run_id}/events", response_model=list[RunEventResponse])
async def get_run_events(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await run_service.get_run_events(db, run_id)

@router.post("/{run_id}/resume")
async def resume_run(
    run_id: uuid.UUID,
    request: ResumeRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    await run_service.resume_run(db, run_id, request.approved, request.feedback)
    return {"status": "resumed"}

@router.get("/{run_id}/summary", response_model=RunSummary)
async def get_run_summary(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await run_service.get_run_summary(db, run_id)

@router.get("/{run_id}/dashboard", response_model=RunDashboard)
async def get_run_dashboard(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await run_service.get_run_dashboard(db, run_id)

@router.get("/{run_id}/groups", response_model=list[CohortGroup])
async def get_run_groups(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await run_service.get_run_groups(db, run_id)

@router.get("/{run_id}/map", response_model=list[StateData])
async def get_run_map(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await run_service.get_run_map(db, run_id)

@router.get("/{run_id}/ripple", response_model=RippleGraph)
async def get_run_ripple(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await run_service.get_run_ripple(db, run_id)

@router.get("/{run_id}/timeline", response_model=list[TimelineDataPoint])
async def get_run_timeline(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await run_service.get_run_timeline(db, run_id)

@router.get("/{run_id}/cube", response_model=DataCubeResponse)
async def get_run_cube(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await run_service.get_run_cube(db, run_id)

@router.get("/{run_id}/report", response_model=ReportResponse)
async def get_run_report(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await run_service.get_run_report(db, run_id)

@router.post("/{run_id}/chat", response_model=ChatResponse)
async def chat_with_run(
    run_id: uuid.UUID,
    request: ChatRequest,
    current_user = Depends(get_current_user)
):
    reply = await run_service.chat_with_run_service(run_id, request.message)
    return ChatResponse(reply=reply)

@router.get("/{run_id}/export/{format}")
async def export_run(
    run_id: uuid.UUID,
    format: str,
):
    return await export_run_service(run_id, format)
