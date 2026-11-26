"""Approval_Request status model (Appendix A.2.9)."""

from __future__ import annotations

from .types import (
    AUTHORIZED_APPROVER,
    ENGINEER,
    FOUNDER,
    INTERNAL_AGENT,
    NEW_RECORD,
    PROJECT_MANAGER,
    SYSTEM,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "approval_request"

STATUSES: tuple[str, ...] = ("Pending", "Approved", "Rejected", "Expired", "Invalidated")
TERMINAL_STATUSES: frozenset[str] = frozenset({"Rejected", "Expired", "Invalidated"})

_HUMAN_APPROVER_GUARD = ("human_principal_only_else_403_and_audit",)

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Pending", (ENGINEER, PROJECT_MANAGER, FOUNDER, INTERNAL_AGENT + " (requester only)"),
         ("action_type_target_content_hash_requester_rationale_present",), 3),
    rows(ENTITY, "Pending", "Approved", (AUTHORIZED_APPROVER,), _HUMAN_APPROVER_GUARD, 3),
    rows(ENTITY, "Pending", "Rejected", (AUTHORIZED_APPROVER,),
         (*_HUMAN_APPROVER_GUARD, "non_empty_reason"), 3),
    rows(ENTITY, "Pending", "Expired", (SYSTEM,), ("configured_expiry_period_reached",), 3),
    rows(ENTITY, "Approved", "Invalidated", (SYSTEM,), ("content_or_parameters_changed_before_execution",), 3),
    rows(ENTITY, "Pending", "Invalidated", (SYSTEM,), ("content_or_parameters_changed_while_pending",), 3),
)
