"""Async SQLAlchemy engine and session management."""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


def _build_async_database_url(database_url: str) -> str:
    """Normalize supported database URLs to async SQLAlchemy drivers."""

    if database_url.startswith("postgresql+asyncpg://"):
        return database_url
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if database_url.startswith("sqlite+aiosqlite://"):
        return database_url
    if database_url.startswith("sqlite:///"):
        return database_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    return database_url


ASYNC_DATABASE_URL = _build_async_database_url(settings.DATABASE_URL)

engine_kwargs = {"pool_pre_ping": True}
if not ASYNC_DATABASE_URL.startswith("sqlite+aiosqlite://"):
    engine_kwargs.update({"pool_size": 5, "max_overflow": 10})


engine = create_async_engine(
    ASYNC_DATABASE_URL,
    **engine_kwargs,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session for request-scoped usage."""

    async with AsyncSessionLocal() as session:
        yield session
