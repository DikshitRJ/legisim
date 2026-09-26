"""Notebook Service Layer.

Provides asynchronous business logic and CRUD operations for simulation notebooks
using SQLAlchemy 2.0 select statements.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.notebook import Notebook
from app.schemas.notebook import NotebookCreate, NotebookUpdate


def _to_uuid(val: uuid.UUID | str) -> uuid.UUID:
    """Safely convert a UUID or string value into a UUID instance.

    Args:
        val: Input UUID object or string representation.

    Returns:
        uuid.UUID: Parsed UUID instance.

    Raises:
        NotFoundError: If val is not a valid UUID string.
    """
    if isinstance(val, uuid.UUID):
        return val
    try:
        return uuid.UUID(val)
    except (ValueError, AttributeError, TypeError):
        raise NotFoundError(f"Notebook with id '{val}' not found") from None


async def list_notebooks(
    db: AsyncSession,
    status_filter: str | None = None,
) -> list[Notebook]:
    """Retrieve notebooks optionally filtered by status.

    Args:
        db: Database async session.
        status_filter: Optional status filter ('active' or 'archived').

    Returns:
        list[Notebook]: List of matching notebook models ordered by modified_at desc.
    """
    stmt = select(Notebook).order_by(Notebook.modified_at.desc())
    if status_filter is not None:
        stmt = stmt.where(Notebook.status == status_filter)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_notebook(
    db: AsyncSession,
    data: NotebookCreate,
) -> Notebook:
    """Create a new notebook with default 'active' status.

    Args:
        db: Database async session.
        data: Notebook creation payload.

    Returns:
        Notebook: Created notebook model.
    """
    now = datetime.now(UTC)
    notebook = Notebook(
        id=uuid.uuid4(),
        title=data.title,
        description=data.description,
        sources=0,
        status="active",
        created_at=now,
        modified_at=now,
    )
    db.add(notebook)
    await db.commit()
    await db.refresh(notebook)
    return notebook


async def get_notebook(
    db: AsyncSession,
    notebook_id: uuid.UUID | str,
) -> Notebook:
    """Retrieve a single notebook by ID.

    Args:
        db: Database async session.
        notebook_id: Unique identifier of the notebook.

    Returns:
        Notebook: Retrieved notebook model.

    Raises:
        NotFoundError: If notebook with given ID does not exist.
    """
    uid = _to_uuid(notebook_id)
    stmt = select(Notebook).where(Notebook.id == uid)
    result = await db.execute(stmt)
    notebook = result.scalar_one_or_none()
    if not notebook:
        raise NotFoundError(f"Notebook with id '{notebook_id}' not found")
    return notebook


async def update_notebook(
    db: AsyncSession,
    notebook_id: uuid.UUID | str,
    data: NotebookUpdate,
) -> Notebook:
    """Update notebook details.

    Args:
        db: Database async session.
        notebook_id: Unique identifier of the notebook to update.
        data: Notebook update payload.

    Returns:
        Notebook: Updated notebook model.

    Raises:
        NotFoundError: If notebook with given ID does not exist.
    """
    notebook = await get_notebook(db, notebook_id)
    if data.title is not None:
        notebook.title = data.title
    if data.description is not None:
        notebook.description = data.description
    notebook.modified_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(notebook)
    return notebook


async def archive_notebook(
    db: AsyncSession,
    notebook_id: uuid.UUID | str,
) -> bool:
    """Archive a notebook by setting its status to 'archived'.

    Args:
        db: Database async session.
        notebook_id: Unique identifier of the notebook to archive.

    Returns:
        bool: True if successfully archived.

    Raises:
        NotFoundError: If notebook with given ID does not exist.
    """
    notebook = await get_notebook(db, notebook_id)
    notebook.status = "archived"
    notebook.modified_at = datetime.now(UTC)
    await db.commit()
    return True
