# TODO: Integrate SSE Endpoint in runs.py

When `app/api/routes/runs.py` is created, you need to add the SSE events endpoint as follows:

```python
from fastapi import APIRouter, Depends, Request, HTTPException
from sse_starlette.sse import EventSourceResponse

from app.services.streaming_service import sse_event_generator
from app.api.deps import get_redis

# ... inside your APIRouter ...

@router.get('/{run_id}/events')
async def stream_events(run_id: str, request: Request, redis = Depends(get_redis)):
    if redis is None:
        raise HTTPException(status_code=503, detail='Redis not available')
    return EventSourceResponse(sse_event_generator(redis, run_id))
```

Ensure `redis.asyncio` is used and the SSE endpoint gracefully handles disconnects, which the EventSourceResponse handles correctly via async generator cancellation.
