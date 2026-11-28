"""Property tests for inquiry submission idempotency and the one-Project-per-inquiry rule."""

from __future__ import annotations

import string
import uuid

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from sqlalchemy import event, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from core.config import Settings
from core.database import create_db_engine, create_session_factory, transaction
from models.base import Base
from models.phase1 import (
    INTERNAL_ORGANIZATION_ID,
    INTERNAL_ORGANIZATION_NAME,
    Organization,
    Project,
    ProjectInquiry,
)
from services.inquiries import InquiryReceipt, InquiryService, InquirySubmission
from services.leads import ConsentGrant

SETTINGS = Settings(inquiry_notification_recipients=["founder"])
_WORD = st.text(string.ascii_letters, min_size=1, max_size=12)


def _fresh_factory() -> tuple[object, sessionmaker[Session]]:
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
    return engine, factory


tokens = st.text(string.ascii_letters + string.digits + "_-.", min_size=16, max_size=64)


@st.composite
def submissions(draw: st.DrawFn, token: str) -> InquirySubmission:
    words = draw(st.lists(_WORD, min_size=4, max_size=10))
    problem = " ".join(words)
    if len(problem) < 20:
        problem = problem + " " + "x" * 20
    return InquirySubmission(
        submission_token=token,
        name=draw(_WORD),
        email=f"{draw(_WORD)}@{draw(_WORD)}.com",
        title=draw(_WORD),
        problem_description=problem,
        consents=(ConsentGrant("contact_and_processing", True, "v1"),),
    )


@st.composite
def delivery_plans(draw: st.DrawFn) -> list[InquirySubmission]:
    """1 to 3 distinct tokens, each delivered 1 to 5 times, in a random interleaving."""
    distinct = draw(st.lists(tokens, min_size=1, max_size=3, unique=True))
    deliveries: list[InquirySubmission] = []
    for token in distinct:
        sub = draw(submissions(token))
        deliveries.extend([sub] * draw(st.integers(min_value=1, max_value=5)))
    return draw(st.permutations(deliveries))


def _deliver(factory: sessionmaker[Session], plan: list[InquirySubmission]) -> list[InquiryReceipt]:
    receipts = []
    for sub in plan:
        with transaction(factory) as s:
            receipts.append(InquiryService(settings=SETTINGS).submit(s, sub, notify=False))
    return receipts


# Property 15: Idempotent inquiry submission
# Validates: Requirements 14.14
@settings(max_examples=100, deadline=None)
@given(plan=delivery_plans())
def test_repeated_token_stores_one_inquiry_and_project(plan: list[InquirySubmission]) -> None:
    engine, factory = _fresh_factory()
    try:
        receipts = _deliver(factory, plan)
        by_token: dict[str, list[InquiryReceipt]] = {}
        for sub, receipt in zip(plan, receipts, strict=True):
            by_token.setdefault(sub.submission_token, []).append(receipt)

        with transaction(factory) as s:
            for token, token_receipts in by_token.items():
                ids = {(r.project_inquiry_id, r.project_id) for r in token_receipts}
                assert len(ids) == 1
                assert sum(r.created for r in token_receipts) == 1
                assert token_receipts[0].created is True
                inquiry_ids = list(
                    s.scalars(
                        select(ProjectInquiry.id).where(ProjectInquiry.submission_token == token)
                    )
                )
                assert len(inquiry_ids) == 1
                project_count = s.scalar(
                    select(func.count())
                    .select_from(Project)
                    .where(Project.project_inquiry_id == inquiry_ids[0])
                )
                assert project_count == 1
            assert s.scalar(select(func.count()).select_from(ProjectInquiry)) == len(by_token)
            assert s.scalar(select(func.count()).select_from(Project)) == len(by_token)
    finally:
        engine.dispose()


# Property 8: One Project per inquiry
# Validates: Requirements 24.15
@settings(max_examples=100, deadline=None)
@given(plan=delivery_plans())
def test_each_inquiry_has_exactly_one_project(plan: list[InquirySubmission]) -> None:
    engine, factory = _fresh_factory()
    try:
        _deliver(factory, plan)
        with transaction(factory) as s:
            inquiry_ids = set(s.scalars(select(ProjectInquiry.id)))
            linked = list(s.scalars(select(Project.project_inquiry_id)))
            assert len(linked) == len(set(linked))
            assert set(linked) == inquiry_ids

        target = next(iter(inquiry_ids))
        with pytest.raises(IntegrityError), transaction(factory) as s:
            s.add(
                Project(
                    id=uuid.uuid4(),
                    organization_id=INTERNAL_ORGANIZATION_ID,
                    project_inquiry_id=target,
                    status="Submitted",
                )
            )
            s.flush()

        with transaction(factory) as s:
            assert s.scalar(select(func.count()).select_from(Project)) == len(inquiry_ids)
    finally:
        engine.dispose()
