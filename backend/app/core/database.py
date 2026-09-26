"""Async SQLAlchemy Database Engine and Session Management.

Provides the async engine, sessionmaker, FastAPI dependency for database sessions,
and lifecycle helpers for initializing and disposing database connections.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

logger = logging.getLogger(__name__)

# SQLAlchemy async engine configured with connection pooling
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.ENVIRONMENT == "development"),
    future=True,
    pool_pre_ping=True,
)

# Async session factory
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding an async database session.

    Yields:
        AsyncSession: Active SQLAlchemy async session.
    """
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database connection and verify connectivity.

    Executed during application startup lifespan.
    """
    logger.info("Initializing database connection to %s...", settings.DATABASE_URL.split("@")[-1])
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connectivity check passed.")
    except Exception as exc:
        logger.warning(
            "Could not connect to database at startup: %s. Continuing in disconnected state.",
            exc,
        )


async def close_db() -> None:
    """Dispose of the database engine and connection pool.

    Executed during application shutdown lifespan.
    """
    logger.info("Disposing database engine connection pool...")
    await engine.dispose()
    logger.info("Database engine disposed.")
