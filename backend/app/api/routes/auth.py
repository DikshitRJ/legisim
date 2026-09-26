from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, get_token
from app.models.officer import Officer
from app.schemas.auth import LoginRequest, LoginResponse, OfficerProfile
from app.schemas.common import SuccessResponse
from app.services.auth_service import authenticate_officer, logout_officer

router = APIRouter()


@router.post("/login", response_model=LoginResponse, summary="Authenticate an officer", description="Login to get an authentication token and user profile.")
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    """Authenticate an officer."""
    officer, token = await authenticate_officer(db, request.officer_id, request.password)
    return LoginResponse(
        token=token,
        user=OfficerProfile.model_validate(officer),
    )


@router.post("/logout", response_model=SuccessResponse, summary="Invalidate current session", description="Logs out the authenticated officer.")
async def logout(
    token: str = Depends(get_token),
    db: AsyncSession = Depends(get_db),
    current_user: Officer = Depends(get_current_user),  # Ensures user is authenticated
) -> SuccessResponse:
    """Log out the currently authenticated officer."""
    await logout_officer(db, token)
    return SuccessResponse(success=True)


@router.get("/me", response_model=OfficerProfile, summary="Get current authenticated user info", description="Retrieves the profile of the currently authenticated officer.")
async def get_me(
    current_user: Officer = Depends(get_current_user),
) -> OfficerProfile:
    """Get current authenticated user profile."""
    return OfficerProfile.model_validate(current_user)
