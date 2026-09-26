from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def mock_officer():
    from app.models.officer import Officer
    return Officer(
        id=uuid.uuid4(),
        email="test@example.com",
        name="Test Officer",
        role="admin",
        password_hash="hash"
    )

@pytest.mark.asyncio
async def test_create_run(mock_officer):
    transport = ASGITransport(app=app)
    from app.api.deps import get_current_user
    app.dependency_overrides[get_current_user] = lambda: mock_officer
    try:
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            with patch("app.api.routes.runs.run_service.create_run", new_callable=AsyncMock) as mock_create:
                run_id = uuid.uuid4()
                class MockRun:
                    id = run_id
                    status = "loading"
                mock_create.return_value = MockRun()

                payload = {
                    "policyText": "A new tax policy.",
                    "cohorts": {"demographics": ["p1", "p2"]}
                }
                resp = await client.post("/api/runs/", json=payload)
                assert resp.status_code == 200
                data = resp.json()
                assert data["runId"] == str(run_id)
                assert data["status"] == "loading"
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_run_status(mock_officer):
    transport = ASGITransport(app=app)
    from app.api.deps import get_current_user
    app.dependency_overrides[get_current_user] = lambda: mock_officer
    try:
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            with patch("app.api.routes.runs.run_service.get_run_status", new_callable=AsyncMock) as mock_status:
                mock_status.return_value = {
                    "stage": "research",
                    "progress": 50.0
                }
                run_id = uuid.uuid4()
                resp = await client.get(f"/api/runs/{run_id}/status")
                assert resp.status_code == 200
                data = resp.json()
                assert data["stage"] == "research"
                assert data["progress"] == 50.0
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_run_summary(mock_officer):
    transport = ASGITransport(app=app)
    from app.api.deps import get_current_user
    app.dependency_overrides[get_current_user] = lambda: mock_officer
    try:
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            with patch("app.api.routes.runs.run_service.get_run_summary", new_callable=AsyncMock) as mock_summary:
                mock_summary.return_value = {
                    "sections": [
                        {"title": "Overview", "content": "Test", "confidence": "High", "kind": "judged"}
                    ],
                    "metrics": [
                        {"label": "Impact", "value": "+5%", "range": "4-6%", "direction": "positive", "kind": "modelled"}
                    ]
                }
                run_id = uuid.uuid4()
                resp = await client.get(f"/api/runs/{run_id}/summary")
                assert resp.status_code == 200
                data = resp.json()
                assert data["sections"][0]["title"] == "Overview"
                assert data["metrics"][0]["value"] == "+5%"
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_resume_run(mock_officer):
    transport = ASGITransport(app=app)
    from app.api.deps import get_current_user
    app.dependency_overrides[get_current_user] = lambda: mock_officer
    try:
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            with patch("app.api.routes.runs.run_service.resume_run", new_callable=AsyncMock) as mock_resume:
                run_id = uuid.uuid4()
                payload = {
                    "approved": True,
                    "feedback": "Looks good"
                }
                resp = await client.post(f"/api/runs/{run_id}/resume", json=payload)
                assert resp.status_code == 200
                assert resp.json()["status"] == "resumed"
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_chat_with_run(mock_officer):
    transport = ASGITransport(app=app)
    from app.api.deps import get_current_user
    app.dependency_overrides[get_current_user] = lambda: mock_officer
    try:
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            with patch("app.api.routes.runs.run_service.chat_with_run_service", new_callable=AsyncMock) as mock_chat:
                mock_chat.return_value = "Here is an answer."
                run_id = uuid.uuid4()
                payload = {
                    "message": "What is the impact?"
                }
                resp = await client.post(f"/api/runs/{run_id}/chat", json=payload)
                assert resp.status_code == 200
                assert resp.json()["reply"] == "Here is an answer."
    finally:
        app.dependency_overrides.clear()
