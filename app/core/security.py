"""Reusable security validation helpers."""

from __future__ import annotations

import re


PASSWORD_MIN_LENGTH = 8
PASSWORD_UPPERCASE_PATTERN = re.compile(r"[A-Z]")
PASSWORD_LOWERCASE_PATTERN = re.compile(r"[a-z]")
PASSWORD_DIGIT_PATTERN = re.compile(r"\d")
PASSWORD_SPECIAL_PATTERN = re.compile(r"[^A-Za-z0-9]")


def normalize_email(value: object) -> str:
    """Normalize an email-like value for consistent validation and persistence."""

    return str(value).strip().lower()


def validate_password_strength(password: str) -> str:
    """Validate password strength and return the original password on success."""

    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"Password must be at least {PASSWORD_MIN_LENGTH} characters long.")
    if PASSWORD_UPPERCASE_PATTERN.search(password) is None:
        raise ValueError("Password must contain at least one uppercase letter.")
    if PASSWORD_LOWERCASE_PATTERN.search(password) is None:
        raise ValueError("Password must contain at least one lowercase letter.")
    if PASSWORD_DIGIT_PATTERN.search(password) is None:
        raise ValueError("Password must contain at least one number.")
    if PASSWORD_SPECIAL_PATTERN.search(password) is None:
        raise ValueError("Password must contain at least one special character.")
    return password
