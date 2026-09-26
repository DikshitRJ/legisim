"""S3 / MinIO Object Storage Service.

Provides an asynchronous client wrapper around aioboto3 for managing
simulation artifacts, precomputed data cubes, and binary exports in MinIO/S3.
"""

from __future__ import annotations

import json
import uuid
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

import aioboto3
from botocore.exceptions import BotoCoreError, ClientError, EndpointConnectionError
from fastapi import HTTPException, Request, status

from app.config import settings
from app.core.exceptions import NotFoundError
from app.core.logging import get_logger

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

logger = get_logger(__name__)


class S3Service:
    """Asynchronous S3 and MinIO service wrapper for LegiSim artifact storage."""

    def __init__(
        self,
        session: aioboto3.Session | None = None,
        bucket_name: str | None = None,
    ) -> None:
        """Initialize the S3 service.

        Args:
            session: Optional pre-configured aioboto3 Session (e.g. from app.state.s3_session).
                     If omitted, a new aioboto3 Session is created.
            bucket_name: Target bucket name. Defaults to settings.S3_BUCKET_NAME.
        """
        self.session: aioboto3.Session = session if session is not None else aioboto3.Session()
        self.bucket_name: str = bucket_name or settings.S3_BUCKET_NAME
        self.access_key: str = settings.S3_ACCESS_KEY
        self.secret_key: str = settings.S3_SECRET_KEY

    @property
    def endpoint_url(self) -> str:
        """Resolve full S3 endpoint URL including protocol scheme."""
        raw = settings.S3_ENDPOINT.strip()
        if raw.startswith("http://") or raw.startswith("https://"):
            return raw
        scheme = "https" if settings.S3_USE_SSL else "http"
        return f"{scheme}://{raw}"

    @asynccontextmanager
    async def client(self) -> AsyncGenerator[Any, None]:
        """Context manager providing an active aioboto3 S3 client.

        Yields:
            S3 client instance.
        """
        async with self.session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        ) as s3_client:
            yield s3_client

    async def upload_json(self, key: str, data: Any) -> str:
        """Upload JSON-serializable data to S3 bucket.

        Args:
            key: Target object key in the S3 bucket.
            data: Dictionary, list, or JSON-serializable structure.

        Returns:
            str: The uploaded object key.

        Raises:
            HTTPException: 503 if S3 endpoint is unreachable, 500 on other storage errors.
        """
        try:
            payload = json.dumps(data, default=str, ensure_ascii=False).encode("utf-8")
            async with self.client() as s3:
                await s3.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=payload,
                    ContentType="application/json",
                )
            logger.info(
                "Uploaded JSON object to s3://%s/%s (%d bytes)",
                self.bucket_name,
                key,
                len(payload),
            )
            return key
        except EndpointConnectionError as exc:
            logger.error(
                "S3 endpoint connection error connecting to %s for upload of '%s': %s",
                self.endpoint_url,
                key,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Storage service unavailable at {self.endpoint_url}",
            ) from exc
        except (ClientError, BotoCoreError) as exc:
            logger.error(
                "Failed to upload JSON to s3://%s/%s: %s",
                self.bucket_name,
                key,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload object '{key}' to storage",
            ) from exc
        except Exception as exc:
            logger.exception("Unexpected error uploading JSON to s3://%s/%s", self.bucket_name, key)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error uploading object '{key}'",
            ) from exc

    async def download_json(self, key: str) -> Any:
        """Download and parse a JSON object from S3.

        Args:
            key: Object key in the S3 bucket.

        Returns:
            Any: Parsed JSON data (dict or list).

        Raises:
            NotFoundError: If the key does not exist in the bucket (404).
            HTTPException: 503 if S3 is unreachable, 502 if JSON is invalid, 500 otherwise.
        """
        try:
            async with self.client() as s3:
                response = await s3.get_object(Bucket=self.bucket_name, Key=key)
                body = await response["Body"].read()
            return json.loads(body.decode("utf-8"))
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code", "")
            if error_code in ("NoSuchKey", "404"):
                logger.warning("Object '%s' not found in S3 bucket '%s'", key, self.bucket_name)
                raise NotFoundError(f"Object '{key}' not found in storage") from exc
            logger.error(
                "ClientError downloading '%s' from s3://%s: %s",
                key,
                self.bucket_name,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Storage error reading '{key}'",
            ) from exc
        except EndpointConnectionError as exc:
            logger.error(
                "S3 endpoint connection error connecting to %s for download of '%s': %s",
                self.endpoint_url,
                key,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Storage service unavailable at {self.endpoint_url}",
            ) from exc
        except json.JSONDecodeError as exc:
            logger.error("Corrupted JSON in s3://%s/%s: %s", self.bucket_name, key, exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Stored object '{key}' contains invalid JSON",
            ) from exc
        except BotoCoreError as exc:
            logger.error(
                "BotoCoreError downloading '%s' from s3://%s: %s",
                key,
                self.bucket_name,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to download object '{key}' from storage",
            ) from exc

    async def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate a presigned URL for downloading an object.

        Args:
            key: Object key in the S3 bucket.
            expires_in: Expiration time in seconds (default: 3600).

        Returns:
            str: Presigned download URL string.

        Raises:
            HTTPException: 503 if S3 is unreachable, 500 on generation failure.
        """
        try:
            async with self.client() as s3:
                url: str = await s3.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.bucket_name, "Key": key},
                    ExpiresIn=expires_in,
                )
            logger.debug(
                "Generated presigned URL for s3://%s/%s (expires in %ds)",
                self.bucket_name,
                key,
                expires_in,
            )
            return url
        except EndpointConnectionError as exc:
            logger.error(
                "S3 connection error generating presigned URL for '%s': %s",
                key,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Storage service unavailable for URL generation",
            ) from exc
        except (ClientError, BotoCoreError) as exc:
            logger.error(
                "Failed to generate presigned URL for s3://%s/%s: %s",
                self.bucket_name,
                key,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate download URL for '{key}'",
            ) from exc

    async def upload_cube(self, run_id: str | uuid.UUID, cube_data: dict[str, Any]) -> str:
        """Upload a precomputed multi-dimensional data cube for a specific simulation run.

        Args:
            run_id: Unique simulation run identifier.
            cube_data: Multi-dimensional data cube dictionary.

        Returns:
            str: S3 key of the stored data cube (runs/{run_id}/cube.json).
        """
        key = f"runs/{str(run_id)}/cube.json"
        return await self.upload_json(key, cube_data)

    async def download_cube(self, run_id: str | uuid.UUID) -> dict[str, Any]:
        """Download the precomputed data cube for a specific simulation run.

        Args:
            run_id: Unique simulation run identifier.

        Returns:
            dict[str, Any]: Parsed data cube dictionary.
        """
        key = f"runs/{str(run_id)}/cube.json"
        result = await self.download_json(key)
        if isinstance(result, dict):
            return result
        return {"data": result}

    async def upload_bytes(
        self,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        """Upload raw bytes to S3 bucket.

        Args:
            key: Target object key in the S3 bucket.
            data: Binary payload bytes.
            content_type: MIME content type string.

        Returns:
            str: The uploaded object key.

        Raises:
            HTTPException: 503 if unreachable, 500 on upload error.
        """
        try:
            async with self.client() as s3:
                await s3.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=data,
                    ContentType=content_type,
                )
            logger.info(
                "Uploaded binary object to s3://%s/%s (%d bytes, type=%s)",
                self.bucket_name,
                key,
                len(data),
                content_type,
            )
            return key
        except EndpointConnectionError as exc:
            logger.error(
                "S3 connection error uploading binary to s3://%s/%s: %s",
                self.bucket_name,
                key,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Storage service unavailable at {self.endpoint_url}",
            ) from exc
        except (ClientError, BotoCoreError) as exc:
            logger.error(
                "Failed to upload binary object to s3://%s/%s: %s",
                self.bucket_name,
                key,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload binary object '{key}'",
            ) from exc

    async def download_bytes(self, key: str) -> bytes:
        """Download raw bytes of an object from S3.

        Args:
            key: Object key in the S3 bucket.

        Returns:
            bytes: Binary content of the object.

        Raises:
            NotFoundError: If the key does not exist.
            HTTPException: 503 if unreachable, 500 on download failure.
        """
        try:
            async with self.client() as s3:
                response = await s3.get_object(Bucket=self.bucket_name, Key=key)
                content: bytes = await response["Body"].read()
            return content
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code", "")
            if error_code in ("NoSuchKey", "404"):
                raise NotFoundError(f"Object '{key}' not found in storage") from exc
            logger.error(
                "ClientError downloading bytes from s3://%s/%s: %s",
                self.bucket_name,
                key,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Storage error reading binary object '{key}'",
            ) from exc
        except EndpointConnectionError as exc:
            logger.error(
                "S3 connection error downloading bytes from s3://%s/%s: %s",
                self.bucket_name,
                key,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Storage service unavailable at {self.endpoint_url}",
            ) from exc
        except BotoCoreError as exc:
            logger.error(
                "BotoCoreError downloading bytes from s3://%s/%s: %s",
                self.bucket_name,
                key,
                exc,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to download binary object '{key}'",
            ) from exc

    async def delete_object(self, key: str) -> bool:
        """Delete an object from the S3 bucket.

        Args:
            key: Object key to delete.

        Returns:
            bool: True if deletion request succeeded.

        Raises:
            HTTPException: 503 if unreachable, 500 on failure.
        """
        try:
            async with self.client() as s3:
                await s3.delete_object(Bucket=self.bucket_name, Key=key)
            logger.info("Deleted object from s3://%s/%s", self.bucket_name, key)
            return True
        except EndpointConnectionError as exc:
            logger.error("S3 connection error deleting s3://%s/%s: %s", self.bucket_name, key, exc)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Storage service unavailable at {self.endpoint_url}",
            ) from exc
        except (ClientError, BotoCoreError) as exc:
            logger.error("Failed to delete object s3://%s/%s: %s", self.bucket_name, key, exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete object '{key}'",
            ) from exc

    async def object_exists(self, key: str) -> bool:
        """Check whether an object exists in the S3 bucket.

        Args:
            key: Object key to check.

        Returns:
            bool: True if object exists, False otherwise.
        """
        try:
            async with self.client() as s3:
                await s3.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code", "")
            if error_code in ("NoSuchKey", "404"):
                return False
            logger.warning("Error checking existence of s3://%s/%s: %s", self.bucket_name, key, exc)
            return False
        except Exception:
            return False

    async def ensure_bucket_exists(self) -> None:
        """Ensure the target bucket exists, creating it if it does not.

        Raises:
            HTTPException: If bucket check or creation fails.
        """
        try:
            async with self.client() as s3:
                try:
                    await s3.head_bucket(Bucket=self.bucket_name)
                except ClientError as exc:
                    error_code = exc.response.get("Error", {}).get("Code", "")
                    if error_code in ("NoSuchBucket", "404"):
                        logger.info("Bucket '%s' does not exist. Creating...", self.bucket_name)
                        await s3.create_bucket(Bucket=self.bucket_name)
                        logger.info("Bucket '%s' created successfully.", self.bucket_name)
                    else:
                        raise
        except EndpointConnectionError as exc:
            logger.error("S3 connection error verifying bucket '%s': %s", self.bucket_name, exc)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Storage service unavailable at {self.endpoint_url}",
            ) from exc
        except (ClientError, BotoCoreError) as exc:
            logger.error("Failed to ensure bucket '%s' exists: %s", self.bucket_name, exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to verify or create bucket '{self.bucket_name}'",
            ) from exc


def get_s3_service(request: Request | None = None) -> S3Service:
    """FastAPI dependency to retrieve an S3Service instance.

    If invoked within an active HTTP request context, uses the application-level
    aioboto3.Session stored on `request.app.state.s3_session` if present.

    Args:
        request: Optional FastAPI Request instance.

    Returns:
        S3Service: Initialized S3Service instance.
    """
    session = None
    if request is not None and hasattr(request, "app"):
        session = getattr(request.app.state, "s3_session", None)
    return S3Service(session=session)
