from __future__ import annotations

from uuid import UUID

from app.schemas.common import CamelModel


class LoginRequest(CamelModel):
    officer_id: str
    password: str


class OfficerProfile(CamelModel):
    id: UUID
    name: str
    role: str


class LoginResponse(CamelModel):
    token: str
    user: OfficerProfile
