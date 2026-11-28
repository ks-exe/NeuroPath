"""Public inquiry endpoints (R14.3, R14.7, R14.8, R14.9, R14.14).

``POST /public/inquiries/submission-token`` issues an opaque idempotency token.
``POST /public/inquiries`` stores Lead, Project_Inquiry and Project in one transaction and
notifies internal users after the commit. A replayed token returns 200 with the original ids.
"""

from __future__ import annotations

import secrets
from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session, sessionmaker

from api.rate_limit import SlidingWindowRateLimiter
from core.config import get_settings
from core.database import create_db_engine, create_session_factory, transaction
from core.errors import RATE_LIMITED, VALIDATION_FAILED, ApiError
from schemas.inquiries import InquiryIn, InquiryReceiptOut, SubmissionTokenOut
from services.inquiries import AI_CONSENT, InquiryService, InquirySubmission
from services.leads import CONTACT_CONSENT, ConsentGrant

router = APIRouter(prefix="/public/inquiries", tags=["public"])

RATE_LIMITER_STATE = "inquiry_rate_limiter"


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    """Lazily built from settings; tests override it through ``app.dependency_overrides``."""
    return create_session_factory(create_db_engine(get_settings().database_url))


def get_inquiry_service() -> InquiryService:
    return InquiryService()


def get_rate_limiter(request: Request) -> SlidingWindowRateLimiter:
    """One limiter per app instance, so a fresh ``create_app()`` starts with empty counts."""
    limiter = getattr(request.app.state, RATE_LIMITER_STATE, None)
    if limiter is None:
        settings = get_settings()
        limiter = SlidingWindowRateLimiter(
            settings.inquiry_rate_limit_max, settings.inquiry_rate_limit_window_seconds
        )
        setattr(request.app.state, RATE_LIMITER_STATE, limiter)
    return limiter


def enforce_rate_limit(
    request: Request, limiter: Annotated[SlidingWindowRateLimiter, Depends(get_rate_limiter)]
) -> None:
    # The direct peer address; X-Forwarded-For is not trusted (no trusted-proxy setting yet).
    client_ip = request.client.host if request.client else "unknown"
    retry_after = limiter.hit(client_ip)
    if retry_after is not None:
        raise ApiError(RATE_LIMITED, headers={"Retry-After": str(retry_after)})


@router.post("/submission-token", response_model=SubmissionTokenOut)
def issue_submission_token() -> SubmissionTokenOut:
    # 32 random bytes -> 43 URL-safe characters, within the 16 to 64 [A-Za-z0-9_-] rule.
    return SubmissionTokenOut(submission_token=secrets.token_urlsafe(32))


@router.post(
    "",
    response_model=InquiryReceiptOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(enforce_rate_limit)],
)
def submit_inquiry(
    body: InquiryIn,
    response: Response,
    factory: Annotated[sessionmaker[Session], Depends(get_session_factory)],
    service: Annotated[InquiryService, Depends(get_inquiry_service)],
) -> InquiryReceiptOut:
    if body.website:
        # Honeypot filled (R14.8): reject without naming the field; nothing is stored.
        raise ApiError(VALIDATION_FAILED)

    consents = [
        ConsentGrant(CONTACT_CONSENT, body.consent_contact, body.consent_wording_version),
        ConsentGrant(AI_CONSENT, body.consent_ai_processing, body.consent_wording_version),
    ]
    submission = InquirySubmission(
        submission_token=body.submission_token,
        name=body.name,
        email=body.email,
        title=body.title,
        problem_description=body.problem_description,
        consents=consents,
        company=body.company,
        desired_outcome=body.desired_outcome,
        existing_systems=body.existing_systems,
        data_and_integrations=body.data_and_integrations,
        expected_users=body.expected_users,
        constraints=body.constraints,
        budget_range=body.budget_range,
        preferred_timeline=body.preferred_timeline,
        service_hint=body.service_hint,
    )
    with transaction(factory) as session:
        receipt = service.submit(session, submission, notify=False)
    # Runs only after the commit, so a rolled-back inquiry never triggers a notification.
    service.notify_submitted(receipt, body.title)

    if not receipt.created:
        response.status_code = status.HTTP_200_OK
    return InquiryReceiptOut(
        project_inquiry_id=receipt.project_inquiry_id,
        project_id=receipt.project_id,
        status_label=receipt.status_label,
    )
