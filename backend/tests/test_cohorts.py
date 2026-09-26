from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def test_client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://testserver")

@pytest.mark.asyncio
async def test_get_categories():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with patch("app.api.routes.cohorts.cohort_service.get_cohort_categories", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = [{"id": "c1", "number": "1", "title": "Category 1", "options": ["opt1"]}]
            resp = await client.get("/api/cohort-categories")
            assert resp.status_code == 200
            data = resp.json()
            assert data[0]["id"] == "c1"

@pytest.mark.asyncio
async def test_list_personas():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with patch("app.api.routes.cohorts.cohort_service.list_personas", new_callable=AsyncMock) as mock_list:
            mock_list.return_value = [{
                "id": "p1",
                "demographics": {"age": "30", "income": "50k", "location": "Urban"},
                "assetsAndVulnerabilities": [],
                "economicDependency": []
            }]
            resp = await client.get("/api/cohorts/personas")
            assert resp.status_code == 200
            data = resp.json()
            assert data[0]["id"] == "p1"
            assert data[0]["demographics"]["age"] == "30"

@pytest.mark.asyncio
async def test_run_jev_selection():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with patch("app.api.routes.cohorts.cohort_service.run_jev_selection", new_callable=AsyncMock) as mock_jev:
            mock_jev.return_value = {
                "policyId": "pol1",
                "threshold": 0.65,
                "totalEvaluated": 1,
                "totalSelected": 1,
                "results": [{"id": "p1", "score": 0.9, "relevant": True}],
                "executionTimeMs": 100
            }
            payload = {
                "policyId": "pol1",
                "targetingProfile": {
                    "policyId": "pol1",
                    "summary": "Sum",
                    "directImpactCriteria": "Direct",
                    "indirectImpactCriteria": "Indirect",
                    "geographicFocus": "Geo"
                },
                "threshold": 0.65
            }
            resp = await client.post("/api/cohorts/jev/select", json=payload)
            assert resp.status_code == 200
            data = resp.json()
            assert data["results"][0]["id"] == "p1"

@pytest.mark.asyncio
async def test_submit_reactions():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with patch("app.api.routes.cohorts.cohort_service.submit_reactions", new_callable=AsyncMock) as mock_submit:
            payload = [
                {
                    "cohortId": "c1",
                    "simulationStep": 1,
                    "stanceSupport": 0.8,
                    "stanceNeutral": 0.1,
                    "stanceOppose": 0.1,
                    "behaviourChanges": [],
                    "reasoning": "Reason",
                    "analogueIds": [],
                    "confidence": 0.9
                }
            ]
            resp = await client.post("/api/cohorts/reactions", json=payload)
            assert resp.status_code == 201
            data = resp.json()
            assert data["success"] is True
