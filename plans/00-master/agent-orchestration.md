# LegiSim Agent Orchestration Workflow

## 1. Orchestration Model

The following diagram illustrates the 5-wave parallel execution strategy for the LegiSim project. Each wave represents a coordinated set of tasks that must be completed and validated before the subsequent wave begins.

```mermaid
flowchart TD
    %% Waves
    subgraph Wave 1: Foundation (Day 1-2)
        A1[Agent 1A: api-designer<br>API Schema Design]
        A2[Agent 1B: data-pipeline-engineer + opencode<br>Data Collection Scripts]
        A3[Agent 1C: ci-cd-engineer<br>Infrastructure Scaffold]
        A4[Agent 1D: backend-implementer<br>JEV Model Service]
    end

    subgraph Wave 2: Core Structure (Days 2-4)
        B1[Agent 2A: database-architect + opencode<br>Database Architecture]
        B2[Agent 2B: copilot + backend-implementer<br>LangGraph Core Nodes]
        B3[Agent 2C: ui-builder + opencode<br>Frontend API Integration]
    end

    subgraph Wave 3: Engines (Days 4-8)
        C1[Agent 3A: copilot<br>Cohort, Ripple, Math Models]
        C2[Agent 3B: backend-implementer<br>Backend API Routes]
        C3[Agent 3C: data-pipeline-engineer<br>Census Data Ingestion]
    end

    subgraph Wave 4: Integration (Days 8-12)
        D1[Agent 4A: copilot<br>Full Pipeline E2E]
        D2[Agent 4B: ui-builder<br>Visualization]
        D3[Agent 4C: test-writer<br>Integration Tests]
    end

    subgraph Wave 5: Polish & Validation (Days 12-16)
        E1[Agent 5A: copilot + data-analyst<br>Backtesting]
        E2[Agent 5B: browser-qa<br>E2E Browser Tests]
        E3[Agent 5C: auth-specialist<br>Auth Integration]
        E4[Agent 5D: security-reviewer + performance-profiler<br>Security & Performance]
    end

    %% Dependencies
    Wave 1 -->|APIs, Data, Infra Ready & Validated| Wave 2
    Wave 2 -->|DB Schema & Core Graph Ready| Wave 3
    Wave 3 -->|Endpoints & Simulation Engines Ready| Wave 4
    Wave 4 -->|E2E Integration & UI Complete| Wave 5
```

## 2. Wave 1 — Foundation (Day 1-2)
*Goal: Establish API contract, data foundations, infra scaffold, and the core JEV ML service. This wave sets the bedrock for all subsequent tasks.*

### Agent 1A: API Schema Design
- **Agent Name**: `api-designer`
- **Plan File Path**: `/plans/01-wave1/1a-api-schema.md`
- **Subagents**: None
- **Input**: LegiSim architectural requirements, frontend UI wireframes, and backend LangGraph constraints.
- **Output**: Comprehensive OpenAPI 3.0 YAML specification.
- **Duration**: Day 1 (4-6 hours)
- **Depends on**: None
- **Exact Steps**:
  1. Initialize `/plans/api/openapi.yaml`.
  2. Define rigorous schemas for `Persona`, `SimulationRun`, `SimulationResult`, and `Policy`.
  3. Define all HTTP endpoints required for the frontend UI (e.g., `GET /simulations`, `POST /simulate`).
  4. Explicitly define internal API routes for the JEV service (`POST /predict` taking persona metadata and policy text).
  5. Include WebSocket definitions for LangGraph state streaming to the frontend.
  6. Validate the spec using OpenAPI linters to ensure 100% compliance.
  7. Tag the final artifact with `#MEMPALACE_OPENAPI_SPEC`.

### Agent 1B: Data Collection Scripts
- **Agent Name**: `data-pipeline-engineer`
- **Plan File Path**: `/plans/01-wave1/1b-data-collection.md`
- **Subagents**: `opencode`
- **Input**: Links to Indian Census data, RBI datasets, and MoSPI economic indicators.
- **Output**: Python ETL scripts and baseline CSV files.
- **Duration**: Day 1-2 (10-12 hours)
- **Depends on**: None
- **Exact Steps**:
  1. Create `/scripts/download_census.py` to fetch state-wise demographics.
  2. Create `/scripts/download_rbi.py` to fetch economic and income distribution statistics.
  3. Write `/scripts/generate_personas.py` using Pandas and Numpy to synthesize 2,000 baseline Indian citizen personas. Ensure traits cover age, income, education, occupation, region, and political leaning.
  4. Ensure output is saved to `/data/baseline_personas.csv`.
  5. Validate dataset headers match the JEV model input requirements.

