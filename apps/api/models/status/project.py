"""Project status model (Appendix A.1)."""

from __future__ import annotations

from dataclasses import dataclass

from .types import (
    ADMINISTRATOR,
    ASSIGNED_ENGINEER,
    AUTHORIZED_REVIEWER,
    CLIENT_MEMBER,
    CLIENT_OWNER,
    FOUNDER,
    NEW_RECORD,
    PRIOR_STATUS,
    PROJECT_LEAD,
    PROJECT_MANAGER,
    SYSTEM,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "project"


@dataclass(frozen=True)
class ProjectStatusInfo:
    status: str
    stage: str
    client_label: str
    phase_enabled: int  # first phase in which transitions into the status are enabled
    terminal: bool
    creation_phase: int | None = None  # set when creation precedes transitions (Submitted)


# A.1.1 Project statuses, in table order.
STATUS_INFO: tuple[ProjectStatusInfo, ...] = (
    ProjectStatusInfo("Draft", "Inquiry", "Draft, not yet sent", 2, False),
    ProjectStatusInfo("Submitted", "Inquiry", "Received", 2, False, creation_phase=1),
    ProjectStatusInfo("Under Review", "Inquiry", "Being reviewed", 2, False),
    ProjectStatusInfo("Awaiting Information", "Inquiry", "Waiting for your answers", 2, False),
    ProjectStatusInfo("Qualified", "Qualified project", "Selected for technical assessment", 2, False),
    ProjectStatusInfo("Assessment in Progress", "Qualified project", "Technical assessment underway", 2, False),
    ProjectStatusInfo("Solution Designed", "Qualified project", "Solution designed", 3, False),
    ProjectStatusInfo("Proposal Draft", "Proposal stage", "Preparing your proposal", 3, False),
    ProjectStatusInfo("Proposal Under Review", "Proposal stage", "Preparing your proposal", 3, False),
    ProjectStatusInfo("Proposal Sent", "Proposal stage", "Proposal sent", 3, False),
    ProjectStatusInfo("Awaiting Client Decision", "Proposal stage", "Proposal ready for your decision", 3, False),
    ProjectStatusInfo("Accepted", "Approved and accepted", "Proposal accepted, agreement in preparation", 3, False),
    ProjectStatusInfo("In Progress", "Active engagement", "Engineering underway", 4, False),
    ProjectStatusInfo("Testing", "Active engagement", "Testing", 4, False),
    ProjectStatusInfo("Awaiting Client Acceptance", "Active engagement", "Preparing handover", 4, False),
    ProjectStatusInfo("Delivered", "Active engagement", "Delivered, awaiting your acceptance", 4, False),
    ProjectStatusInfo("Completed", "Closed", "Completed", 4, True),
    ProjectStatusInfo("On Hold", "Paused", "Paused", 2, False),
    ProjectStatusInfo("Rejected", "Closed", "Not taken forward", 2, True),
    ProjectStatusInfo("Cancelled", "Closed", "Cancelled", 2, True),
)

STATUSES: tuple[str, ...] = tuple(i.status for i in STATUS_INFO)
STATUS_BY_NAME: dict[str, ProjectStatusInfo] = {i.status: i for i in STATUS_INFO}
CLIENT_LABELS: dict[str, str] = {i.status: i.client_label for i in STATUS_INFO}
TERMINAL_STATUSES: frozenset[str] = frozenset(i.status for i in STATUS_INFO if i.terminal)

# "Status order for R24.11 (precedes Accepted)". On Hold takes the position of its
# stored prior status (inferred), so it is not part of the order.
STATUS_ORDER: tuple[str, ...] = (
    "Draft",
    "Submitted",
    "Under Review",
    "Awaiting Information",
    "Qualified",
    "Assessment in Progress",
    "Solution Designed",
    "Proposal Draft",
    "Proposal Under Review",
    "Proposal Sent",
    "Awaiting Client Decision",
    "Accepted",
    "In Progress",
    "Testing",
    "Awaiting Client Acceptance",
    "Delivered",
    "Completed",
)

_ON_HOLD_EXCLUDED = {"Completed", "Rejected", "Cancelled", "On Hold"}
_T28_FROM = tuple(s for s in STATUSES if s not in _ON_HOLD_EXCLUDED)
_T30_FROM = (*STATUS_ORDER[: STATUS_ORDER.index("Awaiting Client Decision") + 1], "On Hold")
_T31_FROM = tuple(s for s in STATUSES if s not in {"Completed", "Rejected", "Cancelled"})

_REVIEWER = (AUTHORIZED_REVIEWER,)
_HUMAN_REVIEWER_GUARDS = ("human_principal_only",)


def _t28() -> tuple[TransitionRow, ...]:
    # Phase: 2, from each status once that status is enabled.
    return tuple(
        r
        for s in _T28_FROM
        for r in rows(
            ENTITY,
            s,
            "On Hold",
            (FOUNDER, ADMINISTRATOR, PROJECT_MANAGER),
            ("non_empty_reason", "store_prior_status_and_reason"),
            max(2, STATUS_BY_NAME[s].phase_enabled),
        )
    )


TRANSITIONS: tuple[TransitionRow, ...] = concat(
    # T01
    rows(ENTITY, NEW_RECORD, "Submitted", (SYSTEM,),
         ("inquiry_submission_valid_consent_honeypot_rate_limit", "submission_token_idempotent"), 1),
    # T02
    rows(ENTITY, NEW_RECORD, "Draft", (SYSTEM,), ("user_signed_in",), 3),
    # T03
    rows(ENTITY, "Draft", "Submitted", (CLIENT_OWNER, CLIENT_MEMBER),
         ("owning_organization_member", "inquiry_validation_and_consent"), 3),
    # T04
    rows(ENTITY, "Submitted", "Under Review", _REVIEWER, (), 2),
    # T05
    rows(ENTITY, "Under Review", "Awaiting Information", _REVIEWER,
         ("inquiry_questions_opened_in_same_request", "inquiry_questions_approved_from_phase_3"), 2),
    # T06
    rows(ENTITY, "Awaiting Information", "Under Review", (SYSTEM,),
         ("client_answered_last_open_inquiry_question",), 2),
    # T07
    rows(ENTITY, "Under Review", "Qualified", _REVIEWER, _HUMAN_REVIEWER_GUARDS, 2),
    # T08
    rows(ENTITY, "Under Review", "Rejected", _REVIEWER,
         (*_HUMAN_REVIEWER_GUARDS, "non_empty_reason_stored_with_decision"), 2),
    # T09
    rows(ENTITY, "Awaiting Information", "Rejected", _REVIEWER,
         (*_HUMAN_REVIEWER_GUARDS, "non_empty_reason_stored_with_decision"), 2),
    # T10
    rows(ENTITY, "Submitted", "Rejected", _REVIEWER,
         (*_HUMAN_REVIEWER_GUARDS, "non_empty_reason_stored_with_decision"), 2),
    # T11
    rows(ENTITY, "Qualified", "Assessment in Progress", (ASSIGNED_ENGINEER, FOUNDER),
         ("technical_assessment_created_in_same_request", "project_status_is_qualified"), 2),
    # T12
    rows(ENTITY, "Assessment in Progress", "Solution Designed", (ASSIGNED_ENGINEER, FOUNDER),
         ("confirmed_technical_assessment_version_exists", "confirmed_solution_architecture_version_exists"), 3),
    # T13
    rows(ENTITY, "Solution Designed", "Proposal Draft", (SYSTEM,),
         ("draft_proposal_version_exists", "proposal_architecture_references_confirmed_version"), 3),
    # T14
    rows(ENTITY, "Proposal Draft", "Proposal Under Review", (SYSTEM,),
         ("proposal_version_in_review",), 3),
    # T15
    rows(ENTITY, "Proposal Under Review", "Proposal Draft", (SYSTEM,),
         ("no_proposal_version_in_review_or_approved",), 3),
    # T16
    rows(ENTITY, "Proposal Under Review", "Proposal Sent", (SYSTEM,),
         ("proposal_version_approved", "approved_approval_request_hash_matches_proposal",
          "every_price_approved_by_authorized_approver"), 3),
    # T17
    rows(ENTITY, "Proposal Sent", "Awaiting Client Decision", (SYSTEM,), (), 3),
    # T18
    rows(ENTITY, "Awaiting Client Decision", "Accepted", (SYSTEM,),
         ("acceptance_record_exists_for_proposal_version", "no_earlier_accepted_version"), 3),
    # T19
    rows(ENTITY, "Awaiting Client Decision", "Proposal Draft", (SYSTEM,),
         ("decline_recorded_on_sent_version",), 3),
    # T20
    rows(ENTITY, "Accepted", "In Progress", (FOUNDER, PROJECT_MANAGER, ADMINISTRATOR),
         ("agreement_in_effect", "audit_log_on_guard_failure", "create_scope_baseline_v1_on_success"), 4),
    # T21
    rows(ENTITY, "In Progress", "Testing", (PROJECT_LEAD, FOUNDER), (), 4),
    # T22
    rows(ENTITY, "Testing", "In Progress", (PROJECT_LEAD, FOUNDER), (), 4),
    # T23
    rows(ENTITY, "Testing", "Awaiting Client Acceptance", (PROJECT_LEAD, PROJECT_MANAGER, FOUNDER),
         ("project_manager_is_current_project_member", "no_open_blocker_or_critical_defects",
          "all_milestone_acceptance_criteria_met"), 4),
    # T24
    rows(ENTITY, "Awaiting Client Acceptance", "Delivered", (PROJECT_LEAD, PROJECT_MANAGER, FOUNDER),
         ("project_manager_is_current_project_member", "all_mandatory_handover_items_done",
          "compute_delivery_reference_and_hash"), 4),
    # T25
    rows(ENTITY, "Delivered", "Completed", (SYSTEM,), ("final_acceptance_record_exists",), 4),
    # T26
    rows(ENTITY, "Delivered", "In Progress", (SYSTEM,), ("final_delivery_rejection_with_reason",), 4),
    # T27
    rows(ENTITY, "Delivered", "Testing", (SYSTEM,), ("final_delivery_rejection_with_reason",), 4),
    # T28
    _t28(),
    # T29
    rows(ENTITY, "On Hold", PRIOR_STATUS, _REVIEWER,
         ("target_equals_stored_prior_status", "target_enabled_in_current_phase"), 2),
    # T30
    rows(ENTITY, _T30_FROM, "Cancelled", (CLIENT_OWNER, CLIENT_MEMBER),
         ("owning_organization_member", "status_or_stored_prior_status_precedes_accepted"), 2),
    # T31
    rows(ENTITY, _T31_FROM, "Cancelled", (FOUNDER,), ("non_empty_reason",), 2),
    # T32 (Solution Designed source from Phase 3)
    rows(ENTITY, ("Qualified", "Assessment in Progress"), "Rejected", _REVIEWER,
         (*_HUMAN_REVIEWER_GUARDS, "non_empty_reason"), 2),
    rows(ENTITY, "Solution Designed", "Rejected", _REVIEWER,
         (*_HUMAN_REVIEWER_GUARDS, "non_empty_reason"), 3),
)
