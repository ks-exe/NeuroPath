"""Shared types for the Appendix A status and transition tables (R8.1).

Each entity module in this package holds its status set and a tuple of
``TransitionRow`` records, transcribed from requirements.md Appendix A.
These modules are data only. The engine (task 4.2) interprets them.

Conventions
-----------
* ``NEW_RECORD`` is the ``from_status`` of a creation row ("(new record)" or
  "(complete-upload)" in Appendix A).
* ``PRIOR_STATUS`` is the ``to_status`` of the Project T29 row (On Hold back to
  the stored prior status).
* Roles are the symbolic names used in Appendix A ("Authorized_Reviewer",
  "Staff (Assigned)", "System", ...). The engine resolves symbolic roles to
  principals. A role listed here that carries a qualifier in Appendix A
  (for example "Client Member with the decision permission") is expressed as
  the role plus a guard name.
* Guards are names resolved from the guard registry by the engine. An empty
  tuple means "None" in Appendix A.
* ``enabled_phase`` is the first phase in which the row is active (R8.6, R24.4).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

NEW_RECORD = "(new record)"
PRIOR_STATUS = "(stored prior status)"

# Symbolic role names used by Appendix A.
SYSTEM = "System"
FOUNDER = "Founder"
ADMINISTRATOR = "Administrator"
ENGINEER = "Engineer"
ASSIGNED_ENGINEER = "Assigned Engineer"
PROJECT_MANAGER = "Project_Manager"
PROJECT_LEAD = "Project Lead"
STAFF_ASSIGNED = "Staff (Assigned)"
CLIENT_OWNER = "Client Owner"
CLIENT_MEMBER = "Client Member"
AUTHORIZED_REVIEWER = "Authorized_Reviewer"
AUTHORIZED_APPROVER = "Authorized_Approver"
DELEGATE = "Delegate"  # Founder delegate under A-06
INTERNAL_AGENT = "Internal_Agent"
AGENT_RUNTIME = "Agent_Runtime"
JOB_OWNER = "Job owner"
SUBMITTER = "Submitter"


@dataclass(frozen=True)
class TransitionRow:
    entity: str
    from_status: str
    to_status: str
    allowed_roles: frozenset[str]
    guards: tuple[str, ...]  # names resolved from the guard registry
    enabled_phase: int


def _as_list(value: str | Iterable[str]) -> list[str]:
    return [value] if isinstance(value, str) else list(value)


def rows(
    entity: str,
    from_status: str | Iterable[str],
    to_status: str | Iterable[str],
    roles: Iterable[str],
    guards: Iterable[str] = (),
    phase: int = 1,
) -> tuple[TransitionRow, ...]:
    """Expand one Appendix A table row into one TransitionRow per (from, to) pair."""
    role_set = frozenset(roles)
    guard_tuple = tuple(guards)
    return tuple(
        TransitionRow(entity, f, t, role_set, guard_tuple, phase)
        for f in _as_list(from_status)
        for t in _as_list(to_status)
    )


def concat(*groups: tuple[TransitionRow, ...]) -> tuple[TransitionRow, ...]:
    return tuple(r for g in groups for r in g)
