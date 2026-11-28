"""Intake protections through the HTTP endpoint (R14.7, R14.8, R14.9, R14.10, R30.5)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from api.main import create_app
from api.public_inquiries import (
    RATE_LIMITER_STATE,
    get_inquiry_service,
    get_session_factory,
)
from api.rate_limit import SlidingWindowRateLimiter
from core.database import create_session_factory, transaction
from models.base import Base
from models.phase1 import (
    INTERNAL_ORGANIZATION_ID,
    INTERNAL_ORGANIZATION_NAME,
    AuditLog,
    ConsentRecord,
    Lead,
    Organization,
    Project,
    ProjectInquiry,
)
from repositories.audit_log import AuditLogRepository
from services.audit import AuditService
from services.inquiries import InquiryReceipt, InquiryService

URL = "/api/v1/public/inquiries"
MODELS = (Lead, ProjectInquiry, Project, ConsentRecord, AuditLog)


class RecordingService(InquiryService):
    """Real InquiryService that records each notification dispatch."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.notified: list[str] = []

    def _notify(self, notifier: Any, receipt: InquiryReceipt, title: str) -> None:
        self.notified.append(title)


class FailingAuditRepository(AuditLogRepository):
    def insert(self, *args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("audit store unavailable")


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
def service() -> RecordingService:
    return RecordingService()


@pytest.fixture
def app(factory: sessionmaker[Session], service: RecordingService) -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_session_factory] = lambda: factory
    app.dependency_overrides[get_inquiry_service] = lambda: service
    return app


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as c:
        yield c


def _token(client: TestClient) -> str:
    return str(client.post(f"{URL}/submission-token").json()["submission_token"])


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


def _counts(factory: sessionmaker[Session]) -> dict[str, int]:
    with transaction(factory) as s:
        return {m.__name__: s.scalar(select(func.count()).select_from(m)) or 0 for m in MODELS}


def _empty() -> dict[str, int]:
    return {m.__name__: 0 for m in MODELS}


def test_rate_limit_is_per_ip_and_window_reopens(app: FastAPI) -> None:
    now = [1000.0]
    setattr(
        app.state, RATE_LIMITER_STATE, SlidingWindowRateLimiter(2, 600, clock=lambda: now[0])
    )
    with (
        TestClient(app, client=("203.0.113.1", 5000)) as first,
        TestClient(app, client=("203.0.113.2", 5000)) as second,
    ):
        assert first.post(URL, json=_body(_token(first))).status_code == 201
        now[0] += 60
        assert first.post(URL, json=_body(_token(first))).status_code == 201
        limited = first.post(URL, json=_body(_token(first)))
        assert limited.status_code == 429
        retry_after = limited.headers["retry-after"]
        assert retry_after.isdigit() and 1 <= int(retry_after) <= 600
        assert int(retry_after) == 540  # first hit at t=1000 expires at t=1600

        # Another client IP has its own window.
        assert second.post(URL, json=_body(_token(second))).status_code == 201

        now[0] += 541
        assert first.post(URL, json=_body(_token(first))).status_code == 201


def test_honeypot_stores_nothing_and_sends_no_notification(
    client: TestClient, factory: sessionmaker[Session], service: RecordingService
) -> None:
    response = client.post(URL, json=_body(_token(client), website="http://spam.example"))
    assert response.status_code == 422
    assert _counts(factory) == _empty()
    assert service.notified == []


def test_accepted_submission_notifies_once(
    client: TestClient, service: RecordingService
) -> None:
    assert client.post(URL, json=_body(_token(client))).status_code == 201
    assert service.notified == ["Forecast demand"]


def test_control_characters_stripped_and_newlines_kept(
    client: TestClient, factory: sessionmaker[Session]
) -> None:
    body = _body(
        _token(client),
        title="Fore\x07cast\x1b demand",
        problem_description="Line one of the problem\x00\r\nline two\x08 of it",
    )
    response = client.post(URL, json=body)
    assert response.status_code == 201
    with transaction(factory) as s:
        inquiry = s.scalars(select(ProjectInquiry)).one()
        assert inquiry.title == "Forecast demand"
        assert inquiry.problem_description == "Line one of the problem\nline two of it"


@pytest.mark.parametrize(
    ("overrides", "field"),
    [
        ({"title": "x" * 201}, "title"),
        ({"problem_description": "x" * 5001}, "problem_description"),
    ],
)
def test_length_limits_return_422_with_field(
    client: TestClient, factory: sessionmaker[Session], overrides: dict[str, Any], field: str
) -> None:
    response = client.post(URL, json=_body(_token(client), **overrides))
    assert response.status_code == 422
    data = response.json()
    assert data["code"] == "validation_failed"
    names = {f["field"] for f in data["fields"]}
    assert field in names or f"body.{field}" in names
    assert _counts(factory) == _empty()


def test_consent_rows_stored_from_request(
    client: TestClient, factory: sessionmaker[Session]
) -> None:
    body = _body(_token(client), consent_ai_processing=True, consent_wording_version="2025-01")
    assert client.post(URL, json=body).status_code == 201
    with transaction(factory) as s:
        inquiry = s.scalars(select(ProjectInquiry)).one()
        rows = list(s.scalars(select(ConsentRecord)))
        assert {(r.consent_type, r.granted, r.wording_version) for r in rows} == {
            ("contact_and_processing", True, "2025-01"),
            ("ai_processing", True, "2025-01"),
        }
        assert all(r.project_inquiry_id == inquiry.id for r in rows)


def test_audit_failure_rolls_back_whole_submission(
    app: FastAPI, factory: sessionmaker[Session]
) -> None:
    failing = RecordingService(audit=AuditService(FailingAuditRepository()))
    app.dependency_overrides[get_inquiry_service] = lambda: failing
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.post(URL, json=_body(_token(client)))
    assert response.status_code == 500
    data = response.json()
    assert data["code"] == "audit_write_failed"
    assert data["request_id"] == response.headers["x-request-id"]
    assert _counts(factory) == _empty()
    assert failing.notified == []
