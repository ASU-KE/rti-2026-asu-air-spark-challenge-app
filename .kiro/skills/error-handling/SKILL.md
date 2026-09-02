---
name: error-handling
description: Error-handling patterns for TypeScript React and Python FastAPI. Use when designing error types, adding retries, or writing user-facing failure messages; reviewing endpoints for missing error handling; or debugging cascading failures and silent error swallowing.
metadata:
  origin: ECC
---

# Error Handling Patterns

## Core Principles

1. **Fail fast and loudly** — surface errors at the boundary where they occur; don't bury them
2. **Typed errors over string messages** — errors are first-class values with structure
3. **User messages ≠ developer messages** — show friendly text to users, log full context server-side
4. **Handle every error** — every `catch` block handles, re-throws, or logs; none swallowed silently
5. **Errors are part of your API contract** — document every error code a client may receive

## TypeScript React (Frontend)

Model the errors your API returns as typed values, turn them into friendly copy, and contain render failures with a boundary.

### Typed Error Classes

```typescript
// Mirror the error codes your FastAPI backend returns, as first-class values
export class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    public readonly details?: unknown,
  ) {
    super(message)
    this.name = this.constructor.name
    // Maintain correct prototype chain in transpiled ES5 JavaScript.
    // Required for `instanceof` checks (e.g., `error instanceof NotFoundError`)
    // to work correctly when extending the built-in Error class.
    Object.setPrototypeOf(this, new.target.prototype)
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, 'NOT_FOUND', 404)
  }
}

export class ValidationError extends AppError {
  constructor(message: string, details: { field: string; message: string }[]) {
    super(message, 'VALIDATION_ERROR', 422, details)
  }
}

export class UnauthorizedError extends AppError {
  constructor(reason = 'Authentication required') {
    super(reason, 'UNAUTHORIZED', 401)
  }
}

export class RateLimitError extends AppError {
  constructor(public readonly retryAfterMs: number) {
    super('Rate limit exceeded', 'RATE_LIMITED', 429)
  }
}
```

### Result Pattern (no-throw style)

For operations where failure is expected and common (fetching from the API, parsing):

```typescript
type Result<T, E = AppError> =
  | { ok: true; value: T }
  | { ok: false; error: E }

function ok<T>(value: T): Result<T> {
  return { ok: true, value }
}

function err<E>(error: E): Result<never, E> {
  return { ok: false, error }
}

// Decode the backend error envelope into a typed AppError
async function fetchUser(id: string): Promise<Result<User>> {
  const res = await fetch(`/api/users/${id}`)
  if (res.status === 404) return err(new NotFoundError('User', id))
  if (!res.ok) {
    const body = await res.json().catch(() => null)
    const code = body?.error?.code ?? 'INTERNAL_ERROR'
    return err(new AppError(body?.error?.message ?? 'Request failed', code, res.status))
  }
  return ok((await res.json()) as User)
}

const result = await fetchUser('abc-123')
if (!result.ok) {
  // TypeScript knows result.error here
  logger.error('Failed to fetch user', { error: result.error })
} else {
  // TypeScript knows result.value here
  console.log(result.value.email)
}
```

### User-Facing Error Messages

Map error codes to human-readable messages. Keep technical details out of user-visible text.

```typescript
const USER_ERROR_MESSAGES: Record<string, string> = {
  NOT_FOUND: 'The requested item could not be found.',
  UNAUTHORIZED: 'Please sign in to continue.',
  FORBIDDEN: "You don't have permission to do that.",
  VALIDATION_ERROR: 'Please check your input and try again.',
  RATE_LIMITED: 'Too many requests. Please wait a moment and try again.',
  INTERNAL_ERROR: 'Something went wrong on our end. Please try again later.',
}

export function getUserMessage(code: string): string {
  return USER_ERROR_MESSAGES[code] ?? USER_ERROR_MESSAGES.INTERNAL_ERROR
}
```

### Fetching with Error Handling

Compose the typed fetch with the message map inside a component. Guard against setting state after unmount, and surface only the friendly message.