### Agent 1C: Infrastructure Scaffold
- **Agent Name**: `ci-cd-engineer`
- **Plan File Path**: `/plans/01-wave1/1c-infra-scaffold.md`
- **Subagents**: None
- **Input**: Project service requirements.
- **Output**: Docker Compose and CI/CD YAML configurations.
- **Duration**: Day 2 (6-8 hours)
- **Depends on**: None
- **Exact Steps**:
  1. Create the root `/docker-compose.yml`.
  2. Define ALL 12 services with precise versioning:
     - `api` (FastAPI backend)
     - `worker` (Celery/LangGraph worker)
     - `frontend` (Next.js)
     - `db` (PostgreSQL with pgvector)
     - `redis` (Cache & Celery broker)
     - `minio` (S3 compatible object storage for artifacts)
     - `jev` (Self-hosted model service)
     - `searxng` (Search)
     - `traefik` (Reverse proxy)
     - `keycloak` (Auth)
     - `langfuse` (LLM Observability)
     - `glitchtip` (Error tracking)
  3. Write `/api/Dockerfile`, `/frontend/Dockerfile`, `/worker/Dockerfile`, and `/jev-service/Dockerfile`.
  4. Configure persistent volumes and internal Docker networks.
  5. Create `/.github/workflows/main.yml` for CI pipelines.
  6. Verify the entire stack stands up using `docker-compose up -d`.

### Agent 1D: JEV Model Service
- **Agent Name**: `backend-implementer`
- **Plan File Path**: `/plans/01-wave1/1d-jev-service.md`
- **Subagents**: None
- **Input**: Model specs for Jurisprudential Evaluation Validator (JEV), HuggingFace BERT link.
- **Output**: Isolated Python FastAPI service serving the BERT model.
- **Duration**: Day 2 (8 hours)
- **Depends on**: Agent 1C (Dockerfile constraints)
- **Exact Steps**:
  1. Initialize `/jev-service/requirements.txt` locking versions for `fastapi`, `uvicorn`, `transformers`, `torch`, `pydantic`.
  2. Write `/jev-service/download_model.py` to pull the JEV BERT model weights from HuggingFace to a local `/models` directory on startup.
  3. Create `/jev-service/main.py` containing a FastAPI app.
  4. Implement the `POST /predict` endpoint which takes `policy_text` and `persona_attributes` and returns a float score between 0.0 and 1.0 (impact/support score).
  5. Add health check endpoint `GET /health` to signify model readiness.
  6. Tag the artifact with `#MEMPALACE_JEV_API`.

## 3. Wave 2 — Core Structure (Days 2-4)
*Goal: Build the state management, database schema, and initial UI hooks.*

### Agent 2A: Database Architecture
- **Agent Name**: `database-architect`
- **Plan File Path**: `/plans/02-wave2/2a-db-architecture.md`
- **Subagents**: `opencode`
- **Input**: OpenAPI definitions, system data requirements.
- **Output**: SQLAlchemy ORM models and Alembic revision scripts.
- **Duration**: Day 3 (8-10 hours)
- **Depends on**: Agent 1A
- **Exact Steps**:
  1. Initialize Alembic environment in `/backend/alembic/`.
  2. Define SQLAlchemy declarative base in `/backend/database.py`.
  3. Create `/backend/models.py` including tables for:
     - `personas` (must use pgvector for similarity searches if applicable, though primarily tabular traits)
     - `policies`
     - `simulation_runs`
     - `simulation_results`
  4. Define foreign key relationships and indices optimized for querying millions of persona responses.
  5. Generate initial migration `/backend/alembic/versions/*_init.py`.
  6. Test migration against the running Wave 1 PostgreSQL container.
  7. Tag with `#MEMPALACE_DB_SCHEMA`.

