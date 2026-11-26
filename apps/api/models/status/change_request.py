"""Change_Request status model (Appendix A.2.19)."""

from __future__ import annotations

from .types import (
    AUTHORIZED_APPROVER,
    CLIENT_MEMBER,
    CLIENT_OWNER,
    FOUNDER,
    NEW_RECORD,
    PROJECT_LEAD,
    PROJECT_MANAGER,
    SUBMITTER,
    SYSTEM,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "change_request"

STATUSES: tuple[str, ...] = ("Submitted", "Under Review", "Approved", "Rejected", "Withdrawn", "Implemented")

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Submitted", (CLIENT_OWNER, CLIENT_MEMBER, "Project_Member"),
         ("project_status_in_progress_testing_awaiting_client_acceptance_or_delivered",
          "description_reason_and_impacts_present", "internal_agent_request_403_and_audit"), 4),
    rows(ENTITY, "Submitted", "Under Review", (PROJECT_MANAGER, PROJECT_LEAD, FOUNDER), (), 4),
    # Approval roles depend on impact: without timeline or cost impact Founder or Project_Manager;
    # with impact Founder or a delegated Authorized_Approver (through R43).
    rows(ENTITY, "Under Review", "Approved", (FOUNDER, PROJECT_MANAGER, AUTHORIZED_APPROVER),
         ("roles_depend_on_timeline_or_cost_impact",
          "acceptance_record_for_change_request_content_hash",
          "approved_approval_request_with_equal_hash_when_timeline_or_cost_impact"), 4),
    rows(ENTITY, "Under Review", "Rejected", (FOUNDER, PROJECT_MANAGER, AUTHORIZED_APPROVER),
         ("roles_depend_on_timeline_or_cost_impact", "non_empty_reason"), 4),
    rows(ENTITY, ("Submitted", "Under Review"), "Withdrawn", (SUBMITTER, FOUNDER), (), 4),
    rows(ENTITY, "Approved", "Implemented", (SYSTEM,),
         ("requested_by_project_lead_member_project_manager_or_founder",
          "create_new_scope_baseline_version_referencing_change_request"), 4),
)
