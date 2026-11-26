"""Documentation checks for the NeuroPath repository.

Verifies that the docs required for the current platform phase exist, that
docs/REQUIREMENTS_V2.md does not duplicate the formal spec requirements, and
that every environment variable in the .env.example files is documented in
docs/ENVIRONMENT.md.

Usage: python scripts/check_docs.py [--phase N] [--root PATH]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

# Docs introduced at each phase. Requirements are cumulative: phase N requires
# every doc listed for phases 0..N.
REQUIRED_DOCS: dict[int, list[str]] = {
    0: [
        "README.md",
        "docs/REQUIREMENTS_V2.md",
        "docs/CHANGELOG_V1_TO_V2.md",
        "docs/ARCHITECTURE.md",
        "docs/ROADMAP.md",
        "docs/MVP_SCOPE.md",
        "docs/AI_AGENT_INSTRUCTIONS.md",
        "docs/ENVIRONMENT.md",
        "docs/DEVELOPMENT.md",
        "docs/TESTING.md",
        "docs/DATABASE.md",
        "docs/IMPLEMENTATION_STATUS.md",
    ],
    1: [],
    2: ["docs/API.md", "docs/SECURITY.md"],
}

SPEC_REQUIREMENTS = ".kiro/specs/neuropath-platform/requirements.md"
REQUIREMENTS_V2 = "docs/REQUIREMENTS_V2.md"
ENVIRONMENT_DOC = "docs/ENVIRONMENT.md"
ENV_EXAMPLES = ["apps/api/.env.example", "apps/web/.env.example"]

EARS_RE = re.compile(r"\b(WHEN|IF|WHILE|WHERE)\b.*\bTHE\b.*\bSHALL\b")
ENV_KEY_RE = re.compile(r"^\s*(?:#\s*)?([A-Z][A-Z0-9_]*)=")
MIN_DUP_LEN = 60
MAX_DUP_REPORTS = 5


def required_docs(phase: int) -> list[str]:
    docs: list[str] = []
    for p in sorted(REQUIRED_DOCS):
        if p <= phase:
            docs.extend(REQUIRED_DOCS[p])
    return docs


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required(root: Path, phase: int) -> list[str]:
    return [
        f"missing required doc for phase {phase}: {rel}"
        for rel in required_docs(phase)
        if not (root / rel).is_file()
    ]


def check_duplication(root: Path) -> list[str]:
    v2 = root / REQUIREMENTS_V2
    spec = root / SPEC_REQUIREMENTS
    if not v2.is_file():
        return []
    spec_lines: set[str] = set()
    if spec.is_file():
        spec_lines = {ln.strip() for ln in _read(spec).splitlines()}

    problems: list[str] = []
    for lineno, line in enumerate(_read(v2).splitlines(), start=1):
        stripped = line.strip()
        reason = None
        if EARS_RE.search(stripped):
            reason = "EARS clause"
        elif len(stripped) >= MIN_DUP_LEN and stripped in spec_lines:
            reason = f"verbatim copy of {SPEC_REQUIREMENTS}"
        if reason:
            problems.append(f"{REQUIREMENTS_V2}:{lineno}: {reason}: {stripped[:100]}")
            if len(problems) >= MAX_DUP_REPORTS:
                break
    return problems


def env_keys(root: Path) -> set[str]:
    keys: set[str] = set()
    for rel in ENV_EXAMPLES:
        path = root / rel
        if not path.is_file():
            continue
        for line in _read(path).splitlines():
            m = ENV_KEY_RE.match(line)
            if m:
                keys.add(m.group(1))
    return keys


def check_env(root: Path) -> list[str]:
    doc = root / ENVIRONMENT_DOC
    if not doc.is_file():
        return []  # already reported as a missing required doc
    text = _read(doc)
    return [
        f"{ENVIRONMENT_DOC}: env var not documented: {key}"
        for key in sorted(env_keys(root))
        if not re.search(rf"\b{re.escape(key)}\b", text)
    ]


def check(root: Path, phase: int) -> list[str]:
    return check_required(root, phase) + check_duplication(root) + check_env(root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phase", type=int, default=int(os.environ.get("PLATFORM_PHASE", "0"))
    )
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parent.parent
    )
    args = parser.parse_args(argv)

    problems = check(args.root, args.phase)
    for p in problems:
        print(p)
    if problems:
        return 1
    print(f"OK: docs checks passed for phase {args.phase}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
