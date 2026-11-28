"""Tests for the SQLAlchemy base, mixins, transactions and Alembic baseline (R6.2-R6.5)."""

import tempfile
import uuid
from pathlib import Path

import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import String, create_engine, event, inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column

from alembic import command
from core.database import create_db_engine, create_session_factory, transaction
from models import (
    INTERNAL_ORGANIZATION_ID,
    INTERNAL_ORGANIZATION_NAME,
    AuditLog,
    ConsentRecord,
    Lead,
    Organization,
    Project,
    ProjectInquiry,
)
from models.base import Base, IdMixin, TenantOwned, TimestampMixin

API_DIR = Path(__file__).resolve().parent.parent


class Widget(IdMixin, TimestampMixin, TenantOwned, Base):
    __tablename__ = "test_widgets"
    name: Mapped[str] = mapped_column(String(50), nullable=False)


def _engine():
    engine = create_db_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


def test_tenant_owned_column_is_not_null_and_indexed() -> None:
    table = Widget.__table__
    assert table.c.organization_id.nullable is False
    assert table.c.created_at.nullable is False
    assert table.c.updated_at.nullable is False
    names = {i.name for i in table.indexes}
    assert "ix_test_widgets_organization_id" in names
    assert table.primary_key.name == "pk_test_widgets"


def test_transaction_commits_on_success_and_rolls_back_on_error() -> None:
    engine = _engine()
    factory = create_session_factory(engine)
    org = uuid.uuid4()
    with transaction(factory) as s:
        s.add(Widget(organization_id=org, name="ok"))
    with pytest.raises(RuntimeError):
        with transaction(factory) as s:
            s.add(Widget(organization_id=org, name="lost"))
            s.flush()
            raise RuntimeError("boom")
    with transaction(factory) as s:
        names = list(s.scalars(select(Widget.name)))
        row = s.scalars(select(Widget)).one()
    assert names == ["ok"]
    assert row.created_at is not None and row.updated_at is not None
    assert inspect(engine).has_table("test_widgets")


PHASE1_TABLES = {
    "organizations",
    "leads",
    "consent_records",
    "project_inquiries",
    "projects",
    "audit_logs",
}


def _alembic_cfg(url: str) -> Config:
    cfg = Config(str(API_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(API_DIR / "alembic"))
    cfg.set_main_option("sqlalchemy.url", url)
    return cfg


def test_alembic_single_head_creates_phase1_tables_only() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        url = f"sqlite+pysqlite:///{(Path(tmp) / 'm.db').as_posix()}"
        cfg = _alembic_cfg(url)
        assert ScriptDirectory.from_config(cfg).get_heads() == ["0003_audit_append_only"]
        command.upgrade(cfg, "head")
        engine = create_engine(url)
        assert set(inspect(engine).get_table_names()) == PHASE1_TABLES | {"alembic_version"}
        command.downgrade(cfg, "base")
        assert inspect(engine).get_table_names() == ["alembic_version"]
        command.upgrade(cfg, "head")
        engine.dispose()


def test_phase1_migration_seeds_internal_org_and_enforces_constraints() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        url = f"sqlite+pysqlite:///{(Path(tmp) / 'm.db').as_posix()}"
        command.upgrade(_alembic_cfg(url), "head")
        engine = create_engine(url)

        @event.listens_for(engine, "connect")
        def _fk_on(dbapi_conn, _record):  # type: ignore[no-untyped-def]
            dbapi_conn.execute("PRAGMA foreign_keys=ON")

        factory = create_session_factory(engine)
        with transaction(factory) as s:
            org = s.scalars(select(Organization)).one()
        assert (org.id, org.name, org.kind) == (
            INTERNAL_ORGANIZATION_ID,
            INTERNAL_ORGANIZATION_NAME,
            "internal",
        )

        # A second internal Organization violates the partial unique index.
        with pytest.raises(IntegrityError):
            with transaction(factory) as s:
                s.add(Organization(name="other", kind="internal"))

        lead_id, inquiry_id = uuid.uuid4(), uuid.uuid4()
        with transaction(factory) as s:
            s.add(Lead(id=lead_id, name="Ada", email="a@x.io", email_normalized_hash="h" * 64))
            s.flush()
            s.add(
                ProjectInquiry(
                    id=inquiry_id,
                    organization_id=INTERNAL_ORGANIZATION_ID,
                    lead_id=lead_id,
                    submission_token="tok-1",
                    title="T",
                    problem_description="p" * 20,
                    entry_path="inquiry_form",
                )
            )
            s.flush()
            s.add(
                Project(
                    organization_id=INTERNAL_ORGANIZATION_ID,
                    project_inquiry_id=inquiry_id,
                    status="Submitted",
                )
            )
            s.add(
                ConsentRecord(
                    lead_id=lead_id,
                    project_inquiry_id=inquiry_id,
                    consent_type="ai_processing",
                    granted=True,
                    wording_version="v1",
                )
            )
            s.add(
                AuditLog(
                    actor_type="system", action="inquiry.submitted", resource_type="project_inquiry"
                )
            )

        # One Project per inquiry; status values are limited to Appendix A.1.
        for project in (
            Project(
                organization_id=INTERNAL_ORGANIZATION_ID,
                project_inquiry_id=inquiry_id,
                status="Submitted",
            ),
            Project(
                organization_id=INTERNAL_ORGANIZATION_ID,
                project_inquiry_id=uuid.uuid4(),
                status="Bogus",
            ),
            Project(
                organization_id=uuid.uuid4(), project_inquiry_id=inquiry_id, status="Submitted"
            ),
        ):
            with pytest.raises(IntegrityError):
                with transaction(factory) as s:
                    s.add(project)
        engine.dispose()
