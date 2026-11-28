"""InquiryService.submit: public Project_Inquiry intake (R14.3, R14.9 to R14.12, R14.14, R24.1).

``submit`` runs in the caller's transaction and writes, in order: the Lead (LeadService),
the Project_Inquiry, the Project created by transition T01 (NEW_RECORD -> Submitted), the
consent rows, and the ``inquiry.submitted`` audit entry. A repeated submission token returns
the original receipt and writes nothing (R14.14).

Honeypot and rate-limit checks belong to the HTTP layer and run before ``submit``; the T01
guard fact for them is therefore asserted here once field validation has passed.
"""

from __future__ import annotations

import logging
import re
import unicodedata
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.config import Settings, get_settings
from core.email import normalize_email
from core.errors import INTERNAL_ERROR, VALIDATION_FAILED, ApiError
from core.integrations.interfaces import NotificationChannel
from core.integrations.local import LogNotificationChannel
from models.phase1 import (
    ENTRY_PATHS,
    INTERNAL_ORGANIZATION_ID,
    Project,
    ProjectInquiry,
)
from models.status import project as project_status
from models.status.types import SYSTEM

from .audit import AuditService, transition_audit_hook
from .leads import CONTACT_CONSENT, ConsentGrant, LeadService
from .transitions import transition

logger = logging.getLogger(__name__)

AI_CONSENT = "ai_processing"
SUBMITTED = "Submitted"
INQUIRY_SUBMITTED_ACTION = "inquiry.submitted"
T01_GUARD_FACTS = {
    "inquiry_submission_valid_consent_honeypot_rate_limit": True,
    "submission_token_idempotent": True,
}

# Token issued by POST /public/inquiries/submission-token (part 2); opaque to this service.
_TOKEN_RE = re.compile(r"^[A-Za-z0-9_\-.]{16,64}$")
# Syntactic check only (R14.3): one "@", non-empty local part, dotted domain, no spaces.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$")

SHORT_FIELDS: tuple[str, ...] = (
    "name",
    "email",
    "company",
    "title",
    "budget_range",
    "preferred_timeline",
    "service_hint",
)
LONG_FIELDS: tuple[str, ...] = (
    "problem_description",
    "desired_outcome",
    "existing_systems",
    "data_and_integrations",
    "expected_users",
    "constraints",
)
REQUIRED_FIELDS: tuple[str, ...] = ("name", "email", "title", "problem_description")


@dataclass(frozen=True)
class InquirySubmission:
    """The R14.1 form fields plus the idempotency token and consents."""

    submission_token: str
    name: str
    email: str
    title: str
    problem_description: str
    consents: Sequence[ConsentGrant] = ()
    company: str | None = None
    desired_outcome: str | None = None
    existing_systems: str | None = None
    data_and_integrations: str | None = None
    expected_users: str | None = None
    constraints: str | None = None
    budget_range: str | None = None
    preferred_timeline: str | None = None
    service_hint: str | None = None
    entry_path: str = "inquiry_form"


@dataclass(frozen=True)
class InquiryReceipt:
    project_inquiry_id: uuid.UUID
    project_id: uuid.UUID
    status: str
    status_label: str
    created: bool


@dataclass
class _SystemPrincipal:
    """T01 is allowed for the System role only; Guest submissions run as the system."""

    roles: frozenset[str] = frozenset({SYSTEM})
    is_human: bool = False
    actor_type: str = "system"


@dataclass
class _NewProject:
    """Transitionable view of a Project that does not exist yet (status None = NEW_RECORD)."""

    entity_type: str = project_status.ENTITY
    status: str | None = None
    prior_status: str | None = None
    facts: Mapping[str, Any] = field(default_factory=lambda: dict(T01_GUARD_FACTS))


def sanitize_text(value: str | None, *, multiline: bool) -> str | None:
    """Remove control characters (keeping newline and tab when ``multiline``), trim.

    Returns None for a missing or blank value. Line endings are normalised to ``\\n``.
    """
    if value is None:
        return None
    text = value.replace("\r\n", "\n").replace("\r", "\n")
    out: list[str] = []
    for ch in text:
        if ch in "\n\t":
            out.append(ch if multiline else " ")
        elif unicodedata.category(ch) != "Cc":
            out.append(ch)
    text = "".join(out).strip()
    return text or None


