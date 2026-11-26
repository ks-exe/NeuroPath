# AI Agent Instructions

Rules for AI coding agents working in this repository. They apply to every change.

## Source of truth

- The canonical specification is `.kiro/specs/neuropath-platform/` (`requirements.md`, `design.md`, `tasks.md`). `docs/REQUIREMENTS_V2.md` only points there; do not copy requirement text into other documents.
- When code and spec disagree, the spec wins. Report the disagreement instead of silently changing either.

## Phase gating

- Work only on tasks of the current phase in `tasks.md`. A phase starts only after the Founder records approval of the previous phase report (R78.2).
- Do not create modules, tables, or routes that belong to a later phase. Migrations create only the tables Appendix B.3 lists for the phase (R6.3).
- Implement one task at a time and keep the change scoped to it.

## AWS and cost

- Do not deploy AWS resources or create billable resources. IaC may be authored and validated locally or in CI (`synth`, `plan`, `validate`) only.
- Any `deploy` or `apply` requires the Founder's written authorization for that specific deployment (R3.6).
- CI and tests make no AWS or Bedrock calls. Use the local adapters in `apps/api/core/integrations/`.

## Secrets

- No secrets in code, tests, fixtures, logs, or committed `.env` files. `.env.example` files hold placeholders only.
- Secrets are read through `SecretsProvider` (`apps/api/core/config.py`). Never prefix a secret with `NEXT_PUBLIC_`.
- When a secret is missing, fail closed (`SecretNotFoundError`); never fabricate a value.

## Status changes

- Change an entity's status only through `transition()` in `apps/api/services/transitions.py`. Do not assign status fields directly; update schemas exclude them.
- Transition tables live as data in `apps/api/models/status/`. Change them only to match Appendix A.

## Lab import rule

- Core modules (inquiries, projects, proposals, identity) must not import from `labs`. Labs may import core.
- `scripts/check_lab_imports.py` enforces this for Python; an ESLint `no-restricted-imports` rule enforces it for `apps/web`.

## Before finishing

Run the full local check and fix every failure:

```
python scripts/dev.py all --skip-build
```

Update the affected documents in `docs/` in the same change set (for example `ENVIRONMENT.md` when adding a variable, `DATABASE.md` when adding a migration, `IMPLEMENTATION_STATUS.md` when a task area changes).

## Content rules

- Do not invent customers, testimonials, prices, metrics, SLAs, or case-study results. Use only content the Founder has supplied or confirmed.
- Describe only what exists or is planned in the spec. Mark unverified items as such.
