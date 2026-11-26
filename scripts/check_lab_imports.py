#!/usr/bin/env python3
"""Lab dependency import check (R1.4, R55.9).

Core modules (inquiries, projects, proposals, identity) must never import a
Lab module (anything under ``labs``). Labs may import core modules.

Usage:  python scripts/check_lab_imports.py [ROOT]
ROOT defaults to the repository root. Exit code 0 = clean, 1 = violations.

Library usage: ``check(root)`` returns a list of ``Violation``.
The web side is enforced by an ESLint ``no-restricted-imports`` rule in
``apps/web/eslint.config.mjs``.
"""
from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

CORE_MODULES = frozenset({"inquiries", "projects", "proposals", "identity"})
LAB_PACKAGE = "labs"
SKIP_DIRS = frozenset({"__pycache__", ".venv", "venv", "node_modules", ".git", ".pytest_cache"})


@dataclass(frozen=True)
class Violation:
    file: str
    line: int
    imported: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: core module imports Lab module '{self.imported}'"


def _is_core_file(rel: Path) -> bool:
    """A file is core if a directory segment or its own stem is a core module name."""
    return any(p in CORE_MODULES for p in rel.parts[:-1]) or rel.stem in CORE_MODULES


def _is_lab_name(dotted: str) -> bool:
    return LAB_PACKAGE in dotted.split(".")


def _lab_imports(tree: ast.AST) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _is_lab_name(alias.name):
                    found.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            prefix = "." * node.level
            if module and _is_lab_name(module):
                found.append((node.lineno, prefix + module))
            else:
                # `from . import labs`, `from api import labs`
                for alias in node.names:
                    if alias.name == LAB_PACKAGE:
                        found.append((node.lineno, f"{prefix}{module}.{alias.name}".replace("..", ".", 0)))
    return found


def check(root: str | Path) -> list[Violation]:
    """Scan every .py file under ``root`` and return Lab-import violations in core files."""
    root = Path(root)
    violations: list[Violation] = []
    for path in sorted(root.rglob("*.py")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts) or not _is_core_file(rel):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as exc:
            violations.append(Violation(rel.as_posix(), getattr(exc, "lineno", 0) or 0, f"<unparseable: {exc}>"))
            continue
        for line, name in _lab_imports(tree):
            violations.append(Violation(rel.as_posix(), line, name))
    return violations


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    root = Path(args[0]) if args else Path(__file__).resolve().parent.parent / "apps" / "api"
    violations = check(root)
    for v in violations:
        print(v, file=sys.stderr)
    if violations:
        print(f"Lab import check FAILED: {len(violations)} violation(s).", file=sys.stderr)
        return 1
    print("Lab import check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
