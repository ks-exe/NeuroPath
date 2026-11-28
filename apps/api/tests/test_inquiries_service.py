"""Tests for InquiryService.submit (R14.3, R14.9 to R14.12, R14.14, R24.1)."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterator

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.orm import Session, sessionmaker

from core.config import Settings
from core.database import create_db_engine, create_session_factory, transaction
from core.errors import VALIDATION_FAILED, ApiError
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
from services.inquiries import InquiryReceipt, InquiryService, InquirySubmission, sanitize_text
from services.leads import ConsentGrant

SETTINGS = Settings(inquiry_notification_recipients=["founder", "ops"])
TOKEN = "tok_0123456789abcdef"
SUBMITTER = "ada@example.com"


class RecordingNotifier:
    def __init__(self, fail: bool = False) -> None:
        self.calls: list[tuple[str, str, str]] = []
        self.fail = fail

    def notify(self, user_id: str, subject: str, body: str) -> None:
        self.calls.append((user_id, subject, body))
        if self.fail:
            raise RuntimeError("channel down")


@pytest.fixture
def factory() -> Iterator[sessionmaker[Session]]:
    engine = create_db_engine("sqlite+pysqlite:///:memory:")

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


def _submission(**overrides: object) -> InquirySubmission:
    base = InquirySubmission(
        submission_token=TOKEN,
        name=" Ada Lovelace ",
        email=" Ada@Example.com ",
        company="Acme",
        title="Forecast demand",
        problem_description="We need to forecast weekly demand\r\nacross 40 stores.\x00",
        expected_users="Planners\tand buyers",
        consents=(
            ConsentGrant("contact_and_processing", True, "v1"),
            ConsentGrant("ai_processing", True, "v1"),
        ),
    )
    return dataclasses.replace(base, **overrides)  # type: ignore[arg-type]


def _submit(factory, sub: InquirySubmission, notifier=None) -> InquiryReceipt:
    with transaction(factory) as s:
        return InquiryService(settings=SETTINGS).submit(
            s, sub, notifier=notifier or RecordingNotifier()
        )


def _counts(factory) -> dict[str, int]:
    with transaction(factory) as s:
        return {
            m.__name__: s.scalar(select(func.count()).select_from(m)) or 0
            for m in (Lead, ProjectInquiry, Project, ConsentRecord, AuditLog)
        }


def test_happy_path_writes_all_rows(factory) -> None:
    notifier = RecordingNotifier()
    receipt = _submit(factory, _submission(), notifier)
    assert receipt.created is True
    assert (receipt.status, receipt.status_label) == ("Submitted", "Received")

    with transaction(factory) as s:
        inquiry = s.get(ProjectInquiry, receipt.project_inquiry_id)
        project = s.get(Project, receipt.project_id)
        assert inquiry is not None and project is not None
        assert inquiry.organization_id == INTERNAL_ORGANIZATION_ID
        assert inquiry.entry_path == "inquiry_form"
        assert inquiry.problem_description == (
            "We need to forecast weekly demand\nacross 40 stores."
        )
        assert inquiry.expected_users == "Planners\tand buyers"
        assert project.status == "Submitted"
        assert project.project_inquiry_id == inquiry.id
        assert project.organization_id == INTERNAL_ORGANIZATION_ID
        lead = s.get(Lead, inquiry.lead_id)
        assert lead is not None and lead.email == SUBMITTER and lead.name == "Ada Lovelace"
        consents = list(s.scalars(select(ConsentRecord)))
        assert {(c.consent_type, c.granted, c.wording_version) for c in consents} == {
            ("contact_and_processing", True, "v1"),
            ("ai_processing", True, "v1"),
        }
        assert all(c.project_inquiry_id == inquiry.id for c in consents)
        actions = sorted(a.action for a in s.scalars(select(AuditLog)))
        assert actions == [
            "consent.recorded",
            "consent.recorded",
            "inquiry.submitted",
            "lead.created",
            "status_transition",
        ]
        transition_row = s.scalars(
            select(AuditLog).where(AuditLog.action == "status_transition")
        ).one()
        assert transition_row.resource_id == project.id
        assert transition_row.metadata_["to"] == "Submitted"

    # Internal recipients only; the submitter is never addressed (R14.12).
    assert [c[0] for c in notifier.calls] == ["founder", "ops"]
    assert all(SUBMITTER not in " ".join(c).lower() for c in notifier.calls)


def test_missing_ai_flag_is_recorded_as_not_granted(factory) -> None:
    _submit(factory, _submission(consents=(ConsentGrant("contact_and_processing", True, "v2"),)))
    with transaction(factory) as s:
        ai = s.scalars(
            select(ConsentRecord).where(ConsentRecord.consent_type == "ai_processing")
        ).one()
        assert (ai.granted, ai.wording_version) == (False, "v2")


def test_same_token_twice_returns_original_and_writes_nothing(factory) -> None:
    first = _submit(factory, _submission())
    before = _counts(factory)
    notifier = RecordingNotifier()
    second = _submit(factory, _submission(title="Different title"), notifier)
    assert second.created is False
    assert (second.project_inquiry_id, second.project_id) == (
        first.project_inquiry_id,
        first.project_id,
    )
    assert _counts(factory) == before
    assert notifier.calls == []


def test_concurrent_duplicate_token_recovers_via_savepoint(factory) -> None:
    first = _submit(factory, _submission())
    before = _counts(factory)

    class RacingService(InquiryService):
        """Misses the stored token on the first lookup, as a concurrent request would."""

        lookups = 0

        def _find_receipt(self, session, token):  # type: ignore[no-untyped-def]
            self.lookups += 1
            if self.lookups == 1:
                return None
            return super()._find_receipt(session, token)

    with transaction(factory) as s:
        receipt = RacingService(settings=SETTINGS).submit(
            s, _submission(), notifier=RecordingNotifier()
        )
    assert receipt.created is False
    assert receipt.project_inquiry_id == first.project_inquiry_id
    assert _counts(factory) == before


@pytest.mark.parametrize(
    ("overrides", "field"),
    [
        ({"problem_description": "too short"}, "problem_description"),
        ({"title": "   "}, "title"),
        ({"consents": ()}, "consents"),
        ({"consents": (ConsentGrant("contact_and_processing", False, "v1"),)}, "consents"),
        ({"title": "x" * 201}, "title"),
        ({"problem_description": "x" * 5001}, "problem_description"),
        ({"email": "not-an-email"}, "email"),
        ({"submission_token": "short"}, "submission_token"),
    ],
)
def test_validation_failures_write_nothing(factory, overrides, field) -> None:
    before = _counts(factory)
    with pytest.raises(ApiError) as exc:
        _submit(factory, _submission(**overrides))
    assert exc.value.code == VALIDATION_FAILED
    assert field in {f for f, _ in exc.value.fields}
    assert _counts(factory) == before


def test_notifier_failure_does_not_fail_submission(factory) -> None:
    notifier = RecordingNotifier(fail=True)
    receipt = _submit(factory, _submission(), notifier)
    assert receipt.created is True
    assert len(notifier.calls) == 2  # each recipient attempted despite the failure
    assert _counts(factory)["ProjectInquiry"] == 1


def test_sanitize_text() -> None:
    assert sanitize_text(" a\x07b\r\nc\td ", multiline=True) == "ab\nc\td"
    assert sanitize_text("a\nb\tc\x1b", multiline=False) == "a b c"
    assert sanitize_text(" \x00 ", multiline=False) is None
    assert sanitize_text(None, multiline=True) is None
