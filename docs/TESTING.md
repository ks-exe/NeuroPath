# Testing

## Stack

| Area | Tools |
|---|---|
| API (Python) | pytest, Hypothesis (property tests), httpx (API client tests) |
| Web_App (TypeScript) | Vitest, Testing Library, jsdom, fast-check (property tests) |
| Browser checks | Playwright with axe (planned for Phase 1; not yet installed) |

## Property test conventions (R77.13)

- Every property test runs at least 100 iterations: `@settings(max_examples=100)` in Hypothesis, `fc.assert(..., { numRuns: 100 })` in fast-check.
- Every property test carries a comment naming its design property and requirement clause, for example:

  ```python
  # Property 6: Status transition validity
  # Validates: Requirements 8.7
  ```

- Implement only the properties numbered in `design.md`. Generators should constrain inputs to the valid domain instead of filtering most cases out.
- Tests use real code paths. Fakes are allowed only for external services, through the local adapters.

The only property test so far is in `apps/web/src/lib/api-client.test.ts` (every accepted path stays under `/api/v1`, Requirements 2.8, 100 runs). It is not one of the numbered design properties. No Hypothesis tests exist yet; the first planned one is task 4.3 (Property 6).

## Current test files

| File | Covers |
|---|---|
| `apps/api/tests/test_health.py` | `/api/v1/health` returns OK and is the only `/api/` route |
| `apps/api/tests/test_config.py` | Env secrets provider fails closed, AWS provider with an injected fake client, `PLATFORM_PHASE` from env, provider selection |
| `apps/api/tests/test_database.py` | `TenantOwned` column is NOT NULL and indexed, `transaction()` commit and rollback, single empty Alembic head |
| `apps/api/tests/test_integrations_local.py` | Local adapters: stub scanner never reports clean, local auth refuses non-local, outbox reports "recorded locally" |
| `apps/api/tests/test_check_lab_imports.py` | Lab import check with allowed and violating fixture trees |
| `apps/api/tests/test_migrations_roundtrip.py` | Migration round trip on SQLite, non-empty database rejection, schema diff, PostgreSQL round trip (gated) |
| `apps/web/src/lib/api-client.test.ts` | API client: calls `/api/v1/health`, maps the error envelope to `ApiError`, rejects absolute URLs and dot segments, property test on path building |

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
