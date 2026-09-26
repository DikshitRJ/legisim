"""Unit tests for S3Service.

Validates initialization, URL resolution, S3 operations (upload/download,
presigned URLs, data cube storage), error handling, and FastAPI dependency integration.
"""

from __future__ import annotations

import json
import uuid
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import aioboto3
import pytest
from botocore.exceptions import BotoCoreError, ClientError, EndpointConnectionError
from fastapi import HTTPException

from app.config import settings
from app.core.exceptions import NotFoundError
from app.services.s3_service import S3Service, get_s3_service


class AsyncContextManagerMock:
    """Mock for async context managers."""

    def __init__(self, return_value: Any) -> None:
        self.return_value = return_value

    async def __aenter__(self) -> Any:
        return self.return_value

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


@pytest.fixture
def mock_s3_client() -> AsyncMock:
    """Create a mock aiobotocore S3 client."""
    client = AsyncMock()
    return client


@pytest.fixture
def mock_session(mock_s3_client: AsyncMock) -> MagicMock:
    """Create a mock aioboto3 Session returning mock_s3_client as context manager."""
    session = MagicMock(spec=aioboto3.Session)
    session.client.return_value = AsyncContextManagerMock(mock_s3_client)
    return session


@pytest.fixture
def s3_service(mock_session: MagicMock) -> S3Service:
    """Create S3Service instance backed by mock_session."""
    return S3Service(session=mock_session)


def test_s3_service_initialization_defaults() -> None:
    """Verify S3Service initializes with default settings when session is omitted."""
    service = S3Service()
    assert service.session is not None
    assert service.bucket_name == settings.S3_BUCKET_NAME
    assert service.access_key == settings.S3_ACCESS_KEY
    assert service.secret_key == settings.S3_SECRET_KEY


def test_s3_service_initialization_custom(mock_session: MagicMock) -> None:
    """Verify S3Service accepts custom session and bucket name."""
    service = S3Service(session=mock_session, bucket_name="custom-bucket")
    assert service.session is mock_session
    assert service.bucket_name == "custom-bucket"


def test_s3_service_endpoint_url_resolution() -> None:
    """Verify endpoint_url resolution with and without explicit protocols."""
    service = S3Service()
    # Default settings has no protocol prefix
    assert service.endpoint_url.startswith("http://") or service.endpoint_url.startswith("https://")

    with patch.object(settings, "S3_ENDPOINT", "http://custom-minio:9000"):
        assert service.endpoint_url == "http://custom-minio:9000"

    with patch.object(settings, "S3_ENDPOINT", "custom-minio:9000"), patch.object(
        settings, "S3_USE_SSL", True
    ):
        assert service.endpoint_url == "https://custom-minio:9000"


