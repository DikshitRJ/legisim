from __future__ import annotations

import json
from collections.abc import AsyncGenerator
from typing import Any

import redis.asyncio as aioredis

from app.config import settings


async def get_redis_pool() -> aioredis.Redis:
    """Create a Redis connection pool."""
    return aioredis.from_url(settings.REDIS_URL, decode_responses=True)


async def publish_run_event(redis: aioredis.Redis, run_id: str, data: dict[str, Any]) -> None:
    """Publish a run update event to Redis pub/sub."""
    channel = f"run_updates:{run_id}"
    await redis.publish(channel, json.dumps(data))


async def subscribe_run_events(redis: aioredis.Redis, run_id: str) -> AsyncGenerator[dict[str, Any], None]:
    """Subscribe to run update events and yield messages."""
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"run_updates:{run_id}")
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                yield json.loads(message["data"])
    finally:
        await pubsub.unsubscribe(f"run_updates:{run_id}")
