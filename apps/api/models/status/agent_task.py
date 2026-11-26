"""Agent_Task status model (Appendix A.2.24)."""

from __future__ import annotations

from .types import FOUNDER, NEW_RECORD, SYSTEM, TransitionRow, concat, rows

ENTITY = "agent_task"

STATUSES: tuple[str, ...] = ("Queued", "Running", "Succeeded", "Failed", "Awaiting Approval", "Cancelled")

# agent_tasks is created in Phase 5 (Appendix B).
TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Queued", ("Orchestrator Internal_Agent", SYSTEM, FOUNDER),
         ("per_day_agent_cost_limit_not_reached",), 5),
    rows(ENTITY, "Queued", "Running", (SYSTEM,),
         ("no_other_agent_task_running", "per_day_cost_limit_checked_before_start"), 5),
    rows(ENTITY, "Running", "Succeeded", (SYSTEM,), ("output_validates_against_agent_output_schema",), 5),
    rows(ENTITY, "Running", "Failed", (SYSTEM,),
         ("output_schema_failure_or_token_limit_or_retries_exhausted_or_workflow_step_failure",), 5),
    rows(ENTITY, "Running", "Awaiting Approval", (SYSTEM,),
         ("sensitive_action_proposed_and_approval_request_created",), 5),
    rows(ENTITY, "Awaiting Approval", "Running", (SYSTEM,),
         ("approval_request_approved_and_content_hash_matches",), 5),
    rows(ENTITY, "Awaiting Approval", "Cancelled", (SYSTEM,),
         ("approval_request_rejected_expired_or_invalidated",), 5),
    rows(ENTITY, "Queued", "Cancelled", (FOUNDER,), (), 5),
    rows(ENTITY, "Running", "Queued", (SYSTEM,), ("transient_failure_with_fewer_than_3_retries",), 5),
)