@pytest.mark.asyncio
async def test_upload_json_success(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test successful JSON upload to S3."""
    test_data = {"policy": "Universal Basic Income", "score": 92.5}
    key = "tests/test_run.json"

    result = await s3_service.upload_json(key, test_data)

    assert result == key
    mock_s3_client.put_object.assert_called_once()
    call_kwargs = mock_s3_client.put_object.call_args[1]
    assert call_kwargs["Bucket"] == settings.S3_BUCKET_NAME
    assert call_kwargs["Key"] == key
    assert call_kwargs["ContentType"] == "application/json"
    assert json.loads(call_kwargs["Body"].decode("utf-8")) == test_data


@pytest.mark.asyncio
async def test_upload_json_connection_error(
    s3_service: S3Service, mock_s3_client: AsyncMock
) -> None:
    """Test upload_json when S3 endpoint is unreachable raises 503."""
    mock_s3_client.put_object.side_effect = EndpointConnectionError(
        endpoint_url=s3_service.endpoint_url
    )

    with pytest.raises(HTTPException) as exc_info:
        await s3_service.upload_json("test.json", {"k": "v"})

    assert exc_info.value.status_code == 503
    assert "unavailable" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_upload_json_client_error(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test upload_json on S3 ClientError raises 500."""
    mock_s3_client.put_object.side_effect = ClientError(
        {"Error": {"Code": "InternalError", "Message": "Failure"}}, "PutObject"
    )

    with pytest.raises(HTTPException) as exc_info:
        await s3_service.upload_json("test.json", {"k": "v"})

    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_download_json_success(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test successful JSON download and parsing from S3."""
    expected_data = {"status": "success", "count": 42}
    body_mock = AsyncMock()
    body_mock.read.return_value = json.dumps(expected_data).encode("utf-8")
    mock_s3_client.get_object.return_value = {"Body": body_mock}

    result = await s3_service.download_json("tests/data.json")

    assert result == expected_data
    mock_s3_client.get_object.assert_called_once_with(
        Bucket=settings.S3_BUCKET_NAME, Key="tests/data.json"
    )


@pytest.mark.asyncio
async def test_download_json_not_found(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test download_json raises NotFoundError when key does not exist."""
    mock_s3_client.get_object.side_effect = ClientError(
        {"Error": {"Code": "NoSuchKey", "Message": "The specified key does not exist."}},
        "GetObject",
    )

    with pytest.raises(NotFoundError) as exc_info:
        await s3_service.download_json("missing.json")

    assert exc_info.value.status_code == 404
    assert "missing.json" in exc_info.value.detail


@pytest.mark.asyncio
async def test_download_json_corrupted(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test download_json raises 502 Bad Gateway when body is not valid JSON."""
    body_mock = AsyncMock()
    body_mock.read.return_value = b"invalid json content {["
    mock_s3_client.get_object.return_value = {"Body": body_mock}

    with pytest.raises(HTTPException) as exc_info:
        await s3_service.download_json("corrupted.json")

    assert exc_info.value.status_code == 502


@pytest.mark.asyncio
async def test_download_json_connection_error(
    s3_service: S3Service, mock_s3_client: AsyncMock
) -> None:
    """Test download_json raises 503 on EndpointConnectionError."""
    mock_s3_client.get_object.side_effect = EndpointConnectionError(
        endpoint_url=s3_service.endpoint_url
    )

    with pytest.raises(HTTPException) as exc_info:
        await s3_service.download_json("file.json")

    assert exc_info.value.status_code == 503


@pytest.mark.asyncio
async def test_get_presigned_url_success(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test presigned URL generation."""
    expected_url = "http://localhost:9000/legisim-data/runs/123/cube.json?token=xyz"
    mock_s3_client.generate_presigned_url.return_value = expected_url

    url = await s3_service.get_presigned_url("runs/123/cube.json", expires_in=1800)

    assert url == expected_url
    mock_s3_client.generate_presigned_url.assert_called_once_with(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET_NAME, "Key": "runs/123/cube.json"},
        ExpiresIn=1800,
    )


@pytest.mark.asyncio
async def test_get_presigned_url_error(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test presigned URL generation error handling."""
    mock_s3_client.generate_presigned_url.side_effect = BotoCoreError()

    with pytest.raises(HTTPException) as exc_info:
        await s3_service.get_presigned_url("runs/123/cube.json")

    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_upload_cube(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test upload_cube uploads to runs/{run_id}/cube.json."""
    run_id = str(uuid.uuid4())
    cube_data = {"dimensions": ["region", "income"], "cells": []}

    key = await s3_service.upload_cube(run_id, cube_data)

    assert key == f"runs/{run_id}/cube.json"
    mock_s3_client.put_object.assert_called_once()
    call_kwargs = mock_s3_client.put_object.call_args[1]
    assert call_kwargs["Key"] == f"runs/{run_id}/cube.json"


@pytest.mark.asyncio
async def test_download_cube(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test download_cube fetches from runs/{run_id}/cube.json."""
    run_id = uuid.uuid4()
    expected_cube = {"dimensions": ["sector"], "cells": [1, 2, 3]}
    body_mock = AsyncMock()
    body_mock.read.return_value = json.dumps(expected_cube).encode("utf-8")
    mock_s3_client.get_object.return_value = {"Body": body_mock}

    cube = await s3_service.download_cube(run_id)

    assert cube == expected_cube
    mock_s3_client.get_object.assert_called_once_with(
        Bucket=settings.S3_BUCKET_NAME, Key=f"runs/{str(run_id)}/cube.json"
    )


@pytest.mark.asyncio
async def test_upload_and_download_bytes(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test upload_bytes and download_bytes operations."""
    payload = b"%PDF-1.4 binary content"
    key = "exports/test.pdf"

    # Upload
    uploaded_key = await s3_service.upload_bytes(key, payload, content_type="application/pdf")
    assert uploaded_key == key
    mock_s3_client.put_object.assert_called_once_with(
        Bucket=settings.S3_BUCKET_NAME,
        Key=key,
        Body=payload,
        ContentType="application/pdf",
    )

    # Download
    body_mock = AsyncMock()
    body_mock.read.return_value = payload
    mock_s3_client.get_object.return_value = {"Body": body_mock}

    downloaded = await s3_service.download_bytes(key)
    assert downloaded == payload


@pytest.mark.asyncio
async def test_delete_object(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test delete_object operation."""
    key = "obsolete/data.json"
    result = await s3_service.delete_object(key)
    assert result is True
    mock_s3_client.delete_object.assert_called_once_with(
        Bucket=settings.S3_BUCKET_NAME, Key=key
    )


@pytest.mark.asyncio
async def test_object_exists(s3_service: S3Service, mock_s3_client: AsyncMock) -> None:
    """Test object_exists returns True when found, False on NoSuchKey."""
    # When object exists
    mock_s3_client.head_object.return_value = {"ContentLength": 100}
    assert await s3_service.object_exists("file.json") is True

    # When object does not exist
    mock_s3_client.head_object.side_effect = ClientError(
        {"Error": {"Code": "NoSuchKey", "Message": "Not found"}}, "HeadObject"
    )
    assert await s3_service.object_exists("missing.json") is False


@pytest.mark.asyncio
async def test_ensure_bucket_exists_already_present(
    s3_service: S3Service, mock_s3_client: AsyncMock
) -> None:
    """Test ensure_bucket_exists does nothing if bucket already exists."""
    mock_s3_client.head_bucket.return_value = {}
    await s3_service.ensure_bucket_exists()
    mock_s3_client.create_bucket.assert_not_called()


@pytest.mark.asyncio
async def test_ensure_bucket_exists_creates_when_missing(
    s3_service: S3Service, mock_s3_client: AsyncMock
) -> None:
    """Test ensure_bucket_exists creates bucket when missing."""
    mock_s3_client.head_bucket.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "Bucket does not exist"}},
        "HeadBucket",
    )
    await s3_service.ensure_bucket_exists()
    mock_s3_client.create_bucket.assert_called_once_with(Bucket=settings.S3_BUCKET_NAME)


def test_get_s3_service_dependency(mock_session: MagicMock) -> None:
    """Test get_s3_service dependency extraction from request app state."""
    request_mock = MagicMock()
    request_mock.app.state.s3_session = mock_session

    service = get_s3_service(request_mock)
    assert service.session is mock_session

    # Without request
    service_default = get_s3_service(None)
    assert service_default.session is not None
