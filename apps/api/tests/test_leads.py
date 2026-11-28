"""Tests for email normalization and Lead upsert (R22.1, R22.4, R22.7, R22.10)."""

from __future__ import annotations

import hashlib
from collections.abc import Iterator

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from core.database import create_db_engine, create_session_factory, transaction
from core.email import email_hash, normalize_email
from core.errors import VALIDATION_FAILED, ApiError
from models import AuditLog
from models.base import Base
from models.phase1 import ConsentRecord, Lead
from services.leads import ConsentGrant, LeadService

CONSENTS = [
    ConsentGrant("contact_and_processing", True, "v1"),
    ConsentGrant("ai_processing", False, "v1"),
]


@pytest.fixture
def factory() -> Iterator[sessionmaker[Session]]:
    engine = create_db_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield create_session_factory(engine)
    engine.dispose()


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("  Ada@Example.COM \t", "ada@example.com"),
        ("ada+tag@example.com", "ada+tag@example.com"),
        ("a.b@example.com", "a.b@example.com"),
    ],
)
def test_normalize_email(raw: str, expected: str) -> None:
    assert normalize_email(raw) == expected
    assert normalize_email(normalize_email(raw)) == expected


def test_email_hash_is_sha256_hex() -> None:
    assert email_hash("ada@example.com") == hashlib.sha256(b"ada@example.com").hexdigest()


def _upsert(s: Session, email: str, name: str = "Ada", consents=CONSENTS) -> Lead:
    return LeadService().upsert_from_inquiry(
        s, name=name, email=email, company="Acme", consents=consents
    )


def test_new_lead_created_with_hash_consents_and_audit(factory) -> None:
    with transaction(factory) as s:
        lead_id = _upsert(s, " Ada@Example.com ").id
    with transaction(factory) as s:
        lead = s.get(Lead, lead_id)
        assert lead is not None
        assert lead.email == "ada@example.com"
        assert lead.email_normalized_hash == email_hash("ada@example.com")
        consents = list(s.scalars(select(ConsentRecord)))
        assert {(c.consent_type, c.granted, c.wording_version) for c in consents} == {
            ("contact_and_processing", True, "v1"),
            ("ai_processing", False, "v1"),
        }
        assert all(c.lead_id == lead_id and c.recorded_at is not None for c in consents)
        actions = sorted(a.action for a in s.scalars(select(AuditLog)))
        assert actions == ["consent.recorded", "consent.recorded", "lead.created"]
        assert all(a.actor_type == "system" for a in s.scalars(select(AuditLog)))


def test_second_submission_links_same_lead_without_overwrite(factory) -> None:
    with transaction(factory) as s:
        first = _upsert(s, "ada@example.com").id
    with transaction(factory) as s:
        second = _upsert(s, "  ADA@example.COM", name="Someone Else").id
    assert first == second
    with transaction(factory) as s:
        assert len(list(s.scalars(select(Lead)))) == 1
        lead = s.get(Lead, first)
        assert lead is not None and lead.name == "Ada"
        assert len(list(s.scalars(select(ConsentRecord)))) == 4
        actions = [a.action for a in s.scalars(select(AuditLog))]
        assert actions.count("lead.created") == 1
        assert actions.count("consent.recorded") == 4


@pytest.mark.parametrize(
    "consents",
    [
        [ConsentGrant("ai_processing", True, "v1")],
        [ConsentGrant("contact_and_processing", False, "v1")],
        [],
    ],
)
def test_missing_contact_consent_rejected(factory, consents) -> None:
    with pytest.raises(ApiError) as exc, transaction(factory) as s:
        _upsert(s, "ada@example.com", consents=consents)
    assert exc.value.code == VALIDATION_FAILED
    with transaction(factory) as s:
        assert list(s.scalars(select(Lead))) == []
