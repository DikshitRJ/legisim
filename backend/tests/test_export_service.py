"""Unit tests for ExportService.

Tests simulation run export stubs for PDF, CSV, PPTX formats, and validates
HTTP 501 Not Implemented responses and 400 Bad Request on invalid formats.
"""

from __future__ import annotations

import uuid

import pytest
from fastapi import HTTPException

from app.services.export_service import export_run


@pytest.mark.asyncio
async def test_export_run_pdf_stub() -> None:
    """Test exporting run to PDF raises HTTP 501 Not Implemented."""
    run_id = str(uuid.uuid4())
    with pytest.raises(HTTPException) as exc_info:
        await export_run(run_id, "pdf")

    assert exc_info.value.status_code == 501
    assert "pdf" in exc_info.value.detail.lower()
    assert "not yet implemented" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_export_run_csv_stub() -> None:
    """Test exporting run to CSV raises HTTP 501 Not Implemented."""
    run_id = str(uuid.uuid4())
    with pytest.raises(HTTPException) as exc_info:
        await export_run(run_id, "csv")

    assert exc_info.value.status_code == 501
    assert "csv" in exc_info.value.detail.lower()
    assert "not yet implemented" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_export_run_pptx_stub() -> None:
    """Test exporting run to PPTX raises HTTP 501 Not Implemented."""
    run_id = str(uuid.uuid4())
    with pytest.raises(HTTPException) as exc_info:
        await export_run(run_id, "pptx")

    assert exc_info.value.status_code == 501
    assert "pptx" in exc_info.value.detail.lower()
    assert "not yet implemented" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_export_run_uuid_instance() -> None:
    """Test export_run accepts a UUID instance directly."""
    run_id = uuid.uuid4()
    with pytest.raises(HTTPException) as exc_info:
        await export_run(run_id, "pdf")

    assert exc_info.value.status_code == 501


@pytest.mark.asyncio
async def test_export_run_invalid_format() -> None:
    """Test export_run with invalid format raises HTTP 400 Bad Request."""
    run_id = str(uuid.uuid4())
    with pytest.raises(HTTPException) as exc_info:
        await export_run(run_id, "docx")  # type: ignore[arg-type]

    assert exc_info.value.status_code == 400
    assert "unsupported export format" in exc_info.value.detail.lower()
    assert "docx" in exc_info.value.detail.lower()
