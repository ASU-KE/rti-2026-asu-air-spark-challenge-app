# Cross-cutting backend patterns

Reference reached from [`backend-patterns`](SKILL.md): concerns layered across API routes rather than on the core request path — caching, background jobs, and structured logging.

## Caching Strategies

### Redis Caching Layer

Wrap a repository with a read-through cache. It conforms to the same `MarketRepository` protocol, so callers are unaware of the cache. Serialize through the Pydantic response schema — `model_dump_json` / `model_validate_json` handle the round trip.

```python
from redis.asyncio import Redis

from app.repositories.market import MarketRepository
from app.schemas.market import MarketResponse


class CachedMarketRepository:
    """Read-through Redis cache wrapping a MarketRepository."""

    TTL_SECONDS = 300  # 5 minutes

    def __init__(self, base_repo: MarketRepository, redis: Redis) -> None:
        self.base_repo = base_repo
        self.redis = redis

    async def find_by_id(self, market_id: int) -> MarketResponse | None:
        key = f"market:{market_id}"

        cached = await self.redis.get(key)
        if cached is not None:
            return MarketResponse.model_validate_json(cached)

        market = await self.base_repo.find_by_id(market_id)
        if market is None:
            return None

        response = MarketResponse.model_validate(market)
        await self.redis.setex(key, self.TTL_SECONDS, response.model_dump_json())
        return response

    async def invalidate(self, market_id: int) -> None:
        await self.redis.delete(f"market:{market_id}")
```

### Cache-Aside Pattern

```python
from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.market import Market
from app.schemas.market import MarketResponse


async def get_market_cached(
    market_id: int, db: AsyncSession, redis: Redis
) -> MarketResponse:
    key = f"market:{market_id}"

    cached = await redis.get(key)
    if cached is not None:
        return MarketResponse.model_validate_json(cached)

    market = await db.get(Market, market_id)
    if market is None:
        raise HTTPException(status_code=404, detail="Market not found")

    response = MarketResponse.model_validate(market)
    await redis.setex(key, 300, response.model_dump_json())
    return response
```

## Background Jobs & Queues

Offload slow work off the request path. Match durability to the work: `BackgroundTasks` for best-effort in-process work, a broker-backed queue for anything that must survive a restart.

### Fire-and-Forget: BackgroundTasks

`BackgroundTasks` runs after the response is sent, in the same process. Simple, but lost on crash or restart — use only for best-effort work.

```python
from fastapi import APIRouter, BackgroundTasks

router = APIRouter()


async def index_market(market_id: int) -> None:
    ...  # expensive indexing work


@router.post("/markets/{market_id}/index", status_code=202)
async def enqueue_index(market_id: int, background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(index_market, market_id)
    return {"success": True, "message": "Job queued"}
```

### Durable Queue: ARQ (Redis-backed)

For retryable work that runs across separate worker processes and survives restarts, enqueue to a broker such as ARQ or Celery. The request path only enqueues; the worker executes.

```python
from arq import create_pool
from arq.connections import RedisSettings


async def index_market(ctx, market_id: int) -> None:
    ...  # runs in a separate worker process


class WorkerSettings:
    functions = [index_market]
    redis_settings = RedisSettings(host="localhost", port=6379)


# In the request path, enqueue instead of blocking:
async def enqueue_index(market_id: int) -> None:
    redis = await create_pool(RedisSettings())
    await redis.enqueue_job("index_market", market_id)
```

## Logging & Monitoring

### Structured Logging

Emit one JSON object per log line so logs are queryable. A stdlib `logging.Formatter` needs no extra dependency; pass per-request fields through `extra`. (For richer pipelines, `structlog` offers the same shape with context binding.)

```python
# app/logging_config.py
import json
import logging
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname.lower(),
            "message": record.getMessage(),
        }
        # Merge structured context passed via extra={"context": {...}}
        context = getattr(record, "context", None)
        if context:
            entry.update(context)
        if record.exc_info:
            entry["error"] = self.formatException(record.exc_info)
        return json.dumps(entry)


def configure_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
```

```python
# Usage — reuse the request_id set by RequestContextMiddleware
import logging

from fastapi import Request

logger = logging.getLogger(__name__)


@router.get("/markets")
async def list_markets(request: Request, db: DbDep) -> dict:
    request_id = request.state.request_id
    logger.info(
        "Fetching markets",
        extra={"context": {"request_id": request_id, "method": "GET", "path": "/markets"}},
    )
    try:
        markets = await fetch_markets(db)
        return {"success": True, "data": markets}
    except Exception:
        logger.error(
            "Failed to fetch markets",
            exc_info=True,
            extra={"context": {"request_id": request_id}},
        )
        raise
```
