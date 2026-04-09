"""User ORM model."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base
from app.db.models.TimestampMixin import TimestampMixin


class User(TimestampMixin, Base):
    """Application user persisted by email primary key."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), primary_key=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
