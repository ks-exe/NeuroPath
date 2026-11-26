"""Lab registration status model (Appendix A.2.21).

R55 places no restriction on the order of Lab status changes, so every ordered
pair of distinct statuses is a row.
"""

from __future__ import annotations

from .types import FOUNDER, TransitionRow, rows

ENTITY = "lab_registration"

STATUSES: tuple[str, ...] = ("disabled", "internal", "client beta", "available")

TRANSITIONS: tuple[TransitionRow, ...] = tuple(
    r
    for f in STATUSES
    for t in STATUSES
    if f != t
    for r in rows(
        ENTITY,
        f,
        t,
        (FOUNDER, "Administrator (delegated by Founder)"),
        ("data_playground_production_leaving_disabled_requires_founder_go_decision",),
        4,
    )
)

