# Development

## Prerequisites

- Python 3.11 or later
- Node.js 20 or later (npm workspaces: `apps/web`, `packages/*`)
- Docker with Compose (for the local stack and image builds)

## Setup

```
# API
cd apps/api
python -m pip install -e ".[dev]"
copy .env.example .env        # Windows; use cp on macOS/Linux. Optional.

# Web_App and shared packages (from the repo root)
npm install
copy apps\web\.env.example apps\web\.env.local   # optional
```

## Commands

`scripts/dev.py` is the cross-platform runner. The `Makefile` wraps the same commands with identical names (`make api-lint`, `make web-test`, `make infra-synth`, `make check-migrations`, `make all`).

| Command | Runs |
|---|---|
| `python scripts/dev.py api lint` | `ruff check .` in `apps/api` |
| `python scripts/dev.py api typecheck` | `mypy` (strict) in `apps/api` |
| `python scripts/dev.py api test` | `pytest -p no:cacheprovider` in `apps/api` |
| `python scripts/dev.py api build` | `docker build -t neuropath-api .` in `apps/api` |
| `python scripts/dev.py web lint` | `npm run lint` (ESLint) in `apps/web` |
| `python scripts/dev.py web typecheck` | `npm run typecheck` (`tsc --noEmit`) |
| `python scripts/dev.py web test` | `npm run test` (`vitest --run`) |
| `python scripts/dev.py web build` | `npm run build` (`next build`) |
| `python scripts/dev.py infra typecheck` | `npm run typecheck` (`tsc --noEmit`) in `infrastructure/cdk` |
| `python scripts/dev.py infra synth` | `npm run synth` (`cdk synth` with placeholder context, no AWS credentials; never deploys) |
| `python scripts/dev.py check lab-imports` | `scripts/check_lab_imports.py` |
| `python scripts/dev.py check docs [--phase N]` | `scripts/check_docs.py` (documentation consistency check) |
| `python scripts/dev.py check migrations [URL]` | `scripts/check_migrations.py` (round trip, see `DATABASE.md`) |
| `python scripts/dev.py all [--skip-build]` | All checks, then lint, typecheck, test, and build for both apps, plus infra typecheck and synth; `--skip-build` skips the builds and synth; prints the failed steps |

Run `python scripts/dev.py all --skip-build` before finishing a change.

## Local stack (Docker Compose)

From the repo root:

```
docker compose -f infrastructure/docker-compose.yml up --build
```

| Service | Port (bound to 127.0.0.1) | Notes |
|---|---|---|
| `postgres` | 5432 | `postgres:16-alpine`, volume `postgres-data` |
| `api` | 8000 | FastAPI; the ENGINE worker runs in-process (A-27); volumes `local-storage`, `local-outbox` |
| `web` | 3000 | Next.js; calls the API at `http://api:8000` server-side |

Compose creates no cloud resources. Variables are listed in `ENVIRONMENT.md`.

## Migration check without a running database

`check migrations` defaults to `Settings.database_url` (local PostgreSQL). When PostgreSQL is not running, the script reports the database as unreachable after a 5-second connect timeout and exits 1. To run the check without PostgreSQL, pass an explicit URL to an empty database:

```
python scripts/dev.py check migrations sqlite:///C:/temp/roundtrip.db
```

The script refuses to run on a database that already has tables.

## CI

`.github/workflows/ci.yml` runs on every push and pull request, with `permissions: contents: read`. It has four jobs:

- **api** (Python 3.12, `postgres:16` service): `api lint`, `api typecheck`, `api test` with `TEST_POSTGRES_URL` set so the PostgreSQL round-trip test runs, `check lab-imports`, `check docs`, then `check migrations` against a freshly created empty database (`migration_check`).
- **web** (Node 20): `npm ci` at the repo root, then `web lint`, `web typecheck`, `web test`, `web build`. `next build` downloads Google fonts, so it needs network access.
- **infra** (Node 20, Python 3.12): `npm ci` at the repo root, then `infra typecheck` and `infra synth`. Synth uses placeholder context; the job never deploys.
- **secrets**: gitleaks scans the full git history and fails on any finding.

CI makes no Bedrock or AWS calls. No AWS credentials are configured and there is no deploy job (R3.6).

To reproduce the api job locally, start PostgreSQL (`docker compose -f infrastructure/docker-compose.yml up -d postgres`), set `TEST_POSTGRES_URL`, and run the same `scripts/dev.py` commands.

## Windows notes

- pytest runs with `-p no:cacheprovider` because writing `.pytest_cache` can fail with permission errors on some Windows setups.
- pytest's `tmp_path` fixture can hit the same permission issue on Windows. Tests that need a temporary directory use `tempfile.mkdtemp()` with explicit cleanup (see `tests/test_migrations_roundtrip.py`).
- `scripts/dev.py` calls `npm.cmd` on Windows automatically.
