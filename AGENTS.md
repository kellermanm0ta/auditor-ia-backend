# AuditorIA Backend

## Stack
- **FastAPI** + **Uvicorn** — async Python 3.11+
- **SQLAlchemy 2.0** + **psycopg2-binary** — PostgreSQL
- **Pydantic v2** / **pydantic-settings** — validation & config
- **pytest** + **pytest-asyncio** + **httpx** (via `ASGITransport`) — testing
- **Ruff** — linter + formatter (line-length 100); B008 suppressed in pyproject.toml
- **Alembic** listed as dep but **not yet configured** — tables created via `Base.metadata.create_all` on startup

## Commands

```bash
# start PostgreSQL
docker compose up -d

# run dev server (from repo root)
uvicorn app.main:app --reload

# tests
pytest                                  # all
pytest tests/test_integrations.py       # single file
pytest -k "integration"                 # by name

# lint & format
ruff check .
ruff format --check .
ruff check --fix .
ruff format .

```

## Architecture

```
app/
  main.py          — FastAPI app + /health; creates DB tables via lifespan
  core/settings.py  — pydantic-settings (reads .env)
  db/session.py    — SQLAlchemy engine + session factory + get_db dependency
  models/          — ORM models (Integration with steps stored as JSON string)
  schemas/         — Pydantic request/response schemas
  services/        — business logic (integration_service uses DB; item_service is in-memory stub)
  api/routes.py             — aggregates all sub-routers
  api/integration_routes.py — /api/integrations CRUD
  api/skill_routes.py       — /api/skills CRUD
  api/output_format_routes.py — /api/output-formats CRUD
  api/history_routes.py     — /api/history CRUD
  api/config_routes.py      — /api/config GET/PUT
scripts/
  init.sql         — PostgreSQL init script (seeds integrations, skills, output_formats, history)
tests/             — pytest-asyncio tests using httpx ASGITransport
```

## Key facts
- `.env` is gitignored; copy `.env.example` to get started
- PostgreSQL runs via `docker compose up -d` (reads env vars from `.env` — no hardcoded credentials)
- `docker compose` requires Docker Engine 24+ and Compose v2.23+; use `docker compose` (plugin), not `docker-compose`
- `DATABASE_URL` in `.env` uses `${POSTGRES_USER}`, `${POSTGRES_PASSWORD}`, `${POSTGRES_DB}` interpolation to stay in sync with Docker Compose
- On Windows, activate venv with `.venv\Scripts\activate` (cmd) or `.venv\Scripts\Activate.ps1` (PowerShell)
- DB is wired into `/api/integrations` routes via `get_db` dependency
- `Integration.steps` stored as JSON string in `TEXT` column; deserialized to `list[str]` via Pydantic `@field_validator`
- Table auto-created on app startup via `Base.metadata.create_all(bind=engine)` in lifespan
- Alembic migrations **not initialized** — run `alembic init alembic` when switching to migration-based schema management
- `asyncio_mode = auto` in pyproject.toml — no need for `@pytest.mark.asyncio` on test functions, but the codebase uses it explicitly
- Ruff replaces flake8/isort/black — no other formatters
- B008 (Depends in function defaults) is suppressed — false positive for FastAPI