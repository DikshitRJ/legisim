"""Tests for Notebooks domain (Schemas, Services, and API Routes)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError

from app.api.deps import get_current_user, get_db
from app.core.exceptions import NotFoundError
from app.main import app
from app.models.notebook import Notebook
from app.models.officer import Officer
from app.schemas.notebook import (
    NotebookCreate,
    NotebookResponse,
    NotebookStatus,
    NotebookUpdate,
)
from app.services import notebook_service

# ==============================================================================
# Schema Tests
# ==============================================================================


def test_notebook_status_enum() -> None:
    """Test NotebookStatus enum values."""
    assert NotebookStatus.ACTIVE.value == "active"
    assert NotebookStatus.ARCHIVED.value == "archived"
    assert str(NotebookStatus.ACTIVE) == "active"


def test_notebook_create_valid() -> None:
    """Test valid NotebookCreate schema instantiation."""
    data = NotebookCreate(title="Test Policy", description="A test simulation notebook.")
    assert data.title == "Test Policy"
    assert data.description == "A test simulation notebook."


def test_notebook_create_missing_fields() -> None:
    """Test NotebookCreate fails validation when required fields are missing."""
    with pytest.raises(ValidationError):
        NotebookCreate.model_validate({"title": "Only Title"})

    with pytest.raises(ValidationError):
        NotebookCreate.model_validate({"description": "Only Description"})


def test_notebook_update_optional() -> None:
    """Test NotebookUpdate supports optional partial fields."""
    update_empty = NotebookUpdate()
    assert update_empty.title is None
    assert update_empty.description is None

    update_title = NotebookUpdate(title="Updated Title")
    assert update_title.title == "Updated Title"
    assert update_title.description is None

    update_desc = NotebookUpdate(description="Updated Description")
    assert update_desc.title is None
    assert update_desc.description == "Updated Description"


def test_notebook_response_serialization() -> None:
    """Test NotebookResponse camelCase aliasing, UUID serialization, and defaults."""
    fixed_id = uuid.uuid4()
    now = datetime.now(UTC)

    class FakeORMNotebook:
        id = fixed_id
        title = "Simulation A"
        description = "Testing economic impact"
        sources = 3
        modified_at = now
        status = "active"

    schema = NotebookResponse.model_validate(FakeORMNotebook())
    assert schema.id == str(fixed_id)
    assert schema.title == "Simulation A"
    assert schema.description == "Testing economic impact"
    assert schema.sources == 3
    assert schema.status == NotebookStatus.ACTIVE
    assert schema.modified_at == now

    dumped = schema.model_dump(by_alias=True)
    assert "modifiedAt" in dumped
    assert "modified_at" not in dumped
    assert dumped["id"] == str(fixed_id)
    assert dumped["sources"] == 3
    assert dumped["status"] == NotebookStatus.ACTIVE


def test_notebook_response_null_handling() -> None:
    """Test NotebookResponse handles None for nullable DB columns cleanly."""
    fixed_id = uuid.uuid4()
    now = datetime.now(UTC)

    class FakeORMNotebook:
        id = fixed_id
        title = "Simulation Null Test"
        description = None
        sources = None
        modified_at = now
        status = "archived"

    schema = NotebookResponse.model_validate(FakeORMNotebook())
    assert schema.sources == 0
    assert schema.description == ""
    assert schema.status == NotebookStatus.ARCHIVED


# ==============================================================================
# Service Layer Tests
# ==============================================================================


@pytest.mark.asyncio
async def test_service_list_notebooks() -> None:
    """Test notebook_service.list_notebooks with and without status filter."""
    db = AsyncMock()
    mock_result = MagicMock()
    mock_notebooks = [
        Notebook(
            id=uuid.uuid4(),
            title="Notebook 1",
            description="Desc 1",
            sources=1,
            status="active",
            created_at=datetime.now(UTC),
            modified_at=datetime.now(UTC),
        )
    ]
    mock_result.scalars.return_value.all.return_value = mock_notebooks
    db.execute.return_value = mock_result

    # Without filter
    result = await notebook_service.list_notebooks(db)
    assert len(result) == 1
    assert result[0].title == "Notebook 1"
    assert db.execute.called

    # With filter
    result_filtered = await notebook_service.list_notebooks(db, status_filter="active")
    assert len(result_filtered) == 1


@pytest.mark.asyncio
async def test_service_create_notebook() -> None:
    """Test notebook_service.create_notebook creates model with active status."""
    db = AsyncMock()
    db.add = MagicMock()
    payload = NotebookCreate(title="New Policy", description="Evaluating child tax credit")

    created = await notebook_service.create_notebook(db, payload)
    assert created.title == "New Policy"
    assert created.description == "Evaluating child tax credit"
    assert created.status == "active"
    assert created.sources == 0
    assert isinstance(created.id, uuid.UUID)
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(created)


@pytest.mark.asyncio
async def test_service_get_notebook_found_and_not_found() -> None:
    """Test notebook_service.get_notebook raises NotFoundError when missing."""
    db = AsyncMock()
    target_id = uuid.uuid4()
    mock_nb = Notebook(
        id=target_id,
        title="Found NB",
        description="Desc",
        sources=0,
        status="active",
        created_at=datetime.now(UTC),
        modified_at=datetime.now(UTC),
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_nb
    db.execute.return_value = mock_result

    # Found
    retrieved = await notebook_service.get_notebook(db, target_id)
    assert retrieved.id == target_id

    # Not found
    mock_result.scalar_one_or_none.return_value = None
    with pytest.raises(NotFoundError):
        await notebook_service.get_notebook(db, uuid.uuid4())

    # Invalid UUID string
    with pytest.raises(NotFoundError):
        await notebook_service.get_notebook(db, "invalid-uuid-string")


@pytest.mark.asyncio
async def test_service_update_notebook() -> None:
    """Test notebook_service.update_notebook partial update."""
    db = AsyncMock()
    target_id = uuid.uuid4()
    existing_nb = Notebook(
        id=target_id,
        title="Original Title",
        description="Original Desc",
        sources=1,
        status="active",
        created_at=datetime.now(UTC),
        modified_at=datetime.now(UTC),
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_nb
    db.execute.return_value = mock_result

    update_payload = NotebookUpdate(title="Modified Title")
    updated = await notebook_service.update_notebook(db, target_id, update_payload)
    assert updated.title == "Modified Title"
    assert updated.description == "Original Desc"
    db.commit.assert_called()


@pytest.mark.asyncio
async def test_service_archive_notebook() -> None:
    """Test notebook_service.archive_notebook updates status to archived."""
    db = AsyncMock()
    target_id = uuid.uuid4()
    existing_nb = Notebook(
        id=target_id,
        title="Active NB",
        description="Desc",
        sources=0,
        status="active",
        created_at=datetime.now(UTC),
        modified_at=datetime.now(UTC),
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_nb
    db.execute.return_value = mock_result

    res = await notebook_service.archive_notebook(db, target_id)
    assert res is True
    assert existing_nb.status == "archived"
    db.commit.assert_called()


# ==============================================================================
# API Route Integration Tests
# ==============================================================================


@pytest.fixture
def mock_officer() -> Officer:
    """Fixture providing a mock authenticated Officer."""
    return Officer(
        id=uuid.uuid4(),
        email="analyst@legisim.gov",
        name="Policy Analyst",
        role="analyst",
        password_hash="hash",
    )


@pytest.mark.asyncio
async def test_routes_require_authentication() -> None:
    """Test that all notebook endpoints require authentication (401/403)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Without auth header
        res_list = await client.get("/api/notebooks")
        assert res_list.status_code in [401, 403]

        res_post = await client.post("/api/notebooks", json={"title": "T", "description": "D"})
        assert res_post.status_code in [401, 403]

        res_get = await client.get(f"/api/notebooks/{uuid.uuid4()}")
        assert res_get.status_code in [401, 403]

        res_put = await client.put(f"/api/notebooks/{uuid.uuid4()}", json={"title": "Updated"})
        assert res_put.status_code in [401, 403]

        res_del = await client.delete(f"/api/notebooks/{uuid.uuid4()}")
        assert res_del.status_code in [401, 403]


