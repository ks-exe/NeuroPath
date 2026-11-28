"""Tests for the AuditService write path (R6.9, R8.4, R30.1, R30.3 to R30.5)."""

from __future__ import annotations

import os
import uuid
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest
from alembic.config import Config
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session, sessionmaker

from alembic import command
from core.database import create_db_engine, create_session_factory, transaction
from core.errors import AUDIT_WRITE_FAILED, ApiError
from core.logging import request_id_var
from models import AuditLog, Organization
from models.base import Base
from repositories.audit_log import AuditLogRepository
from services.audit import (
    REDACTED,
    STATUS_TRANSITION_ACTION,
    AuditService,
    redact,
    transition_audit_hook,
)
from services.transitions import transition

API_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def factory() -> Iterator[sessionmaker[Session]]:
    engine = create_db_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield create_session_factory(engine)
    engine.dispose()


@pytest.fixture
def request_id() -> Iterator[str]:
    token = request_id_var.set("req-audit-1")
    yield "req-audit-1"
    request_id_var.reset(token)


def _rows(factory: sessionmaker[Session]) -> list[AuditLog]:
    with transaction(factory) as s:
        return list(s.scalars(select(AuditLog)))


def test_record_writes_row_with_request_id_and_redacted_metadata(factory, request_id) -> None:
    actor, resource = uuid.uuid4(), uuid.uuid4()
    with transaction(factory) as s:
        AuditService().record(
            s,
            actor_type="user",
            actor_id=actor,
            action="lead.created",
            resource_type="lead",
            resource_id=resource,
            organization_id=None,
            metadata={
                "email_domain": "example.com",
                "Password": "hunter2",
                "nested": {"api-key": "k", "items": [{"access_token": "t", "n": 1}]},
                "note": "x" * 2000,
            },
        )
    [row] = _rows(factory)
    assert (row.actor_type, row.actor_id, row.action) == ("user", actor, "lead.created")
    assert (row.resource_type, row.resource_id, row.organization_id) == ("lead", resource, None)
    assert row.request_id == request_id and row.created_at is not None
    meta = row.metadata_
    assert meta["email_domain"] == "example.com"
    assert meta["Password"] == REDACTED
    assert meta["nested"]["api-key"] == REDACTED
    assert meta["nested"]["items"] == [{"access_token": REDACTED, "n": 1}]
    assert len(meta["note"]) < 600 and meta["note"].endswith("[truncated]")
    assert "hunter2" not in str(meta)


def test_redact_masks_card_and_iban_and_keeps_scalars() -> None:
    out = redact({"card_number": "4111", "IBAN": "FR76", "count": 3, "ok": True, "x": None})
    assert out == {"card_number": REDACTED, "IBAN": REDACTED, "count": 3, "ok": True, "x": None}


def test_audit_failure_rolls_back_whole_transaction(factory, monkeypatch) -> None:
    def boom(self: Session, *a: Any, **k: Any) -> None:
        raise DBAPIError("INSERT", {}, Exception("disk full"))

    with pytest.raises(ApiError) as info:
        with transaction(factory) as s:
            s.add(Organization(name="Acme", kind="client"))
            monkeypatch.setattr(Session, "flush", boom)
            AuditService().record(
                s,
                actor_type="system",
                actor_id=None,
                action="org.created",
                resource_type="organization",
                resource_id=None,
                organization_id=None,
            )
    monkeypatch.undo()
    assert info.value.code == AUDIT_WRITE_FAILED and info.value.status == 500
    with transaction(factory) as s:
        assert s.scalars(select(Organization)).all() == []
        assert s.scalars(select(AuditLog)).all() == []


def test_invalid_actor_type_is_audit_write_failure(factory) -> None:
    with pytest.raises(ApiError) as info:
        with transaction(factory) as s:
            AuditService().record(
                s, actor_type="robot", actor_id=None, action="a", resource_type="r",
                resource_id=None, organization_id=None,
            )
    assert info.value.code == AUDIT_WRITE_FAILED
    assert _rows(factory) == []


