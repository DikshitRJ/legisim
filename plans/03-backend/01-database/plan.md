# Database Architecture Plan

## Overview
PostgreSQL 16 with `pgvector` extension for storing and querying text embeddings of historical policies and facts.

**Subagents Required**: 
- `database-architect` (Schema design & Migrations)
- `backend-implementer` (SQLAlchemy Models)

## Schema Design

### Tables

1. **`users`**
   - `id` (UUID, PK)
   - `email` (VARCHAR, UNIQUE)
   - `role` (VARCHAR)
   - `created_at` (TIMESTAMPTZ)

2. **`notebooks`**
   - `id` (UUID, PK)
   - `user_id` (UUID, FK -> users)
   - `title` (VARCHAR)
   - `description` (TEXT)
   - `status` (VARCHAR: active, archived)
   - `created_at`, `updated_at` (TIMESTAMPTZ)

3. **`runs` (Simulation instances)**
   - `id` (UUID, PK)
   - `notebook_id` (UUID, FK -> notebooks)
   - `status` (VARCHAR: pending, running, completed, failed)
   - `created_at`, `completed_at` (TIMESTAMPTZ)

4. **`run_inputs`**
   - `id` (UUID, PK)
   - `run_id` (UUID, FK -> runs)
   - `policy_text` (TEXT)
   - `context_variables` (JSONB)

5. **`analogues` (Historical matches for pgvector)**
   - `id` (UUID, PK)
   - `title` (VARCHAR)
   - `content` (TEXT)
   - `embedding` (VECTOR(1536)) -- Assuming OpenAI `text-embedding-3-small`
   - `metadata` (JSONB)

6. **`cohorts` (Demographic groups)**
   - `id` (UUID, PK)
   - `run_id` (UUID, FK -> runs)
   - `name` (VARCHAR)
   - `population` (VARCHAR)
   - `income_change` (FLOAT)
   - `behaviors` (JSONB)

7. **`ripple_nodes` / `ripple_edges`**
   - Stores the graph structure for the Ripple Explorer.

## SQLAlchemy Models (Snippet)

```python
from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, JSON, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
from app.models.base import Base

class Notebook(Base):
    __tablename__ = "notebooks"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[str] = mapped_column(String(50), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    runs = relationship("Run", back_populates="notebook")

class Analogue(Base):
    __tablename__ = "analogues"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))
```

## Migration Strategy
1. Initial migration enables `pgvector`.
2. HNSW index created on `analogues.embedding` for fast similarity search.
```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE INDEX ON analogues USING hnsw (embedding vector_cosine_ops);
```
