# Architecture

Status: Phase 0. This document records the stack, the architectural rules in force, the decisions made so far, and deviations from the layout in R1. Requirements: R1, R2, R3, R7, R8, R55 in [the canonical requirements](../.kiro/specs/neuropath-platform/requirements.md). Detailed design: [design.md](../.kiro/specs/neuropath-platform/design.md).

## Stack

| Layer | Technology |
|---|---|
| Web_App (`apps/web`) | Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, React Flow (`@xyflow/react` is already a dependency; diagrams that use it are built in Phase 3) |
| API (`apps/api`) | Python, FastAPI, Pydantic, SQLAlchemy, Alembic |
| Database | PostgreSQL (local: `postgres:16-alpine` in Docker Compose; target: Amazon RDS per R2.3) |
| File storage | Local filesystem adapter (target: Amazon S3 per R2.3) |
| Shared packages | `packages/design-tokens`, `packages/ui`, `packages/api-client` |

The Web_App holds no secrets and calls no privileged AWS service (R2.8). It reaches the API through the server-only `API_BASE_URL` setting.

Later-phase components (Data_Engine with Pandas, Polars and PyArrow; Agent_Runtime with Amazon Bedrock and Strands Agents) are not yet implemented. An AWS service listed in R2.5 is used only when a requirement needs it and its purpose is recorded here (R7.5). No AWS resources exist or are deployed at this stage.

## API layering

- `api/`: routers and HTTP wiring.
- `services/`: business logic; all status changes go through the transition engine (`services/transitions.py`, guards in `services/guards.py`).
- `repositories/`: data access with Organization scoping.
- `models/`: SQLAlchemy models; `models/status/` holds one transition table per entity, generated from Appendix A.
- `schemas/`: Pydantic request and response schemas.
- `workers/`: background job processing.
- `alembic/`: migrations; every schema change goes through Alembic (R6.2). Phase 0 has the `0001_baseline` migration.

## Integration interfaces and local adapters

External services sit behind interfaces in `apps/api/core/integrations/interfaces.py` (R3.3 to R3.5). Local adapters in `core/integrations/local.py` let the platform run without cloud accounts:

| Interface | Local adapter | Stands in for |
|---|---|---|
| `StorageClient` | `FilesystemStorage` (keys confined to a root directory) | S3 |
| `AuthProvider` | `LocalDevAuthProvider` (HMAC-signed tokens, only when `ENVIRONMENT=local`) | Cognito |
| `MalwareScanner` | `StubMalwareScanner` (always returns `unavailable`, so files stay quarantined) | Malware scanning service |
| `EmailSender` | `OutboxEmailSender` (appends to a JSONL outbox; nothing is sent) | Email service |
| `ModelClient` | `RecordedModelClient` (recorded responses; no Bedrock call) | Amazon Bedrock |

`core/integrations/registry.py` records which local substitution is active. No adapter reports success when the underlying operation failed; failures raise an `IntegrationError` subclass.

## Status transition engine

Every status change for every entity goes through one engine (R8):

- Transition tables are data. Each row holds from status, to status, allowed roles, guard names, and the phase that enables it.
- The `PLATFORM_PHASE` setting and Feature_Flags decide whether a row is active. A row for a phase not yet reached is rejected like an undefined transition.
- Guards are named pure functions over loaded state that return pass or fail with a reason.
- An accepted transition writes an Audit_Log entry in the same transaction.
- No endpoint writes a status field directly; update schemas exclude status.

## Lab isolation rule

Labs are independent modules (R1.4, R55). Core modules (`inquiries`, `projects`, `proposals`, `identity`) must never import a Lab module (anything under `labs`); Labs may import core modules.

- API: `scripts/check_lab_imports.py` enforces the rule (`python scripts/dev.py check lab-imports`), and CI fails on a violation (R55.9).
- Web: an ESLint `no-restricted-imports` rule in `apps/web/eslint.config.mjs` enforces the same rule.

## Decisions

### Infrastructure as code tool (A-10, R2.6)

Status: **decided.** The Founder chose **AWS CDK (TypeScript)**. The app lives in `infrastructure/cdk/` (npm workspace `@neuropath/infrastructure`); `infrastructure/` also holds the local `docker-compose.yml`.

Alternatives considered:

| Option | Why not chosen |
|---|---|
| Terraform | Adds HCL and a separate state backend to manage; no shared language with the web app. |
| Plain CloudFormation | Verbose YAML/JSON with no L2 constructs and no type checking. |

Rationale for CDK: it uses TypeScript, the same language as the Web_App and the shared design tokens package; L2 constructs provide secure defaults; cdk-nag (`AwsSolutionsChecks`) checks every synth.

Rules:

- CI and local commands run `typecheck` and `synth` only, with placeholder context and no AWS credentials. Deploying (and bootstrapping) requires the Founder's written authorization (R3.6).
- Stack layout: one `FoundationStack` per environment (`NeuroPath-Foundation-<env>`). Its first resource is the monthly cost budget; later resources are added after it.
- Default tags on every resource: `project=neuropath`, `environment=<env>`, `owner=<owner>`.
- Context keys are listed in `ENVIRONMENT.md` (CDK context).

### Background jobs in Phase 0 to 1

The ENGINE worker runs in-process inside the API container (A-27), as configured in `infrastructure/docker-compose.yml`. Appendix C of the requirements records the triggers for moving to managed queue services.

## Layout deviations (R1.5)

| Deviation | Rationale |
|---|---|
| No root `.env.example`. The API example lives at `apps/api/.env.example` and the web example at `apps/web/.env.example`. | Each app owns its settings; the web example contains no secrets, and keeping files per app avoids mixing server and browser settings. |
| `scripts/dev.py` is the command runner. A `Makefile` exists, but `dev.py` is the cross-platform entry point. | `make` is not available by default on Windows; Python is already required for the API. |
| npm workspaces (`apps/web`, `packages/*`) instead of pnpm. | npm ships with Node.js, so no extra tool is needed. |
| `data_engine` and `agents` directories do not exist yet. | R1.3 requires creating them only in the phase that first needs them. |
