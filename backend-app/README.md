# Backend (`airgents-backend`)

FastAPI backend for AIRgents of Change. The project metadata, dependencies, and
pytest configuration live in the repository-root `pyproject.toml` so CI can run
`uv sync && uv run pytest` from the root.

## Layout

```text
backend-app/
|-- app/
|   |-- main.py          # App factory, exception handlers, router wiring
|   |-- config.py        # Settings from environment (pydantic-settings)
|   |-- routers/         # HTTP routes
|   `-- schemas/         # Pydantic v2 request/response schemas
`-- tests/               # pytest integration tests through the HTTP boundary
```

## Local development

```bash
uv sync                                    # install dependencies (from repo root)
cp backend-app/.env.example .env           # optional: configure provider access
cd backend-app && uv run uvicorn app.main:app --reload
curl -s http://localhost:8000/api/health   # standard response envelope
```

Run `uvicorn` from `backend-app/` so that `app` resolves on the import path;
`uv run` still finds the project and virtualenv at the repository root.

## Tests and typecheck

Run both from the repository root:

```bash
uv run pytest        # full backend suite
uv run mypy          # strict typecheck of backend-app
```

## API conventions

Every response uses the standard envelope — `success`, `data`, `error`, and
`meta` (present only on paginated collections). The frontend consumes it through
`frontend-app/src/api/client.ts`. Routes are served under `/api`, which Vite
proxies to `http://localhost:8000` in local development.
