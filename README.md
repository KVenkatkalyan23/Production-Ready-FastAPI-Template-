# FastAPI Template

## Project Overview

This repository is a backend starter template built with FastAPI, Pydantic v2, and async SQLAlchemy.

It includes:

- environment-based configuration
- reusable request validation schemas
- centralized error handling
- structured logging
- async database session and repository patterns
- pytest-based unit and integration testing with coverage

The current template exposes a minimal `/health` endpoint and establishes reusable patterns for future auth, user, and database-backed features.

## Setup Instructions

1. Create or activate a Python virtual environment.
2. Install the project dependencies.
3. Copy values from [`.env.example`](/abs/path/C:/ai/fastApi-tempate/.env.example) into your local environment files.
4. Set `ENVIRONMENT` in [`.env`](/abs/path/C:/ai/fastApi-tempate/.env) to the environment you want to run, such as `development` or `testing`.

Example on Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy asyncpg aiosqlite pydantic pydantic-settings email-validator pytest pytest-asyncio pytest-cov httpx
```

## Required Environment Variables

The application loads settings from `.env.<environment>` based on the `ENVIRONMENT` value in the root `.env` file.

Required variables:

- `APP_NAME`
- `ENVIRONMENT`
- `DEBUG`
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `CORS_ORIGINS`
- `LOG_LEVEL`
- `LOG_JSON`

Example:

```env
ENVIRONMENT=development
APP_NAME=FastAPI Template
DEBUG=true
LOG_LEVEL=INFO
LOG_JSON=false
DATABASE_URL=sqlite:///./app.db
JWT_SECRET_KEY=replace-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["http://localhost:3000"]
```

## Run the Application

Start the API with Uvicorn from the project root:

```powershell
uvicorn app.main:app --reload
```

The health endpoint is available at:

```text
GET /health
```

## Run Tests

The test suite uses `pytest`, the `testing` environment, and a separate SQLite test database.

Run all tests:

```powershell
pytest
```

Run a specific file:

```powershell
pytest tests/unit/test_security.py
```

Coverage is configured in [`pytest.ini`](/abs/path/C:/ai/fastApi-tempate/pytest.ini) and currently enforces:

- app coverage measurement
- terminal missing-lines report
- `coverage.xml` generation
- minimum coverage threshold of `70%`

## Extend the Template

Use these patterns when adding new features:

- Add request and response schemas under [app/schemas](/abs/path/C:/ai/fastApi-tempate/app/schemas).
- Reuse shared schema primitives in [common.py](/abs/path/C:/ai/fastApi-tempate/app/schemas/common.py) for normalized email, strong password validation, and request model behavior.
- Add ORM models under [app/db/models](/abs/path/C:/ai/fastApi-tempate/app/db/models) and inherit from [Base](/abs/path/C:/ai/fastApi-tempate/app/db/models/base.py) plus reusable mixins like [TimestampMixin.py](/abs/path/C:/ai/fastApi-tempate/app/db/models/TimestampMixin.py).
- Keep persistence logic in repositories under [app/db/repositories](/abs/path/C:/ai/fastApi-tempate/app/db/repositories) and avoid mixing business logic into repository methods.
- Raise reusable app exceptions from [exceptions.py](/abs/path/C:/ai/fastApi-tempate/app/core/exceptions.py) so all errors flow through the centralized handlers in [exception_handlers.py](/abs/path/C:/ai/fastApi-tempate/app/core/exception_handlers.py).
- Keep environment-dependent settings in [config.py](/abs/path/C:/ai/fastApi-tempate/app/core/config.py), not hardcoded in feature code.
- Add unit tests under [tests/unit](/abs/path/C:/ai/fastApi-tempate/tests/unit) and API-level or DB-backed tests under [tests/integration](/abs/path/C:/ai/fastApi-tempate/tests/integration).

## Notes

- Local `.env` files are ignored by Git. Keep only [`.env.example`](/abs/path/C:/ai/fastApi-tempate/.env.example) tracked.
- The test suite expects isolated test data and should not point to development or production databases.