@pytest.mark.asyncio
async def test_routes_crud_operations(mock_officer: Officer) -> None:
    """Test CRUD operations via the API endpoints with mocked auth and database."""
    nb_id = uuid.uuid4()
    now = datetime.now(UTC)
    mock_nb = Notebook(
        id=nb_id,
        title="Fiscal Reform Simulation",
        description="Assessing consumption tax impact",
        sources=2,
        status="active",
        created_at=now,
        modified_at=now,
    )

    mock_db = AsyncMock()

    app.dependency_overrides[get_current_user] = lambda: mock_officer
    app.dependency_overrides[get_db] = lambda: mock_db

    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            # 1. GET /api/notebooks
            with patch("app.services.notebook_service.list_notebooks", return_value=[mock_nb]):
                resp = await client.get("/api/notebooks")
                assert resp.status_code == 200
                data = resp.json()
                assert len(data) == 1
                assert data[0]["id"] == str(nb_id)
                assert data[0]["title"] == "Fiscal Reform Simulation"
                assert "modifiedAt" in data[0]
                assert data[0]["status"] == "active"
                assert data[0]["sources"] == 2

            # 2. POST /api/notebooks
            with patch("app.services.notebook_service.create_notebook", return_value=mock_nb):
                resp = await client.post(
                    "/api/notebooks",
                    json={
                        "title": "Fiscal Reform Simulation",
                        "description": "Assessing consumption tax impact",
                    },
                )
                assert resp.status_code == 201
                data = resp.json()
                assert data["id"] == str(nb_id)
                assert data["title"] == "Fiscal Reform Simulation"
                assert "modifiedAt" in data

            # 3. GET /api/notebooks/{id}
            with patch("app.services.notebook_service.get_notebook", return_value=mock_nb):
                resp = await client.get(f"/api/notebooks/{nb_id}")
                assert resp.status_code == 200
                data = resp.json()
                assert data["id"] == str(nb_id)

            # 4. GET /api/notebooks/{id} Not Found
            with patch(
                "app.services.notebook_service.get_notebook",
                side_effect=NotFoundError("Notebook not found"),
            ):
                resp = await client.get(f"/api/notebooks/{uuid.uuid4()}")
                assert resp.status_code == 404

            # 5. GET /api/notebooks/{invalid_id}
            resp = await client.get("/api/notebooks/not-a-valid-uuid")
            assert resp.status_code == 404

            # 6. PUT /api/notebooks/{id}
            updated_nb = Notebook(
                id=nb_id,
                title="Updated Simulation Title",
                description="Assessing consumption tax impact",
                sources=2,
                status="active",
                created_at=now,
                modified_at=now,
            )
            with patch("app.services.notebook_service.update_notebook", return_value=updated_nb):
                resp = await client.put(
                    f"/api/notebooks/{nb_id}",
                    json={"title": "Updated Simulation Title"},
                )
                assert resp.status_code == 200
                data = resp.json()
                assert data["title"] == "Updated Simulation Title"

            # 7. DELETE /api/notebooks/{id}
            with patch("app.services.notebook_service.archive_notebook", return_value=True):
                resp = await client.delete(f"/api/notebooks/{nb_id}")
                assert resp.status_code == 200
                data = resp.json()
                assert data["success"] is True

    finally:
        app.dependency_overrides.clear()
