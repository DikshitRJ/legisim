from __future__ import annotations

import json
from collections.abc import AsyncGenerator

import redis.asyncio as aioredis

from app.core.redis import subscribe_run_events


async def sse_event_generator(redis: aioredis.Redis, run_id: str) -> AsyncGenerator[dict[str, str], None]:
    """Async generator that yields SSE events from Redis pub/sub."""
    async for data in subscribe_run_events(redis, run_id):
        yield {
            "event": "update",
            "data": json.dumps(data)
        }
        if data.get("status") in ("completed", "failed"):
            break
