"""HTTP tests for the public inquiry endpoints (R14.3, R14.7, R14.8, R14.9, R14.14)."""

from __future__ import annotations

import uuid
from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from api.main import create_app
from api.public_inquiries import get_session_factory
from api.rate_limit import SlidingWindowRateLimiter
from core.database import create_session_factory, transaction
from models.base import Base
from models.phase1 import (
    INTERNAL_ORGANIZATION_ID,
    INTERNAL_ORGANIZATION_NAME,
    Lead,
    Organization,
    Project,
    ProjectInquiry,
)

URL = "/api/v1/public/inquiries"


@pytest.fixture
def factory() -> Iterator[sessionmaker[Session]]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def _fk_on(dbapi_conn, _record):  # type: ignore[no-untyped-def]
        dbapi_conn.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    factory = create_session_factory(engine)
    with transaction(factory) as s:
        s.add(
            Organization(
                id=INTERNAL_ORGANIZATION_ID, name=INTERNAL_ORGANIZATION_NAME, kind="internal"
            )
        )
    yield factory
    engine.dispose()


@pytest.fixture
def client(factory: sessionmaker[Session]) -> Iterator[TestClient]:
    app = create_app()
    app.dependency_overrides[get_session_factory] = lambda: factory
    with TestClient(app) as c:
        yield c


def _token(client: TestClient) -> str:
    response = client.post(f"{URL}/submission-token")
    assert response.status_code == 200
    return str(response.json()["submission_token"])


def _body(token: str, **overrides: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "submission_token": token,
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "title": "Forecast demand",
        "problem_description": "We need to forecast weekly demand across 40 stores.",
        "consent_contact": True,
        "consent_ai_processing": False,
        "consent_wording_version": "v1",
    }
    body.update(overrides)
    return body


def _counts(factory: sessionmaker[Session]) -> tuple[int, int, int]:
    with transaction(factory) as s:
        return tuple(  # type: ignore[return-value]
            s.scalar(select(func.count()).select_from(m)) for m in (Lead, ProjectInquiry, Project)
        )


def test_submission_token_endpoint(client: TestClient) -> None:
    first, second = _token(client), _token(client)
    assert first != second
    assert 16 <= len(first) <= 64


def test_happy_path_creates_records(client: TestClient, factory: sessionmaker[Session]) -> None:
    response = client.post(URL, json=_body(_token(client)))
    assert response.status_code == 201
    data = response.json()
    assert set(data) == {"project_inquiry_id", "project_id", "status_label"}
    assert "x-request-id" in response.headers
    assert _counts(factory) == (1, 1, 1)
    with transaction(factory) as s:
        project = s.get(Project, uuid.UUID(data["project_id"]))
        assert project is not None
        assert project.status == "Submitted"


def test_same_token_twice_returns_original_receipt(
    client: TestClient, factory: sessionmaker[Session]
) -> None:
    token = _token(client)
    first = client.post(URL, json=_body(token))
    second = client.post(URL, json=_body(token))
    assert first.status_code == 201
    assert second.status_code == 200
    assert second.json() == first.json()
    assert _counts(factory) == (1, 1, 1)


@pytest.mark.parametrize(
    ("overrides", "field"),
    [
        ({"email": "not-an-email"}, "body.email"),
        ({"problem_description": "too short"}, "body.problem_description"),
        ({"consent_contact": False}, "body.consent_contact"),
    ],
)
def test_invalid_input_returns_422_envelope(
    client: TestClient, factory: sessionmaker[Session], overrides: dict[str, Any], field: str
) -> None:
    response = client.post(URL, json=_body(_token(client), **overrides))
    assert response.status_code == 422
    data = response.json()
    assert data["code"] == "validation_failed"
    assert field in {f["field"] for f in data["fields"]}
    assert data["request_id"] == response.headers["x-request-id"]
    assert _counts(factory) == (0, 0, 0)


def test_missing_consent_returns_422(client: TestClient) -> None:
    body = _body(_token(client))
    del body["consent_contact"]
    response = client.post(URL, json=body)
    assert response.status_code == 422
    assert response.json()["code"] == "validation_failed"


def test_honeypot_rejected_without_storing(
    client: TestClient, factory: sessionmaker[Session]
) -> None:
    response = client.post(URL, json=_body(_token(client), website="http://spam.example"))
    assert response.status_code == 422
    data = response.json()
    assert data["code"] == "validation_failed"
    assert data["fields"] == []
    assert _counts(factory) == (0, 0, 0)


def test_sixth_request_in_window_is_rate_limited(
    client: TestClient, factory: sessionmaker[Session]
) -> None:
    for _ in range(5):
        assert client.post(URL, json=_body(_token(client))).status_code == 201
    response = client.post(URL, json=_body(_token(client)))
    assert response.status_code == 429
    assert int(response.headers["retry-after"]) >= 1
    data = response.json()
    assert data["code"] == "rate_limited"
    assert data["request_id"] == response.headers["x-request-id"]
    assert _counts(factory)[1] == 5


def test_rate_limiter_window_slides() -> None:
    now = [0.0]
    limiter = SlidingWindowRateLimiter(2, 600, clock=lambda: now[0])
    assert limiter.hit("ip") is None
    now[0] = 100.0
    assert limiter.hit("ip") is None
    assert limiter.hit("ip") == 500
    assert limiter.hit("other") is None
    now[0] = 600.0
    assert limiter.hit("ip") is None
    limiter.reset()
    assert limiter.hit("ip") is None
