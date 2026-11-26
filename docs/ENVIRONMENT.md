# Environment Variables

Sources: `apps/api/.env.example`, `apps/web/.env.example`, and `infrastructure/docker-compose.yml`. API settings are read by `apps/api/core/config.py` (pydantic-settings, also from `apps/api/.env`). Secrets are read through `SecretsProvider`: environment variables locally, AWS Secrets Manager in deployed environments (code only, not provisioned).

## API (`apps/api`)

| Variable | Purpose | Secret | Default |
|---|---|---|---|
| `ENVIRONMENT` | Runtime environment: `local`, `dev`, `staging`, `prod`. Local auth and the env secrets backend are enabled only for `local`. | No | `local` |
| `PLATFORM_PHASE` | Highest delivered platform phase. The transition engine enables rows with `enabled_phase <= PLATFORM_PHASE`. Minimum 1. | No | `1` |
| `DATABASE_URL` | SQLAlchemy database URL. | Yes in deployed environments | `postgresql+psycopg://neuropath:neuropath@localhost:5432/neuropath` (local only) |
| `AWS_REGION` | Region for the AWS Secrets Manager backend. Used only when that backend is active. | No | unset |
| `SECRETS_BACKEND` | `env` or `aws`. | No | `env` when `ENVIRONMENT=local`, otherwise `aws` |
| `LOCAL_STORAGE_PATH` | Root directory for the filesystem storage adapter. Set in Compose to `/data/storage` (volume `local-storage`). | No | Compose: `/data/storage` |
| `LOCAL_OUTBOX_PATH` | File the outbox email adapter writes to. Set in Compose to `/data/outbox/outbox.jsonl` (volume `local-outbox`). | No | Compose: `/data/outbox/outbox.jsonl` |

`LOCAL_STORAGE_PATH` and `LOCAL_OUTBOX_PATH` are set by Compose but are not yet read by `core/config.py`. The adapters currently receive their paths from the caller.

## Web_App (`apps/web`)

| Variable | Purpose | Secret | Default |
|---|---|---|---|
| `API_BASE_URL` | Base URL of the API, used server-side only. Never exposed to the browser. | No | `http://localhost:8000` (`.env.example`); `http://api:8000` in Compose |

No `NEXT_PUBLIC_*` variables exist. Secrets must never use that prefix.

## PostgreSQL (Compose `postgres` service)

| Variable | Purpose | Secret | Default |
|---|---|---|---|
| `POSTGRES_USER` | Database user; also used to build the API `DATABASE_URL` in Compose. | Local only | `neuropath` |
| `POSTGRES_PASSWORD` | Database password. | Yes outside local | `neuropath` (local only) |
| `POSTGRES_DB` | Database name. | No | `neuropath` |

Override these through the shell or an `.env` file next to the Compose file. The defaults are for local development only.

## CDK context (`infrastructure/cdk`)

Passed with `-c key=value` to `cdk synth`. These are CDK context values, not environment variables. `npm run synth` passes placeholders only; real values are supplied by the Founder at deploy time.

| Key | Purpose | Required | Default |
|---|---|---|---|
| `env` | Target environment: `dev`, `staging`, or `prod`. Names the stack and sets the `environment` tag. | No | `dev` |
| `owner` | Value of the `owner` tag. | No | `founder` |
| `account` | AWS account ID. The stack is environment-agnostic when unset. | No | unset |
| `region` | AWS region. The stack is environment-agnostic when unset. | No | unset |
| `budgetLimitUsd` | Monthly cost budget in US dollars (positive number). | Yes | none (synth placeholder `1`) |
| `budgetAlertEmail` | Email address for budget alerts. | Yes | none (synth placeholder `placeholder@example.invalid`) |

## Test-only

| Variable | Purpose | Secret | Default |
|---|---|---|---|
| `TEST_POSTGRES_URL` | Enables the PostgreSQL migration round-trip test (see `TESTING.md`). | Local only | unset (test skipped) |
