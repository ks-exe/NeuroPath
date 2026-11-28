# Implementation Status

Current phase: **Phase 0 (Foundation)** approved by the Founder on 2026-11-26, on condition that the CI result is recorded and the gate re-run (see Known issues). **Phase 1** is next. Task numbers refer to `.kiro/specs/neuropath-platform/tasks.md`.

## Phase 0 by task area

| Area | Status | What exists |
|---|---|---|
| 1. Monorepo structure | Done | `apps/web`, `apps/api` (with `api/`, `core/`, `models/`, `schemas/`, `services/`, `repositories/`, `workers/`, `tests/`), `packages/`, `infrastructure/`, `docs/`, `scripts/`; FastAPI app with `/api/v1/health`; Next.js App Router skeleton; `packages/api-client`; Lab import check (`scripts/check_lab_imports.py` and ESLint rule) with tests |
| 2. Configuration, secrets, integrations | Done | `core/config.py` (settings, `PLATFORM_PHASE`, env and AWS Secrets Manager providers, the latter code only); interfaces and local adapters in `core/integrations/`; substitution registry; tests |
| 3. Database baseline | Done | Declarative base, naming conventions, mixins, `transaction()`; Alembic environment and empty `0001_baseline`; `scripts/check_migrations.py`; round-trip tests (PostgreSQL test gated by `TEST_POSTGRES_URL`) |
| 4. Status Transition Engine | Done | Status tables per entity in `models/status/`; `transition()` with guards and phase enablement in `services/transitions.py` and `services/guards.py`; property test (4.3) and table unit tests (4.4) |
| 5. Local environment, commands, CI | Done | Compose file and Dockerfiles (5.1); `scripts/dev.py` and `Makefile` (5.2); CI pipeline `.github/workflows/ci.yml` with lint, type check, tests with PostgreSQL, Lab import check, migration round-trip check, gitleaks (5.3); AWS CDK skeleton in `infrastructure/cdk/` (`FoundationStack` with the cost budget, default tags, cdk-nag) and the CI `infra` job running typecheck and synth only (5.4) |
| 6. Design system foundation | Done | `packages/design-tokens`, Tailwind configuration, fonts via `next/font`; base primitives in `packages/ui`; token and primitive tests (6.3) |
| 7. Documentation set | Done | Phase 0 documents in `README.md` and `docs/`; `scripts/check_docs.py` (7.2) run in CI; its tests (7.3) |
| 8. Phase 0 gate | Done | `scripts/phase_gate.py`; report `docs/phase-reports/phase-0.md` (gate run 2026-11-26: all checks pass except ci-status NOT RECORDED); Founder approval recorded with the CI condition |

## Phase 1 by task area

| Area | Status | What exists |
|---|---|---|
| 10. Public layout and content source | Done | Typed content in `apps/web/content/` with loaders that return only verified projects, confirmed statements and published articles; global header, navigation (menu below 768 px, `aria-current`, Sign In behind `authEnabled`, off) and footer; tests (10.2, 10.4) |
| 11. Public pages | Done | Homepage, Services with details and `serviceHint`, Solutions, Projects, How We Work, About, Insights, styled 404; page content tests (11.4) |
| 12. API foundation and inquiry intake | Done | Error envelope, request id, JSON logs; migrations `0002_phase1` and `0003_audit_append_only`; `AuditService`; Lead upsert with email normalization; `POST /api/v1/public/inquiries/submission-token` and `POST /api/v1/public/inquiries` (honeypot, sanitization, length limits, per-IP rate limit, idempotent token, local notification only); unit and property tests (12.5, 12.7 to 12.9) |
| 13. Project inquiry form | Done | Form page with all R14.1 fields, client validation, live-region errors, pending state, honeypot; component tests (13.2) |
| 14. SEO, accessibility, performance | Done except optional 14.3, 14.4 | Per-page metadata, `sitemap.ts`, `robots.ts`, one `h1` per page; jsdom accessibility and contrast tests. Playwright with axe (14.3) and Lighthouse CI (14.4) are not set up |
| 15. Phase 1 gate | In progress | `scripts/phase_gate.py --phase 1` re-runs every Phase 0 check and adds public-pages, inquiry-storage, v1-tagline, accessibility (jsdom only) and lighthouse (recorded file only); writes `docs/phase-reports/phase-1.md` |

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
- **CI result not verified:** the repository was pushed to GitHub (commit `cd4f140`), which should have triggered the workflow, but no run result has been seen or recorded.
- **`check migrations` without a database:** with no explicit URL it targets local PostgreSQL. It was observed to hang when PostgreSQL was not running. The script now probes the connection with a 5-second `connect_timeout` before running; confirm this on the next run without PostgreSQL. Pass an explicit URL (for example SQLite) to run it without PostgreSQL.
- **Fonts fetched at build time:** `apps/web/src/app/fonts.ts` uses `next/font/google`, so `next build` downloads Playfair Display, Manrope, and IBM Plex Mono from Google. Builds without network access fail.
- **npm audit:** `npm install` reported 8 vulnerabilities. They have not yet been triaged.
- **`PLATFORM_PHASE` default is 1** although Phase 0 is current; the setting has a minimum of 1.
- **Phase 0 approved with CI unverified:** Phase 0 approved by the Founder with CI unverified; record the first CI result in docs/phase-reports/ci-status.json and re-run the gate.
- **Phase 1 copy pending Founder review:** all public copy marked COPY FOR FOUNDER REVIEW, the consent wording (A-11 open), the R12.10 service detail content, and the contact details shown on the site need Founder review before release.
- **`SITE_URL` is read at build time:** pages are statically rendered, so canonical, Open Graph, sitemap and robots URLs use the value present during `next build`. Each environment needs its own build.
- **Inquiry rate limit is single-process:** the per-IP counter is in memory, so it is not shared across API processes or restarts.
- **Playwright and Lighthouse not set up:** optional tasks 14.3 and 14.4 are not done. Accessibility checks are jsdom-level only, and the Phase 1 gate reports lighthouse NOT RECORDED until `docs/phase-reports/lighthouse.json` is recorded.
- **CI result not recorded for Phase 1:** the Phase 1 gate reports ci-status NOT RECORDED until `docs/phase-reports/ci-status.json` exists.

## Log

- **2026-11-26:** Phase 0 gate run: structure, migrations, docs, lab-imports and deploy-authorization pass; ci-status NOT RECORDED (CI for commit cd4f140 not verified). The Founder approved Phase 0 in the Kiro chat session with this CI condition. Phase 1 is next.
