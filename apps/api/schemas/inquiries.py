"""Request and response bodies for the public inquiry endpoints (R14.1, R14.3, R14.8).

Pydantic checks syntax only (presence, email shape, minimum problem length, consent). The
service's ``sanitize_submission`` applies the configured limits after sanitization.
"""

from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Syntactic email check (R14.3), same rule as services.inquiries.
EMAIL_PATTERN = r"^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$"
TOKEN_PATTERN = r"^[A-Za-z0-9_\-.]{16,64}$"
PROBLEM_MIN_LENGTH = 20


class SubmissionTokenOut(BaseModel):
    submission_token: str


class InquiryIn(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    submission_token: str = Field(pattern=TOKEN_PATTERN)
    name: str = Field(min_length=1)
    email: str = Field(pattern=EMAIL_PATTERN)
    company: str | None = None
    title: str = Field(min_length=1)
    problem_description: str = Field(min_length=PROBLEM_MIN_LENGTH)
    desired_outcome: str | None = None
    existing_systems: str | None = None
    data_and_integrations: str | None = None
    expected_users: str | None = None
    constraints: str | None = None
    budget_range: str | None = None
    preferred_timeline: str | None = None
    service_hint: str | None = None

    consent_contact: bool
    consent_ai_processing: bool = False
    consent_wording_version: str = Field(min_length=1, max_length=32)

    # Honeypot (R14.8): hidden in the form, so a human leaves it empty.
    website: str | None = None

    @field_validator("consent_contact")
    @classmethod
    def _consent_given(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Contact and processing consent is required.")
        return value


class InquiryReceiptOut(BaseModel):
    """Only ids and the client-facing status label; no personal data is echoed."""

    project_inquiry_id: uuid.UUID
    project_id: uuid.UUID
    status_label: str
