# Implementation Guide

## Subagents

- **`api-designer`**: Review this plan and refine the OpenAPI specifications. Maintain API consistency and versioning.
- **`backend-implementer`**: Set up FastAPI structure and implement routers for each domain (Auth, Notebooks, Runs, etc.) using the Pydantic models.
- **`ui-builder`**: Generate frontend TypeScript clients/hooks utilizing these interfaces to fetch data from the backend.

## Backend File Structure

Suggested FastAPI layout:
```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── notebooks.py
│   │   │   ├── runs.py
│   │   │   └── cohorts.py
│   ├── models/
│   │   ├── schemas.py (Contains Pydantic models)
│   ├── services/
│   │   └── simulation.py
│   └── main.py
```

## Synchronization

1. OpenAPI specification is the source of truth.
2. Backend generates `/openapi.json` from FastAPI.
3. Frontend uses tools like `openapi-typescript-codegen` or RTK Query generation to construct typed API hooks from `/openapi.json`.

## Versioning Strategy

- Global prefix: `/api/v1/...`
- Introduce breaking changes in `/api/v2/...`
- Preserve backwards compatibility on v1 for deployed frontend clients.
