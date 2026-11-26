"""Unit tests: code status tables match requirements.md Appendix A (R8.1, R8.3, R8.6).

The parser below reads Appendix A directly from requirements.md and expands
multi-status cells the same way ``models.status.types.rows()`` does (one row
per (from, to) pair).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Any

import pytest

from models.status import NEW_RECORD, PRIOR_STATUS, STATUS_SETS, TRANSITION_TABLES
from models.status.project import CLIENT_LABELS, STATUS_INFO
from services.transitions import transition

REQUIREMENTS = (
    Path(__file__).resolve().parents[3]
    / ".kiro" / "specs" / "neuropath-platform" / "requirements.md"
)

# Appendix A.2 section number (or bold label inside A.2.22) -> entity key in TRANSITION_TABLES.
A2_ENTITIES: dict[str, str] = {
    "A.2.1": "lead",
    "A.2.2": "inquiry_question",
    "A.2.3": "attachment",
    "A.2.4": "invitation",
    "A.2.5": "technical_assessment_version",
    "A.2.6": "solution_architecture_version",
    "A.2.7": "project_requirements_version",
    "A.2.8": "proposal_version",
    "A.2.9": "approval_request",
    "A.2.10": "agreement",
    "A.2.11": "project_milestone",
    "A.2.12": "task",
    "A.2.13": "deliverable_version",
    "A.2.14": "defect",
    "A.2.15": "deployment_record",
    "A.2.16": "handover_checklist_item",
    "A.2.17": "support_request",
    "A.2.18": "maintenance_engagement",
    "A.2.19": "change_request",
    "A.2.20": "commercial_record",
    "A.2.21": "lab_registration",
    "Dataset": "dataset",
    "Pipeline version approval": "pipeline_version",
    "Execution": "pipeline_execution",
    "A.2.23": "job",
    "A.2.24": "agent_task",
    "A.2.25": "content_item",
    "A.2.26": "organization",
}

# Symbolic role vocabulary used to read the A.1.2 "Allowed roles" prose.
_ROLE_WORDS = (
    "Authorized_Reviewer",
    "Assigned Engineer",
    "Engineer",
    "Founder",
    "Administrator",
    "Project_Manager",
    "Project Lead",
    "Client Owner",
    "Client Member",
)


@dataclass
class ParsedAppendix:
    project_status_rows: list[list[str]] = field(default_factory=list)
    project_transition_rows: list[list[str]] = field(default_factory=list)
    statuses: dict[str, tuple[str, ...]] = field(default_factory=dict)
    tables: dict[str, list[list[str]]] = field(default_factory=dict)


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _strip_parens(text: str) -> str:
    prev = None
    while prev != text:
        prev, text = text, re.sub(r"\([^()]*\)", "", text)
    return text


def _parse_status_list(text: str) -> tuple[str, ...]:
    body = _strip_parens(text).split(". ")[0].rstrip(". ")
    return tuple(s.strip() for s in body.split(",") if s.strip())


@cache
def parse_appendix() -> ParsedAppendix:
    lines = REQUIREMENTS.read_text(encoding="utf-8").splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("## Appendix A"))
    end = next(i for i, ln in enumerate(lines) if ln.startswith("### A.3"))
    out = ParsedAppendix()
    section: str | None = None
    entity: str | None = None
    for ln in lines[start:end]:
        if m := re.match(r"#{3,4} (A\.[\d.]+)", ln):
            section = m.group(1)
            entity = A2_ENTITIES.get(section)
            continue
        if m := re.match(r"\*\*(.+?)\.\*\*", ln):
            if section == "A.2.22":
                entity = A2_ENTITIES.get(m.group(1))
        if entity:
            if m := re.search(r"Status(?:es)?: (.+)$", ln):
                if entity == "project_requirements_version":
                    out.statuses[entity] = ("Draft",)  # "Status: Draft, marked AI-generated ..."
                else:
                    out.statuses[entity] = _parse_status_list(m.group(1))
            elif entity == "pipeline_version" and "is unapproved or approved" in ln:
                out.statuses[entity] = ("unapproved", "approved")
        if not ln.startswith("| ") or ln.startswith("|---"):
            continue
        cells = _cells(ln)
        if cells[0] in ("Status", "#", "From"):
            continue
        if section == "A.1.1":
            out.project_status_rows.append(cells)
        elif section == "A.1.2":
            out.project_transition_rows.append(cells)
        elif entity:
            out.tables.setdefault(entity, []).append(cells)
    return out


def _expand_from(cell: str, statuses: tuple[str, ...]) -> list[str]:
    if cell in ("(new record)", "(complete-upload)"):
        return [NEW_RECORD]
    if cell == "Any status":
        return list(statuses)
    if m := re.match(r"Any status except (.+)$", cell):
        excluded = {s.strip() for s in m.group(1).split(",")}
        return [s for s in statuses if s not in excluded]
    if m := re.match(r"(.+?) through (.+?)(?:, or (On Hold)\b.*)?$", cell):
        i, j = statuses.index(m.group(1)), statuses.index(m.group(2))
        return [*statuses[i : j + 1], *([m.group(3)] if m.group(3) else [])]
    return [s.strip() for s in cell.split(",")]


def _expand_to(cell: str) -> list[str]:
    if cell == "Stored prior status":
        return [PRIOR_STATUS]
    return [s.strip() for s in cell.split(",")]


def _pairs(rows: list[list[str]], statuses: tuple[str, ...]) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    for cells in rows:
        froms = _expand_from(cells[0], statuses)
        if cells[1] == "Any other status":
            out |= {(f, t) for f in froms for t in statuses if t != f}
        else:
            out |= {(f, t) for f in froms for t in _expand_to(cells[1])}
    return out


def _roles(tid: str, cell: str) -> frozenset[str]:
    if cell.startswith("System"):
        return frozenset({"System"})  # the named humans only trigger the System move
    if tid == "T28":
        # "Authorized_Reviewer (Founder, Administrator, Project_Manager)": the parenthesis
        # narrows the reviewer set, so the code lists the three roles.
        inner = re.search(r"Authorized_Reviewer \(([^)]*)\)", cell)
        assert inner is not None
        cell = inner.group(1)
    text = re.sub(r"Engineer \(assigned[^)]*\)", "Assigned Engineer", cell)
    text = _strip_parens(text)
    found: set[str] = set()
    for word in _ROLE_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", text):
            found.add(word)
            text = text.replace(word, "")
    return frozenset(found)


def _phase_enabled(cell: str) -> int:
    if m := re.search(r"(\d) \(transitions", cell):
        return int(m.group(1))
    return int(re.match(r"\d", cell).group(0))  # type: ignore[union-attr]


# --- A.1 Project ----------------------------------------------------------------


def test_project_status_rows_match_a11() -> None:
    parsed = parse_appendix().project_status_rows
    assert len(parsed) == len(STATUS_INFO) == 20
    for cells, info in zip(parsed, STATUS_INFO, strict=True):
        status, stage, label, phase, terminal = cells[:5]
        assert (info.status, info.stage, info.client_label) == (status, stage, label)
        assert info.phase_enabled == _phase_enabled(phase), status
        assert info.terminal == (terminal == "Yes"), status
    assert STATUS_SETS["project"] == tuple(c[0] for c in parsed)


def test_every_project_status_has_client_label() -> None:
    for status in STATUS_SETS["project"]:
        assert CLIENT_LABELS.get(status, "").strip(), status


def test_project_transitions_match_a12_row_for_row() -> None:
    statuses = tuple(c[0] for c in parse_appendix().project_status_rows)
    status_phase = {c[0]: _phase_enabled(c[3]) for c in parse_appendix().project_status_rows}
    rows = parse_appendix().project_transition_rows
    assert [c[0] for c in rows] == [f"T{i:02d}" for i in range(1, 33)]

    expected: list[tuple[str, str, frozenset[str], int]] = []
    for tid, frm, to, roles, _guard, _src, phase_cell in rows:
        base = int(phase_cell[0])
        late = re.search(r"\((.+?) source from (\d)\)", phase_cell)
        for f in _expand_from(frm, statuses):
            for t in _expand_to(to):
                phase = base
                if "once that status is enabled" in phase_cell:
                    phase = max(base, status_phase[f])
                if late and f == late.group(1):
                    phase = int(late.group(2))
                expected.append((f, t, _roles(tid, roles), phase))

    actual = [
        (r.from_status, r.to_status, r.allowed_roles, r.enabled_phase)
        for r in TRANSITION_TABLES["project"]
    ]
    key = lambda x: (x[0], x[1], sorted(x[2]), x[3])  # noqa: E731
    assert sorted(actual, key=key) == sorted(expected, key=key)


# --- A.2 other entities -----------------------------------------------------------


def test_every_a2_entity_is_parsed_and_present() -> None:
    parsed = parse_appendix()
    assert set(parsed.statuses) == set(A2_ENTITIES.values())
    assert set(TRANSITION_TABLES) == {"project", *A2_ENTITIES.values()}


@pytest.mark.parametrize("entity", sorted(set(A2_ENTITIES.values())))
def test_a2_status_set_matches(entity: str) -> None:
    assert STATUS_SETS[entity] == parse_appendix().statuses[entity]


@pytest.mark.parametrize("entity", sorted(set(A2_ENTITIES.values())))
def test_a2_transition_pairs_match(entity: str) -> None:
    parsed = parse_appendix()
    statuses = parsed.statuses[entity]
    expected = _pairs(parsed.tables[entity], statuses)
    actual = {(r.from_status, r.to_status) for r in TRANSITION_TABLES[entity]}
    assert actual == expected
    used = {s for pair in expected for s in pair} - {NEW_RECORD}
    assert used <= set(statuses), used - set(statuses)


# --- error payloads (R8.3, R8.6) -------------------------------------------------


@dataclass
class _Entity:
    entity_type: str
    status: str | None
    prior_status: str | None = None
    facts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class _Principal:
    roles: frozenset[str]
    is_human: bool = True


FOUNDER = _Principal(frozenset({"Founder"}))


def test_guard_failure_payload() -> None:
    entity = _Entity("project", "On Hold", prior_status="Under Review")
    res = transition(entity, "Cancelled", FOUNDER, "  ", platform_phase=2)
    assert not res.accepted and res.rejection is not None
    rej = res.rejection
    assert rej.kind == "guard_failed"
    assert rej.guard == "non_empty_reason"
    assert "non_empty_reason" in rej.message and "reason is required" in rej.message
    assert (rej.current_status, rej.target) == ("On Hold", "Cancelled")
    assert rej.allowed_targets == ("Cancelled",)
    assert entity.status == "On Hold"


def test_disabled_status_payload() -> None:
    entity = _Entity("project", "Accepted", facts={"agreement_status": "In Effect"})
    res = transition(entity, "In Progress", FOUNDER, None, platform_phase=3)
    assert not res.accepted and res.rejection is not None
    rej = res.rejection
    assert rej.kind == "disabled_status"
    assert "'In Progress'" in rej.message and "phase 3" in rej.message
    assert rej.guard is None
    assert entity.status == "Accepted"


def test_invalid_transition_payload() -> None:
    entity = _Entity("project", "Draft")
    res = transition(entity, "Completed", FOUNDER, "r", platform_phase=4)
    assert not res.accepted and res.rejection is not None
    rej = res.rejection
    assert rej.kind == "invalid_transition"
    assert "'Draft'" in rej.message and "'Completed'" in rej.message
    assert rej.guard is None
    assert "Cancelled" in rej.allowed_targets and "Completed" not in rej.allowed_targets
    assert entity.status == "Draft"
