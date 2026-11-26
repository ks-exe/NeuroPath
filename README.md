# NEUROPATH

Monorepo for the NEUROPATH platform: the public company website, client acquisition and Founder CRM, solution discovery and proposals, project delivery, Labs, and the internal OPS and ENGINE automation. The work is delivered in phases 0 to 6 (see [docs/ROADMAP.md](docs/ROADMAP.md)). The canonical requirements are in [.kiro/specs/neuropath-platform/requirements.md](.kiro/specs/neuropath-platform/requirements.md).

No cloud resources are provisioned by this repository. Local development uses local adapters for storage, auth, email, malware scanning and AI models.

## Layout

| Path | Contents |
|---|---|
| `apps/api` | FastAPI backend: `api` (routers), `core` (config, database, integrations), `models` (SQLAlchemy models, status tables), `schemas`, `services` (transition engine, guards), `repositories`, `workers`, `tests`, `alembic` (migrations) |
| `apps/web` | Next.js web app (TypeScript, Tailwind CSS, shadcn/ui) |
| `packages` | Shared code: `design-tokens`, `ui`, `api-client` |
| `infrastructure` | `docker-compose.yml` for the local stack |
| `scripts` | `dev.py` command runner, `check_lab_imports.py`, `check_migrations.py` |
| `docs` | Project documentation; `docs/archive` holds the V1 requirements |

## Prerequisites

- Python 3.11+
- Node.js 20+ and npm
- Docker (for the Compose stack and the API image build)

## Quick start

Install dependencies:

```sh
pip install -e "apps/api[dev]"   # API plus lint, type and test tools
npm install                      # npm workspaces: apps/web and packages/*
```

Copy the example environment files and adjust local values:

- `apps/api/.env.example` to `apps/api/.env`
- `apps/web/.env.example` to `apps/web/.env.local`

Run checks with the cross-platform runner:

```sh
python scripts/dev.py api  lint|typecheck|test|build
python scripts/dev.py web  lint|typecheck|test|build
python scripts/dev.py check lab-imports|docs|migrations
python scripts/dev.py all [--skip-build]
```

Start the local stack (PostgreSQL, API on port 8000, web on port 3000, bound to 127.0.0.1):

```sh
docker compose -f infrastructure/docker-compose.yml up --build
```

## Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): stack, integrations, status transitions, Lab isolation, layout deviations
- [docs/ROADMAP.md](docs/ROADMAP.md): phases and the phase gate rule
- [docs/MVP_SCOPE.md](docs/MVP_SCOPE.md): MVP scope
- [docs/REQUIREMENTS_V2.md](docs/REQUIREMENTS_V2.md): pointer to the canonical requirements
- [docs/CHANGELOG_V1_TO_V2.md](docs/CHANGELOG_V1_TO_V2.md): V1 to V2 changes
