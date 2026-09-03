---
name: backend-patterns
description: Backend architecture for Python FastAPI services and their data access — REST endpoints, repository and service layers, query optimization, error handling, auth, rate limiting, caching, background jobs, and structured logging. Use when building or reviewing server-side APIs; for FastAPI framework specifics — schemas, dependency injection, routers — see fastapi-patterns.
metadata:
  origin: ECC
---

# Backend Development Patterns

Patterns for scalable Python FastAPI services: the request path (routing, data access, errors, auth) plus cross-cutting concerns. For framework-level detail — Pydantic schemas, dependency injection, router and transactional service wiring — see `fastapi-patterns`; this skill stays on the architecture those pieces plug into.

## API Design Patterns

### RESTful API Structure

```text
GET    /markets                 # List resources
GET    /markets/{id}            # Get single resource
POST   /markets                 # Create resource
PUT    /markets/{id}            # Replace resource
PATCH  /markets/{id}            # Update resource
DELETE /markets/{id}            # Delete resource

# Query parameters for filtering, sorting, pagination
GET /markets?status=active&sort=volume&limit=20&offset=0
```

### Repository Pattern

Abstract data access behind a `Protocol` so services depend on the interface, not the SQLAlchemy session. A structural `Protocol` lets any conforming class (real, cached, fake) substitute without inheritance.

```python
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.market import Market
from app.schemas.market import CreateMarketDto, MarketFilters, UpdateMarketDto


class MarketRepository(Protocol):
    async def find_all(self, filters: MarketFilters | None = None) -> list[Market]: ...
    async def find_by_id(self, market_id: int) -> Market | None: ...
    async def create(self, data: CreateMarketDto) -> Market: ...
    async def update(self, market_id: int, data: UpdateMarketDto) -> Market: ...
    async def delete(self, market_id: int) -> None: ...


class SqlAlchemyMarketRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_all(self, filters: MarketFilters | None = None) -> list[Market]:
        stmt = select(Market)
        if filters and filters.status:
            stmt = stmt.where(Market.status == filters.status)
        if filters and filters.limit:
            stmt = stmt.limit(filters.limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # Other methods...
```

### Service Layer Pattern

Business logic lives in the service and depends on the repository abstraction, keeping data access swappable. For transaction boundaries inside a service — commit/rollback and `IntegrityError` handling — see `fastapi-patterns`.

```python
class MarketService:
    def __init__(self, repo: MarketRepository) -> None:
        self.repo = repo

    async def search_markets(self, query: str, limit: int = 10) -> list[Market]:
        embedding = await generate_embedding(query)
        matches = await self._vector_search(embedding, limit)

        markets = await self.repo.find_by_ids([m.id for m in matches])

        # Sort by similarity score from the vector search
        score_by_id = {m.id: m.score for m in matches}
        return sorted(markets, key=lambda market: score_by_id.get(market.id, 0.0))

    async def _vector_search(self, embedding: list[float], limit: int):
        ...  # Vector search implementation
```

### Middleware Pattern

Middleware processes every request in a pipeline — request IDs, timing, correlation headers. Register it once on the app. Keep authentication in FastAPI dependencies (see `fastapi-patterns`), not middleware, so status signals stay per-route.

```python
# app/middleware.py
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        request.state.request_id = request_id

        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000

        response.headers["x-request-id"] = request_id
        response.headers["x-response-time-ms"] = f"{elapsed_ms:.1f}"
        return response


# app/main.py
app.add_middleware(RequestContextMiddleware)
```

## Database Patterns

### Query Optimization

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def top_markets(db: AsyncSession):
    # GOOD: select only the columns you use
    result = await db.execute(
        select(Market.id, Market.name, Market.status, Market.volume)
        .where(Market.status == "active")
        .order_by(Market.volume.desc())
        .limit(10)
    )
    return result.all()


async def top_markets_wasteful(db: AsyncSession):
    # BAD: load full entities when a few columns would do
    result = await db.execute(select(Market))
    return result.scalars().all()