### Agent 2B: LangGraph Core Nodes
- **Agent Name**: `copilot`
- **Plan File Path**: `/plans/02-wave2/2b-langgraph-core.md`
- **Subagents**: `backend-implementer`
- **Input**: JEV Service API, Database Schema.
- **Output**: LangGraph graph definition and core execution nodes.
- **Duration**: Days 3-4 (12 hours)
- **Depends on**: Agent 1D, Agent 2A
- **Exact Steps**:
  1. Define the global state in `/backend/graph/state.py` using TypedDicts reflecting the simulation phases.
  2. Implement `/backend/graph/nodes/intake.py` to parse initial user policy inputs.
  3. Implement `/backend/graph/nodes/research.py` utilizing SearXNG to fetch context on the policy domain.
  4. Implement `/backend/graph/nodes/review.py` for LLM (GLM API) initial policy evaluation.
  5. Implement `/backend/graph/nodes/jev_select.py` which interfaces with the database to query target personas.
  6. Implement `/backend/graph/nodes/prompt_hydrate.py` to prepare batches of data for the JEV service.
  7. Write unit tests ensuring state dictates flow correctly.

### Agent 2C: Frontend API Integration
- **Agent Name**: `ui-builder`
- **Plan File Path**: `/plans/02-wave2/2c-frontend-api.md`
- **Subagents**: `opencode`
- **Input**: `openapi.yaml`.
- **Output**: Next.js API utilities and React hooks.
- **Duration**: Day 4 (6 hours)
- **Depends on**: Agent 1A
- **Exact Steps**:
  1. Use openapi-typescript or similar to generate types in `/frontend/src/types/api.d.ts`.
  2. Create Axios/Fetch wrapper in `/frontend/src/lib/apiClient.ts`.
  3. Develop robust TanStack Query hooks in `/frontend/src/hooks/useSimulation.ts` and `/frontend/src/hooks/usePersonas.ts`.
  4. Implement error boundaries and retry logic for API failures.

## 4. Wave 3 — Engines (Days 4-8)
*Goal: The heavy simulation logic, API implementation, and real-world data ingestion.*

### Agent 3A: Cohort + Ripple + Math
- **Agent Name**: `copilot`
- **Plan File Path**: `/plans/03-wave3/3a-simulation-engines.md`
- **Subagents**: None
- **Input**: LangGraph state, JEV API constraints.
- **Output**: Advanced simulation nodes.
- **Duration**: Days 4-6 (16 hours)
- **Depends on**: Agent 2B
- **Exact Steps**:
  1. Create `/backend/graph/nodes/cohort_reactions.py`. Implement async HTTP calls targeting the JEV service's `/predict` endpoint, batching persona requests efficiently.
  2. Create `/backend/graph/nodes/ripple.py`. Implement secondary effect algorithms (e.g., if policy impacts agriculture negatively, ripple to rural retail consumption).
  3. Create `/backend/graph/nodes/math_models.py`. Inject economic formulas to estimate fiscal impact based on cohort behavior.
  4. Ensure node failures fallback gracefully and append error logs to the graph state.

### Agent 3B: Backend API Routes
- **Agent Name**: `backend-implementer`
- **Plan File Path**: `/plans/03-wave3/3b-backend-routes.md`
- **Subagents**: None
- **Input**: Database models, OpenAPI specs, LangGraph triggers.
- **Output**: Fully functional FastAPI endpoints.
- **Duration**: Days 5-7 (14 hours)
- **Depends on**: Agent 2A, Agent 1A
- **Exact Steps**:
  1. Setup dependency injection for DB sessions and authenticated users in `/backend/api/dependencies.py`.
  2. Implement CRUD routes in `/backend/api/routes.py` (e.g., Persona management).
  3. Implement the simulation trigger route which submits a job to Redis/Celery and returns a `job_id`.
  4. Implement WebSocket endpoint `/backend/api/ws.py` to stream LangGraph execution progress directly to the frontend.

### Agent 3C: Census Data Ingestion
- **Agent Name**: `data-pipeline-engineer`
- **Plan File Path**: `/plans/03-wave3/3c-census-ingestion.md`
- **Subagents**: None
- **Input**: Wave 1 raw datasets, Wave 2 DB schema.
- **Output**: Loaded database.
- **Duration**: Days 6-8 (10 hours)
- **Depends on**: Agent 1B, Agent 2A
- **Exact Steps**:
  1. Expand on baseline scripts in `/scripts/census_etl.py`.
  2. Connect to the PostgreSQL database using SQLAlchemy.
  3. Transform and map the CSV files into DB inserts using bulk copy operations.
  4. Verify that data distributions (e.g., gender ratio, state populations) match real-world Indian demographics.

