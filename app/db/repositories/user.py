"""Repository helpers for user persistence."""

from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class UserRepository:
    """Reusable async persistence operations for users."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, *, email: str, password_hash: str, full_name: str) -> User:
        """Create and persist a user record."""

        user = User(email=email, password_hash=password_hash, full_name=full_name)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a single user by email primary key."""

        return await self.session.get(User, email)

    async def list_users(self) -> Sequence[User]:
        """Return all users ordered by email for stable results."""

        result = await self.session.execute(select(User).order_by(User.email))
        return result.scalars().all()

    async def update_user(self, email: str, **updates: str) -> User | None:
        """Apply simple field updates to an existing user."""

        user = await self.get_by_email(email)
        if user is None:
            return None

        for field, value in updates.items():
            if hasattr(user, field):
                setattr(user, field, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user
