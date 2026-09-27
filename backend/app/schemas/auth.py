from __future__ import annotations

from uuid import UUID

from app.schemas.common import CamelModel


class LoginRequest(CamelModel):
    officer_id: str
    password: str
    # Optional fields used only during first-time sign-up registration
    name: str | None = None
    designation: str | None = None


class OfficerProfile(CamelModel):
    id: UUID
    name: str
    role: str
    designation: str | None = None


class LoginResponse(CamelModel):
    token: str
    user: OfficerProfile
