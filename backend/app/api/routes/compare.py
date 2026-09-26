from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.schemas.run import CompareRequest, CompareResponse
from app.services import run_service

router = APIRouter()

@router.post("/", response_model=CompareResponse)
async def compare_runs(
    request: CompareRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await run_service.compare_runs(db, request.run_ids)
