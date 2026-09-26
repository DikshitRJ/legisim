"""Custom HTTP Exceptions and Exception Handlers.

Provides standard HTTP exception classes with preconfigured status codes
and handlers for uniform JSON error responses across the API.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from fastapi import FastAPI

logger = logging.getLogger(__name__)


class NotFoundError(HTTPException):
    """Exception raised when a requested resource is not found (404)."""

    def __init__(
        self,
        detail: str = "Resource not found",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            headers=headers,
        )


class ForbiddenError(HTTPException):
    """Exception raised when action is forbidden by permissions (403)."""

    def __init__(
        self,
        detail: str = "Access forbidden",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers=headers,
        )


class BadRequestError(HTTPException):
    """Exception raised when client sends an invalid request (400)."""

    def __init__(
        self,
        detail: str = "Bad request",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=headers,
        )


class ConflictError(HTTPException):
    """Exception raised when resource conflict occurs (409)."""

    def __init__(
        self,
        detail: str = "Resource conflict",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            headers=headers,
        )


class UnauthorizedError(HTTPException):
    """Exception raised when client authentication fails (401)."""

    def __init__(
        self,
        detail: str = "Authentication required",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers,
        )


async def http_exception_handler(
    request: Request,  # noqa: ARG001
    exc: HTTPException,
) -> JSONResponse:
    """Handle standard and custom HTTPExceptions, producing a unified JSON error payload.

    Args:
        request: FastAPI Request instance.
        exc: Raised HTTPException.

    Returns:
        JSONResponse: Uniform error response with status code and message.
    """
    detail_content: Any = exc.detail
    message = detail_content if isinstance(detail_content, str) else str(detail_content)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": message},
        headers=exc.headers,
    )


async def validation_exception_handler(
    request: Request,  # noqa: ARG001
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle Pydantic RequestValidationErrors with field details.

    Args:
        request: FastAPI Request instance.
        exc: Raised RequestValidationError.

    Returns:
        JSONResponse: 422 error response with validation failure details.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Validation error",
            "errors": exc.errors(),
        },
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Catch-all unhandled exception handler logging the incident.

    Args:
        request: FastAPI Request instance.
        exc: Unhandled exception.

    Returns:
        JSONResponse: 500 error response.
    """
    logger.exception(
        "Unhandled exception processing request path: %s method: %s error: %s",
        request.url.path,
        request.method,
        exc,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers on the FastAPI application instance.

    Args:
        app: FastAPI application instance.
    """
    app.add_exception_handler(HTTPException, cast(Any, http_exception_handler))
    app.add_exception_handler(RequestValidationError, cast(Any, validation_exception_handler))
    app.add_exception_handler(Exception, generic_exception_handler)
