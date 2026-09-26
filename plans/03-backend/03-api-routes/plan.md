# API Routes Plan

## Overview
RESTful architecture built with FastAPI. Routes are grouped logically.

**Subagents Required**:
- `api-designer` (Contract specification)
- `backend-implementer` (Implementation)

## Routes

### 1. Notebooks (`/api/notebooks`)
- `GET /` - List user's notebooks.
- `POST /` - Create a notebook.
- `GET /{id}` - Get notebook details.
- `PUT /{id}` - Update notebook.
- `DELETE /{id}` - Archive notebook.

### 2. Runs & Simulations (`/api/runs`)
- `POST /` - Trigger a new simulation (returns a Run ID, starts background task).
- `GET /{id}` - Get run status and results.
- `GET /{id}/stream` - SSE endpoint for live updates (see Streaming plan).
- `GET /{id}/dashboard` - Get dashboard metrics data cube.
- `GET /{id}/map` - Get spatial map data cube.

### 3. Analytics (`/api/analytics`)
- `GET /ripple/{run_id}` - Get nodes and edges.
- `GET /timeline/{run_id}` - Time-series projections.

## Request & Response Schemas

```python
# app/schemas/notebook.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class NotebookBase(BaseModel):
    title: str
    description: Optional[str] = None

class NotebookCreate(NotebookBase):
    pass

class NotebookResponse(NotebookBase):
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
```

## Router Example

```python
# app/api/routes/notebooks.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.schemas.notebook import NotebookResponse, NotebookCreate
from app.services import notebook_service

router = APIRouter(prefix="/notebooks", tags=["notebooks"])

@router.get("/", response_model=list[NotebookResponse])
async def list_notebooks(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return await notebook_service.get_user_notebooks(db, user_id=user["sub"])
```
