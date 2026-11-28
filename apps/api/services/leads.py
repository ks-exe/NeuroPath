"""LeadService Phase 1 path: create or link a Lead from an inquiry (R22.1, R22.4, R22.7)."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.email import email_hash, normalize_email
from core.errors import VALIDATION_FAILED, ApiError
from models.phase1 import CONSENT_TYPES, ConsentRecord, Lead

from .audit import AuditService

CONTACT_CONSENT = "contact_and_processing"


@dataclass(frozen=True)
class ConsentGrant:
    consent_type: str
    granted: bool
    wording_version: str


class LeadService:
    def __init__(self, audit: AuditService | None = None) -> None:
        self._audit = audit or AuditService()

    def upsert_from_inquiry(
        self,
        session: Session,
        *,
        name: str,
        email: str,
        company: str | None,
        consents: Sequence[ConsentGrant],
        project_inquiry_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Lead:
        """Create or link the submitter's Lead and append one ConsentRecord per consent.

        Runs in the caller's transaction. Guest submissions are audited with actor "system".
        """
        lead = self.upsert_lead(
            session,
            name=name,
            email=email,
            company=company,
            consents=consents,
            project_inquiry_id=project_inquiry_id,
            organization_id=organization_id,
        )
        self.record_consents(
            session,
            lead,
            consents,
            project_inquiry_id=project_inquiry_id,
            organization_id=organization_id,
        )
        return lead

    def upsert_lead(
        self,
        session: Session,
        *,
        name: str,
        email: str,
        company: str | None,
        consents: Sequence[ConsentGrant],
        project_inquiry_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Lead:
        """Validate, then create or link the Lead. Consents are validated, not written."""
        normalized = normalize_email(email)
        _validate(name, normalized, consents)
        digest = email_hash(normalized)

        # Several Leads may share a hash (no unique index). Phase 1 links to the oldest and
        # never merges; flagging and reviewed merge are the Phase 2 flow (R22.5, R22.6).
        lead = session.scalars(
            select(Lead)
            .where(Lead.email_normalized_hash == digest)
            .order_by(Lead.created_at, Lead.id)
            .limit(1)
        ).first()

        if lead is None:
            lead = Lead(
                name=name.strip(),
                email=normalized,
                company=(company.strip() or None) if company else None,
                email_normalized_hash=digest,
            )
            session.add(lead)
            session.flush()
            self._audit.record(
                session,
                actor_type="system",
                actor_id=None,
                action="lead.created",
                resource_type="lead",
                resource_id=lead.id,
                organization_id=organization_id,
                metadata={"project_inquiry_id": project_inquiry_id},
            )
        # An existing Lead keeps its name and company: the spec does not allow overwrite.
        return lead

    def record_consents(
        self,
        session: Session,
        lead: Lead,
        consents: Sequence[ConsentGrant],
        *,
        project_inquiry_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> None:
        """Append one ConsentRecord (and audit entry) per consent (R14.10)."""
        for consent in consents:
            record = ConsentRecord(
                lead_id=lead.id,
                organization_id=organization_id,
                project_inquiry_id=project_inquiry_id,
                consent_type=consent.consent_type,
                granted=consent.granted,
                wording_version=consent.wording_version,
            )
            session.add(record)
            session.flush()
            self._audit.record(
                session,
                actor_type="system",
                actor_id=None,
                action="consent.recorded",
                resource_type="consent_record",
                resource_id=record.id,
                organization_id=organization_id,
                metadata={
                    "lead_id": lead.id,
                    "consent_type": consent.consent_type,
                    "granted": consent.granted,
                    "wording_version": consent.wording_version,
                },
            )


def _validate(name: str, normalized: str, consents: Sequence[ConsentGrant]) -> None:
    fields: list[tuple[str, str]] = []
    if not name.strip():
        fields.append(("name", "Name is required."))
    if not normalized or "@" not in normalized:
        fields.append(("email", "A valid email is required."))
    seen: set[str] = set()
    for c in consents:
        if c.consent_type not in CONSENT_TYPES:
            fields.append(("consents", f"Unknown consent type {c.consent_type!r}."))
        elif c.consent_type in seen:
            fields.append(("consents", f"Duplicate consent type {c.consent_type!r}."))
        if not c.wording_version.strip():
            fields.append(("consents", "Consent wording version is required."))
        seen.add(c.consent_type)
    if not any(c.consent_type == CONTACT_CONSENT and c.granted for c in consents):
        fields.append(("consents", "Contact and processing consent is required."))
    if fields:
        raise ApiError(VALIDATION_FAILED, fields=fields)