## 5. Wave 4 — Integration (Days 8-12)
*Goal: Tie the simulation pipeline to final reporting and visual frontend mapping.*

### Agent 4A: Full Pipeline E2E
- **Agent Name**: `copilot`
- **Plan File Path**: `/plans/04-wave4/4a-full-pipeline.md`
- **Subagents**: None
- **Input**: All completed graph nodes.
- **Output**: Fully compiled LangGraph application.
- **Duration**: Days 8-10 (12 hours)
- **Depends on**: Agent 3A
- **Exact Steps**:
  1. Develop `/backend/graph/nodes/viz_planner.py` to structure data for the frontend (aggregating cohort data for charts).
  2. Develop `/backend/graph/nodes/write_report.py` to call the GLM API and generate a narrative markdown report of the simulation.
  3. Develop `/backend/graph/nodes/critic.py` as an evaluation loop to ensure report accuracy against JEV raw numbers.
  4. Compile the full workflow in `/backend/graph/workflow.py` and run a comprehensive test script.
  5. Store resulting artifacts to MinIO.

### Agent 4B: Visualization
- **Agent Name**: `ui-builder`
- **Plan File Path**: `/plans/04-wave4/4b-visualization.md`
- **Subagents**: None
- **Input**: UI mockups, Frontend hooks.
- **Output**: Data-rich interactive UI.
- **Duration**: Days 9-11 (18 hours)
- **Depends on**: Agent 2C
- **Exact Steps**:
  1. Build MapLibre visualization in `/frontend/src/components/Map.tsx`. Render Indian states and color-code based on cohort impact scores.
  2. Build complex demographic charts in `/frontend/src/components/Chart.tsx` utilizing ECharts (e.g., Income vs Impact scatter plots).
  3. Build `/frontend/src/components/Flow.tsx` using React Flow to visualize the LangGraph pipeline execution in real-time based on WebSocket messages.

### Agent 4C: Integration Tests
- **Agent Name**: `test-writer`
- **Plan File Path**: `/plans/04-wave4/4c-integration-tests.md`
- **Subagents**: None
- **Input**: Complete backend source code.
- **Output**: Extensive Pytest suite.
- **Duration**: Days 10-12 (12 hours)
- **Depends on**: Agent 3B, Agent 4A
- **Exact Steps**:
  1. Configure pytest environment in `/backend/tests/conftest.py` with test databases.
  2. Write API tests in `/backend/tests/test_api.py`.
  3. Write LangGraph tests in `/backend/tests/test_graph.py`.
  4. Create fixtures that mock out HTTP calls to SearXNG, Keycloak, and JEV.

## 6. Wave 5 — Polish & Validation (Days 12-16)
*Goal: Ensure the system is robust, secure, and well-documented.*

### Agent 5A: Backtesting
- **Agent Name**: `copilot`
- **Plan File Path**: `/plans/05-wave5/5a-backtesting.md`
- **Subagents**: `data-analyst`
- **Input**: E2E pipeline, historical policy texts.
- **Output**: Refined prompts and parameter tuning.
- **Duration**: Days 12-14 (12 hours)
- **Depends on**: Agent 4A
- **Exact Steps**:
  1. Input historical texts (e.g., 2016 Demonetization, 2017 GST).
  2. Collect the simulated output from the JEV service and LangGraph nodes.
  3. Compare results to verified historical impact metrics (provided by data-analyst).
  4. Adjust prompt templates and ripple multipliers in the graph to tune accuracy.

### Agent 5B: E2E Browser Tests
- **Agent Name**: `browser-qa`
- **Plan File Path**: `/plans/05-wave5/5b-e2e-tests.md`
- **Subagents**: None
- **Input**: Running frontend application.
- **Output**: Playwright test specs.
- **Duration**: Days 13-15 (10 hours)
- **Depends on**: Agent 4B
- **Exact Steps**:
  1. Initialize Playwright in the `/frontend` directory.
  2. Write `/frontend/tests/login.spec.ts` testing Keycloak flows.
  3. Write `/frontend/tests/simulation_flow.spec.ts` executing the golden path: policy input, wait for LangGraph completion via WS, and validating chart rendering.