```typescript
import { useEffect, useState } from 'react'

function UserProfile({ id }: { id: string }) {
  const [user, setUser] = useState<User | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    fetchUser(id).then(result => {
      if (!active) return
      if (result.ok) setUser(result.value)
      else setErrorMessage(getUserMessage(result.error.code))
    })
    return () => {
      active = false
    }
  }, [id])

  if (errorMessage) return <p role="alert">{errorMessage}</p>
  if (!user) return <p>Loading…</p>
  return <h1>{user.email}</h1>
}
```

### React Error Boundary

Catches render-time errors a `try/catch` cannot reach.

```typescript
import { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  fallback: ReactNode
  onError?: (error: Error, info: ErrorInfo) => void
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    this.props.onError?.(error, info)
    console.error('Unhandled React error:', error, info)
  }

  render() {
    if (this.state.hasError) return this.props.fallback
    return this.props.children
  }
}

// Usage
<ErrorBoundary fallback={<p>Something went wrong. Please refresh.</p>}>
  <MyComponent />
</ErrorBoundary>
```

## Python FastAPI (Backend)

Define a domain exception hierarchy, translate it to the standard envelope in exception handlers, and retry only transient upstream failures.

### Custom Exception Hierarchy

```python
class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str, code: str, status_code: int = 500):
        super().__init__(message)
        self.code = code
        self.status_code = status_code

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} not found: {id}", "NOT_FOUND", 404)

class ValidationError(AppError):
    def __init__(self, message: str, details: list[dict] | None = None):
        super().__init__(message, "VALIDATION_ERROR", 422)
        self.details = details or []
```

### Exception Handlers

Register handlers once on the app. Every response follows the same envelope `{"error": {"code", "message"}}` the frontend decodes.

```python
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)
app = FastAPI()

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    error: dict = {"code": exc.code, "message": str(exc)}
    if getattr(exc, "details", None):
        error["details"] = exc.details
    return JSONResponse(status_code=exc.status_code, content={"error": error})

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": [
                    {"field": ".".join(str(p) for p in e["loc"]), "message": e["msg"]}
                    for e in exc.errors()
                ],
            }
        },
    )

@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": "HTTP_ERROR", "message": exc.detail}},
    )

@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    # Log full details, return a generic message
    logger.exception("Unexpected error")
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"}},
    )
```

Raise the typed errors from route handlers and let the handlers shape the response:

```python
@app.get("/api/users/{user_id}")
async def get_user(user_id: str) -> User:
    user = await repo.find_by_id(user_id)
    if user is None:
        raise NotFoundError("User", user_id)
    return user
```

### Retry with Exponential Backoff

Wrap calls to external services. Retry transient failures (5xx, timeouts), never client errors (4xx).

```python
import asyncio
import random
from functools import wraps
from typing import Awaitable, Callable, TypeVar

import httpx

T = TypeVar("T")

def retry(
    max_attempts: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
    retry_if: Callable[[Exception], bool] = lambda exc: True,
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """Retry an async call with exponential backoff and jitter."""
    def decorator(fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            for attempt in range(1, max_attempts + 1):
                try:
                    return await fn(*args, **kwargs)
                except Exception as exc:
                    if attempt == max_attempts or not retry_if(exc):
                        raise
                    jitter = random.uniform(0, base_delay)
                    delay = min(base_delay * 2 ** (attempt - 1) + jitter, max_delay)
                    await asyncio.sleep(delay)
            raise AssertionError("unreachable")
        return wrapper
    return decorator

# Usage: retry transient upstream failures, not application errors
@retry(
    max_attempts=3,
    retry_if=lambda exc: not isinstance(exc, AppError) or exc.status_code >= 500,
)
async def fetch_inventory(sku: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://inventory.internal/items/{sku}")
        resp.raise_for_status()
        return resp.json()
```

## Error Handling Checklist

Before merging any code that touches error handling, confirm every item — the review is complete only when all are checked:

- [ ] Every `catch`/`except` block handles, re-throws, or logs — no silent swallowing
- [ ] API errors follow the standard envelope `{ error: { code, message } }`
- [ ] User-facing messages contain no stack traces or internal details
- [ ] Full error context is logged server-side
- [ ] Custom error classes extend a base `AppError` with a `code` field
- [ ] Async functions surface errors to callers — no fire-and-forget without fallback
- [ ] Retry logic only retries retriable errors (not 4xx client errors)
- [ ] React components are wrapped in `ErrorBoundary` for rendering errors
