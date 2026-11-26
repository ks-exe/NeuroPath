"""Tests for the SQLAlchemy base, mixins, transactions and Alembic baseline (R6.2-R6.5)."""

import tempfile
import uuid
from pathlib import Path

import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import String, create_engine, inspect, select
from sqlalchemy.orm import Mapped, mapped_column

from alembic import command
from core.database import create_db_engine, create_session_factory, transaction
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


def test_alembic_baseline_is_single_empty_head() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        cfg = Config(str(API_DIR / "alembic.ini"))
        cfg.set_main_option("script_location", str(API_DIR / "alembic"))
        url = f"sqlite+pysqlite:///{(Path(tmp) / 'm.db').as_posix()}"
        cfg.set_main_option("sqlalchemy.url", url)
        assert ScriptDirectory.from_config(cfg).get_heads() == ["0001_baseline"]
        command.upgrade(cfg, "head")
        engine = create_engine(url)
        assert inspect(engine).get_table_names() == ["alembic_version"]
        command.downgrade(cfg, "base")
        command.upgrade(cfg, "head")
        engine.dispose()
