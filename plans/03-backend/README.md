# Backend Implementation Plan: LegiSim

This directory contains the implementation plans for the LegiSim backend, organized by domain.

## Architecture Overview

LegiSim is built on a modern, asynchronous Python stack:
- **Framework:** FastAPI
- **Language:** Python 3.12+ (Pydantic V2)
- **Database:** PostgreSQL 16 + pgvector (via SQLAlchemy 2.0 async + Alembic)
- **Cache & Pub/Sub:** Redis
- **File Storage:** MinIO (S3-compatible)
- **Authentication:** Keycloak (OIDC) / Auth.js
- **Orchestration/LLM:** LangGraph + Langchain
- **Observability:** Langfuse (LLM Tracing), GlitchTip (Error tracking)
- **Deployment:** Docker Compose + Traefik

## Directory Structure

```text
backend/
├── app/
│   ├── main.py              # FastAPI application setup
│   ├── config.py            # Pydantic BaseSettings
│   ├── models/              # SQLAlchemy 2.0 ORM models
│   ├── schemas/             # Pydantic V2 models for I/O
│   ├── api/
│   │   ├── routes/          # FastAPI APIRouters
│   │   └── deps.py          # FastAPI dependencies (get_db, get_current_user)
│   ├── services/            # Core business logic
│   ├── engine/              # LangGraph pipelines and LLM calls
│   ├── math/                # Economic model templates & solvers
│   ├── data/                # Data ETL and parsing utilities
│   └── core/                # JWT validation, error handling, logging config
├── migrations/              # Alembic environment and versions
├── tests/                   # Pytest suite
│   ├── conftest.py
│   ├── api/
│   └── engine/
├── docker/                  # Dockerfiles and entrypoints
├── requirements.txt         # or pyproject.toml (Poetry/uv)
└── README.md
```

## Dependency List

Key Python packages:
- `fastapi`, `uvicorn[standard]`
- `sqlalchemy[asyncio]`, `alembic`, `asyncpg`
- `pydantic`, `pydantic-settings`
- `langgraph`, `langchain`, `langchain-openai`
- `redis`, `boto3` or `aioboto3`
- `python-jose`, `passlib`
- `langfuse`

## Sub-Plans

1. [Database Schema & ORM](01-database/plan.md)
2. [Authentication & Authorization](02-auth/plan.md)
3. [API Routes](03-api-routes/plan.md)
4. [Data Cube (Precomputation)](04-data-cube/plan.md)
5. [Streaming & SSE](05-streaming/plan.md)
6. [Infrastructure & Deployment](06-infrastructure/plan.md)
