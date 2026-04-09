"""Tests for the async user repository."""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.models.base import Base
from app.db.models.user import User
from app.db.repositories.user import UserRepository


@pytest_asyncio.fixture
async def session() -> AsyncIterator[AsyncSession]:
    """Provide an isolated async database session per test."""

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_factory() as db_session:
        yield db_session

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_and_get_user_by_email(session: AsyncSession) -> None:
    """Users should be persisted and loaded by email primary key."""

    repository = UserRepository(session)

    created = await repository.create_user(
        email="alice@example.com",
        password_hash="hashed-password",
        full_name="Alice Example",
    )

    fetched = await repository.get_by_email("alice@example.com")

    assert fetched is not None
    assert fetched.email == "alice@example.com"
    assert created.email == fetched.email
    assert created.password_hash == "hashed-password"
    assert created.full_name == "Alice Example"
    assert "id" not in User.__table__.columns
    assert User.__table__.primary_key.columns.keys() == ["email"]


@pytest.mark.asyncio
async def test_list_users_returns_stable_email_order(session: AsyncSession) -> None:
    """Listing should return persisted users ordered by email."""

    repository = UserRepository(session)
    await repository.create_user(
        email="zara@example.com",
        password_hash="hash-z",
        full_name="Zara Example",
    )
    await repository.create_user(
        email="bob@example.com",
        password_hash="hash-b",
        full_name="Bob Example",
    )

    users = await repository.list_users()

    assert [user.email for user in users] == ["bob@example.com", "zara@example.com"]


@pytest.mark.asyncio
async def test_update_user_updates_mutable_fields_and_timestamp(session: AsyncSession) -> None:
    """Updating a user should persist changes and keep audit fields populated."""

    repository = UserRepository(session)
    created = await repository.create_user(
        email="carol@example.com",
        password_hash="hash-c",
        full_name="Carol Example",
    )

    updated = await repository.update_user(
        "carol@example.com",
        full_name="Carol Updated",
        password_hash="hash-updated",
    )

    assert updated is not None
    assert updated.email == "carol@example.com"
    assert updated.full_name == "Carol Updated"
    assert updated.password_hash == "hash-updated"
    assert isinstance(updated.created_at, datetime)
    assert isinstance(updated.updated_at, datetime)
    assert updated.updated_at >= created.updated_at


@pytest.mark.asyncio
async def test_update_user_returns_none_for_missing_user(session: AsyncSession) -> None:
    """Missing users should not raise when update is requested."""

    repository = UserRepository(session)

    updated = await repository.update_user("missing@example.com", full_name="Missing")

    assert updated is None