```

### N+1 Query Prevention

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def markets_with_creators(db: AsyncSession):
    # GOOD: eager-load the relationship in one extra round trip
    result = await db.execute(
        select(Market).options(selectinload(Market.creator))
    )
    for market in result.scalars().all():
        use(market.creator)  # already loaded


async def markets_n_plus_one(db: AsyncSession):
    # BAD: N+1 — one query per row
    result = await db.execute(select(Market))
    for market in result.scalars().all():
        creator = await db.get(User, market.creator_id)  # N queries
        use(creator)
```

### Transaction Pattern

Group multiple writes into one atomic unit of work with `async with db.begin()`: it commits on success and rolls back on any exception. For where these boundaries belong — inside the service layer, catching `IntegrityError` — see `fastapi-patterns`.

```python
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.market import Market
from app.models.position import Position


async def create_market_with_position(
    db: AsyncSession, market: Market, position: Position
) -> None:
    async with db.begin():  # commit on success, rollback on any exception
        db.add(market)
        db.add(position)
```

## Error Handling Patterns

### Centralized Error Handler

Register exception handlers on the app so every route returns one consistent error envelope. A domain `ApiError` carries the status; validation and unexpected errors get their own shapes.

```python
# app/errors.py
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class ApiError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def handle_api_error(request: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": exc.message},
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"success": False, "error": "Validation failed", "details": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
        logger.error("Unexpected error", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Internal server error"},
        )
```

### Retry with Exponential Backoff

```python
import asyncio
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


async def fetch_with_retry(
    fn: Callable[[], Awaitable[T]], max_retries: int = 3
) -> T:
    last_exc: Exception | None = None
    for attempt in range(max_retries):
        try:
            return await fn()
        except Exception as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 1s, 2s, 4s
    assert last_exc is not None
    raise last_exc


# Usage
async def load() -> dict:
    return await fetch_with_retry(lambda: fetch_from_api())
```

## Authentication & Authorization

Authentication — verifying identity from JWT/OAuth2 — belongs to `fastapi-patterns`, which owns the `get_current_user` dependency. This skill covers the authorization layer built on top of it: mapping the authenticated user to permissions.

### Role-Based Access Control

Model permissions as immutable sets keyed by role, then gate routes with a dependency factory that reuses the authentication dependency.

```python
from enum import StrEnum
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.dependencies import CurrentUserDep  # authentication wiring from fastapi-patterns
from app.models.user import User


class Permission(StrEnum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"


ROLE_PERMISSIONS: dict[str, frozenset[Permission]] = {
    "admin": frozenset(Permission),
    "moderator": frozenset({Permission.READ, Permission.WRITE, Permission.DELETE}),
    "user": frozenset({Permission.READ, Permission.WRITE}),
}


def require_permission(permission: Permission):
    def dependency(current_user: CurrentUserDep) -> User:
        if permission not in ROLE_PERMISSIONS.get(current_user.role, frozenset()):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return dependency


# Usage: compose the permission gate as a route dependency
@router.delete("/markets/{market_id}", status_code=204)
async def delete_market(
    market_id: int,
    _: Annotated[User, Depends(require_permission(Permission.DELETE))],
) -> None:
    ...
```

## Rate Limiting

Rate limiting must use a shared store such as Redis, a gateway, or the platform's
native limiter, so limits hold across replicas and survive deploys. Per-process
in-memory counters reset on deploy, split across replicas, and fail open in
multi-instance environments.

In FastAPI, apply the limit as a route dependency or ASGI middleware backed by
that shared store (e.g. a Redis-backed limiter). Keep this layer responsible for
choosing the integration point and error shape; use `api-design` for the HTTP
contract and `security-review` for abuse-case review.

## Cross-cutting concerns

Caching, background jobs, and structured logging layer across routes rather than sitting on the core request path — see [cross-cutting patterns](cross-cutting-patterns.md).
