"""Migration round-trip check (R6.7).

On an empty database: record the schema, run ``upgrade head`` then
``downgrade base``, and compare the reflected schema with the starting state.

Usage:
    python scripts/check_migrations.py [DATABASE_URL]

The URL defaults to ``Settings.database_url``. Exit code 0 means the schema
matched, 1 means it differed (a diff is printed) or the check could not run.
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
API_DIR = REPO_ROOT / "apps" / "api"

# Alembic's own bookkeeping table survives a downgrade (empty); ignore it.
IGNORED_TABLES = {"alembic_version"}


class NonEmptyDatabaseError(RuntimeError):
    """The target database already contains tables; refusing to touch it."""


def _ensure_api_on_path() -> None:
    if str(API_DIR) not in sys.path:
        sys.path.insert(0, str(API_DIR))


def reflect_schema(url: str) -> dict[str, Any]:
    """Return a JSON-serializable description of the database schema."""
    from sqlalchemy import create_engine, inspect

    engine = create_engine(url)
    try:
        insp = inspect(engine)
        schema: dict[str, Any] = {}
        for table in sorted(insp.get_table_names()):
            if table in IGNORED_TABLES:
                continue
            schema[table] = {
                "columns": [
                    {
                        "name": c["name"],
                        "type": str(c["type"]),
                        "nullable": c["nullable"],
                        "default": None if c.get("default") is None else str(c["default"]),
                    }
                    for c in sorted(insp.get_columns(table), key=lambda c: c["name"])
                ],
                "primary_key": insp.get_pk_constraint(table).get("constrained_columns", []),
                "foreign_keys": sorted(
                    json.dumps(
                        {
                            "columns": fk["constrained_columns"],
                            "referred_table": fk["referred_table"],
                            "referred_columns": fk["referred_columns"],
                        },
                        sort_keys=True,
                    )
                    for fk in insp.get_foreign_keys(table)
                ),
                "unique": sorted(
                    json.dumps(sorted(u["column_names"])) for u in insp.get_unique_constraints(table)
                ),
                "indexes": sorted(
                    json.dumps(
                        {
                            "name": i["name"],
                            "columns": i["column_names"],
                            "unique": bool(i.get("unique")),
                        },
                        sort_keys=True,
                    )
                    for i in insp.get_indexes(table)
                ),
            }
        # Non-table objects that migrations may create.
        schema["__views__"] = sorted(insp.get_view_names())
        return schema
    finally:
        engine.dispose()


def _has_user_objects(url: str) -> bool:
    from sqlalchemy import create_engine, inspect

    engine = create_engine(url)
    try:
        insp = inspect(engine)
        tables = set(insp.get_table_names()) - IGNORED_TABLES
        return bool(tables or insp.get_view_names())
    finally:
        engine.dispose()


def _alembic_config(url: str) -> Any:
    from alembic.config import Config

    cfg = Config()
    cfg.set_main_option("script_location", str(API_DIR / "alembic"))
    # '%' must be escaped for ConfigParser interpolation.
    cfg.set_main_option("sqlalchemy.url", url.replace("%", "%%"))
    return cfg


def diff_schemas(before: dict[str, Any], after: dict[str, Any]) -> str:
    """Return a unified diff of two schema snapshots ('' when equal)."""
    a = json.dumps(before, indent=2, sort_keys=True).splitlines()
    b = json.dumps(after, indent=2, sort_keys=True).splitlines()
    return "\n".join(
        difflib.unified_diff(a, b, "before upgrade", "after downgrade", lineterm="")
    )


def check_round_trip(url: str) -> str:
    """Run upgrade head / downgrade base on an empty database.

    Returns an empty string when the schema matches the starting state, or a
    diff otherwise. Raises NonEmptyDatabaseError if the database has tables.
    """
    _ensure_api_on_path()
    from alembic import command

    if _has_user_objects(url):
        raise NonEmptyDatabaseError(
            "Refusing to run: the target database is not empty. Use a fresh database."
        )

    before = reflect_schema(url)
    cfg = _alembic_config(url)
    command.upgrade(cfg, "head")
    command.downgrade(cfg, "base")
    after = reflect_schema(url)
    return diff_schemas(before, after)


CONNECT_TIMEOUT_SECONDS = 5


def probe_database(url: str) -> str | None:
    """Try a connection with a short timeout; return an error summary or None."""
    from sqlalchemy import create_engine, text

    engine = create_engine(url, connect_args=_connect_args(url))
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return None
    except Exception as exc:
        return str(exc).strip().splitlines()[0] if str(exc).strip() else type(exc).__name__
    finally:
        engine.dispose()


def _connect_args(url: str) -> dict[str, Any]:
    if url.startswith("sqlite"):
        return {}
    return {"connect_timeout": CONNECT_TIMEOUT_SECONDS}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migration upgrade/downgrade round-trip check")
    parser.add_argument("database_url", nargs="?", help="defaults to Settings.database_url")
    args = parser.parse_args(argv)

    _ensure_api_on_path()
    url = args.database_url
    if not url:
        from core.config import get_settings

        url = get_settings().database_url

    error = probe_database(url)
    if error:
        print(
            f"ERROR: database is unreachable ({error}). Start it, or pass an explicit "
            "URL, e.g. sqlite:///<path>.",
            file=sys.stderr,
        )
        return 1

    try:
        diff = check_round_trip(url)
    except NonEmptyDatabaseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # connection or migration failure
        print(f"ERROR: migration round trip failed: {exc}", file=sys.stderr)
        return 1

    if diff:
        print("Schema after downgrade differs from the starting state:")
        print(diff)
        return 1
    print("OK: upgrade head then downgrade base restores the starting schema.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
