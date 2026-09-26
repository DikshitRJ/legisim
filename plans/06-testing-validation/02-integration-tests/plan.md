# Integration and Automated Testing Plan

This document outlines the traditional automated testing strategies for the LegiSim platform to ensure reliability, regression prevention, and contract adherence between services.

## 1. Subagent Assignment
- `test-writer`: Write unit and integration tests across Python and TypeScript codebases.
- `browser-qa`: Implement and maintain Playwright E2E tests.

## 2. Backend API & Logic Tests (Python)

### Tools: `pytest`, `pytest-asyncio`, `httpx`

**Unit Testing Strategy**:
- Focus on CRUD operations for policies, users, and simulations.
- Mock database connections using Pytest fixtures and `testcontainers-python` for ephemeral PostgreSQL databases.

**API Integration Tests**:
- Spin up the FastAPI app using `TestClient`.
- Test request validation (Pydantic models).
- Test JWT authentication and Keycloak integration (using mocked JWKS).

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_simulation(auth_headers, test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/simulations/",
            json={"policy_title": "Universal Basic Income", "description": "1000 per month"},
            headers=auth_headers
        )
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
```

### LangGraph Pipeline Mocks
To test the orchestration without incurring LLM costs and latency:
- Mock the `ChatOpenAI` or `ChatAnthropic` classes.
- Ensure the graph transitions correctly between nodes (e.g., from `initial_research` to `draft_report`).

## 3. Database Migration Tests

- Ensure Alembic migrations can run `upgrade head` and `downgrade base` cleanly.
- Verify `pgvector` index creation on mock data.

## 4. Frontend Component Tests (TypeScript)

### Tools: `Jest`, `React Testing Library (RTL)`

**Component Strategy**:
- Test complex UI states (loading, error, success) for components like the Simulation Canvas and Markdown renderer.
- Mock API calls using `msw` (Mock Service Worker) to return deterministic responses.

```typescript
import { render, screen } from '@testing-library/react';
import { SimulationCanvas } from '@/components/SimulationCanvas';

test('renders pending state correctly', () => {
  render(<SimulationCanvas status="pending" />);
  expect(screen.getByText(/Initializing simulation engine/i)).toBeInDocument();
});
```

## 5. SSE Streaming Tests

Server-Sent Events (SSE) are critical for real-time feedback.
- **Backend**: Use `httpx` to consume the `/api/v1/simulations/{id}/stream` endpoint and assert the sequence of `data: ` chunks matches the expected event model.
- **Frontend**: Mock the `EventSource` API in Jest to ensure the UI updates iteratively as messages arrive.

## 6. End-to-End Tests (E2E)

### Tools: `Playwright`

- Define user journeys: Login -> Create Policy -> Run Simulation -> View Report.
- Run tests across Chromium, Firefox, and WebKit.
- Handle authentication state using Playwright's `storageState` to bypass login screens for tests that don't explicitly test the auth flow.

```typescript
import { test, expect } from '@playwright/test';

test('user can create a simulation', async ({ page }) => {
  await page.goto('/dashboard');
  await page.click('text=New Simulation');
  await page.fill('input[name="title"]', 'Test Policy');
  await page.click('button[type="submit"]');
  
  await expect(page.locator('.simulation-status')).toHaveText('Running...');
});
```

## 7. Test Data Fixtures and Factories

- Use `factory_boy` (Python) to generate realistic simulation models, users, and policy inputs.
- Keep a `seeds.sql` file for standard testing contexts.
