# Streaming & SSE Plan

## Overview
LangGraph simulations take 30-90 seconds. To keep the user engaged, the backend must stream progress, agent thoughts, and partial data using Server-Sent Events (SSE).

**Subagents Required**:
- `backend-implementer`

## Mechanism
1. FastAPI initiates a background task (e.g., Celery, arq, or Redis Queue) to run the LangGraph workflow.
2. The LangGraph nodes publish progress events to a Redis Pub/Sub channel keyed by the `run_id`.
3. The client connects to `GET /api/runs/{run_id}/stream`.
4. The FastAPI route subscribes to the Redis channel and yields SSE lines.

## Redis Pub/Sub Payload
```json
{
  "step": "cohort_analysis",
  "progress": 45,
  "message": "Analyzing demographic impact on rural farmers...",
  "partial_data": {}
}
```

## FastAPI SSE Endpoint

```python
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import asyncio
import json

router = APIRouter()

async def redis_event_generator(run_id: str, redis_client):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"run_updates:{run_id}")
    
    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                yield {
                    "event": "update",
                    "data": json.dumps(data)
                }
                if data.get("status") in ("completed", "failed"):
                    break
    finally:
        await pubsub.unsubscribe(f"run_updates:{run_id}")

@router.get("/runs/{run_id}/stream")
async def stream_run(run_id: str, request: Request):
    redis = request.app.state.redis
    return EventSourceResponse(redis_event_generator(run_id, redis))
```
