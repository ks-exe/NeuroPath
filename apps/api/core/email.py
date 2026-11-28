"""Email normalization for Lead matching (R22.4, R22.10)."""

from __future__ import annotations

import hashlib


def normalize_email(value: str) -> str:
    """Trim surrounding whitespace and lowercase (R22.4). Idempotent (R22.10)."""
    return value.strip().lower()


def email_hash(normalized: str) -> str:
    """SHA-256 hex digest of an already normalized email (``leads.email_normalized_hash``)."""
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
