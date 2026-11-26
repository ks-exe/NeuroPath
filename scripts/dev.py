"""Cross-platform dev runner: one command per check for each app.

Usage:
    python scripts/dev.py api  lint|typecheck|test|build
    python scripts/dev.py web  lint|typecheck|test|build
    python scripts/dev.py infra typecheck|synth
    python scripts/dev.py check lab-imports|docs|migrations [ARGS...]
    python scripts/dev.py gate --phase N [ARGS...]
    python scripts/dev.py all [--skip-build]
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = ROOT / "apps" / "api"
WEB = ROOT / "apps" / "web"
INFRA = ROOT / "infrastructure" / "cdk"
PY = sys.executable
NPM = "npm.cmd" if sys.platform == "win32" else "npm"

Cmd = tuple[list[str], Path]

COMMANDS: dict[str, dict[str, Cmd]] = {
    "api": {
        "lint": ([PY, "-m", "ruff", "check", "."], API),
        "typecheck": ([PY, "-m", "mypy"], API),
        "test": ([PY, "-m", "pytest", "-p", "no:cacheprovider"], API),
        "build": (["docker", "build", "-t", "neuropath-api", "."], API),
    },
    "web": {
        "lint": ([NPM, "run", "lint"], WEB),
        "typecheck": ([NPM, "run", "typecheck"], WEB),
        "test": ([NPM, "run", "test"], WEB),
        "build": ([NPM, "run", "build"], WEB),
    },
    # CDK app: synth only, never deploy (R3.6). Synth uses placeholder
    # context and needs no AWS credentials.
    "infra": {
        "typecheck": ([NPM, "run", "typecheck"], INFRA),
        "synth": ([NPM, "run", "synth"], INFRA),
    },
}

CHECKS: dict[str, Cmd] = {
    "lab-imports": ([PY, str(ROOT / "scripts" / "check_lab_imports.py")], ROOT),
    "docs": ([PY, str(ROOT / "scripts" / "check_docs.py")], ROOT),
    "migrations": ([PY, str(ROOT / "scripts" / "check_migrations.py")], ROOT),
}

# Phase gate (R78): run manually, not part of `all` or CI, because the
# recorded CI result is one of its inputs.
GATE: Cmd = ([PY, str(ROOT / "scripts" / "phase_gate.py")], ROOT)


def run(label: str, cmd: Cmd) -> int:
    args, cwd = cmd
    print(f"\n==> {label}: {' '.join(args)}  (cwd={cwd})", flush=True)
    if shutil.which(args[0]) is None and not Path(args[0]).exists():
        print(f"missing executable: {args[0]}", file=sys.stderr)
        return 127
    return subprocess.call(args, cwd=cwd)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    sub = p.add_subparsers(dest="group", required=True)
    for app, cmds in COMMANDS.items():
        sp = sub.add_parser(app)
        sp.add_argument("action", choices=list(cmds))
    sp = sub.add_parser("check")
    sp.add_argument("action", choices=list(CHECKS))
    sp.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="passed through (e.g. DATABASE_URL for migrations, --phase N for docs)",
    )
    sp = sub.add_parser("gate", help="phase gate check and report (R78)")
    sp.add_argument("--phase", type=int, required=True)
    sp.add_argument("extra", nargs=argparse.REMAINDER,
                    help="passed through (--ci-status, --database-url, --report)")
    sp = sub.add_parser("all")
    sp.add_argument("--skip-build", action="store_true", help="skip image/next builds and CDK synth")
    a = p.parse_args(argv)

    if a.group == "all":
        failed: list[str] = []
        steps: list[tuple[str, Cmd]] = [(f"check {k}", v) for k, v in CHECKS.items()]
        for action in ("lint", "typecheck", "test", "build", "synth"):
            if action in ("build", "synth") and a.skip_build:
                continue
            for app, cmds in COMMANDS.items():
                if action in cmds:
                    steps.append((f"{app} {action}", cmds[action]))
        for label, cmd in steps:
            if run(label, cmd) != 0:
                failed.append(label)
        print("\nFAILED: " + ", ".join(failed) if failed else "\nAll checks passed.")
        return 1 if failed else 0
    if a.group == "gate":
        args, cwd = GATE
        return run("gate", ([*args, "--phase", str(a.phase), *a.extra], cwd))
    if a.group == "check":
        args, cwd = CHECKS[a.action]
        return run(f"check {a.action}", ([*args, *a.extra], cwd))
    return run(f"{a.group} {a.action}", COMMANDS[a.group][a.action])


if __name__ == "__main__":
    sys.exit(main())
