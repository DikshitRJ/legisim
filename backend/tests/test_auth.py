from __future__ import annotations

import uuid
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.models.officer import Officer


@pytest.fixture
def mock_officer():
    return Officer(
        id=uuid.uuid4(),
        email="test@example.com",
        name="Test Officer",
        role="admin",
        password_hash="hash"
    )

@pytest.mark.asyncio
async def test_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with patch("app.api.routes.auth.authenticate_officer") as mock_auth:
            officer = Officer(
                id=uuid.uuid4(),
                email="test@example.com",
                name="Test Officer",
                role="admin",
                password_hash="hash"
            )
            mock_auth.return_value = (officer, "fake-token")
            resp = await client.post("/api/auth/login", json={"officerId": "test@example.com", "password": "password"})
            assert resp.status_code == 200
            data = resp.json()
            assert data["token"] == "fake-token"
            assert data["user"]["name"] == "Test Officer"

@pytest.mark.asyncio
async def test_logout(mock_officer):
    transport = ASGITransport(app=app)
    from app.api.deps import get_current_user, get_token

    app.dependency_overrides[get_current_user] = lambda: mock_officer
    app.dependency_overrides[get_token] = lambda: "fake-token"

    try:
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            with patch("app.api.routes.auth.logout_officer"):
                resp = await client.post("/api/auth/logout")
                assert resp.status_code == 200
                data = resp.json()
                assert data["success"] is True
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_me(mock_officer):
    transport = ASGITransport(app=app)
    from app.api.deps import get_current_user
    app.dependency_overrides[get_current_user] = lambda: mock_officer
    try:
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            resp = await client.get("/api/auth/me")
            assert resp.status_code == 200
            data = resp.json()
            assert data["name"] == "Test Officer"
    finally:
        app.dependency_overrides.clear()
