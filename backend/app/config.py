"""Application Configuration Settings.

Loads environment variables using Pydantic Settings with support for
.env files and system environment variables.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    # Core
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "change-me-in-production"
    DOMAIN: str = "localhost"

    # Database
    DATABASE_URL: str = (
        "postgresql+asyncpg://legisim:legisim_db_pass@localhost:5432/legisim"
    )

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # MinIO/S3
    S3_ENDPOINT: str = "localhost:9000"
    S3_ACCESS_KEY: str = "admin"
    S3_SECRET_KEY: str = "minio_admin_pass"
    S3_BUCKET_NAME: str = "legisim-data"
    S3_USE_SSL: bool = False

    # Auth/JWT
    JWT_SECRET_KEY: str = "jwt-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440  # 24 hours

    # AI Services
    ZAI_API_KEY: str = ""
    SEARXNG_URL: str = "http://localhost:8080"
    JEV_SERVICE_URL: str = "http://localhost:8001/predict"

    # Observability
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = ""
    GLITCHTIP_DSN: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings: Settings = Settings()