def test_repository_exposes_insert_and_read_only() -> None:
    public = {n for n in dir(AuditLogRepository) if not n.startswith("_")}
    assert public == {"insert", "get", "list_for_organization", "list_for_resource"}


def test_repository_reads(factory) -> None:
    repo, org, res = AuditLogRepository(), None, uuid.uuid4()
    with transaction(factory) as s:
        row = repo.insert(
            s, actor_type="system", actor_id=None, action="a", resource_type="project",
            resource_id=res, organization_id=org, request_id=None, metadata={},
        )
        rid = row.id
    with transaction(factory) as s:
        assert repo.get(s, rid) is not None
        assert [r.id for r in repo.list_for_resource(s, "project", res)] == [rid]


@dataclass
class _Entity:
    entity_type: str
    status: str | None
    prior_status: str | None = None
    facts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class _Principal:
    roles: frozenset[str]
    is_human: bool = True
    id: uuid.UUID | None = None


def test_transition_hook_writes_one_row_on_accept_and_none_on_reject(factory) -> None:
    user_id, project_id = uuid.uuid4(), uuid.uuid4()
    founder = _Principal(frozenset({"Founder"}), id=user_id)
    with transaction(factory) as s:
        hook = transition_audit_hook(s, resource_id=project_id, organization_id=None)
        rejected = transition(
            _Entity("project", "On Hold", prior_status="Under Review"),
            "Cancelled", founder, "  ", audit_hook=hook, platform_phase=2,
        )
        accepted = transition(
            _Entity("project", "On Hold", prior_status="Under Review"),
            "Cancelled", founder, "client withdrew", audit_hook=hook, platform_phase=2,
        )
    assert not rejected.accepted and accepted.accepted
    [row] = _rows(factory)
    assert (row.actor_type, row.actor_id) == ("user", user_id)
    assert (row.action, row.resource_type, row.resource_id) == (
        STATUS_TRANSITION_ACTION, "project", project_id,
    )
    assert row.metadata_ == {
        "entity": "project", "from": "On Hold", "to": "Cancelled", "reason": "client withdrew",
    }


def test_transition_hook_without_principal_id_is_system(factory) -> None:
    with transaction(factory) as s:
        hook = transition_audit_hook(s, resource_id=None, organization_id=None)
        res = transition(
            _Entity("project", "On Hold", prior_status="Under Review"), "Cancelled",
            _Principal(frozenset({"Founder"})), "r", audit_hook=hook, platform_phase=2,
        )
    assert res.accepted
    [row] = _rows(factory)
    assert (row.actor_type, row.actor_id) == ("system", None)


@pytest.mark.skipif(
    not os.environ.get("TEST_POSTGRES_URL"),
    reason="TEST_POSTGRES_URL not set (Compose PostgreSQL required)",
)
def test_postgres_trigger_rejects_update_and_delete() -> None:
    base = create_engine(os.environ["TEST_POSTGRES_URL"], isolation_level="AUTOCOMMIT")
    name = "audit_" + uuid.uuid4().hex[:12]
    with base.connect() as conn:
        conn.execute(text(f'CREATE DATABASE "{name}"'))
    url = base.url.set(database=name).render_as_string(hide_password=False)
    try:
        cfg = Config(str(API_DIR / "alembic.ini"))
        cfg.set_main_option("script_location", str(API_DIR / "alembic"))
        cfg.set_main_option("sqlalchemy.url", url)
        command.upgrade(cfg, "head")
        engine = create_engine(url)
        factory = create_session_factory(engine)
        with transaction(factory) as s:
            AuditService().record(
                s, actor_type="system", actor_id=None, action="a", resource_type="r",
                resource_id=None, organization_id=None,
            )
        for stmt in ("UPDATE audit_logs SET action = 'b'", "DELETE FROM audit_logs"):
            with pytest.raises(DBAPIError, match="append-only"):
                with engine.begin() as conn:
                    conn.execute(text(stmt))
        with engine.connect() as conn:
            assert conn.execute(text("SELECT action FROM audit_logs")).scalars().all() == ["a"]
        engine.dispose()
    finally:
        with base.connect() as conn:
            conn.execute(text(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))
        base.dispose()
