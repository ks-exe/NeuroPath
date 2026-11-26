# Implementation Status

Current phase: **Phase 0 (Foundation)**, in progress. Task numbers refer to `.kiro/specs/neuropath-platform/tasks.md`.

## Phase 0 by task area

| Area | Status | What exists |
|---|---|---|
| 1. Monorepo structure | Done | `apps/web`, `apps/api` (with `api/`, `core/`, `models/`, `schemas/`, `services/`, `repositories/`, `workers/`, `tests/`), `packages/`, `infrastructure/`, `docs/`, `scripts/`; FastAPI app with `/api/v1/health`; Next.js App Router skeleton; `packages/api-client`; Lab import check (`scripts/check_lab_imports.py` and ESLint rule) with tests |
| 2. Configuration, secrets, integrations | Done | `core/config.py` (settings, `PLATFORM_PHASE`, env and AWS Secrets Manager providers, the latter code only); interfaces and local adapters in `core/integrations/`; substitution registry; tests |
| 3. Database baseline | Done | Declarative base, naming conventions, mixins, `transaction()`; Alembic environment and empty `0001_baseline`; `scripts/check_migrations.py`; round-trip tests (PostgreSQL test gated by `TEST_POSTGRES_URL`) |
| 4. Status Transition Engine | Done | Status tables per entity in `models/status/`; `transition()` with guards and phase enablement in `services/transitions.py` and `services/guards.py`; property test (4.3) and table unit tests (4.4) |
| 5. Local environment, commands, CI | Done | Compose file and Dockerfiles (5.1); `scripts/dev.py` and `Makefile` (5.2); CI pipeline `.github/workflows/ci.yml` with lint, type check, tests with PostgreSQL, Lab import check, migration round-trip check, gitleaks (5.3); AWS CDK skeleton in `infrastructure/cdk/` (`FoundationStack` with the cost budget, default tags, cdk-nag) and the CI `infra` job running typecheck and synth only (5.4) |
| 6. Design system foundation | Done | `packages/design-tokens`, Tailwind configuration, fonts via `next/font`; base primitives in `packages/ui`; token and primitive tests (6.3) |
| 7. Documentation set | In progress | Phase 0 documents in `README.md` and `docs/`. Not yet: `scripts/check_docs.py` (7.2) and its tests (7.3) |
| 8. Phase 0 gate | Not started | `scripts/phase_gate.py` |

## Active local substitutions

From `LOCAL_SUBSTITUTIONS` in `apps/api/core/integrations/registry.py`:

| Interface | Local adapter | Deployed target | Note |
|---|---|---|---|
| `StorageClient` | `FilesystemStorage` | Private Amazon S3 buckets | |
| `AuthProvider` | `LocalDevAuthProvider` | Amazon Cognito | Enabled only when `ENVIRONMENT=local` |
| `MalwareScanner` | `StubMalwareScanner` | Not yet chosen (A-16) | Always reports unavailable; files stay quarantined |
| `EmailSender` | `OutboxEmailSender` | Email provider (Appendix C) | Writes to outbox file/log |
| `ModelClient` | `RecordedModelClient` | Amazon Bedrock | Recorded responses; no Bedrock call |

`SecretsProvider` uses `EnvSecretsProvider` locally; `AwsSecretsManagerProvider` exists as code only. No AWS resources are provisioned.

## Known issues

- **CDK budget values are placeholders:** `npm run synth` uses `budgetLimitUsd=1` and `budgetAlertEmail=placeholder@example.invalid`. The Founder must provide the real budget amount and alert email at deploy time. Nothing is deployed, and deploying requires the Founder's written authorization.
- **CI not yet run on GitHub:** the workflow parses as valid YAML but has not run on a hosted runner yet.
- **`check migrations` without a database:** with no explicit URL it targets local PostgreSQL. It was observed to hang when PostgreSQL was not running. The script now probes the connection with a 5-second `connect_timeout` before running; confirm this on the next run without PostgreSQL. Pass an explicit URL (for example SQLite) to run it without PostgreSQL.
- **Fonts fetched at build time:** `apps/web/src/app/fonts.ts` uses `next/font/google`, so `next build` downloads Playfair Display, Manrope, and IBM Plex Mono from Google. Builds without network access fail.
- **npm audit:** `npm install` reported 8 vulnerabilities. They have not yet been triaged.
- **`PLATFORM_PHASE` default is 1** although Phase 0 is current; the setting has a minimum of 1.