def sanitize_submission(
    submission: InquirySubmission, settings: Settings | None = None
) -> dict[str, str | None]:
    """Sanitize and validate every field; raise validation_failed listing all field errors."""
    cfg = settings or get_settings()
    errors: list[tuple[str, str]] = []
    clean: dict[str, str | None] = {}

    for name in SHORT_FIELDS + LONG_FIELDS:
        multiline = name in LONG_FIELDS
        raw = getattr(submission, name)
        if raw is not None and not isinstance(raw, str):
            errors.append((name, "Must be text."))
            continue
        value = sanitize_text(raw, multiline=multiline)
        limit = cfg.inquiry_long_text_max_length if multiline else cfg.inquiry_short_text_max_length
        if value is None and name in REQUIRED_FIELDS:
            errors.append((name, "This field is required."))
        elif value is not None and len(value) > limit:
            errors.append((name, f"Must be at most {limit} characters."))
        clean[name] = value

    email = clean.get("email")
    if email is not None:
        email = normalize_email(email)
        clean["email"] = email
        if not _EMAIL_RE.match(email):
            errors.append(("email", "A valid email is required."))

    problem = clean.get("problem_description")
    minimum = cfg.inquiry_problem_description_min_length
    if problem is not None and len(problem) < minimum:
        errors.append(("problem_description", f"Must be at least {minimum} characters."))

    if not isinstance(submission.submission_token, str) or not _TOKEN_RE.match(
        submission.submission_token
    ):
        errors.append(("submission_token", "A valid submission token is required."))
    if submission.entry_path not in ENTRY_PATHS:
        errors.append(("entry_path", "Unknown entry path."))
    if not any(c.consent_type == CONTACT_CONSENT and c.granted for c in submission.consents):
        errors.append(("consents", "Contact and processing consent is required."))

    if errors:
        raise ApiError(VALIDATION_FAILED, fields=errors)
    return clean


def _with_ai_flag(consents: Sequence[ConsentGrant]) -> list[ConsentGrant]:
    """Always record the AI-processing flag (R14.10); absent means not granted."""
    out = list(consents)
    if not any(c.consent_type == AI_CONSENT for c in out):
        contact = next(c for c in out if c.consent_type == CONTACT_CONSENT)
        out.append(ConsentGrant(AI_CONSENT, False, contact.wording_version))
    return out


