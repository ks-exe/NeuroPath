"""Appendix A status sets and transition tables as data (R8.1, R24.2).

One module per entity. ``TRANSITION_TABLES`` maps the entity key to its rows.
The engine that interprets these rows is implemented separately.
"""

from __future__ import annotations

from . import (
    agent_task,
    agreement,
    approval_request,
    attachment,
    change_request,
    commercial_record,
    content_item,
    dataset,
    defect,
    deliverable_version,
    deployment_record,
    handover_checklist_item,
    inquiry_question,
    invitation,
    job,
    lab_registration,
    lead,
    maintenance_engagement,
    organization,
    pipeline_execution,
    pipeline_version,
    project,
    project_milestone,
    project_requirements,
    proposal_version,
    solution_architecture,
    support_request,
    task,
    technical_assessment,
)
from .types import NEW_RECORD, PRIOR_STATUS, TransitionRow

_MODULES = (
    project, lead, inquiry_question, attachment, invitation, technical_assessment,
    solution_architecture, project_requirements, proposal_version, approval_request,
    agreement, project_milestone, task, deliverable_version, defect, deployment_record,
    handover_checklist_item, support_request, maintenance_engagement, change_request,
    commercial_record, lab_registration, dataset, pipeline_version, pipeline_execution,
    job, agent_task, content_item, organization,
)

TRANSITION_TABLES: dict[str, tuple[TransitionRow, ...]] = {m.ENTITY: m.TRANSITIONS for m in _MODULES}
STATUS_SETS: dict[str, tuple[str, ...]] = {
    m.ENTITY: (m.STATUSES if m.ENTITY != "project" else project.STATUSES) for m in _MODULES
}

__all__ = ["NEW_RECORD", "PRIOR_STATUS", "STATUS_SETS", "TRANSITION_TABLES", "TransitionRow"]
