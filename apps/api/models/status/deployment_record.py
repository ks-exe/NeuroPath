"""Deployment_Record status model (Appendix A.2.15)."""

from __future__ import annotations

from .types import FOUNDER, NEW_RECORD, PROJECT_MANAGER, STAFF_ASSIGNED, TransitionRow, concat, rows

ENTITY = "deployment_record"

STATUSES: tuple[str, ...] = ("Planned", "In Progress", "Succeeded", "Failed", "Rolled Back")

_ROLES = (STAFF_ASSIGNED, PROJECT_MANAGER, FOUNDER)

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Planned", _ROLES,
         ("environment_type_in_dev_staging_production", "version_or_commit_reference_present",
          "no_secret_pattern_match"), 4),
    rows(ENTITY, "Planned", "In Progress", _ROLES, (), 4),
    rows(ENTITY, "In Progress", "Succeeded", _ROLES, (), 4),
    rows(ENTITY, "In Progress", "Failed", _ROLES, (), 4),
    rows(ENTITY, ("Succeeded", "Failed"), "Rolled Back", _ROLES, (), 4),
)