class InquiryService:
    def __init__(
        self,
        *,
        leads: LeadService | None = None,
        audit: AuditService | None = None,
        settings: Settings | None = None,
    ) -> None:
        self._audit = audit or AuditService()
        self._leads = leads or LeadService(self._audit)
        self._settings = settings

    @property
    def settings(self) -> Settings:
        return self._settings or get_settings()

    def submit(
        self,
        session: Session,
        submission: InquirySubmission,
        *,
        notifier: NotificationChannel | None = None,
        notify: bool = True,
    ) -> InquiryReceipt:
        """Store the inquiry. ``notify=False`` lets the caller send the internal notification
        with ``notify_submitted`` after its transaction commits."""
        clean = sanitize_submission(submission, self.settings)
        token = submission.submission_token

        existing = self._find_receipt(session, token)
        if existing is not None:
            return existing

        consents = _with_ai_flag(submission.consents)
        savepoint = session.begin_nested()
        try:
            receipt = self._create(session, submission, clean, consents)
            savepoint.commit()
        except IntegrityError:
            # A concurrent request stored the same token between the lookup and the flush.
            savepoint.rollback()
            existing = self._find_receipt(session, token)
            if existing is None:
                raise
            return existing
        except BaseException:
            if savepoint.is_active:
                savepoint.rollback()
            raise

        if notify:
            self._notify(notifier or LogNotificationChannel(), receipt, clean["title"] or "")
        return receipt

    def notify_submitted(
        self,
        receipt: InquiryReceipt,
        title: str,
        *,
        notifier: NotificationChannel | None = None,
    ) -> None:
        """Notify internal users of a newly created inquiry; no-op for a replayed token."""
        if not receipt.created:
            return
        clean_title = sanitize_text(title, multiline=False) or ""
        self._notify(notifier or LogNotificationChannel(), receipt, clean_title)

    def _find_receipt(self, session: Session, token: str) -> InquiryReceipt | None:
        row = session.execute(
            select(ProjectInquiry.id, Project.id, Project.status)
            .join(Project, Project.project_inquiry_id == ProjectInquiry.id)
            .where(ProjectInquiry.submission_token == token)
        ).first()
        if row is None:
            return None
        inquiry_id, project_id, status = row
        return InquiryReceipt(
            inquiry_id, project_id, status, project_status.CLIENT_LABELS[status], False
        )

    def _create(
        self,
        session: Session,
        submission: InquirySubmission,
        clean: dict[str, str | None],
        consents: Sequence[ConsentGrant],
    ) -> InquiryReceipt:
        # Phase 1 has no client Organizations: every inquiry is owned by the internal one.
        org_id = INTERNAL_ORGANIZATION_ID
        inquiry_id = uuid.uuid4()
        project_id = uuid.uuid4()

        lead = self._leads.upsert_lead(
            session,
            name=clean["name"] or "",
            email=clean["email"] or "",
            company=clean["company"],
            consents=consents,
            project_inquiry_id=inquiry_id,
            organization_id=org_id,
        )

        inquiry = ProjectInquiry(
            id=inquiry_id,
            organization_id=org_id,
            lead_id=lead.id,
            submission_token=submission.submission_token,
            title=clean["title"],
            problem_description=clean["problem_description"],
            desired_outcome=clean["desired_outcome"],
            existing_systems=clean["existing_systems"],
            data_and_integrations=clean["data_and_integrations"],
            expected_users=clean["expected_users"],
            constraints=clean["constraints"],
            budget_range=clean["budget_range"],
            preferred_timeline=clean["preferred_timeline"],
            service_hint=clean["service_hint"],
            entry_path=submission.entry_path,
        )
        session.add(inquiry)
        session.flush()  # raises IntegrityError on a duplicate submission_token

        draft = _NewProject()
        result = transition(
            draft,
            SUBMITTED,
            _SystemPrincipal(),
            "Inquiry submitted",
            audit_hook=transition_audit_hook(
                session, resource_id=project_id, organization_id=org_id, service=self._audit
            ),
        )
        if not result.accepted or draft.status is None:
            logger.error("T01 rejected: %s", result.rejection)
            raise ApiError(INTERNAL_ERROR)
        session.add(
            Project(
                id=project_id,
                organization_id=org_id,
                project_inquiry_id=inquiry_id,
                status=draft.status,
            )
        )
        session.flush()

        self._leads.record_consents(
            session, lead, consents, project_inquiry_id=inquiry_id, organization_id=org_id
        )
        self._audit.record(
            session,
            actor_type="system",
            actor_id=None,
            action=INQUIRY_SUBMITTED_ACTION,
            resource_type="project_inquiry",
            resource_id=inquiry_id,
            organization_id=org_id,
            metadata={
                "project_id": project_id,
                "lead_id": lead.id,
                "entry_path": submission.entry_path,
            },
        )
        return InquiryReceipt(
            inquiry_id, project_id, draft.status, project_status.CLIENT_LABELS[draft.status], True
        )

    def _notify(self, notifier: NotificationChannel, receipt: InquiryReceipt, title: str) -> None:
        """Notify internal recipients only (R14.12). A failure never fails the submission."""
        subject = "New project inquiry"
        body = f"Project inquiry {receipt.project_inquiry_id}: {title}"
        for recipient in self.settings.inquiry_notification_recipients:
            try:
                notifier.notify(recipient, subject, body)
            except Exception as exc:
                logger.warning(
                    "inquiry notification failed",
                    extra={
                        "project_inquiry_id": str(receipt.project_inquiry_id),
                        "recipient": recipient,
                    },
                    exc_info=exc,
                )
