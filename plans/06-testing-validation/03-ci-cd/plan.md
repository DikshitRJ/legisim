# CI/CD Pipeline Plan

This document defines the Continuous Integration and Continuous Deployment strategy for LegiSim using GitHub Actions and Docker.

## 1. Subagent Assignment
- `ci-cd-engineer`: Write GitHub Actions workflows, Dockerfiles, and deployment scripts.
- `test-writer`: Maintain the test environments inside the pipeline.

## 2. GitHub Actions Workflow

The CI/CD pipeline runs on all PRs to `main` and on pushes to `main`. It is divided into two phases to ensure fast feedback.

### Phase 1: Code Quality & Static Analysis
Fails fast if code does not meet formatting or typing standards.

**Backend Tasks**:
- `black --check .` (Formatting)
- `ruff check .` (Linting)
- `mypy .` (Type checking)

**Frontend Tasks**:
- `npm run lint` (ESLint)
- `npm run format:check` (Prettier)
- `npm run type-check` (tsc)

### Phase 2: Integration Tests
Runs only if Phase 1 passes. Uses Docker Compose to spin up necessary services.

- Start PostgreSQL with `pgvector`.
- Start Redis (for Celery/LangGraph states).
- Run Pytest (Backend tests).
- Run Jest (Frontend tests).
- Run Playwright (E2E tests).

```yaml
name: LegiSim CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install backend dependencies
        run: pip install black ruff mypy
      - name: Backend Quality
        run: |
          black --check backend/
          ruff check backend/
          mypy backend/
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Frontend Quality
        run: |
          cd frontend
          npm ci
          npm run lint
          npm run type-check

  test:
    needs: quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Start Services
        run: docker-compose -f docker-compose.test.yml up -d
      - name: Run Backend Tests
        run: docker exec legisim-backend-test pytest
      - name: Run Frontend Tests
        run: cd frontend && npm test
      - name: Run E2E Tests
        run: cd frontend && npx playwright test
```

## 3. Docker Build and Push

On a successful merge to `main`, Docker images are built and pushed to the container registry (e.g., GitHub GHCR or AWS ECR).

- **Images**: `legisim-frontend`, `legisim-backend`.
- Tags are based on the Git commit SHA for traceability (`:sha-123456`) and `:latest`.

## 4. Branch Protection Rules

- **Require Pull Request reviews**: At least 1 approval.
- **Require status checks to pass**: The `LegiSim CI` workflow (both `quality` and `test` jobs) must pass before merging.
- **No direct pushes to main**.

## 5. Deployment Strategy

LegiSim follows a **Staging -> Production** progression.

1. **Staging Environment**: 
   - Automatically deployed from the `main` branch upon a successful CI run.
   - Hosted on a sub-domain (e.g., `staging.legisim.io`).
   - Uses a separate Staging database.
   - Manual QA and exploratory testing happen here.

2. **Production Environment**:
   - Deployed via a manual trigger (GitHub Release or manual workflow dispatch).
   - Follows rolling updates to minimize downtime.
   - Database migrations are applied automatically during the deployment process via an init-container or pre-deployment hook.
