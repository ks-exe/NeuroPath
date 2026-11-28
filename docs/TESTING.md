# Testing

## Stack

| Area | Tools |
|---|---|
| API (Python) | pytest, Hypothesis (property tests), httpx (API client tests) |
| Web_App (TypeScript) | Vitest, Testing Library, jsdom, fast-check (property tests) |
| Browser checks | Playwright with axe: not set up (optional task 14.3) |
| Lighthouse | Lighthouse CI: not set up (optional task 14.4) |

## Property test conventions (R77.13)

- Every property test runs at least 100 iterations: `@settings(max_examples=100)` in Hypothesis, `fc.assert(..., { numRuns: 100 })` in fast-check.
- Every property test carries a comment naming its design property and requirement clause, for example:

  ```python
  # Property 6: Status transition validity
  # Validates: Requirements 8.7
  ```

- Implement only the properties numbered in `design.md`. Generators should constrain inputs to the valid domain instead of filtering most cases out.
- Tests use real code paths. Fakes are allowed only for external services, through the local adapters.

Property tests exist in `test_transition_validity_property.py` (Property 6), `test_email_normalization_property.py`, `test_inquiry_properties.py` (submission idempotency, one Project per inquiry) and `apps/web/src/lib/api-client.test.ts` (paths stay under `/api/v1`).

## Current test files

### API (`apps/api/tests`)

| File | Covers |
|---|---|
| `test_health.py` | `/api/v1/health` returns OK |
| `test_config.py` | Env secrets provider fails closed, AWS provider with an injected fake client, `PLATFORM_PHASE` from env, provider selection |
| `test_database.py` | Base, mixins, `transaction()` commit and rollback, Alembic baseline (R6.2 to R6.5) |
| `test_integrations_local.py` | Local adapters: stub scanner never reports clean, local auth refuses non-local, outbox reports "recorded locally" |
| `test_check_lab_imports.py` | Lab import check with allowed and violating fixture trees (R1.4) |
| `test_check_docs.py` | `scripts/check_docs.py` (R5.1, R5.6) |
| `test_migrations_roundtrip.py` | Migration round trip on SQLite, non-empty database rejection, schema diff, PostgreSQL round trip (gated) |
| `test_transition_tables.py` | Code status tables match Appendix A (R8.1, R8.3, R8.6) |
| `test_transition_validity_property.py` | Property 6, status transition validity (R8.7) |
| `test_audit.py` | `AuditService` write path, redaction, rollback on audit failure, insert/read-only repository, transition hook; PostgreSQL append-only trigger (gated by `TEST_POSTGRES_URL`) (R6.9, R8.4, R30.1, R30.3 to R30.5) |
| `test_errors.py` | Request id handling, error envelope for 404/409/422/500, sensitive log fields dropped |
| `test_leads.py` | Email normalization and Lead upsert (R22.1, R22.4, R22.7, R22.10) |
| `test_email_normalization_property.py` | Property tests for `core/email.py` |
| `test_inquiries_service.py` | `InquiryService.submit` stores Lead, Project_Inquiry, Project and consent records (R14.3, R14.9 to R14.12, R14.14, R24.1) |
| `test_public_inquiries.py` | HTTP tests for the public inquiry endpoints (R14.3, R14.7, R14.8, R14.9, R14.14) |
| `test_intake_protections.py` | Per-IP rate limit, honeypot, single notification, control-character stripping, length limits, consent rows, rollback on audit failure (R14.7 to R14.10, R30.5) |
| `test_inquiry_properties.py` | Property tests: submission idempotency and one Project per inquiry |

### Web_App (`apps/web/src`)

| File | Covers |
|---|---|
| `lib/api-client.test.ts` | API client: `/api/v1` paths, error envelope to `ApiError`, rejects absolute URLs and dot segments, property test on path building |
| `design-system.test.ts` | Brand tokens, radius cap, motion cap, lint rule against gradients and glassmorphism (R4.2, R4.4, R4.5) |
| `ui-primitives.test.tsx` | `packages/ui` primitives |
| `content-loaders.test.ts` | Content loaders: verified projects, published articles, confirmed statements, service groups, capabilities |
| `components/site-header.test.tsx` | Header menu toggle, `aria-current`, Sign In flag, footer (R9.3 to R9.5) |
| `components/inquiry-form.test.tsx` | Inquiry form validation, API error mapping, success, pending state, service hint, honeypot (R14.4 to R14.6, R14.13) |
| `pages-content.test.tsx` | Every public page renders with exactly one h1 and no V1 tagline; homepage section order; 404 page (R10.1, R10.11, R13.7) |
| `seo.test.ts` | Unique metadata per page, sitemap and robots (R15) |
| `a11y.test.tsx` | Skip link, single main landmark, keyboard access and text alternatives on every public page (R15.4, R15.6) |
| `a11y-contrast.test.ts` | WCAG 2.2 AA contrast of design token pairings (R15.5) |

## Accessibility and Lighthouse

The accessibility checks run in jsdom (`a11y.test.tsx`, `a11y-contrast.test.ts`). They do not render in a browser and do not run axe. Playwright with axe (task 14.3) and Lighthouse CI (task 14.4) are optional and not set up.

The Phase 1 gate reads Lighthouse scores from `docs/phase-reports/lighthouse.json` (performance, accessibility, best-practices and seo, each at least 90 per R15.9). The gate never runs Lighthouse. Without that file the `lighthouse` check is NOT RECORDED and the gate fails.

## Running tests

```
python scripts/dev.py api test     # pytest -p no:cacheprovider in apps/api
python scripts/dev.py web test     # vitest --run in apps/web
python scripts/dev.py all --skip-build
```

A single API test file: `python -m pytest -p no:cacheprovider tests/test_config.py` from `apps/api`.

## PostgreSQL round-trip test

`test_round_trip_postgres_has_empty_diff` runs only when `TEST_POSTGRES_URL` is set; otherwise pytest skips it. It creates a fresh database with a random name, runs `upgrade head` and `downgrade base`, asserts an empty schema diff, and drops the database. The URL needs a user allowed to create databases, for example with the Compose stack running:

```
# PowerShell
$env:TEST_POSTGRES_URL = "postgresql+psycopg://neuropath:neuropath@localhost:5432/neuropath"
python scripts/dev.py api test
```
