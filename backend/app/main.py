"""LegiSim FastAPI Application.

Main entry point for the LegiSim backend application, setting up lifespan handlers,
CORS middleware, exception handlers, API routers, and health check endpoints.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.cohorts import categories_router, router as cohorts_router
from app.api.routes.compare import router as compare_router
from app.api.routes.notebooks import router as notebooks_router
from app.api.routes.runs import router as runs_router
from app.config import settings
from app.core.database import close_db, init_db
from app.core.exceptions import register_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.schemas.common import HealthResponse

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager for startup and shutdown events.

    Initializes database pools, Redis connections, and S3 clients on startup,
    and cleanly disposes of them on shutdown.
    """
    # Startup
    setup_logging()
    logger.info("Starting LegiSim Backend [%s]...", settings.ENVIRONMENT)

    # Initialize Database
    await init_db()

    # Initialize Redis client pool
    try:
        import redis.asyncio as aioredis

        app.state.redis = aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
        logger.info("Redis connection pool initialized.")
    except Exception as exc:
        logger.warning("Redis initialization failed: %s. Continuing without Redis cache.", exc)
        app.state.redis = None

    # Initialize S3 / MinIO client session
    try:
        import aioboto3

        app.state.s3_session = aioboto3.Session()
        logger.info("S3/MinIO session initialized for endpoint %s.", settings.S3_ENDPOINT)
    except Exception as exc:
        logger.warning("S3 session initialization failed: %s.", exc)
        app.state.s3_session = None

    logger.info("LegiSim Backend startup complete.")

    yield

    # Shutdown
    logger.info("Shutting down LegiSim Backend...")

    # Close Redis pool
    if getattr(app.state, "redis", None) is not None:
        try:
            await app.state.redis.close()
            logger.info("Redis connection pool closed.")
        except Exception as exc:
            logger.error("Error closing Redis connection: %s", exc)

    # Close Database engine pool
    await close_db()

    logger.info("LegiSim Backend shutdown complete.")


# Instantiate FastAPI application
app: FastAPI = FastAPI(
    title="LegiSim Backend API",
    description="LegiSim Policy Simulation Platform Backend",
    version="0.1.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    openapi_url="/openapi.json" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan,
)

# CORS Middleware Configuration
if settings.ENVIRONMENT == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"^https?://.*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            f"http://{settings.DOMAIN}",
            f"https://{settings.DOMAIN}",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register Custom Exception Handlers
register_exception_handlers(app)

# Root API Router with /api prefix
api_router: APIRouter = APIRouter(prefix="/api")


@api_router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["health"],
    summary="Health Check",
    description="Verifies the operational status of the service.",
)
async def health_check() -> HealthResponse:
    """Return health status of the service."""
    return HealthResponse(
        status="healthy",
        environment=settings.ENVIRONMENT,
        version="0.1.0",
    )


# ==============================================================================
# Domain Routers
# ==============================================================================
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(notebooks_router, prefix="/notebooks", tags=["notebooks"])
api_router.include_router(runs_router, prefix="/runs", tags=["runs"])
api_router.include_router(cohorts_router, prefix="/cohorts", tags=["cohorts"])
api_router.include_router(categories_router, prefix="/cohort-categories", tags=["cohorts"])
api_router.include_router(compare_router, prefix="/compare", tags=["compare"])

# Include the main api router in the application
app.include_router(api_router)
