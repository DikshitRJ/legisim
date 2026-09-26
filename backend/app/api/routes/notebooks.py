"""Notebooks API Routes.

Implements REST endpoints for managing simulation notebooks and their statuses,
adhering to the OpenAPI 3.0 specification.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.exceptions import NotFoundError
from app.models.officer import Officer
from app.schemas.common import SuccessResponse
from app.schemas.notebook import (
    NotebookCreate,
    NotebookResponse,
    NotebookStatus,
    NotebookUpdate,
)
from app.services import notebook_service

router = APIRouter()


def _parse_id(val: str | uuid.UUID) -> uuid.UUID:
    """Convert path parameter string or UUID to uuid.UUID instance.

    Args:
        val: Raw path identifier.

    Returns:
        uuid.UUID: Parsed UUID.

    Raises:
        NotFoundError: If format is invalid.
    """
    if isinstance(val, uuid.UUID):
        return val
    try:
        return uuid.UUID(val)
    except (ValueError, AttributeError, TypeError):
        raise NotFoundError(f"Notebook with id '{val}' not found") from None


@router.get(
    "",
    response_model=list[NotebookResponse],
    status_code=status.HTTP_200_OK,
    summary="List notebooks",
    description="Retrieves a list of notebooks, optionally filtered by status.",
)
@router.get(
    "/",
    response_model=list[NotebookResponse],
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def list_notebooks(
    status: NotebookStatus | None = Query(
        default=None,
        description="Filter by status",
    ),
    db: AsyncSession = Depends(get_db),
    current_user: Officer = Depends(get_current_user),  # noqa: ARG001
) -> list[NotebookResponse]:
    """Retrieve a list of notebooks, optionally filtered by status."""
    status_val = status.value if isinstance(status, NotebookStatus) else status
    notebooks = await notebook_service.list_notebooks(db=db, status_filter=status_val)
    return [NotebookResponse.model_validate(nb) for nb in notebooks]


@router.post(
    "",
    response_model=NotebookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new notebook",
    description="Creates a new notebook.",
)
@router.post(
    "/",
    response_model=NotebookResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
async def create_notebook(
    data: NotebookCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Officer = Depends(get_current_user),  # noqa: ARG001
) -> NotebookResponse:
    """Create a new notebook."""
    notebook = await notebook_service.create_notebook(db=db, data=data)
    return NotebookResponse.model_validate(notebook)


@router.get(
    "/{id}",
    response_model=NotebookResponse,
    status_code=status.HTTP_200_OK,
    summary="Get single notebook",
    description="Retrieves the details of a specific notebook by its ID.",
)
async def get_notebook(
    id: str = Path(..., description="Notebook ID"),
    db: AsyncSession = Depends(get_db),
    current_user: Officer = Depends(get_current_user),  # noqa: ARG001
) -> NotebookResponse:
    """Retrieve the details of a specific notebook by its ID."""
    notebook_id = _parse_id(id)
    notebook = await notebook_service.get_notebook(db=db, notebook_id=notebook_id)
    return NotebookResponse.model_validate(notebook)


@router.put(
    "/{id}",
    response_model=NotebookResponse,
    status_code=status.HTTP_200_OK,
    summary="Update notebook details",
    description="Updates the details of an existing notebook.",
)
async def update_notebook(
    data: NotebookUpdate,
    id: str = Path(..., description="Notebook ID"),
    db: AsyncSession = Depends(get_db),
    current_user: Officer = Depends(get_current_user),  # noqa: ARG001
) -> NotebookResponse:
    """Update the details of an existing notebook."""
    notebook_id = _parse_id(id)
    notebook = await notebook_service.update_notebook(
        db=db, notebook_id=notebook_id, data=data
    )
    return NotebookResponse.model_validate(notebook)


@router.delete(
    "/{id}",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Archive a notebook",
    description="Archives a notebook, changing its status to archived.",
)
async def archive_notebook(
    id: str = Path(..., description="Notebook ID"),
    db: AsyncSession = Depends(get_db),
    current_user: Officer = Depends(get_current_user),  # noqa: ARG001
) -> SuccessResponse:
    """Archive a notebook by ID."""
    notebook_id = _parse_id(id)
    await notebook_service.archive_notebook(db=db, notebook_id=notebook_id)
    return SuccessResponse(success=True)
