"""Shared pytest fixtures and test environment setup."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


os.environ["ENVIRONMENT"] = "testing"

from app.db.models.base import Base
from app.db.session import get_db
from app.main import app


TESTS_DIR = Path(__file__).resolve().parent
TEST_DATABASE_PATH = TESTS_DIR / "test_suite.db"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DATABASE_PATH.as_posix()}"


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Provide the isolated database URL used by the test suite."""

    return TEST_DATABASE_URL


@pytest_asyncio.fixture
async def db_session(test_database_url: str) -> AsyncIterator[AsyncSession]:
    """Provide an isolated async database session per test."""

    if TEST_DATABASE_PATH.exists():
        TEST_DATABASE_PATH.unlink()

    engine = create_async_engine(test_database_url)
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        yield session

    await engine.dispose()
    if TEST_DATABASE_PATH.exists():
        TEST_DATABASE_PATH.unlink()


@pytest.fixture
def sample_user_payload() -> dict[str, str]:
    """Reusable valid user payload for unit and integration tests."""

    return {
        "email": "tester@example.com",
        "password": "Valid1!Pass",
        "full_name": "Test User",
    }


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Provide a FastAPI test client with dependency override cleanup."""

    app.dependency_overrides.clear()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_db(db_session: AsyncSession) -> Iterator[TestClient]:
    """Provide a test client with the database dependency overridden."""

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
