"""Inquiry_Question status model (Appendix A.2.2)."""

from __future__ import annotations

from .types import (
    AGENT_RUNTIME,
    AUTHORIZED_REVIEWER,
    CLIENT_MEMBER,
    CLIENT_OWNER,
    NEW_RECORD,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "inquiry_question"

STATUSES: tuple[str, ...] = ("Draft", "Open", "Answered", "Withdrawn")
TERMINAL_STATUSES: frozenset[str] = frozenset({"Answered", "Withdrawn"})

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Draft", (AGENT_RUNTIME, "R67 workflow agent", AUTHORIZED_REVIEWER),
         ("linked_to_project_inquiry",), 3),
    rows(ENTITY, NEW_RECORD, "Open", (AUTHORIZED_REVIEWER,), ("reviewer_request_counts_as_approval",), 2),
    rows(ENTITY, "Draft", "Open", (AUTHORIZED_REVIEWER,),
         ("reviewer_approval_recorded_before_delivery", "guest_inquiry_invitation_accepted_or_founder_approved_email"), 3),
    rows(ENTITY, "Draft", "Withdrawn", (AUTHORIZED_REVIEWER,), (), 3),
    rows(ENTITY, "Open", "Answered", (CLIENT_OWNER, CLIENT_MEMBER),
         ("non_empty_answer_within_max_length", "question_belongs_to_client_organization"), 2),
    rows(ENTITY, "Open", "Withdrawn", (AUTHORIZED_REVIEWER,), (), 2),
)
