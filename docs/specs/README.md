# Legisim Domain Specifications

This directory contains the highly structured, modular specifications for the Legisim platform. To enable decoupled, parallel development across frontend and backend agents, the system's architecture has been divided into core **domains**.

## Directory Structure

The specs are organized by domain. Each folder represents a distinct functional area of the platform:

* **`auth/`**: Authentication, user sessions, and officer access.
* **`cohorts/`**: Cohort configurations, demographics, JEV model parameters, and persona definitions.
* **`notebooks/`**: Management of simulation notebooks, their metadata, and lifecycle statuses.
* **`ripple/`**: The causal ripple graph engine, including definitions for domains, nodes, and edges.
* **`runs/`**: The core simulation engine, encompassing run inputs, prediction outputs, timeline data, reports, and dashboard chart metrics.

## Inside Each Domain

Within every domain folder, you will find three standardized files. They serve as the strict contract between the database layer, the backend API, and the frontend client.

### 1. `database.md` (PostgreSQL Schema)
* **What it is:** The relational database design for the domain.
* **How to use it:** Backend database architects and implementers should use this to construct SQLAlchemy/SQLModel models, apply constraints, and write Alembic migrations. 
* **Key contents:** Tables, columns, precise data types, foreign key relationships, indexes, and Mermaid Entity-Relationship Diagrams (ERDs).

### 2. `api-docs.md` (Human-Readable API Guide)
* **What it is:** A plain English explanation of the domain's REST endpoints.
* **How to use it:** Developers and AI planners should read this to understand the high-level business logic, the expected request flow, and how the endpoints interact with each other.

### 3. `openapi.yaml` (Strict OpenAPI 3.0 Spec)
* **What it is:** The machine-readable contract defining the API endpoints and JSON schemas.
* **How to use it:** 
  * **Frontend:** Feed this into code generators (e.g., `openapi-typescript-codegen`, Orval) to automatically generate typed HTTP clients and React hooks.
  * **Backend:** Use this to scaffold FastAPI routers, Pydantic request/response models, and ensure strict input validation.

## Workflow

1. **Source of Truth:** These files act as the absolute source of truth. If a data model or endpoint behavior needs to change, update these specifications **before** touching the code.
2. **Parallel Implementation:** A frontend agent can use the `openapi.yaml` to build UI components with mocked data, while a backend agent simultaneously uses `database.md` and `openapi.yaml` to build the actual routes and tables.
