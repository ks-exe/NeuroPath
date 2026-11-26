"""Organization status model (Appendix A.2.26).

While suspended, requests from users of the Organization return HTTP 403 (R73.8).
"""

from __future__ import annotations

from .types import FOUNDER, TransitionRow, concat, rows

ENTITY = "organization"

STATUSES: tuple[str, ...] = ("active", "suspended")

_ROLES = (FOUNDER, "Administrator (permitted by Founder)")

# Organization status columns are created in Phase 5 (Appendix B).
TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, "active", "suspended", _ROLES, ("non_empty_reason",), 5),
    rows(ENTITY, "suspended", "active", _ROLES, (), 5),
)
