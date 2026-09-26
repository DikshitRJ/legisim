"""Export Service for LegiSim simulation results.

Provides export generation stubs for formats such as PDF, CSV, and PPTX.
Returns HTTP 501 Not Implemented until the report generation pipeline is ready.
"""

from __future__ import annotations

import uuid
from typing import Literal

from fastapi import HTTPException, status

ExportFormat = Literal["pdf", "csv", "pptx"]


async def export_run(
    run_id: str | uuid.UUID,  # noqa: ARG001
    format: ExportFormat | str,
) -> bytes:
    """Export simulation results in the specified format.

    Currently a stub — returns HTTP 501 Not Implemented.
    Will be implemented when report generation pipeline is ready.

    Args:
        run_id: Unique identifier of the simulation run.
        format: Target export format ('pdf', 'csv', or 'pptx').

    Returns:
        bytes: Raw binary content of the exported artifact.

    Raises:
        HTTPException: HTTP 400 if format is invalid; HTTP 501 as export is not yet implemented.
    """
    valid_formats = {"pdf", "csv", "pptx"}
    format_str = str(format).lower()
    if format_str not in valid_formats:
        formats_list = ", ".join(sorted(valid_formats))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported export format '{format}'. Supported formats: {formats_list}",
        )

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Export to {format_str} format is not yet implemented. Coming soon.",
    )
