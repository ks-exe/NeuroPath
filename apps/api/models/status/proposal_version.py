"""Proposal_Version status model (Appendix A.2.8)."""

from __future__ import annotations

from .types import (
    AGENT_RUNTIME,
    ASSIGNED_ENGINEER,
    AUTHORIZED_APPROVER,
    DELEGATE,
    FOUNDER,
    NEW_RECORD,
    PROJECT_MANAGER,
    SYSTEM,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "proposal_version"

STATUSES: tuple[str, ...] = ("Draft", "In Review", "Approved", "Sent", "Superseded", "Withdrawn")
# A change to these versions is rejected (R36.10).
IMMUTABLE_STATUSES: frozenset[str] = frozenset({"Approved", "Sent", "Superseded", "Withdrawn"})

_FOUNDER_OR_DELEGATE = (FOUNDER, DELEGATE)

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Draft", (AGENT_RUNTIME, ASSIGNED_ENGINEER, PROJECT_MANAGER, FOUNDER),
         ("architecture_references_confirmed_solution_architecture_version_else_422",
          "preliminary_statement_present"), 3),
    rows(ENTITY, "Draft", "In Review", (ASSIGNED_ENGINEER, PROJECT_MANAGER, FOUNDER),
         ("all_r36_3_sections_present",), 3),
    rows(ENTITY, "In Review", "Draft", (ASSIGNED_ENGINEER, PROJECT_MANAGER, AUTHORIZED_APPROVER), (), 3),
    rows(ENTITY, "In Review", "Approved", (AUTHORIZED_APPROVER,),
         ("every_price_entered_or_approved_by_authorized_approver", "store_content_hash_and_freeze_content"), 3),
    rows(ENTITY, "Approved", "Sent", _FOUNDER_OR_DELEGATE,
         ("status_is_approved", "matching_approved_approval_request_else_403_and_audit"), 3),
    rows(ENTITY, "Sent", "Superseded", (SYSTEM,),
         ("another_version_of_same_proposal_sent_or_accepted",), 3),
    rows(ENTITY, "Approved", "Superseded", (SYSTEM,), ("later_version_of_same_proposal_sent",), 3),
    rows(ENTITY, ("Draft", "In Review", "Approved"), "Withdrawn", _FOUNDER_OR_DELEGATE,
         ("non_empty_reason",), 3),
    rows(ENTITY, "Sent", "Withdrawn", _FOUNDER_OR_DELEGATE,
         ("no_acceptance_record_on_version", "non_empty_reason"), 3),
)
