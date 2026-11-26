"""Unit tests for scripts/check_docs.py (R5.1, R5.6)."""
import contextlib
import importlib.util
import io
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT = _REPO_ROOT / "scripts" / "check_docs.py"
_spec = importlib.util.spec_from_file_location("check_docs", _SCRIPT)
checker = importlib.util.module_from_spec(_spec)
sys.modules["check_docs"] = checker
_spec.loader.exec_module(checker)

SPEC_LINE = (
    "The platform keeps a single source of truth for formal requirements in the spec."
)


@pytest.fixture
def root():
    d = tempfile.mkdtemp()
    try:
        yield Path(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _complete_tree(root: Path, phase: int = 0) -> None:
    for rel in checker.required_docs(phase):
        _write(root, rel, "# doc\n")
    _write(root, checker.REQUIREMENTS_V2, "# Requirements\n\nSee the spec requirements.md.\n")
    _write(root, checker.SPEC_REQUIREMENTS, f"# Spec\n\n{SPEC_LINE}\n")
    _write(root, "apps/api/.env.example", "DATABASE_URL=postgres://x\n# SECRET_KEY=\n")
    _write(root, checker.ENVIRONMENT_DOC, "| DATABASE_URL | db |\n| SECRET_KEY | key |\n")


def _run_main(root: Path, phase: int = 0) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return checker.main(["--phase", str(phase), "--root", str(root)])


def test_complete_phase0_tree_passes(root):
    _complete_tree(root)
    assert checker.check(root, 0) == []
    assert _run_main(root) == 0


def test_missing_required_doc_reported(root):
    _complete_tree(root)
    (root / "docs/ROADMAP.md").unlink()
    problems = checker.check(root, 0)
    assert len(problems) == 1
    assert "docs/ROADMAP.md" in problems[0]
    assert _run_main(root) == 1


def test_phase2_requires_api_and_security_cumulatively(root):
    _complete_tree(root, phase=0)
    docs = checker.required_docs(2)
    assert set(checker.required_docs(0)) <= set(docs)
    assert {"docs/API.md", "docs/SECURITY.md"} <= set(docs)
    problems = checker.check_required(root, 2)
    assert len(problems) == 2
    assert any("docs/API.md" in p for p in problems)
    assert any("docs/SECURITY.md" in p for p in problems)
    assert _run_main(root, phase=2) == 1


def test_ears_clause_in_requirements_v2_flagged(root):
    _complete_tree(root)
    _write(
        root,
        checker.REQUIREMENTS_V2,
        "# Requirements\n\nWHEN a user logs in, THE System SHALL record the event.\n",
    )
    problems = checker.check_duplication(root)
    assert len(problems) == 1
    assert "EARS clause" in problems[0]
    assert ":3:" in problems[0]
    assert _run_main(root) == 1


def test_verbatim_spec_line_flagged(root):
    _complete_tree(root)
    assert len(SPEC_LINE) >= checker.MIN_DUP_LEN
    _write(root, checker.REQUIREMENTS_V2, f"# Requirements\n\n  {SPEC_LINE}\n")
    problems = checker.check_duplication(root)
    assert len(problems) == 1
    assert "verbatim copy" in problems[0]


def test_short_pointer_doc_passes(root):
    _complete_tree(root)
    _write(
        root,
        checker.REQUIREMENTS_V2,
        "# Requirements V2\n\nFormal requirements live in "
        ".kiro/specs/neuropath-platform/requirements.md.\n",
    )
    assert checker.check_duplication(root) == []


def test_undocumented_env_keys_reported(root):
    _complete_tree(root)
    _write(
        root,
        "apps/api/.env.example",
        "DATABASE_URL=x\n# SECRET_KEY=\n# OPTIONAL_FLAG=\nNEW_KEY=1\n",
    )
    assert checker.env_keys(root) == {"DATABASE_URL", "SECRET_KEY", "OPTIONAL_FLAG", "NEW_KEY"}
    problems = checker.check_env(root)
    assert len(problems) == 2
    assert any(p.endswith(": NEW_KEY") for p in problems)
    assert any(p.endswith(": OPTIONAL_FLAG") for p in problems)
    assert _run_main(root) == 1


def test_documented_env_keys_pass(root):
    _complete_tree(root)
    assert checker.check_env(root) == []


def test_real_repository_passes_phase0():
    assert checker.check(_REPO_ROOT, 0) == []
