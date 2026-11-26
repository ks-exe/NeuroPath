"""Unit tests for scripts/check_lab_imports.py (R1.4)."""
import contextlib
import importlib.util
import io
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "check_lab_imports.py"
_spec = importlib.util.spec_from_file_location("check_lab_imports", _SCRIPT)
checker = importlib.util.module_from_spec(_spec)
sys.modules["check_lab_imports"] = checker
_spec.loader.exec_module(checker)


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


def _run_main(root: Path) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return checker.main([str(root)])


def test_lab_importing_core_is_allowed(root):
    _write(root, "labs/lab_a.py", "from projects import service\nimport inquiries\n")
    _write(root, "projects/service.py", "import os\n")
    assert checker.check(root) == []
    assert _run_main(root) == 0


@pytest.mark.parametrize(
    "source,imported",
    [
        ("import labs.x\n", "labs.x"),
        ("from labs.x import y\n", "labs.x"),
        ("from . import labs\n", "labs"),
    ],
)
def test_core_importing_lab_is_violation(root, source, imported):
    _write(root, "projects/service.py", "import os\n" + source)
    violations = checker.check(root)
    assert len(violations) == 1
    v = violations[0]
    assert v.file == "projects/service.py"
    assert v.line == 2
    assert imported in v.imported
    assert _run_main(root) == 1


def test_non_core_file_may_import_lab(root):
    _write(root, "api/main.py", "import labs.x\n")
    assert checker.check(root) == []


def test_skipped_dirs_ignored(root):
    _write(root, "projects/__pycache__/bad.py", "import labs.x\n")
    assert checker.check(root) == []
