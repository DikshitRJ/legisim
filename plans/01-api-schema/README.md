# API Schema Plan

## Overview

This directory contains the unified API schema definition for the LegiSim project. The API acts as the single source of truth and contract between the frontend (React/Next.js) and the backend (FastAPI/Python). 

## Why a Unified Schema?

1. **Clear Contracts**: Establishes exact data structures expected by the frontend and provided by the backend.
2. **Type Safety**: Enables automatic generation of TypeScript interfaces and Python Pydantic models.
3. **Parallel Development**: Allows frontend and backend agents to work independently based on a shared understanding of the API.
4. **Validation**: Ensures that data entering and leaving the system adheres to strict business rules.

## How to Use

- **Frontend Agents**: Use the specifications in `openapi-spec.md` to build API client services and define TypeScript interfaces.
- **Backend Agents**: Use the definitions in `data-models.md` to construct FastAPI routes, Pydantic validation schemas, and database serialization logic.
- **Architects/Planners**: Reference these documents when extending functionality or adding new simulation features.
