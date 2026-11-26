"""Support_Request status model (Appendix A.2.17)."""

from __future__ import annotations

from .types import (
    CLIENT_MEMBER,
    CLIENT_OWNER,
    FOUNDER,
    NEW_RECORD,
    PROJECT_MANAGER,
    STAFF_ASSIGNED,
    SYSTEM,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "support_request"

STATUSES: tuple[str, ...] = ("New", "Triaged", "In Progress", "Awaiting Client", "Resolved", "Closed")

_STAFF = (STAFF_ASSIGNED, PROJECT_MANAGER, FOUNDER)
_CLIENT = (CLIENT_OWNER, CLIENT_MEMBER)

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "New", _CLIENT,
         ("owning_organization_member", "type_in_bug_question_improvement_incident",
          "title_and_description_present", "project_of_client_organization_else_404_in_eligible_status"), 4),
    rows(ENTITY, "New", "Triaged", _STAFF, (), 4),
    rows(ENTITY, "Triaged", "In Progress", _STAFF, (), 4),
    rows(ENTITY, "In Progress", "Awaiting Client", _STAFF, (), 4),
    rows(ENTITY, "Awaiting Client", "In Progress", (SYSTEM, *_STAFF), ("system_on_client_comment",), 4),
    rows(ENTITY, "In Progress", "Resolved", _STAFF, (), 4),
    rows(ENTITY, "Resolved", "Closed", (*_STAFF, *_CLIENT), ("client_of_owning_organization",), 4),
    rows(ENTITY, "Resolved", "In Progress", (*_CLIENT, *_STAFF), ("client_of_owning_organization",), 4),
    rows(ENTITY, ("New", "Triaged"), "Closed", _STAFF, ("non_empty_reason",), 4),
)
