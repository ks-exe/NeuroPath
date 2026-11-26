"""Status Transition Engine (R8.2 to R8.6).

``transition()`` is the only way to change a status. It looks up the Appendix A
row, applies phase enablement, checks roles, evaluates guards, then sets the
status and calls the audit hook. The hook runs in the caller's transaction. If
it raises, the status change is rolled back on the entity and the error propagates.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, Literal, Protocol

from core.config import get_settings
from models.status import NEW_RECORD, PRIOR_STATUS, TRANSITION_TABLES, TransitionRow

from .guards import GUARD_REGISTRY, GuardContext, evaluate


class Transitionable(Protocol):
    entity_type: str
    status: str | None  # None for a record not yet created
    prior_status: str | None
    facts: Mapping[str, Any]  # loaded state read by guards


class Principal(Protocol):
    roles: frozenset[str]
    is_human: bool


@dataclass(frozen=True)
class AuditEntry:
    entity_type: str
    prior_status: str | None
    new_status: str
    reason: str | None
    principal: Principal


AuditHook = Callable[[AuditEntry], None]

RejectionKind = Literal["invalid_transition", "disabled_status", "role_not_allowed", "guard_failed"]


@dataclass(frozen=True)
class Rejection:
    kind: RejectionKind
    entity_type: str
    current_status: str | None
    target: str
    message: str
    guard: str | None = None  # named failed guard
    allowed_targets: tuple[str, ...] = ()
    details: tuple[str, ...] = ()


@dataclass(frozen=True)
class TransitionResult:
    accepted: bool
    prior_status: str | None = None
    new_status: str | None = None
    effects: tuple[str, ...] = ()  # follow-up actions for the owning service
    rejection: Rejection | None = None


def _row_enabled(row: TransitionRow, phase: int) -> bool:
    if row.enabled_phase > phase:
        return False
    for g in row.guards:
        spec = GUARD_REGISTRY.get(g)
        if spec is not None and spec.min_phase > phase:
            return False
    return True


def _targets_match(row: TransitionRow, target: str, prior_status: str | None) -> bool:
    if row.to_status == PRIOR_STATUS:
        return prior_status is not None and target == prior_status
    return row.to_status == target


def allowed_targets(
    entity: Transitionable, principal: Principal, platform_phase: int | None = None
) -> tuple[str, ...]:
    """Targets reachable now by the principal's roles (for error bodies)."""
    phase = _phase(platform_phase)
    src = NEW_RECORD if entity.status is None else entity.status
    out: list[str] = []
    for r in TRANSITION_TABLES.get(entity.entity_type, ()):
        if r.from_status != src or not _row_enabled(r, phase):
            continue
        if not (r.allowed_roles & principal.roles):
            continue
        t = entity.prior_status if r.to_status == PRIOR_STATUS else r.to_status
        if t and t not in out:
            out.append(t)
    return tuple(out)


def _phase(platform_phase: int | None) -> int:
    return get_settings().platform_phase if platform_phase is None else platform_phase


def transition(
    entity: Transitionable,
    target: str,
    principal: Principal,
    reason: str | None,
    *,
    audit_hook: AuditHook | None = None,
    platform_phase: int | None = None,
) -> TransitionResult:
    """Move ``entity`` to ``target`` if an enabled row, role and guards allow it."""
    phase = _phase(platform_phase)
    current = entity.status
    src = NEW_RECORD if current is None else current
    table = TRANSITION_TABLES.get(entity.entity_type, ())

    def reject(kind: RejectionKind, msg: str, guard: str | None = None) -> TransitionResult:
        return TransitionResult(
            False,
            rejection=Rejection(
                kind, entity.entity_type, current, target, msg, guard,
                allowed_targets(entity, principal, phase),
            ),
        )

    candidates = [
        r for r in table if r.from_status == src and _targets_match(r, target, entity.prior_status)
    ]
    if not candidates:
        return reject(
            "invalid_transition",
            f"{entity.entity_type}: transition from '{current}' to '{target}' is not defined",
        )
    enabled = [r for r in candidates if _row_enabled(r, phase)]
    if not enabled:
        return reject(
            "disabled_status",
            f"{entity.entity_type}: status '{target}' is not enabled in platform phase {phase}",
        )
    permitted = [r for r in enabled if r.allowed_roles & principal.roles]
    if not permitted:
        return reject(
            "role_not_allowed",
            f"{entity.entity_type}: no role of the principal may move '{current}' to '{target}'",
        )

    ctx = GuardContext(
        entity.entity_type, current, target, reason, principal.is_human,
        entity.prior_status, entity.facts,
    )
    first_failure: tuple[str, str] | None = None
    chosen: TransitionRow | None = None
    for row in permitted:
        failure = None
        for name in row.guards:
            ok, why = evaluate(name, ctx)
            if not ok:
                failure = (name, why or f"Guard '{name}' failed")
                break
        if failure is None:
            chosen = row
            break
        first_failure = first_failure or failure
    if chosen is None:
        assert first_failure is not None
        return reject("guard_failed", first_failure[1], first_failure[0])

    effects = tuple(g for g in chosen.guards if GUARD_REGISTRY[g].is_effect)
    old_prior = entity.prior_status
    if "store_prior_status_and_reason" in effects:
        entity.prior_status = current
    entity.status = target
    try:
        if audit_hook is not None:
            audit_hook(AuditEntry(entity.entity_type, current, target, reason, principal))
    except Exception:
        entity.status = current
        entity.prior_status = old_prior
        raise
    return TransitionResult(True, current, target, effects)
