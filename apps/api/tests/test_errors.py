import json
import logging
import uuid

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.main import create_app
from core import errors
from core.logging import JsonFormatter, resolve_request_id


def _app() -> FastAPI:
    app = create_app()

    @app.get("/test/items/{item_id}")
    def item(item_id: int) -> dict[str, int]:
        return {"id": item_id}

    @app.get("/test/boom")
    def boom() -> None:
        raise RuntimeError("secret db password=hunter2")

    @app.get("/test/conflict")
    def conflict() -> None:
        raise errors.ApiError(
            errors.INVALID_TRANSITION, "Not allowed from Draft.", fields=[("status", "bad")]
        )

    return app


@pytest.fixture
def client() -> TestClient:
    return TestClient(_app(), raise_server_exceptions=False)


def test_safe_incoming_request_id_is_echoed(client: TestClient) -> None:
    r = client.get("/api/v1/health", headers={"X-Request-ID": "abc-123.x_y"})
    assert r.headers["X-Request-ID"] == "abc-123.x_y"


@pytest.mark.parametrize("bad", ["a" * 65, "has space", "inj\\nected", ""])
def test_unsafe_request_id_is_replaced(client: TestClient, bad: str) -> None:
    r = client.get("/api/v1/health", headers={"X-Request-ID": bad})
    assert r.headers["X-Request-ID"] != bad
    uuid.UUID(r.headers["X-Request-ID"], version=4)


def test_404_uses_envelope(client: TestClient) -> None:
    r = client.get("/api/v1/nope")
    assert r.status_code == 404
    body = r.json()
    assert body["code"] == "not_found"
    assert body["fields"] == []
    assert body["request_id"] == r.headers["X-Request-ID"]


def test_422_lists_fields(client: TestClient) -> None:
    r = client.get("/test/items/notanint")
    assert r.status_code == 422
    body = r.json()
    assert body["code"] == "validation_failed"
    assert [f["field"] for f in body["fields"]] == ["path.item_id"]
    assert body["request_id"] == r.headers["X-Request-ID"]


def test_500_is_generic_and_logged(client: TestClient, caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.ERROR, logger="api"):
        r = client.get("/test/boom", headers={"X-Request-ID": "req-500"})
    assert r.status_code == 500
    assert r.json() == {
        "code": "internal_error",
        "message": "An internal error occurred.",
        "fields": [],
        "request_id": "req-500",
    }
    assert "hunter2" not in r.text
    record = next(rec for rec in caplog.records if rec.exc_info)
    line = json.loads(JsonFormatter().format(record))
    assert line["request_id"] == "req-500"
    assert "RuntimeError" in line["exc_info"]


def test_api_error_maps_to_envelope(client: TestClient) -> None:
    r = client.get("/test/conflict")
    assert r.status_code == 409
    assert r.json()["code"] == "invalid_transition"
    assert r.json()["message"] == "Not allowed from Draft."
    assert r.json()["fields"] == [{"field": "status", "message": "bad"}]


def test_json_formatter_drops_sensitive_extras() -> None:
    record = logging.LogRecord("x", logging.INFO, "", 0, "hello", None, None)
    record.authorization = "Bearer t"
    record.cookie = "s=1"
    record.path = "/a"
    line = json.loads(JsonFormatter().format(record))
    assert line["message"] == "hello"
    assert line["path"] == "/a"
    assert "authorization" not in line and "cookie" not in line


def test_resolve_request_id_generates_uuid() -> None:
    uuid.UUID(resolve_request_id(None), version=4)
