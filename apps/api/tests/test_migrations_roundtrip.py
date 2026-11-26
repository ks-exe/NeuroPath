"""Integration test: migration upgrade head / downgrade base round trip (R6.7)."""
import importlib.util
import os
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text

_SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "check_migrations.py"
_spec = importlib.util.spec_from_file_location("check_migrations", _SCRIPT)
cm = importlib.util.module_from_spec(_spec)
sys.modules["check_migrations"] = cm
_spec.loader.exec_module(cm)


@pytest.fixture
def sqlite_url():
    d = tempfile.mkdtemp()
    try:
        yield "sqlite:///" + (Path(d) / "roundtrip.db").as_posix()
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_round_trip_sqlite_has_empty_diff(sqlite_url):
    assert cm.check_round_trip(sqlite_url) == ""


def test_non_empty_database_is_rejected(sqlite_url):
    engine = create_engine(sqlite_url)
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE leftover (id INTEGER PRIMARY KEY)"))
    engine.dispose()
    with pytest.raises(cm.NonEmptyDatabaseError):
        cm.check_round_trip(sqlite_url)
    # The existing table must be untouched.
    assert "leftover" in cm.reflect_schema(sqlite_url)


def test_diff_schemas_reports_differences():
    before = {"__views__": []}
    after = {
        "__views__": [],
        "t": {
            "columns": [{"name": "id", "type": "INTEGER", "nullable": False, "default": None}],
            "primary_key": ["id"],
            "foreign_keys": [],
            "unique": [],
            "indexes": [],
        },
    }
    diff = cm.diff_schemas(before, after)
    assert diff != ""
    assert '"t"' in diff
    assert cm.diff_schemas(after, after) == ""


@pytest.mark.skipif(
    not os.environ.get("TEST_POSTGRES_URL"),
    reason="TEST_POSTGRES_URL not set (Compose PostgreSQL required)",
)
def test_round_trip_postgres_has_empty_diff():
    base = create_engine(os.environ["TEST_POSTGRES_URL"], isolation_level="AUTOCOMMIT")
    name = "rt_" + uuid.uuid4().hex[:12]
    with base.connect() as conn:
        conn.execute(text(f'CREATE DATABASE "{name}"'))
    fresh_url = base.url.set(database=name).render_as_string(hide_password=False)
    try:
        assert cm.check_round_trip(fresh_url) == ""
    finally:
        with base.connect() as conn:
            conn.execute(text(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))
        base.dispose()