### Agent 5C: Auth
- **Agent Name**: `auth-specialist`
- **Plan File Path**: `/plans/05-wave5/5c-auth.md`
- **Subagents**: None
- **Input**: Keycloak config.
- **Output**: Hardened API and Frontend routes.
- **Duration**: Days 13-14 (8 hours)
- **Depends on**: Agent 3B, Agent 4B
- **Exact Steps**:
  1. Apply Keycloak realm configurations.
  2. Wrap FastAPI endpoints requiring specific user roles (e.g., `admin`, `analyst`).
  3. Configure Next.js middleware to redirect unauthenticated users and validate JWT tokens server-side.

### Agent 5D: Security & Performance
- **Agent Name**: `security-reviewer`
- **Plan File Path**: `/plans/05-wave5/5d-security-perf.md`
- **Subagents**: `performance-profiler`
- **Input**: Final codebase, Docker images.
- **Output**: Audit documentation, Code optimizations.
- **Duration**: Days 15-16 (14 hours)
- **Depends on**: All previous tasks
- **Exact Steps**:
  1. Run dependency scans (e.g., safety, npm audit).
  2. Profile the LangGraph execution times, looking for I/O bottlenecks in PostgreSQL or Redis.
  3. Add necessary database indexes to `backend/alembic` migrations.
  4. Write final `/docs/security_audit.md`.

## 7. Handoff Protocol

### MemPalace Tags
To prevent context window bloat and ensure precise communication, agents must use MemPalace tags.
When an agent finishes a major structural artifact, they MUST tag their final output message:
- `#MEMPALACE_OPENAPI_SPEC` - Generated by 1A.
- `#MEMPALACE_DB_SCHEMA` - Generated by 2A.
- `#MEMPALACE_JEV_API` - Generated by 1D.

Subsequent agents explicitly instruct the planner to retrieve these tags. For example, Agent 3B's prompt will include: "Fetch #MEMPALACE_OPENAPI_SPEC and #MEMPALACE_DB_SCHEMA before implementing FastAPI routes."

### Agent Briefing Template
Every agent invocation MUST follow this format strictly:

```text
[Task Name]
Role: [Agent Role]
Files to Edit: [Comma separated list of absolute paths]
Dependencies: [List of files from previous waves they must read]
Context: [Brief description of how this fits into the LegiSim architecture]
Instructions:
1. [Step 1]
2. [Step 2]
Acceptance Criteria:
- [Criterion 1]
```

### Wave Completion Verification (Docker Health Checks)
Before transitioning to the next wave, the orchestrator (`parent`) must execute:
`docker-compose ps` and `docker-compose logs`.
The orchestrator must verify that all services (especially Postgres and JEV) are marked as `healthy`.
The next wave CANNOT begin until all infrastructure from the previous wave is verified as stable. If a service is crashing, a debugging agent must be dispatched to fix it prior to wave advancement.

## 8. Conflict Resolution

| Scenario | Resolution |
|----------|------------|
| Schema Mismatches | Halt immediately. Ping `parent` for a regression check. Review the original OpenAPI spec. DO NOT arbitrarily change foreign keys without checking `models.py`. |
| Dependency Cycles | Extract shared models/schemas to a neutral `/backend/schemas.py` file. Python imports must strictly flow downwards. |
| Container Failures | Inspect `docker logs [service]`. Attempt one single self-correction code fix. If unresolved after one attempt, escalate to `parent`. |
| Graph State Conflicts | Revert to schema defined in `state.py`. Ensure all nodes return dictionary patches perfectly compliant with the `TypedDict`. |
| Frontend Type Errors | Re-run the OpenAPI code generation script. Ensure backend changes are synced to `api.yaml`. |

## 9. Success Metrics

| Milestone | Verification |
|-----------|--------------|
| E2E Simulation | Pipeline executes in < 45 seconds for a 5-node graph with 2,000 JEV inferences. |
| JEV Performance | Model latency is < 15ms per batched prediction request. |
| Code Quality | Minimum > 80% test coverage on backend APIs and frontend core logic. |
| UI Responsiveness | Maps and Charts render in < 2 seconds post-simulation data fetch from backend. |
| Infra Setup | `docker-compose up` leads to full system readiness (including large JEV model downloads) in < 3 minutes. |
| API Compliance | 100% adherence to OpenAPI schema on all endpoints. |
| JEV Benchmarks | BERT model validation scores align with ground-truth historical impacts within a 5% margin of error during backtesting. |
