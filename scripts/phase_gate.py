"""Phase gate check and phase report skeleton (R78.1, R78.4, R78.5).

Runs the gate checks for a phase and writes ``docs/phase-reports/phase-N.md``
from recorded results only. Nothing is assumed: a result that was not
recorded is reported as NOT RECORDED and fails the gate.

Usage:
    python scripts/phase_gate.py --phase {0,1} [--ci-status PATH]
        [--database-url URL] [--report PATH]

Inputs:
    --ci-status   recorded result of the last CI run (JSON), default
                  docs/phase-reports/ci-status.json, e.g.
                  {"run_id": 123, "commit": "abc", "conclusion": "success",
                   "recorded_at": "2025-01-01T00:00:00Z"}
                  The GitHub API is never called.
    deployments   docs/phase-reports/deployments.json: a list of deploy
                  records, each with an "authorization" reference to the
                  Founder's written authorization. Missing file = no deploys.
    lighthouse    (phase 1) docs/phase-reports/lighthouse.json: recorded scores,
                  e.g. {"scores": {"performance": 95, "accessibility": 100,
                  "best-practices": 96, "seo": 100}, "url": "...",
                  "recorded_at": "..."}. Lighthouse is never run by the gate.
                  Missing file = NOT RECORDED.

Phase 1 re-runs every Phase 0 check (R78.3) and adds the R78.6 checks: the
public page render tests, the inquiry storage tests, a V1 tagline scan, the
jsdom-level accessibility tests and the recorded Lighthouse scores.

Exit code 0 only if every check passes. The Founder approval section of the
report is left blank; the gate never fills it in.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

PASS, FAIL, NOT_RECORDED = "PASS", "FAIL", "NOT RECORDED"

REPORTS_DIR = Path("docs/phase-reports")
DEFAULT_CI_STATUS = REPORTS_DIR / "ci-status.json"
DEPLOYMENTS_FILE = REPORTS_DIR / "deployments.json"
STATUS_DOC = Path("docs/IMPLEMENTATION_STATUS.md")
ARCH_DOC = Path("docs/ARCHITECTURE.md")


@dataclass
class Result:
    name: str
    status: str
    detail: str
    data: dict[str, object] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.status == PASS


@dataclass
class Context:
    root: Path
    phase: int
    ci_status: Path
    database_url: str | None


Check = Callable[[Context], Result]


# --------------------------------------------------------------------------
# Phase 0 checks
# --------------------------------------------------------------------------

PHASE0_REQUIRED_DIRS = [
    "apps/web",
    "apps/api",
    *(f"apps/api/{d}" for d in
      ("api", "core", "models", "schemas", "services", "repositories", "workers", "tests")),
    "packages",
    "infrastructure",
    "infrastructure/cdk",
    "docs",
    "scripts",
]
# R1.3: later-phase directories must not exist yet.
PHASE0_ABSENT_DIRS = ["data_engine", "agents", "apps/api/labs"]


def check_structure(ctx: Context) -> Result:
    missing = [d for d in PHASE0_REQUIRED_DIRS if not (ctx.root / d).is_dir()]
    present = [d for d in PHASE0_ABSENT_DIRS if (ctx.root / d).exists()]
    problems = [f"missing dir: {d}" for d in missing] + [
        f"later-phase dir exists too early: {d}" for d in present
    ]
    if problems:
        return Result("structure", FAIL, "; ".join(problems))
    return Result(
        "structure", PASS,
        f"{len(PHASE0_REQUIRED_DIRS)} required dirs present; "
        f"absent as required: {', '.join(PHASE0_ABSENT_DIRS)}",
    )


def check_docs_set(ctx: Context) -> Result:
    import check_docs

    problems = check_docs.check(ctx.root, ctx.phase)
    if problems:
        return Result("docs", FAIL, "; ".join(problems))
    return Result("docs", PASS, f"documentation set for phase {ctx.phase} complete")


def check_migrations_round_trip(ctx: Context) -> Result:
    import check_migrations

    try:
        if ctx.database_url:
            diff = check_migrations.check_round_trip(ctx.database_url)
            where = "given database"
        else:
            with tempfile.TemporaryDirectory() as tmp:
                url = f"sqlite:///{Path(tmp, 'gate.db').as_posix()}"
                diff = check_migrations.check_round_trip(url)
            where = "fresh temporary SQLite database"
    except Exception as exc:  # noqa: BLE001 - any failure fails the gate
        return Result("migrations", FAIL, f"round trip could not run: {exc}")
    if diff:
        return Result("migrations", FAIL, "schema after downgrade differs:\n" + diff)
    return Result("migrations", PASS, f"upgrade head / downgrade base round trip on {where}")


def check_lab_isolation(ctx: Context) -> Result:
    import check_lab_imports

    violations = check_lab_imports.check(ctx.root / "apps" / "api")
    if violations:
        return Result("lab-imports", FAIL, "; ".join(str(v) for v in violations))
    return Result("lab-imports", PASS, "no core module imports a Lab module")


def check_ci_status(ctx: Context) -> Result:
    path = ctx.ci_status
    if not path.is_file():
        return Result("ci-status", NOT_RECORDED, f"no recorded CI result at {_rel(ctx, path)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return Result("ci-status", FAIL, f"unreadable CI status file: {exc}")
    if not isinstance(data, dict):
        return Result("ci-status", FAIL, "CI status file must be a JSON object")
    conclusion = data.get("conclusion")
    summary = (
        f"run {data.get('run_id', '?')} on commit {data.get('commit', '?')}, "
        f"conclusion={conclusion!r}, recorded_at={data.get('recorded_at', '?')}"
    )
    status = PASS if conclusion == "success" else FAIL
    return Result("ci-status", status, summary, data)


def check_deploy_authorization(ctx: Context) -> Result:
    path = ctx.root / DEPLOYMENTS_FILE
    if not path.is_file():
        return Result("deploy-authorization", PASS, "no deploys recorded")
    try:
        records = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return Result("deploy-authorization", FAIL, f"unreadable {DEPLOYMENTS_FILE}: {exc}")
    if not isinstance(records, list):
        return Result("deploy-authorization", FAIL, f"{DEPLOYMENTS_FILE} must be a JSON list")
    unauthorized = [
        i for i, r in enumerate(records)
        if not (isinstance(r, dict) and isinstance(r.get("authorization"), str)
                and r["authorization"].strip())
    ]
    if unauthorized:
        return Result(
            "deploy-authorization", FAIL,
            f"deploy record(s) without a Founder authorization: indexes {unauthorized}",
        )
    return Result("deploy-authorization", PASS,
                  f"{len(records)} deploy record(s), all with a Founder authorization")


# --------------------------------------------------------------------------
# Phase 1 checks
# --------------------------------------------------------------------------

NPM = "npm.cmd" if sys.platform == "win32" else "npm"
LIGHTHOUSE_FILE = REPORTS_DIR / "lighthouse.json"
LIGHTHOUSE_CATEGORIES = ("performance", "accessibility", "best-practices", "seo")
LIGHTHOUSE_MIN = 90  # R15.9
V1_TAGLINE = "Engineering Intelligence. Enabling Growth."
TAGLINE_SCAN_DIRS = ("apps/web/src", "apps/web/content")
TAGLINE_SCAN_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".md", ".mdx", ".json", ".css"}
SUBPROCESS_TIMEOUT_S = 600


def _run_command(name: str, args: list[str], cwd: Path, what: str) -> Result:
    """Run a test command; PASS only on exit code 0."""
    try:
        proc = subprocess.run(
            args, check=False, cwd=cwd, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=SUBPROCESS_TIMEOUT_S,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return Result(name, FAIL, f"{what}: could not run `{' '.join(args)}`: {exc}")
    if proc.returncode == 0:
        return Result(name, PASS, f"{what}: `{' '.join(args)}` exited 0")
    tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-15:])
    return Result(name, FAIL, f"{what}: `{' '.join(args)}` exited {proc.returncode}\n{tail}")


def check_public_pages(ctx: Context) -> Result:
    return _run_command(
        "public-pages",
        [NPM, "run", "test", "--", "src/pages-content.test.tsx"],
        ctx.root / "apps" / "web",
        "every public page renders with one h1 and no V1 tagline (pages-content.test.tsx)",
    )


def check_inquiry_storage(ctx: Context) -> Result:
    return _run_command(
        "inquiry-storage",
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q",
         "tests/test_public_inquiries.py", "tests/test_inquiries_service.py"],
        ctx.root / "apps" / "api",
        "a submission stores Lead, Project_Inquiry and Project",
    )


def check_accessibility(ctx: Context) -> Result:
    return _run_command(
        "accessibility",
        [NPM, "run", "test", "--", "src/a11y.test.tsx", "src/a11y-contrast.test.ts"],
        ctx.root / "apps" / "web",
        "jsdom-level checks only (skip link, landmarks, text alternatives, token contrast); "
        "no browser or axe run",
    )


def _is_test_file(path: Path) -> bool:
    return ".test." in path.name or "__tests__" in path.parts


def check_v1_tagline(ctx: Context) -> Result:
    hits: list[str] = []
    scanned = 0
    for rel in TAGLINE_SCAN_DIRS:
        base = ctx.root / rel
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in TAGLINE_SCAN_SUFFIXES:
                continue
            if _is_test_file(path):
                continue
            scanned += 1
            if V1_TAGLINE in path.read_text(encoding="utf-8", errors="replace"):
                hits.append(_rel(ctx, path))
    if hits:
        return Result("v1-tagline", FAIL, "V1 tagline found in: " + ", ".join(hits))
    return Result("v1-tagline", PASS,
                  f"{scanned} source files in {', '.join(TAGLINE_SCAN_DIRS)} "
                  "(test files excluded) contain no V1 tagline")


def check_lighthouse(ctx: Context) -> Result:
    path = ctx.root / LIGHTHOUSE_FILE
    if not path.is_file():
        return Result("lighthouse", NOT_RECORDED,
                      f"no recorded Lighthouse result at {LIGHTHOUSE_FILE.as_posix()}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return Result("lighthouse", FAIL, f"unreadable {LIGHTHOUSE_FILE.as_posix()}: {exc}")
    scores = data.get("scores", data) if isinstance(data, dict) else None
    if not isinstance(scores, dict):
        return Result("lighthouse", FAIL, "Lighthouse file must be a JSON object with scores")
    parts: list[str] = []
    ok = True
    for cat in LIGHTHOUSE_CATEGORIES:
        value = scores.get(cat)
        if not isinstance(value, int | float) or isinstance(value, bool):
            parts.append(f"{cat}=missing")
            ok = False
            continue
        parts.append(f"{cat}={value:g}")
        ok = ok and value >= LIGHTHOUSE_MIN
    detail = f"{', '.join(parts)} (minimum {LIGHTHOUSE_MIN} each, R15.9)"
    return Result("lighthouse", PASS if ok else FAIL, detail, data)


PHASE0_CHECKS: list[Check] = [
    check_structure,
    check_ci_status,
    check_migrations_round_trip,
    check_docs_set,
    check_lab_isolation,
    check_deploy_authorization,
]

PHASE_CHECKS: dict[int, list[Check]] = {
    0: PHASE0_CHECKS,
    # R78.3: Phase 1 re-runs every Phase 0 check, then its own.
    1: [
        *PHASE0_CHECKS,
        check_public_pages,
        check_inquiry_storage,
        check_v1_tagline,
        check_accessibility,
        check_lighthouse,
    ],
}

# Requirement IDs delivered by a phase and the checks that must pass for each
# to be listed as delivered.
PHASE_REQUIREMENTS: dict[int, dict[str, list[str]]] = {
    0: {
        "R1": ["structure", "lab-imports"],
        "R2": ["structure"],
        "R3": ["deploy-authorization", "ci-status"],
        "R4": ["ci-status"],
        "R5": ["ci-status", "docs"],
        "R6": ["migrations"],
        "R7": ["docs"],
        "R8": ["ci-status"],
    },
    1: {
        "R9": ["public-pages", "accessibility"],
        "R10": ["public-pages", "v1-tagline"],
        "R11": ["public-pages"],
        "R12": ["public-pages"],
        "R13": ["public-pages"],
        "R14": ["inquiry-storage", "migrations"],
        "R15": ["accessibility", "lighthouse"],
    },
}

NEXT_PHASE_PLAN: dict[int, str] = {
    0: "Phase 1 (public website and inquiry intake): R9 to R15, tasks 10 to 16 in "
       "`.kiro/specs/neuropath-platform/tasks.md`. Starts only after the Founder "
       "approves this report (R78.2).",
    1: "Phase 2 (Client Acquisition and Founder CRM): R16 to R30, tasks 17 "
       "to 32 in `.kiro/specs/neuropath-platform/tasks.md`. Starts only after the "
       "Founder approves this report (R78.2).",
}


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------

def _rel(ctx: Context, path: Path) -> str:
    try:
        return path.resolve().relative_to(ctx.root.resolve()).as_posix()
    except ValueError:
        return str(path)


def known_issues(root: Path) -> list[str]:
    path = root / STATUS_DOC
    if not path.is_file():
        return []
    items: list[str] = []
    in_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_section = line.strip().lower() == "## known issues"
            continue
        if in_section and line.lstrip().startswith(("- ", "* ")):
            items.append(line.strip()[2:])
    return items


PENDING_RE = re.compile(r"pending|not yet|open|undecided|unresolved|tbd", re.IGNORECASE)
ASSUMPTION_RE = re.compile(r"\bA-\d{2}\b")


def open_assumptions(root: Path) -> dict[str, list[str]]:
    """A-xx IDs mentioned on a line that marks them pending, with source docs."""
    found: dict[str, list[str]] = {}
    for rel in (STATUS_DOC, ARCH_DOC):
        path = root / rel
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not PENDING_RE.search(line):
                continue
            for aid in ASSUMPTION_RE.findall(line):
                srcs = found.setdefault(aid, [])
                if rel.as_posix() not in srcs:
                    srcs.append(rel.as_posix())
    return dict(sorted(found.items()))


def render_report(ctx: Context, results: list[Result]) -> str:
    by_name = {r.name: r for r in results}
    ci = by_name.get("ci-status")
    lines = [
        f"# Phase {ctx.phase} report",
        "",
        (
            f"Generated by `scripts/phase_gate.py --phase {ctx.phase}` on "
            f"{datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}. "
            "Every entry comes from a check executed by the gate or a recorded result file."
        ),
        "",
        f"Gate result: **{'PASS' if all(r.passed for r in results) else 'FAIL'}**",
        "",
        "## Delivered requirement IDs",
        "",
    ]
    for rid, needed in PHASE_REQUIREMENTS.get(ctx.phase, {}).items():
        ok = all(by_name.get(n) is not None and by_name[n].passed for n in needed)
        state = "delivered" if ok else "not verified"
        lines.append(f"- {rid}: {state} (checks: {', '.join(needed)})")
    lines += ["", "## Check results", "", "| Check | Result | Detail |", "| --- | --- | --- |"]
    for r in results:
        detail = r.detail.replace("|", "\\|").replace("\n", "<br>")
        lines.append(f"| {r.name} | {r.status} | {detail} |")
    lines += ["", "## Test results", ""]
    if ci is None or ci.status == NOT_RECORDED:
        lines.append(f"Not recorded: no CI result file at `{_rel(ctx, ctx.ci_status)}`.")
    else:
        lines.append(f"From the recorded CI run: {ci.detail}.")
        for key in ("jobs", "tests"):
            if key in ci.data:
                lines.append(f"- {key}: `{json.dumps(ci.data[key])}`")
    lines += ["", "## Known issues", ""]
    issues = known_issues(ctx.root)
    lines += [f"- {i}" for i in issues] or [f"None listed in `{STATUS_DOC.as_posix()}`."]
    lines += ["", "## Open assumptions", ""]
    assumptions = open_assumptions(ctx.root)
    lines += [f"- {aid} (mentioned as pending in {', '.join(srcs)})"
              for aid, srcs in assumptions.items()] or [
        f"None marked pending in `{STATUS_DOC.as_posix()}` or `{ARCH_DOC.as_posix()}`."]
    lines += [
        "", "## Next phase plan", "",
        NEXT_PHASE_PLAN.get(ctx.phase, "Not defined."),
        "", "## Founder approval", "",
        "Approved by: ____________________",
        "",
        "Date: ____________________",
        "",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def run_gate(ctx: Context) -> list[Result]:
    results: list[Result] = []
    for check in PHASE_CHECKS[ctx.phase]:
        try:
            results.append(check(ctx))
        except Exception as exc:  # noqa: BLE001 - report, never assume success
            results.append(Result(check.__name__.removeprefix("check_"), FAIL,
                                  f"check crashed: {exc}"))
    return results


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Phase gate check (R78)")
    p.add_argument("--phase", type=int, required=True, choices=sorted(PHASE_CHECKS))
    p.add_argument("--ci-status", type=Path, default=None)
    p.add_argument("--database-url", default=None)
    p.add_argument("--report", type=Path, default=None)
    p.add_argument("--root", type=Path, default=ROOT)
    a = p.parse_args(argv)

    root = a.root.resolve()
    ctx = Context(
        root=root,
        phase=a.phase,
        ci_status=a.ci_status or root / DEFAULT_CI_STATUS,
        database_url=a.database_url,
    )
    results = run_gate(ctx)
    report_path = a.report or root / REPORTS_DIR / f"phase-{a.phase}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(ctx, results), encoding="utf-8")

    print(f"Phase {a.phase} gate:")
    for r in results:
        print(f"  [{r.status}] {r.name}: {r.detail.splitlines()[0] if r.detail else ''}")
    ok = all(r.passed for r in results)
    print(f"Report written to {_rel(ctx, report_path)}")
    print("GATE PASSED" if ok else "GATE FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
