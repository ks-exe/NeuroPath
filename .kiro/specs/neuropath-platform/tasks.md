# Implementation Plan: NEUROPATH Platform

## Overview

This plan turns `design.md` into incremental coding tasks, phase by phase (R78). Each phase ends with a gate checkpoint, and the next phase starts only after the Founder records approval of the previous phase report (R78.2).

**Stack.** API: Python, FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL. Web_App: Next.js (App Router), React, TypeScript, Tailwind CSS, shadcn/ui, React Flow. Local environment: Docker Compose (`web`, `api` with in-process worker, `postgres`) with local adapters for every external service (R3).

**Testing.** Python: pytest and Hypothesis. TypeScript: Vitest, Testing Library, fast-check, Playwright with axe for browser checks. Every property-based test runs at least 100 iterations (`@settings(max_examples=100)` or `fc.assert(..., { numRuns: 100 })`) and carries a comment naming its design property and requirement clause, e.g. `# Property 6: Status transition validity / Validates: Requirements 8.7` (R77.13).

**AWS and cost.** No task deploys AWS resources or creates billable resources. Infrastructure as code may be authored and validated (`synth`/`plan`/`validate`) locally or in CI only. Any `deploy`/`apply` step requires the Founder's written authorization for that specific deployment (R3.6) and is out of scope for these tasks.

**Phase table scope.** Migrations create only the tables Appendix B.3 lists for the phase (R6.3). Phase 0 has an empty baseline revision; Phase 1 creates `organizations`, `leads`, `consent_records`, `project_inquiries`, `projects`, `audit_logs`; Phase 2 creates the Phase 2 list and column additions.

## Tasks

### Phase 0: Foundation (R1 to R8)

- [x] 1. Set up the monorepo structure
  - [x] 1.1 Create the top-level layout and the API package skeleton
    - Create `apps/web`, `apps/api`, `packages`, `infrastructure`, `docs`, `scripts`
    - In `apps/api` create `api/`, `core/`, `models/`, `schemas/`, `services/`, `repositories/`, `workers/`, `tests/` with `pyproject.toml` (FastAPI, Pydantic, pydantic-settings, SQLAlchemy 2.x, Alembic, psycopg, pytest, Hypothesis, ruff, mypy)
    - Add a FastAPI app factory `apps/api/api/main.py` with a `/api/v1/health` route only
    - Do not create `data_engine/`, `agents/`, or `apps/api/labs/` yet (R1.3)
    - _Requirements: 1.1, 1.2, 1.3, 2.2_
  - [x] 1.2 Create the Next.js Web_App skeleton
    - Next.js App Router with TypeScript strict mode, Tailwind CSS, shadcn/ui setup, React Flow dependency, ESLint, Vitest, fast-check
    - Add a typed API client in `packages/api-client` that calls only `/api/v1` (no AWS SDK, no secrets in `NEXT_PUBLIC_*` variables)
    - _Requirements: 2.1, 2.8_
  - [x] 1.3 Implement the Lab dependency import check
    - `scripts/check_lab_imports.py`: parse Python imports with `ast` and fail when a core module (inquiries, projects, proposals, identity) imports from `labs`; equivalent check for `apps/web` route groups via an ESLint `no-restricted-imports` rule
    - _Requirements: 1.4_
  - [x]* 1.4 Write unit tests for the Lab import check
    - Fixture trees with an allowed import (Lab imports core) and a violation (core imports Lab)
    - _Requirements: 1.4_

- [x] 2. Implement configuration, secrets, and integration interfaces
  - [x] 2.1 Implement settings and the secrets provider
    - `apps/api/core/config.py` with pydantic-settings; `SecretsProvider` interface with an environment implementation (local) and an AWS Secrets Manager implementation (code only, not provisioned)
    - Add `PLATFORM_PHASE` setting used by the transition engine
    - Add `.env.example` with no real values
    - _Requirements: 3.1, 3.2, 3.7_
  - [x] 2.2 Define the integration interfaces and local adapters
    - Interfaces in `apps/api/core/integrations/`: `StorageClient`, `AuthProvider`, `MalwareScanner`, `EmailSender`, `NotificationChannel`, `ModelClient`
    - Local adapters: filesystem storage, local dev-token auth (enabled only when `ENVIRONMENT=local`), stub scanner that always returns "scanner unavailable", file/log outbox email, recorded-response model client
    - A substitution registry that lists active local substitutions for the implementation status record
    - _Requirements: 3.3, 3.4, 3.5_
  - [x]* 2.3 Write unit tests for local adapters
    - Stub scanner never reports clean; local auth adapter refuses to load outside `local`; outbox adapter reports "recorded locally", never "delivered"
    - _Requirements: 3.4_

- [x] 3. Set up the database baseline
  - [x] 3.1 Configure SQLAlchemy and Alembic
    - Declarative base with naming conventions for keys, constraints, indexes; mixins for `id`, `created_at`, `updated_at`, and a `TenantOwned` mixin adding indexed, non-null `organization_id`
    - Session factory with one transaction per service call
    - `alembic/` environment and an empty baseline revision (Appendix B.3, Phase 0)
    - _Requirements: 6.2, 6.3, 6.4, 6.5_
  - [x] 3.2 Implement the migration round-trip check
    - `scripts/check_migrations.py`: on an empty database, record schema, run `upgrade head`, `downgrade base`, and compare the reflected schema to the starting state
    - _Requirements: 6.7_
  - [x]* 3.3 Write an integration test for migration up and down
    - Run against the Compose PostgreSQL service; fail on any schema difference
    - _Requirements: 6.7_

- [x] 4. Implement the Status Transition Engine
  - [x] 4.1 Encode Appendix A status sets and transition tables as data
    - One source file per entity under `apps/api/models/status/` (e.g. `project.py`, `lead.py`, `invitation.py`, `inquiry_question.py`, `attachment.py`, `technical_assessment.py`), each a list of `TransitionRow(entity, from_status, to_status, allowed_roles, guards, enabled_phase)`
    - Include client-facing labels for Project statuses (A.1)
    - _Requirements: 8.1, 24.2_
  - [x] 4.2 Implement `transition()` with guards and phase enablement
    - Guard registry of pure functions returning `(passed, reason)`; rows whose `enabled_phase` exceeds `PLATFORM_PHASE` or whose guard entity is not delivered are treated as disabled
    - Structured rejections: undefined transition, disabled status (named), failed guard (named)
    - Accepted transitions call an audit hook in the same transaction (wired to AuditService in task 12.3)
    - Update schemas exclude status fields
    - _Requirements: 8.2, 8.3, 8.4, 8.5, 8.6_
  - [x]* 4.3 Write property test for transition validity
    - **Property 6: Status transition validity**
    - Generate (entity, s1, s2, role) tuples with Hypothesis; assert acceptance iff a matching enabled row exists
    - **Validates: Requirements 8.7**
  - [x]* 4.4 Write unit tests for the transition tables
    - Parse the Appendix A tables from `requirements.md` and assert the code tables match row for row; test guard-failure and disabled-status error payloads
    - _Requirements: 8.1, 8.3, 8.6_

- [x] 5. Set up local environment, developer commands, and CI
  - [x] 5.1 Write Docker Compose and Dockerfiles
    - `infrastructure/docker-compose.yml` with `web`, `api` (with in-process worker), `postgres`; Dockerfiles for both apps; volumes for local storage and outbox
    - _Requirements: 3.3_
  - [x] 5.2 Add one command per check for each app
    - API: `ruff check`, `mypy`, `pytest`, build image; Web: `eslint`, `tsc --noEmit`, `vitest --run`, `next build`; expose via `scripts/` (or a Makefile) with identical names
    - _Requirements: 7.1_
  - [x] 5.3 Create the CI pipeline
    - Workflow running lint, type check, tests (with a PostgreSQL service), secret scanning (gitleaks), the Lab import check, and the migration round-trip check on every push
    - CI makes no Bedrock or AWS calls; IaC is validated only (no deploy job)
    - _Requirements: 3.7, 7.2, 6.7_
  - [x] 5.4 Author the IaC skeleton without deploying it
    - Use the IaC tool recorded for A-10 (ask the Founder if not yet recorded); define default tags (project, environment, owner) applied to every resource and an AWS budget alarm as the first resource per environment
    - Validate with `cdk synth` or `terraform validate`/`plan` only; any deploy or apply requires the Founder's written authorization (R3.6)
    - _Requirements: 2.6, 3.6, 7.3, 7.4_

- [x] 6. Implement the design system foundation
  - [x] 6.1 Create shared design tokens and Tailwind configuration
    - `packages/design-tokens`: colors #762B3B, #F4F0E9, #171515, #D9D0C6, #A76C58; Playfair Display, Manrope, IBM Plex Mono via `next/font`; max card radius 4 px; motion durations ≤ 300 ms; `prefers-reduced-motion` disables non-essential animation
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_
  - [x] 6.2 Build base UI primitives in `packages/ui`
    - Button, Card, Section, Heading, MonoLabel, Field components using tokens only; no gradients or glass effects
    - _Requirements: 4.1, 4.4_
  - [x]* 6.3 Write unit tests for tokens and primitives
    - Assert token values, radius ≤ 4 px, durations ≤ 300 ms, and a lint rule rejecting `bg-gradient-*` and `backdrop-blur` classes in Web_App sources
    - _Requirements: 4.2, 4.4, 4.5_

- [x] 7. Create the Phase 0 documentation set and its check
  - [x] 7.1 Write the Phase 0 documents
    - `README.md`; `docs/REQUIREMENTS_V2.md` (pointer only to the canonical spec), `CHANGELOG_V1_TO_V2.md`, `ARCHITECTURE.md` (stack, IaC choice, decisions, layout deviations), `ROADMAP.md`, `MVP_SCOPE.md`, `AI_AGENT_INSTRUCTIONS.md`; plus `ENVIRONMENT.md`, `DEVELOPMENT.md`, `TESTING.md`, `DATABASE.md` (migration strategy), `IMPLEMENTATION_STATUS.md` (including local substitutions), because Phase 0 delivers what they describe
    - _Requirements: 1.5, 2.7, 3.1, 3.4, 5.1, 5.2, 5.3, 5.6, 6.8_
  - [x] 7.2 Implement `scripts/check_docs.py`
    - Verify the required document set for the current phase exists, that `REQUIREMENTS_V2.md` does not duplicate requirement text, and that every variable in `.env.example` appears in `ENVIRONMENT.md`; run in CI
    - _Requirements: 3.1, 5.1, 5.6_
  - [x]* 7.3 Write unit tests for the docs check
    - _Requirements: 5.1, 5.6_

- [x] 8. Implement the Phase 0 gate check
  - [x] 8.1 Implement `scripts/phase_gate.py --phase 0`
    - Confirms repository structure, CI status from the last run, migration round trip, the documentation set, and that no IaC deploy has run without a recorded Founder authorization; writes the phase report skeleton (delivered requirement IDs, test results, known issues, open assumptions, next phase plan) from recorded results only
    - _Requirements: 78.1, 78.4, 78.5_

- [x] 9. Checkpoint: Phase 0 gate
  - Ensure all tests pass, ask the user if questions arise.
  - The Phase 0 gate (R78.5) passes and the phase report is ready for Founder review; Phase 1 starts only after recorded Founder approval (R78.2).

### Phase 1: Public Company Website (R9 to R15)

- [x] 10. Build the public layout and content source
  - [x] 10.1 Create the structured content source
    - Typed content files in `apps/web/content/`: service groups A to F with detail lists, projects (title, description, technologies, `verification`), Why NEUROPATH statements (`confirmed`), About statements, Insights articles (`published`), Solutions capabilities with availability status
    - Loader functions that return only verified projects, confirmed statements, and published articles
    - _Requirements: 11.1, 11.4, 11.5, 11.6, 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 13.6_
  - [x]* 10.2 Write unit tests for the content loaders
    - Unverified projects and unpublished articles are omitted; empty sources produce the "being prepared" and "forthcoming" states with no placeholder entries
    - _Requirements: 11.2, 11.3, 11.5, 13.6_
  - [x] 10.3 Implement the global header, navigation, and footer
    - Links Home, Services, Solutions, Projects, How We Work, About, Insights, Contact; header CTA "Start a Project" to the inquiry form; Sign In link behind an `authEnabled` flag (off in Phase 1); menu control below 768 px; `aria-current="page"`; footer with all destinations and "Technology. Engineered to Solve."; no authentication on public routes
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7_
  - [x]* 10.4 Write component tests for navigation
    - Menu toggle below 768 px, `aria-current` on the active item, Sign In hidden when the flag is off
    - _Requirements: 9.3, 9.4, 9.5_

- [x] 11. Implement the public pages
  - [x] 11.1 Implement the homepage
    - Sections in order: Hero, What We Solve, Engineering Capabilities, Industries and Business Use Cases, Selected Projects and Case Studies, How We Work, Why NEUROPATH, Final Project Inquiry CTA; Hero heading, tagline, and both CTAs with their targets; journey steps in the required order; Playground and Solution Architect shown only as supporting capabilities outside the Hero
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 10.10, 11.1, 11.3_
  - [x] 11.2 Implement the Services page and service details
    - Six groups with detail content (engagements, deliverables, technologies), feasibility statement, scraping compliance statement for groups B and E, "Start a Project" passing the group as an optional `serviceHint` query parameter
    - _Requirements: 12.1, 12.8, 12.9, 12.10, 12.11_
  - [x] 11.3 Implement Solutions, Projects, How We Work, About, Insights, and the 404 page
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7_
  - [x]* 11.4 Write unit tests for page content rules
    - Homepage section order; no page contains "Engineering Intelligence. Enabling Growth."; unknown routes render the styled 404 with navigation
    - _Requirements: 10.1, 10.11, 13.7_

- [x] 12. Implement the API foundation and public inquiry intake
  - [x] 12.1 Add the error envelope, request id, and structured logging
    - Middleware assigning a request id; JSON logs carrying it; exception handlers returning `{code, message, fields, request_id}`; router mounted under `/api/v1`
    - _Requirements: 19.3, 19.4_
  - [x] 12.2 Create the Phase 1 models and migration
    - Tables `organizations` (internal seed row), `leads` (normalized email, unique index), `consent_records` (text version, timestamp, AI-processing flag), `project_inquiries` (submission token unique), `projects` (status, one-to-one FK unique on `project_inquiry_id`), `audit_logs`; tenant-owned tables carry `organization_id` (Appendix B.3 Phase 1)
    - _Requirements: 6.1, 6.3, 6.4, 6.5, 14.10, 24.1_
  - [x] 12.3 Implement the AuditService write path
    - `AuditService.record` writes inside the caller's transaction with actor type, actor id, action, resource, Organization, timestamp, request id, and redacted metadata; an audit write failure rolls back the whole transaction and returns HTTP 500 with the envelope
    - Repository exposes insert and read only; a PostgreSQL trigger rejects UPDATE and DELETE on `audit_logs`
    - Wire the transition engine audit hook to this service
    - _Requirements: 6.9, 8.4, 30.1, 30.3, 30.4, 30.5_
  - [x] 12.4 Implement email normalization and Lead upsert
    - `normalize_email` (trim, lowercase); `LeadService.upsert_from_inquiry` creates or links a Lead and stores the consent record
    - _Requirements: 22.1, 22.4, 22.7_
  - [x]* 12.5 Write property test for email normalization
    - **Property 16: Email normalization idempotence**
    - **Validates: Requirements 22.10**
  - [x] 12.6 Implement `InquiryService.submit` and the public endpoints
    - `POST /public/inquiries/submission-token` and `POST /public/inquiries`; Pydantic validation (name, email syntax, problem ≥ 20 chars, title, consent); honeypot rejection; text sanitization and configured max lengths; in-memory per-IP limit of 5 per 10 minutes returning 429 with `Retry-After`
    - One transaction stores Lead, Project_Inquiry, Project in Submitted (transition T01), and the Audit_Log entry; a repeated token returns the original receipt without new records
    - Notify internal users through the `NotificationChannel` local implementation only; no email to the submitter
    - _Requirements: 14.3, 14.7, 14.8, 14.9, 14.10, 14.11, 14.12, 14.14, 24.1_
  - [x]* 12.7 Write property test for idempotent submission
    - **Property 15: Idempotent inquiry submission**
    - Deliver each generated submission 1 to 5 times with the same token; assert one Project_Inquiry and one Project
    - **Validates: Requirements 14.14**
  - [x]* 12.8 Write property test for one Project per inquiry
    - **Property 8: One Project per inquiry**
    - **Validates: Requirements 24.15**
  - [x]* 12.9 Write unit tests for intake protections
    - Honeypot, rate limit and `Retry-After`, sanitization, length limits, consent fields stored, audit rollback on forced audit failure
    - _Requirements: 14.7, 14.8, 14.9, 14.10, 30.5_

- [x] 13. Implement the project inquiry form
  - [x] 13.1 Build the inquiry form page
    - All R14.1 fields with visible labels; no required technology category; optional service hint prefilled from `serviceHint` and clearable; field-level client validation; on API error show the error and keep values; on success show confirmation and clear; disabled submit and loading state while pending; errors announced through a live region; hidden honeypot field
    - _Requirements: 12.11, 14.1, 14.2, 14.4, 14.5, 14.6, 14.13, 15.7, 15.8_
  - [x]* 13.2 Write component tests for the inquiry form
    - _Requirements: 14.4, 14.5, 14.6, 14.13_

- [x] 14. Implement SEO, accessibility, and performance requirements
  - [x] 14.1 Add metadata, sitemap, and robots
    - Per-page unique title, description, canonical URL, Open Graph via the Next.js metadata API; `sitemap.ts` and `robots.ts`; one `h1` per page; per-route font and script loading
    - _Requirements: 15.1, 15.2, 15.3, 15.10_
  - [x] 14.2 Apply accessibility rules across public pages
    - Text alternatives, WCAG 2.2 AA contrast for text, controls, and focus indicators, full keyboard operation
    - _Requirements: 15.4, 15.5, 15.6_
  - [ ]* 14.3 Write Playwright accessibility and layout tests
    - axe checks on every public page; exactly one `h1`; no horizontal scroll at 360, 768, 1280, and 1920 px
    - _Requirements: 4.7, 15.3, 15.4, 15.5, 15.6, 15.7_
  - [ ]* 14.4 Add Lighthouse CI for the homepage
    - Mobile profile on a production build with thresholds of 90 for Performance, Accessibility, Best Practices, and SEO
    - _Requirements: 15.9_

- [x] 15. Implement the Phase 1 gate check
  - [x] 15.1 Extend `phase_gate.py` with `--phase 1` and update affected docs
    - Confirms all public pages render, a form submission stores Lead, Project_Inquiry, and Project, Lighthouse and accessibility results pass, and no page shows the V1 tagline; update `DATABASE.md`, `TESTING.md`, `ENVIRONMENT.md`, `IMPLEMENTATION_STATUS.md` in the same change set
    - _Requirements: 5.4, 5.5, 78.1, 78.3, 78.6_

- [ ] 16. Checkpoint: Phase 1 gate
  - Ensure all tests pass, ask the user if questions arise.
  - The Phase 1 gate (R78.6) passes, Phase 0 features still work (R78.3), and the phase report is ready for Founder review before Phase 2 starts (R78.2).

### Phase 2: Client Acquisition and Founder CRM (R16 to R30)

- [ ] 17. Complete the API conventions
  - [ ] 17.1 Add validation and rate-limit handling
    - Pydantic validation errors return HTTP 422 with code, message, and offending fields; per-principal and per-IP limits with values from configuration; HTTP 429 with `Retry-After`
    - _Requirements: 19.1, 19.2, 19.5, 19.6_
  - [ ] 17.2 Add the OpenAPI drift check
    - `scripts/check_openapi.py` compares the generated OpenAPI paths, methods, and schemas with `docs/API.md`; create `docs/API.md` and run the check in CI
    - _Requirements: 5.2, 19.9_
  - [ ]* 17.3 Write unit tests for the error envelope and rate limits
    - _Requirements: 19.2, 19.3, 19.6_

- [ ] 18. Implement identity, sessions, and the permission matrix
  - [ ] 18.1 Create the identity migration
    - `users`, `organization_members` (role Owner or Member), `invitations` (normalized email, organization, expiry, status, accepted_at); add `leads.converted_user_id` and `project_inquiries.submitted_by_user_id` (Appendix B.3 Phase 2)
    - _Requirements: 6.1, 6.3, 6.4, 6.5, 25.5_
  - [ ] 18.2 Implement the AuthProvider adapters and session handling
    - Cognito adapter (JWKS verification of signature, issuer, audience, expiry; code only, no pool provisioned) and the local adapter; no password storage in the API; session in HTTP-only, secure, same-site cookies; logout revokes the refresh token; invalidated tokens return 401; provider outage returns a structured "authentication temporarily unavailable" error and grants no session
    - _Requirements: 16.1, 16.12, 16.13, 16.14, 16.15_
  - [ ] 18.3 Implement Principal resolution and the Appendix A.3 permission matrix
    - Code-defined matrix in `apps/api/core/permissions.py`; dependency building `Principal` (platform role, memberships, Internal_Agent permission set); deny by default; Founder holds every permission; 401 for missing auth, 403 for missing permission; reject any assignment giving an Internal_Agent Administrator, Founder, or unrestricted access
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5, 17.6, 17.7, 17.8_
  - [ ]* 18.4 Write property test for matrix conformance
    - **Property 1: Role permission matrix conformance**
    - Generate (role ≠ Founder, endpoint) pairs from the route table; assert a success status only when A.3 grants the permission
    - **Validates: Requirements 17.12**
  - [ ] 18.5 Implement `IdentityService` registration, login, recovery, and staff accounts
    - `/auth/register` (requires a valid, unused, unexpired Invitation bound to the normalized email; otherwise structured error and no account), `/auth/login` (unverified accounts denied; lockout after 5 consecutive failures), `/auth/logout`, `/auth/me`, recovery with identical body, status, and timing class; password policy ≥ 12 characters; `POST /admin/staff-accounts` with Founder-selected role; Audit_Log entries for account creation, invitation use, lockout, staff account creation
    - _Requirements: 16.3, 16.4, 16.5, 16.6, 16.7, 16.8, 16.9, 16.10, 16.11, 16.16_
  - [ ]* 18.6 Write unit tests for identity flows
    - Enumeration-safe recovery, lockout on the fifth failure, rejected registrations (no, expired, used, mismatched invitation), unverified sign-in denied
    - _Requirements: 16.4, 16.6, 16.7, 16.9_
  - [ ] 18.7 Implement role assignment
    - `PUT /admin/users/{id}/role` through IdentityService with an Audit_Log entry recording actor, target, previous role, new role, time
    - Per-user grants (R17.11, Optional) are deferred because `user_permission_grants` is a Phase 3 table (Appendix B.3)
    - _Requirements: 17.8, 17.10_

- [ ] 19. Implement tenant isolation
  - [ ] 19.1 Implement `OrgScope`, tenant repositories, and visibility-aware serializers
    - Every tenant repository method requires an `OrgScope` and applies the Organization filter; internal-only methods require `scope.internal_staff`; cross-Organization reads by Clients return 404; serializers drop Internal_Only records and fields for Client principals
    - _Requirements: 6.6, 18.1, 18.2, 18.5_
  - [ ] 19.2 Implement `/users/me` and `/organizations`
    - _Requirements: 18.6_
  - [ ]* 19.3 Write property test for tenant isolation
    - **Property 2: Tenant isolation**
    - Generate two Organizations with random records; call every Client-readable endpoint as a Client of A; assert no record owned by B appears
    - **Validates: Requirements 18.7**
  - [ ]* 19.4 Write property test for Client visibility
    - **Property 3: Client visibility**
    - Assert no Internal_Only record or field appears in any response to a Client principal
    - **Validates: Requirements 18.8**

- [ ] 20. Implement Organizations and Invitations
  - [ ] 20.1 Implement `OrganizationService`
    - Create Invitation bound to the Lead's normalized email and a new Organization (name from the inquiry company field, editable before sending) or an existing one; expiry from configuration; Owners invite only into their own Organization (404 otherwise); revoke unaccepted invitations; accept with a row lock: reject expired, revoked, used, or email-mismatched invitations, convert Lead to Client, create membership (Owner for the first Client), link Organization to Project; Audit_Log entry for create, send, accept, reject, revoke
    - Endpoints `POST /organizations/{id}/invitations`, `POST /invitations/{id}/revoke`, `POST /invitations/accept`, `PUT /organizations/{id}/members/{user_id}/role`
    - _Requirements: 16.2, 16.11, 25.1, 25.2, 25.3, 25.4, 25.5, 25.6, 25.7, 25.8, 25.9, 25.10, 25.11, 25.12_
  - [ ]* 20.2 Write property test for single-use invitations
    - **Property 5: Single-use invitation**
    - Generate sequences of accept attempts, including concurrent ones; assert at most one acceptance is recorded
    - **Validates: Requirements 25.13**

- [ ] 21. Implement the ENGINE job queue baseline
  - [ ] 21.1 Implement the `JobQueue` interface and in-process worker
    - `jobs` table with unique `(job_type, dedupe_key)` and `organization_id`; `submit`, `status`, `cancel`; worker claiming with `FOR UPDATE SKIP LOCKED` and a lease; up to 3 retries with backoff; handler receives an `OrgScope` for the Job's Organization only; `GET /jobs/{id}` scoped to permitted principals; long-running endpoints return 202 with the job id
    - Dead-letter records are deferred (`job_dead_letters` is a Phase 5 table); final failures mark the Job Failed and notify internal users
    - _Requirements: 19.7, 19.8_
  - [ ]* 21.2 Write unit tests for the job queue
    - Duplicate submission returns the existing id; expired lease becomes claimable; retry count stops at 3
    - _Requirements: 19.7, 19.8_

- [ ] 22. Implement secure attachments
  - [ ] 22.1 Implement `AttachmentService` and endpoints
    - `attachments` table; `POST /attachments/upload-url` returns a URL valid ≤ 10 minutes for one key under the Organization prefix, after verifying the prefix; `complete-upload` verifies the object exists, checks extension and real content type by magic bytes, allowlist, and configured size, deletes and rejects with a named reason on failure, then submits a scan Job (202)
    - Scan handler: clean → available; detected or scanner unavailable → quarantined plus internal notification
    - `GET /attachments/{id}/download-url` only for available Attachments, to members of the owning Organization or permitted internal roles, URL ≤ 10 minutes, with an Audit_Log entry
    - Document the allowlist in a new `docs/SECURITY.md`
    - _Requirements: 18.3, 18.4, 20.2, 20.3, 20.4, 20.5, 20.6, 20.7, 20.8, 20.9, 20.10, 20.11_
  - [ ]* 22.2 Write property test for quarantine
    - **Property 14: Quarantine**
    - Generate Attachments in every status and scanner outcome; assert a download URL is issued only when status is available
    - **Validates: Requirements 20.12**
  - [ ] 22.3 Author the private attachment bucket in IaC (not deployed)
    - Block all public access, encryption at rest, tags; validate only, deployment requires the Founder's written authorization (R3.6)
    - _Requirements: 3.6, 20.1_

- [ ] 23. Implement inquiry review and the early Project lifecycle
  - [ ] 23.1 Enable the Phase 2 Project transitions and guards
    - Statuses Draft, Submitted, Under Review, Awaiting Information, Qualified, Rejected, Cancelled, On Hold enabled at `PLATFORM_PHASE=2`; add `projects.prior_status`, `status_reason`, `assigned_engineer_id`; On Hold requires a reason and stores the prior status; resume returns to the prior status; Client cancellation allowed only before Accepted; each change writes an Audit_Log entry and enqueues a Notification for the Project owner; `POST /projects/{id}/transitions`, `GET /projects`, `GET /projects/{id}` with client-facing labels for Clients
    - _Requirements: 24.2, 24.3, 24.4, 24.5, 24.6, 24.8, 24.9, 24.10, 24.11, 24.12, 24.13_
  - [ ] 23.2 Implement review actions in `InquiryService`
    - `inquiry_questions` table; `request-info` creates Open Inquiry_Questions and moves to Awaiting Information; `reject` requires a reason; `qualify` moves to Qualified; `assign-reviewer` records the Engineer; decisions accepted only from human principals; Audit_Log entry per decision
    - _Requirements: 21.1, 21.2, 21.3, 21.4, 21.5, 21.6, 21.7, 21.8, 21.10_
  - [ ] 23.3 Implement Client answers to Inquiry_Questions
    - `POST` answer endpoint for Clients; reject non-Open questions; set Answered; answering the last Open question moves the Project from Awaiting Information to Under Review
    - _Requirements: 24.7, 26.3, 26.4_
  - [ ]* 23.4 Write property test for Project transition conformance
    - **Property 7: Project status transition conformance and integrity**
    - Generate random sequences of review, answer, hold, resume, and cancel requests from random roles; assert every recorded change matches an enabled A.1 row and every stored status is reachable from Submitted
    - **Validates: Requirements 21.11, 24.14**
  - [ ]* 23.5 Write unit tests for review edge cases
    - Reject without reason, Internal_Agent decision refused, disabled-status error, On Hold without reason, Client cancel after Accepted
    - _Requirements: 21.4, 21.8, 24.4, 24.8, 24.12_

- [ ] 24. Implement Lead management
  - [ ] 24.1 Implement `LeadService` management features
    - `lead_sources`, `opt_out_entries`; add `leads.status`, `possible_duplicate`, `merged_into_lead_id`; per-item source; Lead transitions from A.2 through the engine; flag both Leads on a matching normalized email; merge only on reviewer approval, preserving sources and consents; opt-out adds the normalized email and writes an Audit_Log entry; contact actions targeting opted-out emails are rejected; endpoints `GET /admin/leads`, `GET /admin/leads/{id}`, `POST /admin/leads/{id}/merge`, `POST /admin/leads/{id}/opt-out`
    - _Requirements: 22.2, 22.3, 22.5, 22.6, 22.7, 22.8, 22.9_
  - [ ]* 24.2 Write property test for opt-out
    - **Property 17: Opt-out**
    - Generate Leads, opt-outs, and contact attempts; assert no outgoing contact is recorded for opted-out emails
    - **Validates: Requirements 22.11**

- [ ] 25. Implement notifications
  - [ ] 25.1 Implement `NotificationService` and event dispatch
    - `notifications`, `notification_preferences`; in-app Notifications for inquiry stored, question asked, question answered, status change, attachment quarantined; event types of later phases disabled by phase; recipients see only their own Notifications; email sent through `EmailSender` only on opt-in; external-party email (other than Cognito messages) held for Founder approval; provider failure keeps the in-app Notification and records the failure with no success reported
    - Endpoints `GET /notifications`, `POST /notifications/mark-read`, `GET`/`PUT /notifications/preferences`
    - Replace the Phase 1 local-only internal notification in `InquiryService.submit` with this service
    - _Requirements: 14.12, 27.1, 27.2, 27.3, 27.4, 27.5, 27.6, 27.7, 27.9, 27.10, 27.11, 27.12, 27.13_
  - [ ]* 25.2 Write property test for email opt-in
    - **Property 18: Email opt-in**
    - **Validates: Requirements 27.14**
  - [ ]* 25.3 Write unit tests for notification scoping and provider failure
    - _Requirements: 27.9, 27.13_

- [ ] 26. Implement Technical_Assessment records
  - [ ] 26.1 Implement the Technical_Assessment service and endpoints
    - `technical_assessments`, `technical_assessment_versions`; start only for Qualified Projects (moves to Assessment in Progress; Solution Designed stays disabled until Phase 3); enumerated feasibility and complexity; justification required (422); disciplines from the six service groups; Internal_Only with 404 for Clients; each edit stores a new version and leaves earlier versions unchanged; Audit_Log entries
    - Endpoints `POST /admin/inquiries/{id}/technical-assessments`, `GET /admin/technical-assessments/{id}/versions`, plus a version-create endpoint
    - _Requirements: 29.1, 29.2, 29.3, 29.4, 29.5, 29.6, 29.7, 29.8, 29.9, 29.10, 29.11_
  - [ ]* 26.2 Write property test for version history
    - **Property 11: Version history invariant**
    - **Validates: Requirements 29.13**

- [ ] 27. Implement Audit_Log search and audit guarantees
  - [ ] 27.1 Implement `AuditService.search` and `GET /admin/audit-logs`
    - Add search indexes on `audit_logs`; filters by actor, action, resource, time range; start after end returns 422; non Founder/Administrator returns 403; ensure authentication, role, status, review, attachment, consent, invitation, export, and external communication events all call `record`
    - _Requirements: 30.2, 30.6, 30.7, 30.8_
  - [ ]* 27.2 Write property test for audit completeness
    - **Property 9: Audit completeness**
    - Run random committed state-changing calls; assert exactly one new Audit_Log entry per call
    - **Validates: Requirements 30.9**
  - [ ]* 27.3 Write property test for append-only audit
    - **Property 10: Audit log is append-only**
    - Snapshot entries, run random operations including attempted UPDATE/DELETE, assert all earlier entries remain unchanged
    - **Validates: Requirements 30.10**

- [ ] 28. Implement the inbox and Founder dashboard APIs
  - [ ] 28.1 Implement the inquiry inbox endpoints
    - `GET /admin/inquiries` with server-side filters (status, date range, reviewer) and per-status counts from stored rows; `GET /admin/inquiries/{id}` with fields, Attachments with scan status, questions and answers, status and decision history
    - _Requirements: 23.1, 23.2, 23.3, 23.4_
  - [ ] 28.2 Implement the Founder dashboard metrics endpoint
    - Counts per status, new inquiries in range, Qualified, Rejected, Awaiting Information, Open questions, Leads, Client Organizations, Clients; recent Audit_Log activity; zeros for empty data; 422 when start is after end; Founder and Administrator only
    - _Requirements: 28.1, 28.2, 28.3, 28.4, 28.5, 28.7_
  - [ ]* 28.3 Write property test for count integrity
    - **Property 12: Count integrity**
    - Generate data sets, filter combinations, and date ranges; compare inbox and dashboard counts with counts computed directly from the generated rows
    - **Validates: Requirements 23.8, 28.9**

- [ ] 29. Build the Web_App authentication and Client_Workspace
  - [ ] 29.1 Implement sign-in, registration, and recovery pages
    - Next.js route handlers set and clear HTTP-only cookies; no tokens in client storage; enable the header Sign In link from Phase 2; `/dashboard` routes redirect unauthenticated users to Sign In and back after sign-in
    - _Requirements: 2.8, 9.3, 16.12, 16.14, 26.10_
  - [ ] 29.2 Implement the Client_Workspace dashboard
    - `/dashboard` shows the Client's inquiries and Projects with client-facing status labels, Open questions with an answer form, recent Client_Visible updates, and Notifications; values come from API responses only; loading, empty (with next action), and error-with-retry states
    - _Requirements: 24.6, 26.1, 26.2, 26.3, 26.5, 26.6, 26.7, 26.8, 26.9_
  - [ ]* 29.3 Write property test for workspace isolation
    - **Property 4: Client workspace isolation**
    - Against the endpoints the workspace calls, generate multi-Organization data and assert every returned record belongs to the Client's Organizations and is Client_Visible
    - **Validates: Requirements 26.12**
  - [ ] 29.4 Implement the notification bell
    - Unread count and mark-as-read for the current user
    - _Requirements: 27.8_

- [ ] 30. Build the Founder_Control_Center Phase 2 screens
  - [ ] 30.1 Implement the inquiry inbox and detail screens
    - Filters, status counts, detail view, request-info, qualify, reject-with-reason, assign-reviewer actions; AI analysis labeled AI-generated and advisory; controls hidden by permission; loading, empty, and error-with-retry states
    - _Requirements: 17.9, 21.9, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7_
  - [ ] 30.2 Implement the Founder dashboard screen
    - _Requirements: 28.1, 28.2, 28.3, 28.6, 28.7, 28.8_
  - [ ] 30.3 Implement Lead, Invitation, staff account, and Audit_Log screens
    - Lead list with duplicate flags, merge approval, opt-out; invitation creation with editable Organization name and revoke; staff account creation with role; Audit_Log search with filters
    - _Requirements: 16.5, 22.6, 22.8, 25.2, 25.11, 30.6_
  - [ ] 30.4 Implement the internal Technical_Assessment form and version history view
    - _Requirements: 29.3, 29.4, 29.5, 29.6, 29.9_
  - [ ]* 30.5 Write component tests for Founder_Control_Center screens
    - Permission-hidden controls, reject requires reason, loading, empty, and error states
    - _Requirements: 17.9, 21.4, 23.5, 23.6, 23.7, 28.8_

- [ ] 31. Wire Phase 2 together and implement the gate check
  - [ ] 31.1 Write the Phase 2 API integration test
    - One flow: inquiry submitted, invitation created and accepted, Client signs in, reviewer requests information, Client answers, Project returns to Under Review, reviewer qualifies, Technical_Assessment started, notifications and Audit_Log entries present, dashboard counts match stored rows
    - _Requirements: 21.2, 24.7, 25.4, 27.1, 28.4, 30.9, 78.7_
  - [ ] 31.2 Extend `phase_gate.py` with `--phase 2` and update affected docs
    - Confirms invitation-based sign-in, A.3 matrix tests, tenant isolation property tests, inbox and review actions, the Awaiting Information loop, notifications, dashboard counts, and the Audit_Log; update `DATABASE.md`, `API.md`, `SECURITY.md`, `ENVIRONMENT.md`, `TESTING.md`, `IMPLEMENTATION_STATUS.md` in the same change set
    - _Requirements: 5.4, 5.5, 78.1, 78.3, 78.7_

- [ ] 32. Checkpoint: Phase 2 gate
  - Ensure all tests pass, ask the user if questions arise.
  - The Phase 2 gate (R78.7) passes, Phase 0 and Phase 1 features still work (R78.3), and the phase report is ready for Founder review before Phase 3 starts (R78.2).

### Phase 3: Solution Discovery and Proposal (R31 to R43)

- [ ] 33. Lay the Phase 3 data and platform foundation
  - [ ] 33.1 Create the Phase 3 models and migration
    - Tables `user_permission_grants`, `feature_flags`, `solution_architect_drafts`, `project_requirements_versions`, `solution_architectures`, `solution_architecture_versions`, `proposals` (unique `project_id`), `proposal_versions`, `price_entries`, `cost_estimates`, `approval_requests`, `acceptance_records`, `agreements`, `communications`, `usage_records`; add `inquiry_questions.approved_by`, `approved_at`, `ai_generated`, `technical_assessment_versions.ai_generated`, `attachments.agreement_id`, `communication_id` (Appendix B.3 Phase 3)
    - Version tables carry `UNIQUE (parent_id, version_number)`; approved and accepted artifacts carry `content_hash`; status CHECK constraints regenerated from the transition data; `acceptance_records` gets INSERT and SELECT grants only plus an UPDATE/DELETE-rejecting trigger; working downgrade
    - _Requirements: 6.1, 6.2, 6.3, 6.7, 36.1, 38.14_
  - [ ] 33.2 Implement the shared canonical hashing function
    - `core/hashing.py`: `canonical_json(content)` (sorted keys, UTF-8, no insignificant whitespace, decimals as strings) and `content_hash(content)` as SHA-256 hex; `verify_content_hash(artifact, expected_hash)`; every Phase 3 hash (Proposal_Version approval, Approval_Request, Acceptance_Record, export) calls this one function
    - _Requirements: 36.9, 38.5, 40.13, 43.1, 43.5_
  - [ ]* 33.3 Write unit tests for canonical hashing
    - Key order, whitespace, and decimal formatting do not change the hash; any content change does
    - _Requirements: 36.9, 43.5_
  - [ ] 33.4 Implement `FeatureFlagService` backed by `feature_flags`
    - Flags read by the status engine (task 4.2) and by services; seeded flags `solution_architect` (staff invocation), `solution_architect_lab` (public Lab), and `per_user_permission_grants`, all off by default; Founder-only `PUT /admin/feature-flags/{key}` writing an Audit_Log entry with previous and new value; the full configuration screen stays in Phase 5 (R73)
    - _Requirements: 8.6, 24.4, 31.10_
  - [ ] 33.5 Implement per-user permission grants (R17.11, Optional)
    - Behind the `per_user_permission_grants` flag; `POST /admin/permission-grants` and `DELETE /admin/permission-grants/{id}` (Founder only, 403 otherwise) grant or revoke one Appendix A.3 permission for a named user; reject permissions not in A.3 with 422; Principal resolution (request lifecycle step 3) adds active grants; Audit_Log entry for each grant and revocation
    - Grants are the delegation mechanism for Authorized_Approver under A-06 (tasks 34.1 and 41.2)
    - _Requirements: 17.11, 37.2, 43.3_
  - [ ]* 33.6 Write unit tests for permission grants
    - Grant enables exactly the named permission, revocation removes it, flag off returns 404, non-Founder 403, Audit_Log entries present; rerun the Property 1 matrix test with no grants to confirm A.3 conformance is unchanged
    - _Requirements: 17.11, 17.12_
  - [ ] 33.7 Add the Phase 3 transition data
    - Appendix A.1 Project rows enabled at `PLATFORM_PHASE=3` (Assessment in Progress to Solution Designed, the proposal statuses through Awaiting Client Decision, and Accepted with T18 per A-35); Appendix A.2 tables for Inquiry_Question (Draft, Open, Answered, Withdrawn), Proposal_Version, Approval_Request, and Agreement; each row names its guard, and rows whose guard is not yet registered stay disabled per task 4.2
    - _Requirements: 8.1, 8.6, 33.4, 36.2, 39.6, 43.2_
  - [ ]* 33.8 Extend the status transition property test to the Phase 3 tables
    - **Property 6: Status transition validity**
    - Generate status pairs and roles for the Phase 3 entities; assert acceptance if and only if a matching enabled row exists
    - **Validates: Requirements 8.7**

- [ ] 34. Implement Approval_Requests (R43)
  - [ ] 34.1 Implement `ApprovalService` and endpoints
    - Record action type, target, exact content or parameters with `content_hash`, requester (user or Internal_Agent), rationale, status; transitions through the engine; decisions only from an Authorized_Approver (Founder, or a delegate holding the approval grant); Internal_Agent or non-approver decisions return 403 and write an Audit_Log entry; approve requires the presented hash to equal the stored hash; decision Audit_Log entry with approver, time, decision, reason
    - `require_approved(action_type, target, content)` helper recomputes the hash and blocks the action with an Audit_Log entry when no Approved request matches; a content change on an Approved request sets it to Invalidated
    - Endpoints `POST /admin/approvals`, `GET /admin/approvals?status=pending`, `POST /admin/approvals/{id}/approve`, `POST /admin/approvals/{id}/reject`
    - _Requirements: 43.1, 43.2, 43.3, 43.4, 43.5, 43.6, 43.8, 43.9_
  - [ ] 34.2 Register the Approval_Request expiry scheduled job type
    - Job type on the queue from task 21.1 moves Pending requests past the configured expiry period (A-08) to Expired and blocks the action
    - _Requirements: 43.7_
  - [ ] 34.3 Route external email through Approval_Requests
    - Replace the Phase 2 Founder-approval hold for external-party email (task 25.1) with an Approval_Request of action type external email; `EmailSender` sends only content whose hash matches the Approved request; Cognito messages stay exempt
    - _Requirements: 27.11, 40.6, 43.10_
  - [ ]* 34.4 Write property test for approved execution
    - **Property 30: Approved execution**
    - Generate approval requests, decisions, content edits, and execution attempts; assert every executed Sensitive_Action has an Approved request whose hash equals the executed content hash
    - **Validates: Requirements 43.12**
  - [ ]* 34.5 Write unit tests for approval edge cases
    - Non-approver and Internal_Agent decisions (403 plus audit), hash mismatch on approve, invalidation after edit, expiry blocks execution
    - _Requirements: 43.4, 43.6, 43.7, 43.8_

- [ ] 35. Implement usage and cost tracking (R42)
  - [ ] 35.1 Implement `UsageService`
    - `record_usage` writes `usage_records` per Organization for uploads, storage, Jobs, and AI calls (tokens, model id, estimated cost); non-negative validation; hooks in `AttachmentService` (upload and storage) and the job worker (Job completion cost)
    - `check_limit` against per-Organization and global AI cost limits from configuration (A-08); an exceeded limit raises `LimitExceeded` naming the limit and sends a Notification to the Founder; the Organization `tier` attribute is never read; no billing code
    - _Requirements: 42.1, 42.2, 42.3, 42.4, 42.5, 42.6, 42.7_
  - [ ] 35.2 Wrap every `ModelClient` with limit checks and usage recording
    - `MeteredModelClient` decorator around the configured client (recorded-response stub from task 2.2 or the Bedrock adapter): checks limits before the call, records input tokens, output tokens, model id, and cost after it; a missing cost value is recorded as a structured failure, not as zero
    - _Requirements: 32.12, 42.2, 42.5_
  - [ ] 35.3 Implement the usage endpoints
    - `GET /admin/usage` and `GET /admin/usage/organizations/{id}` (Founder and Administrator only) returning per-Organization and total usage and estimated cost for a selected period, computed from stored rows; usage data is Internal_Only
    - _Requirements: 42.8_
  - [ ]* 35.4 Write property test for cost aggregation
    - **Property 29: Cost aggregation**
    - Generate usage records across Organizations and periods; assert reported totals equal the sum of per-call estimated costs
    - **Validates: Requirements 42.9**
  - [ ]* 35.5 Write unit tests for limits
    - Per-Organization and global limit exceeded return the named structured error and notify the Founder; `tier` changes have no effect
    - _Requirements: 42.5, 42.6_

- [ ] 36. Implement the Agent_Runtime and the Bedrock adapter
  - [ ] 36.1 Implement the Agent_Runtime task runner
    - `TaskSpec` with instructions, a fixed tool set captured at task start, and a Pydantic output schema; untrusted inputs passed only as delimited `DataBlock`s and never merged into instructions; validation with at most 2 retries, then `StructuredFailure` with nothing stored; outputs marked AI-generated and Internal_Only; all calls go through `MeteredModelClient`
    - _Requirements: 31.4, 32.9, 32.10, 32.11, 32.13_
  - [ ] 36.2 Implement `BedrockModelClient` (adapter code only)
    - `boto3` `bedrock-runtime` Converse call with model id, region, and per-model token prices from configuration; maps token usage to `ModelResult`; provider errors become structured failures; selected only outside `ENVIRONMENT=local` and only when configured; no AWS resource is created or deployed; CI and local runs keep the recorded-response stub
    - Add recorded responses for each Phase 3 task schema (analysis, questions, assessment, architecture, proposal, cost estimate), including invalid outputs for retry tests and an embedded-instruction input
    - _Requirements: 3.3, 3.4, 32.12, 77.10_
  - [ ]* 36.3 Write unit tests for the Bedrock adapter
    - `botocore` Stubber only, no network: request shape, token and cost mapping, provider error mapping; a test asserts the default CI configuration resolves to the stub
    - _Requirements: 32.12, 77.10_

- [ ] 37. Implement AI requirement analysis and the Solution_Architect (R31, R32)
  - [ ] 37.1 Implement the requirement analysis Job
    - Analysis Pydantic schema covering every R32.7 section; recommended disciplines limited to the six service groups; assumption statements flagged; input built from Project_Inquiry fields and answered Inquiry_Questions; Attachment text included only with the AI-processing consent flag and an available Attachment, otherwise the exclusion reason is written to the Job result; over-length fields return 422 naming the field; success stores a new `project_requirements_versions` row in Draft, AI-generated, Internal_Only
    - _Requirements: 32.1, 32.2, 32.3, 32.4, 32.6, 32.7, 32.8, 32.13_
  - [ ] 37.2 Implement `DiscoveryService` Solution_Architect invocation and endpoints
    - `POST /solutions/analyze` (202), `POST /solutions/{id}/clarify` (202), `GET /solutions/{id}`, `POST /solutions/{id}/generate-architecture` (202), `POST /solutions/{id}/generate-proposal` (202), `GET /solutions/{id}/export`; allowed only for Projects in Qualified or Under Review (409 otherwise), Authorized_Reviewer only (403), 404 when the `solution_architect` flag is off; result stored as a `solution_architect_drafts` row; Audit_Log entry with actor, Project, Job id; the Job never calls `transition`
    - Publish a named part of a draft to the Client_Workspace with an Audit_Log entry naming the part; the rest stays Internal_Only
    - _Requirements: 31.1, 31.2, 31.3, 31.4, 31.5, 31.6, 31.10, 31.12, 31.13_
  - [ ] 37.3 Implement the public Solution_Architect Lab API path
    - Enabled only by the `solution_architect_lab` flag (404 otherwise); Guest analyses counted against the configured limit, returning 429 stating sign-in is required; Guest results are not stored before sign-in; output converts to a Project_Inquiry draft saved only after sign-in; R14 intake is unchanged and independent of the flag
    - _Requirements: 31.7, 31.8, 31.9, 31.11_
  - [ ]* 37.4 Write property test for status preservation
    - **Property 13: Status preservation by AI and agent work**
    - Generate Projects in Qualified and Under Review and Solution_Architect Jobs with stub outputs, including failures; assert the Project status before and after each Job is equal
    - **Validates: Requirements 31.14**
  - [ ]* 37.5 Write property test for the analysis tool set and no partial output
    - **Property 19: AI analysis tool set and no partial output**
    - Generate inputs with embedded instructions and stub outputs that fail validation; assert the tool set equals the configured set and failed Jobs leave the `project_requirements_versions` count unchanged
    - **Validates: Requirements 32.14, 32.15**
  - [ ]* 37.6 Write unit tests for analysis and invocation rules
    - 409 on disallowed status, 403, 404 with flag off, 422 field naming, attachment exclusion reason, two retries then failure, Guest 429
    - _Requirements: 31.2, 31.3, 31.9, 31.10, 32.4, 32.6, 32.10_

- [ ] 38. Implement the clarification workflow (R33)
  - [ ] 38.1 Implement Inquiry_Question drafting, approval, and sending
    - `POST /admin/inquiries/{id}/questions/draft` (202) generates Draft questions from the analysis missing-information list (`ai_generated=true`); reviewers add Draft questions manually; `POST /admin/question-sets/{id}/approve` records `approved_by` and `approved_at`; `POST /admin/question-sets/{id}/send` returns 409 for any question without approval and moves approved questions to Open; Guest-submitted inquiries receive questions only after the Invitation is accepted or through an Approved external email Approval_Request (A-09); Audit_Log entry on create, approve, send, answer, withdraw
    - _Requirements: 33.1, 33.2, 33.3, 33.4, 33.8, 33.9_
  - [ ] 38.2 Implement answering and re-analysis
    - `POST /question-sets/{id}/answers` attaches answers to the same Project_Inquiry and sets Answered; Withdrawn returns 409, another Organization returns 404; a reviewer re-analysis request runs task 37.1 and stores a new version, leaving earlier versions unchanged
    - _Requirements: 33.5, 33.6, 33.7_
  - [ ]* 38.3 Write property test for approval before delivery
    - **Property 20: Approval before delivery of questions**
    - Generate question lifecycles and answer sequences; assert every delivered question has an earlier approval timestamp and the Project_Inquiry count per Project is unchanged
    - **Validates: Requirements 33.10, 33.11**
  - [ ]* 38.4 Write unit tests for clarification errors
    - Send without approval (409), answer to Withdrawn (409), cross-Organization answer (404), Guest delivery blocked before Invitation acceptance
    - _Requirements: 33.3, 33.6, 33.8_

- [ ] 39. Implement assessment drafting and solution architecture (R34, R35)
  - [ ] 39.1 Implement AI-drafted Technical_Assessment versions and confirmation
    - Draft Job (requires a stored analysis) creates a version with the R29 structure, `ai_generated=true`, unconfirmed; labels outside the six service groups are rejected with a structured error; complexity exactly one of Low, Medium, High, Very High with non-empty justification; `POST /admin/technical-assessments/{id}/versions/{version}/confirm` (Engineer or Founder, 403 otherwise) records confirming user and time; saving an edit stores a new Confirmed version; Audit_Log entries on draft and confirm
    - _Requirements: 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.8_
  - [ ] 39.2 Implement the `ArchitectureGraph` schema and validator
    - Typed nodes and edges per Appendix B.4; validation reports each violation by name in the 422 `fields` (unique ids, edge endpoints exist, allowed node and edge types, acyclic containment, no self-loops); technology stack items need a non-empty rationale; technical decisions need decision, alternatives, and rationale
    - _Requirements: 35.1, 35.2, 35.3_
  - [ ] 39.3 Implement Solution_Architecture versions and endpoints
    - `POST /admin/projects/{id}/architectures` (manual or from a Solution_Architect draft), `GET /admin/architectures/{id}/versions`, `POST /admin/architectures/{id}/versions/{version}/confirm` (Engineer or Founder, Audit_Log entry), `GET /admin/architectures/{id}/versions/{version}/export.json`; each change stores a new version and leaves earlier versions unchanged; Internal_Only until included in an Approved Proposal_Version, with 404 for Clients otherwise
    - _Requirements: 35.4, 35.7, 35.8, 35.9, 35.10_
  - [ ] 39.4 Register the Solution Designed guard
    - Pure guard requiring a Confirmed Technical_Assessment_Version and a confirmed Solution_Architecture_Version; failure returns 409 with the guard named
    - _Requirements: 34.7_
  - [ ]* 39.5 Write property test for graph round trip
    - **Property 22: Architecture graph round trip**
    - Generate valid graphs; assert JSON serialize then parse yields an equal graph
    - **Validates: Requirements 35.11**
  - [ ]* 39.6 Write property test for graph integrity
    - **Property 23: Architecture graph integrity**
    - Generate valid and corrupted graphs (dangling edges, duplicate ids, unknown types); assert every accepted graph has unique ids and valid endpoints and every corrupted one is rejected naming the violation
    - **Validates: Requirements 35.12**
  - [ ]* 39.7 Write property test for the Solution Designed guard
    - **Property 21: Solution Designed guard**
    - Generate assessment and architecture confirmation states and transition attempts; assert every Project in Solution Designed has both confirmed versions
    - **Validates: Requirements 34.9**
  - [ ]* 39.8 Write unit tests for assessment confirmation
    - Non-Engineer confirmation (403), invalid label, missing justification, Audit_Log entries
    - _Requirements: 34.2, 34.3, 34.6, 34.8_

- [ ] 40. Checkpoint: discovery flow
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 41. Implement proposals and pricing (R36, R37)
  - [ ] 41.1 Implement `ProposalService` versioning and approval
    - One Proposal per Project; `POST /admin/proposals`, `POST /admin/proposals/{id}/versions`, `GET /admin/proposals/{id}/versions`, `POST /admin/proposal-versions/{id}/submit-for-review`, `POST /admin/proposal-versions/{id}/approve`; version schema requires every R36.3 section and the preliminary, not-a-contract statement; the architecture section accepts only a confirmed Solution_Architecture_Version (422 otherwise); the indicative cost section is filled only from task 41.2 and 41.3 records
    - `generate-proposal` (task 37.2) creates a Draft version marked AI-generated; the proposal output schema has no customer, benchmark, or guarantee fields, and drafts containing configured guarantee phrases are rejected
    - Approval by an Authorized_Approver computes and stores `content_hash`; edits to Approved, Sent, Superseded, or Withdrawn versions return 409 and require a new version; Audit_Log entry on each status change; Project moves to Proposal Under Review per Appendix A.1
    - _Requirements: 36.1, 36.2, 36.3, 36.4, 36.5, 36.6, 36.7, 36.8, 36.9, 36.10, 36.12_
  - [ ] 41.2 Implement `PricingService` price entries
    - `POST /admin/price-entries`, `GET /admin/price-entries`, `POST /admin/price-entries/{id}/approve`; only an Authorized_Approver (Founder or A-06 delegate via grant) enters or approves (403 otherwise); approval goes through an Approval_Request (task 34.1); currency and amount validation; a Proposal_Version includes only approved prices; Audit_Log entry with actor, amount, currency, and Proposal_Version on enter, edit, approve
    - _Requirements: 37.1, 37.2, 37.3, 37.8, 43.10_
  - [ ] 41.3 Implement Cost_Estimates
    - `POST /admin/cost-estimates`, `GET /admin/cost-estimates/{id}`; Agent_Runtime task separates cloud infrastructure cost from NEUROPATH service fees with assumptions per figure; missing grounded inputs produce "no estimate provided" with the missing list; any figure without a traceable stored input is rejected with a structured error; labeled indicative and Internal_Only until approved
    - _Requirements: 37.4, 37.5, 37.6, 37.7_
  - [ ]* 41.4 Write property test for proposal hash immutability
    - **Property 24: Proposal hash immutability**
    - Generate Approved versions and later operation sequences, including rejected edits; assert the recomputed hash always equals the stored hash
    - **Validates: Requirements 36.13**
  - [ ]* 41.5 Write unit tests for proposals and pricing
    - Unconfirmed architecture (422), missing preliminary statement, edit of Approved version (409), non-approver price (403), untraceable estimate figure rejected, missing inputs produce no estimate
    - _Requirements: 36.4, 36.7, 36.10, 37.3, 37.5, 37.7_

- [ ] 42. Implement proposal sending and export (R40)
  - [ ] 42.1 Implement send and withdraw
    - `POST /admin/proposal-versions/{id}/send` only for Approved versions (409 otherwise) and only with an Approved Approval_Request for "issuing commercial quotations" and "sharing confidential information" whose hash equals the version hash (403 plus Audit_Log entry otherwise); sets Sent, supersedes the previously Sent version, makes it Client_Visible for the owning Organization, notifies the Client, and moves the Project to Proposal Sent then Awaiting Client Decision; external email only through task 34.3; `POST /admin/proposal-versions/{id}/withdraw`; Audit_Log entry with actor, version, and hash
    - _Requirements: 40.1, 40.2, 40.3, 40.4, 40.5, 40.6, 40.7, 40.8, 40.11_
  - [ ] 42.2 Implement proposal export
    - `GET /proposal-versions/{id}/export` renders a PDF from stored content only after `verify_content_hash` passes (renderer library recorded in `ARCHITECTURE.md`); includes the preliminary, not-a-contract statement; Approved or Sent for staff, Sent only for Clients of the owning Organization (404 otherwise); Audit_Log entry with actor, version, and hash
    - _Requirements: 36.11, 40.9, 40.10, 40.11_
  - [ ]* 42.3 Write property test for single sent version and export fidelity
    - **Property 28: Single sent version and export fidelity**
    - Generate send, withdraw, and new-version sequences; assert at most one Sent version per Proposal and every export is generated from content matching the approved hash
    - **Validates: Requirements 40.12, 40.13**
  - [ ]* 42.4 Write property test for approved pricing
    - **Property 25: Approved pricing**
    - Generate price entries with and without approval and send attempts; assert every price in a Sent version has a recorded Authorized_Approver approval
    - **Validates: Requirements 37.9**
  - [ ]* 42.5 Write unit tests for sending and export
    - Send of non-Approved (409), missing or mismatched approval (403 plus audit), Client export of Draft or In Review (404), preliminary statement present in the PDF text
    - _Requirements: 40.2, 40.4, 40.9, 40.10_

- [ ] 43. Implement client proposal decisions (R38)
  - [ ] 43.1 Implement Communications for proposal clarification
    - `communications` rows with visibility (Client_Visible or Internal_Only), Project and optional Proposal_Version link, author, and body; Client reads filter on visibility; edit history (`communication_versions`) stays in Phase 4
    - _Requirements: 38.7, 18.8_
  - [ ] 43.2 Implement `record_client_decision` and off-platform acceptance
    - `POST /proposal-versions/{id}/decisions` with kind accept, decline, or request_clarification; Clients see only Sent versions of their own Organization (404 otherwise); decision permission per Appendix A.3 for Owner and Member (403 otherwise); Superseded or Withdrawn returns 409 with no record; accept takes a row lock on the Proposal, returns 409 if an acceptance exists, creates an Acceptance_Record with user, Organization, time, version, and the approved `content_hash`, supersedes other Sent versions, and moves the Project to Accepted (T18, A-35) through a guard requiring the Acceptance_Record
    - Decline stores user, time, and optional reason; clarification creates a Client_Visible Communication and keeps Awaiting Client Decision; `POST /admin/proposal-versions/{id}/offplatform-acceptance` (Founder) requires an evidence reference (422 otherwise) and marks the source off-platform; every decision writes an Audit_Log entry and notifies the Founder
    - _Requirements: 38.1, 38.2, 38.3, 38.4, 38.5, 38.6, 38.7, 38.8, 38.9, 38.10, 38.11, 38.12, 38.13, 38.14, 38.15_
  - [ ]* 43.3 Write property test for accepted equals approved
    - **Property 26: Accepted equals approved**
    - Generate concurrent and repeated decisions across versions, including off-platform acceptances; assert each Acceptance_Record hash equals the approval hash and at most one version per Proposal has an accept
    - **Validates: Requirements 38.16, 38.17**
  - [ ]* 43.4 Write unit tests for client decisions
    - Member without permission (403), non-Sent or other-Organization version (404), second acceptance (409), off-platform without evidence (422), clarification keeps the Project status
    - _Requirements: 38.2, 38.4, 38.7, 38.9, 38.11_

- [ ] 44. Implement Agreement records (R39)
  - [ ] 44.1 Implement `AgreementService` and endpoints
    - `POST /admin/agreements`, `GET /agreements/{id}`, `POST /admin/agreements/{id}/transitions`, `POST /admin/agreements/{id}/signed-document`; Founder or Administrator only (403 otherwise); creation requires an accepted Proposal_Version for the Project (422 otherwise); parties, Project, accepted version, effective date, optional end date (end before effective returns 422); statuses through the engine (409 on undefined transitions); signed document stored as an Attachment under R20 via `attachments.agreement_id`; notes Internal_Only; Clients see status and the document marked approved for the Client only; no e-signature or payment code; Audit_Log entries
    - The Maintenance_Engagement reference waits for Phase 4 (`agreements.maintenance_engagement_id`)
    - _Requirements: 39.1, 39.2, 39.3, 39.4, 39.5, 39.6, 39.7, 39.8, 39.10, 39.11, 39.12_
  - [ ] 44.2 Register the activation guard for Phase 4
    - Pure guard `agreement_in_effect` on the Accepted to In Progress row with `enabled_phase=4`, so the row stays disabled in Phase 3
    - _Requirements: 39.9_
  - [ ]* 44.3 Write property test for the activation guard
    - **Property 27: Activation guard**
    - With the phase set to 4 in the test, generate Agreement states and activation attempts; assert every allowed transition to In Progress has an Agreement In Effect at that time
    - **Validates: Requirements 39.13**
  - [ ]* 44.4 Write unit tests for Agreements
    - No accepted version (422), date order (422), non-Founder/Administrator (403), undefined transition (409), Client sees status and approved document only
    - _Requirements: 39.2, 39.3, 39.5, 39.6, 39.11_

- [ ] 45. Implement consultation requests and Engineering_Service_Requests (R41)
  - [ ] 45.1 Implement the Engineering_Service_Request and consultation API
    - `POST /projects/{id}/service-requests`, `GET /projects/{id}/service-requests`, and a public submission path; fields problem, desired outcome, systems and data, constraints, optional service hint (empty allowed); creates the Project_Inquiry through the R14 path with the same validation, rate limit, consent, and submission token; signed-in Clients link to their own Organization only
    - Lab output actions: request consultation and submit inquiry create Project_Inquiry, Project (Submitted), and Lead; request detailed proposal creates an Internal_Only Communication note and no Proposal_Version, price, or quotation; save solution requires sign-in; Audit_Log entry for each action
    - _Requirements: 41.2, 41.3, 41.4, 41.6, 41.7, 41.8, 41.9_
  - [ ]* 45.2 Write property test for idempotent service request submission
    - **Property 15: Idempotent inquiry submission**
    - Generate repeated Engineering_Service_Request and Lab-action submissions with the same key; assert exactly one Project_Inquiry and one Project
    - **Validates: Requirements 41.10**

- [ ] 46. Build the Founder_Control_Center Phase 3 screens
  - [ ] 46.1 Implement discovery screens
    - Solution_Architect invocation control (hidden when the flag is off or the user lacks permission); data-category disclosure before the first analysis; analysis versions labeled AI-generated; question drafting, approval, and send; Technical_Assessment draft review and confirm; architecture view rendering React Flow from validated graph data only with a text alternative listing nodes and connections; publish-part control
    - _Requirements: 31.5, 31.10, 32.5, 33.2, 34.5, 35.5, 35.6_
  - [ ] 46.2 Implement proposal, pricing, approval, agreement, and usage screens
    - Proposal version editor and history, submit for review, approve, send, withdraw, export; price entries and Cost_Estimates labeled indicative; pending Approval_Requests queue with approve and reject-with-reason; off-platform acceptance with evidence reference; Agreement creation, transitions, and signed document upload; usage per Organization and total for a period; loading, empty, and error-with-retry states
    - _Requirements: 36.11, 37.6, 38.8, 39.1, 40.1, 42.8, 43.3_
  - [ ]* 46.3 Write component tests for Phase 3 Founder screens
    - Hidden controls by permission and flag, disclosure shown before first analysis, diagram text alternative, approval reject requires reason
    - _Requirements: 17.9, 31.10, 32.5, 35.6_

- [ ] 47. Build the Client_Workspace and public Phase 3 screens
  - [ ] 47.1 Extend the Client_Workspace
    - Sent proposals with export download and Accept, Decline (optional reason), Request Clarification controls shown per permission; Agreement status and approved document; published Solution_Architect parts; Engineering_Service_Request form in the workspace; values from API responses only
    - _Requirements: 31.5, 38.1, 38.3, 39.11, 40.5, 41.1, 41.4_
  - [ ] 47.2 Implement the public Solution_Architect Lab and service request pages
    - Lab page shown only when `solution_architect_lab` is on; Guest limit message with sign-in prompt on 429; "Discuss This Solution With NEUROPATH" control with request consultation, submit inquiry, request detailed proposal, and save solution (sign-in required for save); public Engineering_Service_Request form with an optional service hint
    - _Requirements: 31.7, 31.8, 31.9, 41.1, 41.2, 41.5, 41.8_
  - [ ]* 47.3 Write component and Playwright tests for Client and Lab screens
    - Decision controls by permission, Lab hidden with flag off, save requires sign-in, form submits with empty service hint
    - _Requirements: 31.10, 38.4, 41.2, 41.8_

- [ ] 48. Wire Phase 3 together and implement the gate check
  - [ ] 48.1 Write the Phase 3 API integration test
    - One flow with the recorded-response stub: qualified inquiry analyzed, questions approved, sent, and answered, re-analysis stored, Technical_Assessment and architecture confirmed, Project in Solution Designed, proposal drafted, priced, approved, approval-gated send, Client accepts, Project Accepted, Agreement created; a second flow declines; Audit_Log entries and usage records present; no Bedrock call made
    - _Requirements: 32.13, 33.7, 34.7, 38.13, 39.1, 40.8, 77.10, 78.8_
  - [ ] 48.2 Add the Lab-independence regression test
    - With both Solution_Architect flags off, the R14 inquiry flow and Phase 2 review flow pass and Solution_Architect endpoints return 404
    - _Requirements: 31.10, 31.11_
  - [ ] 48.3 Extend `phase_gate.py` with `--phase 3` and update affected docs
    - Confirms inquiry analysis, clarification, Technical_Assessment confirmation, validated architecture, Proposal versioning, human-approved pricing, approval-gated sending, client accept and decline, and Agreement records; confirms the Bedrock adapter is code only with no deployment record and CI uses the stub; update `DATABASE.md`, `API.md`, `SECURITY.md` (hashing, approvals, prompt-injection handling), `ENVIRONMENT.md` (model and limit settings), `ARCHITECTURE.md`, `TESTING.md`, `IMPLEMENTATION_STATUS.md` in the same change set
    - _Requirements: 5.4, 5.5, 77.10, 78.1, 78.3, 78.8_

- [ ] 49. Checkpoint: Phase 3 gate
  - Ensure all tests pass, ask the user if questions arise.
  - The Phase 3 gate (R78.8) passes, Phase 0 to Phase 2 features still work (R78.3), and the phase report is ready for Founder review before Phase 4 starts (R78.2).

### Phase 4A: Project Delivery (R44 to R55, R79)

- [ ] 50. Create the Phase 4 database migration
  - [ ] 50.1 Write the Alembic migration for the Phase 4 (4A) tables in Appendix B.3
    - Tables: `project_members`, `project_milestones`, `milestone_acceptance_criteria`, `project_tasks`, `communication_versions`, `deliverables`, `deliverable_versions`, `test_activities`, `defects`, `deployment_records`, `handover_checklist_items`, `delivery_references`, `change_requests`, `scope_baselines`, `support_requests`, `support_comments`, `maintenance_engagements`, `commercial_records`, `lab_registrations`, `feature_flag_organizations`
    - Column additions: `attachments` gets `deliverable_version_id`, `test_activity_id`, `handover_checklist_item_id`, `support_request_id`, `support_comment_id`; `acceptance_records` gets `project_milestone_id`, `deliverable_version_id`, `delivery_reference_id`, `change_request_id`; `agreements` gets `maintenance_engagement_id`
    - Data Playground tables come in Phase 4B, not in this migration
    - `organization_id` on every tenant-owned table (scoping is enforced by `OrgScope` repositories, task 19.1); append-only triggers on `scope_baselines` and Acceptance_Records; check constraints for status and severity enums
    - _Requirements: 6.9, 44.4, 45.1, 46.1, 47.8, 53.1, 54.2, 55.6, 79.1_
  - [ ]* 50.2 Write migration tests
    - Upgrade and downgrade run clean; a cross-Organization read through the `OrgScope` repositories returns nothing; update and delete on `scope_baselines` fail
    - _Requirements: 6.9, 54.10_

- [ ] 51. Implement Project activation and team assignment
  - [ ] 51.1 Enable Phase 4 Project statuses and the activation guard
    - Enable In Progress, Testing, Awaiting Client Acceptance, Delivered, and Completed per Appendix A.1; Accepted to In Progress runs the `agreement_in_effect` guard (R39.9) and rejects with a structured error and Audit_Log entry when it fails
    - On success, create Scope_Baseline version 1 copying scope, milestones, and deliverables from the accepted Proposal_Version in the same transaction
    - _Requirements: 39.9, 44.1, 44.2, 44.3, 54.1_
  - [ ] 51.2 Implement Project_Member assignment and the assigned-writer dependency
    - Assign, change role, and unassign (end date kept) with roles Project Lead, Engineer, Reviewer; staff users only; Audit_Log entries; Client team view returns display name, project role, and Client_Visible contact fields only
    - Reusable `require_project_writer` dependency (current member, Founder, or Administrator) applied to every delivery write route; Engineer access limited to assigned Projects
    - _Requirements: 44.4, 44.5, 44.6, 44.7, 44.8, 44.9, 44.10_
  - [ ]* 51.3 Write unit tests for activation and assignment
    - Activation rejected without an Agreement In Effect; Scope_Baseline v1 created once; unassigned user write returns 403; Client team view hides internal fields
    - _Requirements: 44.3, 44.7, 44.10, 54.1_

- [ ] 52. Implement milestones and tasks
  - [ ] 52.1 Implement Project_Milestone endpoints
    - CRUD with due date not before planned start; statuses per Appendix A.2; Client accept and reject (reason required) only in Ready for Review, creating Acceptance_Records; progress computed from Task counts and never accepted as input; Audit_Log and R27 Notifications
    - _Requirements: 45.1, 45.2, 45.3, 45.4, 45.5, 45.6, 45.7, 45.8, 45.10_
  - [ ]* 52.2 Write property test for milestone progress
    - **Property 31: Milestone progress formula**
    - Generate Task status mixes; assert progress in 0 to 100 and equal to Done over non-Cancelled times 100, 0 when none
    - **Validates: Requirements 45.11**
  - [ ] 52.3 Implement Task endpoints
    - Tasks within one milestone, Internal_Only by default; statuses per Appendix A.2; Blocked requires a reason; assignee must be a current Project_Member; assignee change audited; derived overdue flag; Client writes return 403 and Client reads return Client_Visible Tasks only
    - _Requirements: 46.1, 46.2, 46.3, 46.4, 46.5, 46.6, 46.7, 46.8, 46.9_
  - [ ]* 52.4 Write unit tests for Tasks
    - Non-member assignee rejected, Blocked without reason rejected, Client write 403, overdue derivation
    - _Requirements: 46.3, 46.4, 46.6, 46.7_

- [ ] 53. Implement project communication
  - [ ] 53.1 Implement the Project thread and project updates
    - One thread per Project; staff messages Internal_Only by default, Client messages Client_Visible; edits write a `communication_versions` row with editor and time; server-side sanitization; attachments via R20; project updates with status summary from members, Founder, or Project_Manager; AI-drafted updates held until human approval; Notifications and Audit_Log for Client_Visible posts
    - _Requirements: 47.1, 47.2, 47.3, 47.4, 47.5, 47.6, 47.7, 47.8, 47.9, 47.10_
  - [ ]* 53.2 Write unit tests for communication isolation
    - Client thread response contains no Internal_Only message; edit history retained; script payload sanitized
    - _Requirements: 47.4, 47.8, 47.9, 47.11_

- [ ] 54. Implement Deliverables
  - [ ] 54.1 Implement Deliverable and version endpoints
    - Types per R48.1, optional milestone link, new version per revision; Source-Code Handover Reference stored as repository URL plus commit or tag, rejecting embedded credentials or tokens; files via R20 scan and Presigned_URLs; Approved for Client by permission holders; Client download audited; Client accept or reject (reason required) creates Acceptance_Records
    - _Requirements: 48.1, 48.2, 48.3, 48.4, 48.5, 48.6, 48.7, 48.8, 48.9_
  - [ ]* 54.2 Write unit tests for Deliverable access
    - Client cannot download non-approved or other-Organization versions; URL with credentials rejected; download writes Audit_Log
    - _Requirements: 48.4, 48.7, 48.9_

- [ ] 55. Implement testing and quality records
  - [ ] 55.1 Implement test activities, acceptance criteria, Defects, and the quality gate
    - Test activities with Pass, Fail, Blocked and R20 evidence; per-milestone criteria Met or Not Met; Defects with A-18 severities and Appendix A.2 statuses; resolution note required for Resolved and Won't Fix; Founder approval for Won't Fix on Blocker or Critical; Client testing feedback as Client_Visible entry
    - In Progress to Testing by Project Lead; Testing to Awaiting Client Acceptance guarded, rejection lists blocking Defects and unmet criteria; Audit_Log on every change
    - _Requirements: 49.1, 49.2, 49.3, 49.4, 49.5, 49.6, 49.7, 49.8, 49.9, 49.10_
  - [ ]* 55.2 Write property test for the quality gate
    - **Property 32: Quality gate**
    - Generate Defect and criterion sets; assert the transition succeeds only when the R49.8 guard holds
    - **Validates: Requirements 49.11**

- [ ] 56. Implement deployment records and handover
  - [ ] 56.1 Implement the secret detection validator
    - `apps/api/app/core/secret_detection.py` with configurable patterns (keys, tokens, private keys, connection strings with passwords); returns the field name only and never logs the matched value
    - _Requirements: 50.3, 50.13_
  - [ ] 56.2 Implement Deployment_Record and Handover_Checklist endpoints
    - Deployment_Records with environment type, version reference, Appendix A.2 statuses (409 on undefined transitions), Internal_Only by default; credential handover as secret-store or out-of-band reference only; one checklist per Project; mandatory Done items need evidence; Awaiting Client Acceptance to Delivered guarded with open items listed; Client writes 403; Audit_Log entries
    - _Requirements: 50.1, 50.2, 50.4, 50.5, 50.6, 50.7, 50.8, 50.9, 50.10, 50.11_
  - [ ]* 56.3 Write property test for the handover gate
    - **Property 33: Handover gate**
    - Generate checklists with mixed mandatory item statuses; assert Delivered only when all mandatory items are Done
    - **Validates: Requirements 50.12**
  - [ ]* 56.4 Write property test for no stored secrets
    - **Property 34: No stored secrets**
    - Generate field values with embedded secret-shaped strings; assert rejection and that no stored row matches any pattern
    - **Validates: Requirements 50.13**

- [ ] 57. Implement final delivery acceptance
  - [ ] 57.1 Implement the delivery reference and final decision endpoints
    - On entering Delivered, compute and store the delivery reference (approved Deliverable versions, checklist statuses) and its content hash; accept creates an Acceptance_Record with the hash and moves to Completed; reject requires a reason and moves to In Progress or Testing per Appendix A.1; permission 403, other Organization 404, wrong status 409; Founder off-platform acceptance requires evidence (422 otherwise); Notifications and Audit_Log
    - _Requirements: 51.1, 51.2, 51.3, 51.4, 51.5, 51.6, 51.7, 51.8, 51.9, 51.10, 51.11, 51.12_
  - [ ]* 57.2 Write property test for completion and delivery acceptance
    - **Property 35: Completion and delivery acceptance**
    - Generate delivery and decision sequences; assert every Completed Project has a final Acceptance_Record whose hash equals the Delivered reference hash
    - **Validates: Requirements 51.13, 51.14**

- [ ] 58. Implement support requests
  - [ ] 58.1 Implement Support_Request and support comment endpoints
    - Client creation on own-Organization Projects in eligible statuses (404 for other Organizations, structured error for ineligible status); Appendix A.2 statuses with 409; comment visibility rules; R20 attachments and sanitization; no response-time commitment displayed; Client history list; Notifications and Audit_Log
    - _Requirements: 52.1, 52.2, 52.3, 52.4, 52.5, 52.6, 52.7, 52.8, 52.9, 52.10_
  - [ ]* 58.2 Write unit tests for support tenancy and comment isolation
    - Other-Organization Project returns 404 with no row created; Client responses exclude Internal_Only comments
    - _Requirements: 52.2, 52.11, 52.12_

- [ ] 59. Implement Maintenance_Engagements
  - [ ] 59.1 Implement Maintenance_Engagement endpoints
    - Create linked to one same-Organization originating Project with status Proposed; Appendix A.2 statuses with 409; Proposed to Active requires an Agreement In Effect via `agreements.maintenance_engagement_id` and the R39.9 guard; reason required for Suspended or Ended; maintenance tasks reuse the R46 rules; Support_Request links only from the originating Project; Client read limited to status, Client_Visible scope, and Agreement status; Audit_Log
    - _Requirements: 53.1, 53.2, 53.3, 53.4, 53.5, 53.7, 53.8, 53.9, 53.10, 53.11_
  - [ ]* 59.2 Write unit tests for maintenance activation
    - Activation without Agreement In Effect rejected and audited; Support_Request from another Project rejected
    - _Requirements: 53.4, 53.8, 53.11_

- [ ] 60. Implement change requests and scope baselines
  - [ ] 60.1 Implement Change_Request and Scope_Baseline endpoints
    - Submission by Client or Project_Member while the Project is in an Active_Engagement status; Internal_Agent impact edits return 403 and are audited; Appendix A.2 statuses with 409; timeline or cost impact needs an Approved R43 Approval_Request with matching content hash, otherwise Founder or Project_Manager decision; Approved requires a client or off-platform Acceptance_Record for the content hash; Implemented creates the next Scope_Baseline version referencing the Change_Request; edit or delete of a baseline returns 405 or 409; Notifications and Audit_Log
    - _Requirements: 54.2, 54.3, 54.4, 54.5, 54.6, 54.7, 54.8, 54.9, 54.10, 54.11_
  - [ ]* 60.2 Write property test for scope baseline immutability and provenance
    - **Property 36: Scope baseline immutability and provenance**
    - Generate random operation sequences; assert earlier versions unchanged and each version above 1 references one Change_Request Approved before creation
    - **Validates: Requirements 54.12, 54.13**

- [ ] 61. Implement the Lab module framework
  - [ ] 61.1 Create `apps/api/labs/` with the Lab registry
    - Registration with unique id, name, status (disabled, internal, client beta, available), controlling Feature_Flag, and non-overlapping owned route prefixes, stored in `lab_registrations`; register the Data Engineering Playground (disabled) and the AI Solution Architect Lab (public path, flag `solution_architect_lab`)
    - The Engineering_Service_Request stays a core feature and is not a Lab (R41)
    - Route middleware returns 404 per status and principal, using `feature_flag_organizations` for client beta; status change only by Founder or delegated Administrator, audited; Web_App hides navigation for disabled Labs via an API Lab-status endpoint
    - _Requirements: 1.4, 55.1, 55.2, 55.3, 55.4, 55.5, 55.6, 55.7, 55.10, 55.11_
  - [ ] 61.2 Extend the Lab import check
    - Extend `scripts/check_lab_imports.py` (task 1.3) to cover `apps/api/labs/` and the new Lab modules; it already runs in CI
    - _Requirements: 55.8, 55.9_
  - [ ]* 61.3 Write property test for Lab independence
    - **Property 38: Lab independence**
    - With every Lab disabled, run the R14 inquiry and R44 to R54 project flow tests; assert they pass and Lab routes return 404
    - **Validates: Requirements 55.12**

- [ ] 62. Implement Commercial_Records
  - [ ] 62.1 Implement Commercial_Record endpoints (status tracking only)
    - Types, non-negative amount, ISO 4217 currency, due date, Appendix A.2 statuses with 409; one Project link plus optional same-Project links (field error otherwise); create or change only by the Founder or a delegate, 403 and audit for others and for Internal_Agent or AI principals; card number and bank credential patterns rejected; no payment processing code
    - Draft to Issued requires an Approved Approval_Request of type issue commercial quotation with matching content hash (R43.10); Paid Recorded requires an evidence reference; Overdue derived after due date; Internal_Only by default; Client responses list Client_Visible records only; Audit_Log on create, status, amount, and visibility changes
    - _Requirements: 43.10, 79.1, 79.2, 79.3, 79.4, 79.5, 79.6, 79.7, 79.8, 79.9, 79.10, 79.11, 79.12, 79.13, 79.14, 79.15, 79.16, 79.18_
  - [ ]* 62.2 Write property test for human-authored amounts
    - **Property 37: Human-authored amounts**
    - Generate principals (Founder, delegate, staff, Internal_Agent, AI) and amount writes; assert every stored amount was last set by the Founder or a delegate
    - **Validates: Requirements 79.17**
  - [ ]* 62.3 Write unit tests for Commercial_Record guards
    - Issue without approval rejected, card number rejected with no value stored, Paid Recorded without evidence rejected, Client sees no Internal_Only record
    - _Requirements: 79.8, 79.11, 79.12, 79.18_

- [ ] 63. Build the Founder_Control_Center Phase 4 screens
  - [ ] 63.1 Implement project delivery screens
    - Activation control with guard error display; team assignment; milestones with computed progress; task board; thread with visibility selector and edit history; Deliverable versions and approval; test, criteria, and Defect views with quality-gate errors; deployments and handover checklist; final acceptance and off-platform record
    - _Requirements: 44.3, 44.4, 45.7, 46.1, 47.2, 48.6, 49.9, 50.9, 51.9_
  - [ ] 63.2 Implement support, maintenance, change request, Lab, and commercial screens
    - Support queue with comment visibility; Maintenance_Engagements; Change_Request review and Scope_Baseline history; Lab status management; Commercial_Records with approval request for issue and Paid Recorded evidence; loading, empty, and error-with-retry states
    - _Requirements: 52.5, 53.1, 54.9, 55.7, 79.8, 79.10_
  - [ ]* 63.3 Write component tests for Phase 4 Founder screens
    - Visibility defaults to Internal_Only, guard errors listed, Lab status control hidden without permission
    - _Requirements: 47.2, 49.9, 55.7_

- [ ] 64. Build the Client_Workspace Phase 4 screens
  - [ ] 64.1 Extend the Client_Workspace
    - Upcoming Client_Visible milestones with progress and accept or reject; team view; project thread; approved Deliverables with download and decision; final delivery decision; Support_Request form and history with no response-time text; Maintenance_Engagement status; Change_Request submission and decisions; Client_Visible Commercial_Records read only
    - _Requirements: 44.7, 45.9, 47.4, 48.8, 51.3, 52.8, 52.9, 53.9, 54.3, 79.14_
  - [ ]* 64.2 Write component and Playwright tests for Client Phase 4 screens
    - Rejection requires reason, no write controls for Tasks or deployments, disabled Lab not in navigation
    - _Requirements: 45.6, 46.7, 51.8, 55.4_

- [ ] 65. Checkpoint: delivery core
  - Ensure all tests pass, ask the user if questions arise.

### Phase 4B: Data Engineering Playground (R56 to R63, only after a go decision, A-04)

- [ ] 66. Checkpoint: confirm the Founder's go decision for the Playground (A-04)
  - Confirm the Founder's go decision is recorded at the Phase 4 gate before any task 67 to 74 work starts; if no go decision is recorded, skip tasks 67 to 74 and keep the Playground Lab disabled
  - Ensure all tests pass, ask the user if questions arise.
  - _Requirements: 55.11, 78.2_

- [ ] 67. Create the Phase 4B database migration
  - [ ] 67.1 Add the Alembic revision for Playground tables
    - Tables per Appendix B.3 for Phase 4B: `datasets`, `dataset_profiles`, `pipelines`, `pipeline_versions`, `recommendations`, `pipeline_executions`; read the exact columns, keys, and retention from `requirements.md` Appendix B.3 and B.5
    - `organization_id` on tenant-owned tables with `OrgScope` repositories; status check constraints from Appendix A; working downgrade; upgrade, downgrade, upgrade round trip on an empty database
    - _Requirements: 6.3, 6.7, 56.17, 57.5, 59.6_
  - [ ]* 67.2 Write migration tests
    - Round trip on an empty database; cross-Organization queries through repositories return nothing
    - _Requirements: 6.7, 77.5_

- [ ] 68. Create the root `data_engine/` package
  - [ ] 68.1 Implement format handling, profiling, and validation
    - Create `data_engine/` with `profiling`, `validation`, `transformations`, `feature_engineering`, `reporting` modules; CSV, XLSX, and JSON readers behind a format interface; extension, content type, size, and row limit checks
    - Profile: row and column counts, inferred types, missing counts, numeric and categorical statistics, invalid values, outliers, inconsistent formats, wrong types, leakage indicators; identical Profiles for the same file; no partial Profile on parse failure
    - _Requirements: 56.4, 56.13, 56.14, 57.2, 57.3, 57.4, 57.7, 57.10, 57.11_
  - [ ] 68.2 Implement the Operation allowlist and transformations
    - Allowlist (remove duplicates, drop columns, drop rows by condition, fill missing values, and the rest listed in R59.12) with a parameter schema per Operation; deterministic Pandas, Polars, PyArrow, and scikit-learn implementations; the same code path serves preview and execution; the original file is never modified
    - _Requirements: 59.5, 59.12, 59.13, 59.15, 60.2_
  - [ ] 68.3 Implement feature engineering and reporting
    - Seeded split before any fit; encoders, scalers, imputers, and selectors fit on the training split only; fitted transform metadata stored with the output; leakage warnings; cleaned dataset, quality report, transformation summary, pipeline configuration, and CSV, Parquet, JSON, XLSX writers
    - _Requirements: 61.1, 61.2, 61.3, 62.1, 62.3, 62.4, 62.5, 62.7_
  - [ ]* 68.4 Write property test for profile correctness and idempotence
    - **Property 40: Profile correctness and idempotence**
    - **Validates: Requirements 57.10, 57.11**
  - [ ]* 68.5 Write property test for preview fidelity and original file immutability
    - **Property 42: Preview fidelity and original file immutability**
    - **Validates: Requirements 59.15, 59.16**
  - [ ]* 68.6 Write property test for output integrity, CSV round trip, and format equivalence
    - **Property 46: Output integrity, CSV round trip, and format equivalence**
    - **Validates: Requirements 61.8, 61.9, 61.10**
  - [ ]* 68.7 Write property test for split determinism, disjointness, and train-only fit
    - **Property 48: Split determinism, disjointness, and train-only fit**
    - **Validates: Requirements 62.9, 62.10, 62.11**

- [ ] 69. Implement Dataset upload through the R20 attachment path
  - [ ] 69.1 Implement the dataset endpoints and upload gate
    - `/api/v1/datasets` upload-url, complete-upload, list, get, delete, profile; Guest gets 401 and no object; Presigned_URL valid at most 10 minutes through the R20 storage path; Dataset created only after the object exists; recorded processing confirmation; same-Organization Project link only (404 otherwise); server-side extension, content type, size, row, and time limits; malware scan through the R20 path with quarantine; Audit_Log on create, reject, and quarantine; profiling as a Job returning 202 under R19 and R64, isolated with CPU, memory, and time limits
    - _Requirements: 56.2, 56.3, 56.5, 56.8, 56.9, 56.10, 56.11, 56.12, 56.13, 56.14, 56.15, 56.16, 56.17, 56.18, 56.19, 57.1, 57.9_
  - [ ] 69.2 Wire the profiling Job
    - Run `data_engine` profiling through the ENGINE; store the Profile in `dataset_profiles`; expose status queued, running, completed, failed
    - _Requirements: 57.1, 57.5, 57.7_
  - [ ]* 69.3 Write property test for the upload gate
    - **Property 39: Upload gate**
    - **Validates: Requirements 56.20**
  - [ ]* 69.4 Write unit tests for upload rejections
    - Disallowed extension, mismatched content type, oversize, malformed file, malware, cross-Organization link, expired presigned URL, Guest 401
    - _Requirements: 56.3, 56.12, 56.14, 56.15_

- [ ] 70. Implement AI Recommendations with bounded disclosure
  - [ ] 70.1 Implement the Recommendation service
    - Agent_Runtime sends only Profile statistics and a sample bounded by Founder configuration; Dataset contents treated as untrusted input; schema validation with at most 2 retries then a structured error; accept only allowlisted Operations with valid parameters, otherwise discard and record; first-use disclosure of what is sent to the AI provider; usage and cost recorded under R42 with Organization limits; Recommendations are added to a Pipeline only after user approval
    - Model-generated code is never executed; no code path evaluates model output as code
    - _Requirements: 58.1, 58.2, 58.3, 58.4, 58.5, 58.6, 58.7, 58.9, 58.10, 58.11_
  - [ ]* 70.2 Write property test for Recommendation allowlist and bounded disclosure
    - **Property 41: Recommendation allowlist and bounded disclosure**
    - **Validates: Requirements 58.12, 58.13**
  - [ ]* 70.3 Write unit tests for Recommendation handling
    - Embedded instruction in cell values ignored, out-of-allowlist Operation discarded, retry limit, no code execution of model output
    - _Requirements: 58.4, 58.6, 58.7, 58.9_

- [ ] 71. Implement the Pipeline builder and execution as ENGINE Jobs
  - [ ] 71.1 Implement pipeline endpoints and versioning
    - `/api/v1/pipelines` create, list, get, patch, validate, execute; a new Pipeline version on each change with prior versions unchanged; validation of allowlist, parameters, and referenced columns; recorded approval of the current version required, cleared on change, 409 without approval and no Job; Audit_Log on approval and clearing; destructive Operations need explicit confirmation
    - _Requirements: 59.1, 59.6, 59.7, 59.8, 59.9, 59.10, 59.11, 59.14_
  - [ ] 71.2 Implement execution as ENGINE Jobs
    - Execution creates a Job (202); Operations run in order with per-Operation status, times, counts, warnings, errors, and log lines; stop on first failure with no later Operation started and no output completed; Notification on failure under R27; log lines hold only counts, column names, and Operation names; time and resource limit termination; duplicate delivery processed once; up to 3 retries with backoff on transient failure; Audit_Log on start, complete, fail
    - _Requirements: 60.1, 60.2, 60.3, 60.4, 60.5, 60.7, 60.8, 60.9, 60.10, 60.11_
  - [ ]* 71.3 Write property test for execution determinism and stop on failure
    - **Property 43: Execution determinism and stop on failure**
    - **Validates: Requirements 60.12, 60.13**
  - [ ]* 71.4 Write property test for execution log redaction
    - **Property 44: Execution log redaction**
    - **Validates: Requirements 60.14**
  - [ ]* 71.5 Write property test for idempotent job delivery
    - **Property 45: Idempotent job delivery**
    - **Validates: Requirements 60.15**
  - [ ]* 71.6 Write unit tests for Pipeline approval and execution
    - Execute without approval returns 409, approval cleared after edit, timeout termination, transient retry limit
    - _Requirements: 59.8, 59.9, 59.10, 60.8, 60.10_

- [ ] 72. Implement outputs and downloads
  - [ ] 72.1 Implement output records and download endpoints
    - `/api/v1/datasets/*`, `/api/v1/pipelines/*`, and `/api/v1/executions/{id}/outputs/{format}/download-url` for CSV, Parquet, JSON, and XLSX through R20 Presigned_URLs; another Organization gets 404 and no URL; only stored-record metrics for the completion dashboard data
    - _Requirements: 61.1, 61.3, 61.4, 61.7_
  - [ ]* 72.2 Write property test for dashboard metrics from records
    - **Property 47: Dashboard metrics from records**
    - **Validates: Requirements 61.11**
  - [ ]* 72.3 Write unit tests for download authorization
    - Cross-Organization download 404, unsupported format rejected, expired URL
    - _Requirements: 61.3, 61.4_

- [ ] 73. Implement ML preparation, retention, consent, and deletion
  - [ ] 73.1 Implement ML preparation endpoints and rules
    - Target column required before any ML Operation; seeded split before fitting; train-only fit; leakage confirmation; output described as prepared for modeling
    - _Requirements: 62.2, 62.3, 62.4, 62.6, 62.7, 62.8_
  - [ ] 73.2 Implement deletion, retention, and consent
    - Self-service Dataset deletion removes object, outputs, and Profile with Audit_Log and no Approval_Request (A-36); 404 afterwards and for other Organizations; retention period from configuration (A-08) with a retention Job; retention period shown per Dataset; training use of customer data only with recorded consent; no direct object exposure
    - _Requirements: 63.1, 63.2, 63.3, 63.4, 63.5, 63.6, 63.7_
  - [ ]* 73.3 Write property test for Dataset deletion and retention
    - **Property 49: Dataset deletion and retention**
    - **Validates: Requirements 63.8, 63.9**
  - [ ]* 73.4 Write unit tests for consent and self-delete
    - Self-delete needs no approval, cross-Organization delete removes nothing, no training use without consent
    - _Requirements: 63.3, 63.7_

- [ ] 74. Build the Playground web screens gated by the Lab registration
  - [ ] 74.1 Implement upload, dataset, and profile screens
    - `/labs/data-playground` with drag-and-drop and picker upload, client-side extension and size checks, progress with cancel, processing confirmation; `/dashboard/datasets` and `/dashboard/datasets/[datasetId]` with sortable column summaries, status announced to screen readers, retention period; routes owned by the Playground Lab registration and hidden when disabled
    - _Requirements: 56.1, 56.6, 56.7, 56.8, 57.6, 57.8, 63.5_
  - [ ] 74.2 Implement recommendation, pipeline, and report screens
    - Recommendation display with the AI label and first-use disclosure; `/dashboard/pipelines` and `/dashboard/pipelines/[pipelineId]` with graph, enable and disable, parameter editing, bounded preview, approval, destructive confirmation; live Execution status and logs; `/dashboard/reports/[reportId]` completion dashboard; ML preparation target and leakage controls; deletion confirmation
    - _Requirements: 58.3, 58.8, 59.2, 59.3, 59.4, 59.11, 60.6, 61.5, 61.6, 62.2, 62.6, 62.8, 63.6_
  - [ ]* 74.3 Write component and Playwright tests for Playground screens
    - Disabled Lab shows no navigation and routes return 404; upload cancel; destructive confirmation required; no ML-ready claim
    - _Requirements: 55.4, 56.7, 59.11, 62.8_

- [ ] 75. Implement the Phase 4 gate check
  - [ ] 75.1 Extend `phase_gate.py` with `--phase 4` and update affected docs
    - Confirms the Phase 4A delivery flows; when a go decision is recorded, confirms the Playground flow (upload, profile, recommend, approve, execute, download, delete); confirms no flow requires a Dataset and the Playground stays disabled in production without a recorded go decision; update `DATABASE.md`, `API.md`, `SECURITY.md`, `ENVIRONMENT.md`, `ARCHITECTURE.md`, `TESTING.md`, `IMPLEMENTATION_STATUS.md` in the same change set
    - _Requirements: 5.4, 5.5, 55.11, 78.1, 78.3, 78.9, 78.10_

- [ ] 76. Checkpoint: Phase 4 gate
  - The Phase 4 gate (R78.9, R78.10) passes, Phase 0 to Phase 3 features still work (R78.3), and the phase report is ready for Founder review before Phase 5 starts (R78.2).
  - Ensure all tests pass, ask the user if questions arise.

### Phase 5: ENGINE and OPS (R64 to R73)

- [ ] 77. Create the Phase 5 database migration
  - [ ] 77.1 Add the Alembic revision for Phase 5 tables
    - Tables per Appendix B.3 for Phase 5: `job_dead_letters`, `operational_need_records`, `agent_registrations`, `agent_tasks`, `system_configurations`; complete the `jobs` columns that Appendix B.3 assigns to Phase 5 (`requester_agent_id`, `parent_job_id`, `result`, cost and duration columns); read the exact columns, keys, indexes, and retention from `requirements.md` Appendix B.3 and B.5
    - Optional tables created only in the same revision when their agents are in scope: `content_items` (R71) and `approved_sources` (R70); unique `(job_id)` on `job_dead_letters`, unique `agent_key`, unique `config_key`, partial unique `source_pattern` where `revoked_at` is null; status check constraints from Appendix A.2 (A.2.23, A.2.24, A.2.25); working downgrade; upgrade, downgrade, upgrade round trip on an empty database
    - _Requirements: 6.3, 6.7, 64.11, 65.1, 66.2, 73.5_
  - [ ]* 77.2 Write migration tests
    - Round trip on an empty database; tenant-owned tables reject queries without an `OrgScope`; Phase 5 status constraints reject undefined statuses
    - _Requirements: 6.7, 77.5_

- [ ] 78. Complete the ENGINE job framework
  - [ ] 78.1 Implement the job type registry
    - Code registry with job type id, Pydantic parameter schema, handler module, permission set, and CPU, memory, and time limits; unknown job type rejected with a structured error and Audit_Log entry; invalid parameters rejected with field-level errors and no Job record; parameters containing code, scripts, or expressions rejected; executed handler always resolved from the registry
    - _Requirements: 64.1, 64.2, 64.3, 64.4_
  - [ ] 78.2 Complete Job lifecycle, idempotency, retries, and limits
    - Statuses Queued, Running, Succeeded, Failed, Cancelled with only Appendix A.2 transitions; dedupe key required and a matching delivery returns the existing Job id with no further effect; up to 3 retries with backoff on transient failure; termination on CPU, memory, or time limit with a reason naming the limit; record duration and estimated cost in `usage_records` on completion
    - _Requirements: 64.5, 64.6, 64.7, 64.8, 64.15_
  - [ ] 78.3 Enforce per-job Organization scope and permission sets
    - Handler receives an `OrgScope` for the Job's Organization and only the operations in the job type permission set; a request for another Organization's record or an operation outside the set is denied, sets the Job to Failed, and writes an Audit_Log entry
    - _Requirements: 64.9, 64.10_
  - [ ] 78.4 Implement dead letters, failure notification, and scheduled job types
    - Store a `job_dead_letters` row (job id, type, redacted parameters, error, attempt count) when retries are exhausted; Notification to the Job owner through R27 on Failed; `GET` dead-letter endpoints for Founder and Administrators; register retention enforcement, Approval_Request expiry, and Commercial_Record overdue computation as scheduled job types
    - _Requirements: 64.11, 64.12, 64.14_
  - [ ] 78.5 Confirm the queue interface stays replaceable
    - Keep submit, status, and cancel behind the `JobQueue` interface with the in-process worker as the local implementation; add a contract test suite that any other implementation must pass
    - _Requirements: 64.13_
  - [ ]* 78.6 Write property test for exactly-once job effect and registry-only execution
    - **Property 50: Exactly-once job effect and registry-only execution**
    - Generate sequences of 1 to 6 deliveries sharing a dedupe key, with transient failures and redeliveries; assert stored effects equal one successful execution and the executed handler is the registered one
    - **Validates: Requirements 64.16, 64.17**
  - [ ]* 78.7 Write unit tests for the job framework
    - Unknown type, invalid parameters, code in parameters, retry limit of 3, limit termination reasons, cross-Organization denial, dead-letter content redaction
    - _Requirements: 64.2, 64.3, 64.4, 64.7, 64.8, 64.10, 64.11_

- [ ] 79. Implement the Agent_Runtime and agent registry
  - [ ] 79.1 Implement the agent registry and the operational need records
    - `agent_registrations` with agent id, purpose, instructions reference and hash, tool list, output schema, enabled flag, model configuration, Dataset access flag, and operational need reference; entries for Orchestrator, Business Intelligence, Lead Research, Marketing, Content, Outreach, Engineering Assistant, Data Assistant, and Quality & Security, all disabled by default; `operational_need_records` with proposed, approved, withdrawn; enabling only by the Founder against an approved need, otherwise rejected with a structured error and Audit_Log entry; Audit_Log with previous and new values on every registry change
    - _Requirements: 65.1, 65.2, 65.3, 65.4, 65.13_
  - [ ] 79.2 Implement scoped prompts, tool enforcement, and output validation
    - Separate scoped prompt per agent built from that agent's instructions only; tool call outside the registry tool list denied with an Audit_Log entry (agent id, tool name, Agent_Task id); output validated against the agent output schema before storage or hand-off, with no stored output and status Failed on failure; inputs limited to fields in the Agent_Task input definition and raw Dataset contents excluded unless the Founder enables Dataset access; inbound content treated as untrusted data and never changing instructions or the tool list
    - _Requirements: 65.5, 65.6, 65.7, 65.8, 65.9, 65.10_
  - [ ] 79.3 Implement the Orchestrator and Internal_Agent principals
    - Orchestrator routes only by creating Agent_Tasks, with a tool list of task creation and task status only; each agent runs as an Internal_Agent principal under R17 with its own permission set from `agent_registrations`; a role assignment giving an agent the Administrator or Founder role is rejected
    - _Requirements: 65.11, 65.12_
  - [ ]* 79.4 Write property test for agent tool set and validated output
    - **Property 51: Agent tool set and validated output**
    - Generate registry entries, mid-execution registry edits, tool requests, and stub outputs that pass and fail the schema; assert the available tools equal the entry's tool list at execution start and every stored output validates
    - **Validates: Requirements 65.14, 65.15**
  - [ ]* 79.5 Write unit tests for the agent runtime
    - Enable without need or by non-Founder rejected, tool denial audited, injected instructions in inquiry text leave tools unchanged, Administrator role assignment rejected, Dataset contents excluded by default
    - _Requirements: 65.4, 65.6, 65.9, 65.10, 65.12_

- [ ] 80. Implement Agent_Task recording, limits, and cost monitoring
  - [ ] 80.1 Implement Agent_Task creation and recording
    - Create each Agent_Task as a Job through R64 with status Queued; record task id, agent id, input, output, status, duration, model id, token counts, estimated cost, error, and trace; statuses Queued, Running, Succeeded, Failed, Awaiting Approval, Cancelled per Appendix A.2.24; redact secrets and personal data per the documented redaction policy before writing; unknown cost recorded as unknown and counted in a missing cost count
    - _Requirements: 66.1, 66.2, 66.3, 66.4, 66.10_
  - [ ] 80.2 Implement limits, retries, and daily cost bound
    - Up to 3 retries with backoff on transient failure; stop on the per-task token limit with a reason naming it; at most one Agent_Task Running at a time; per-day cost limit checked before each task starts, no new task for the rest of the day when reached, Notification to the Founder, and rejection of submissions with a structured error naming the limit; limits read from `system_configurations`; write token counts, model id, and estimated cost to `usage_records` under R42
    - _Requirements: 66.5, 66.6, 66.7, 66.8, 66.9, 66.12_
  - [ ] 80.3 Implement the admin endpoints
    - `/api/v1/admin` endpoints for agents, agent tasks, approvals, and dead letters restricted to the roles Appendix A.3 permits (Founder writes, Administrator reads; Agent_Task cancel Founder only)
    - _Requirements: 66.11, 64.11_
  - [ ]* 80.4 Write property test for daily cost bound
    - **Property 52: Daily cost bound**
    - Generate sequences of Agent_Tasks with random costs and a daily limit; assert the day's total never exceeds the limit plus the cost of at most one task that was running when the limit was reached
    - **Validates: Requirements 66.13**
  - [ ]* 80.5 Write unit tests for task recording and limits
    - Redaction of seeded secrets and emails, token limit stop, retry limit, unknown cost counted, submission rejected at the limit, one running task at a time
    - _Requirements: 66.4, 66.5, 66.6, 66.8, 66.10, 66.12_

- [ ] 81. Implement the inquiry processing workflow
  - [ ] 81.1 Implement the workflow run through the ENGINE
    - On a stored Project_Inquiry with the AI processing consent flag, create one workflow run as a parent Job with the Project_Inquiry id as dedupe key; without consent create no run and record the reason on the Project as Internal_Only; steps in order requirement summary, draft clarification questions, discipline suggestion, quality review, each as an Agent_Task; store status, start, end, and duration per step
    - _Requirements: 67.1, 67.2, 67.3, 67.6, 67.12_
  - [ ] 81.2 Implement step outputs and failure handling
    - Summary through the R32 analysis capability; questions as Inquiry_Question drafts under R33 requiring human approval; discipline suggestion with only R32 labels, each with a justification; every output Internal_Only and labelled advisory and AI-generated; a failed step halts the workflow, records the step and error, runs no later step, and notifies the Founder; Notification to the Founder and assigned Authorized_Reviewer when the quality review completes
    - _Requirements: 67.4, 67.5, 67.7, 67.8, 67.9_
  - [ ] 81.3 Enforce workflow permission limits
    - Workflow agents hold no permission to change Project status, qualify or reject, create a price or Commercial_Record, or send a Communication; any such request returns HTTP 403 with an Audit_Log entry
    - _Requirements: 67.10, 67.11_
  - [ ]* 81.4 Extend the status preservation property test to workflow runs
    - **Property 13: Status preservation by AI and agent work**
    - Generate Projects in every early status and workflow runs with failing steps and denied status-change attempts; assert the Project status before and after each run is equal apart from human changes
    - **Validates: Requirements 67.13**
  - [ ]* 81.5 Write unit tests for the workflow
    - No consent no run, duplicate trigger runs once, step failure halts and notifies, unlabelled discipline rejected, 403 on status change request
    - _Requirements: 67.2, 67.7, 67.5, 67.11, 67.12_

- [ ] 82. Implement OPS approvals for Sensitive_Actions
  - [ ] 82.1 Wire agent proposals to Approval_Requests
    - A proposed Sensitive_Action creates an R43 Approval_Request (action type, target, exact content, hash, requesting agent, rationale) and sets the Agent_Task to Awaiting Approval; hold the action while Pending; Notification to the Founder; decisions only from the Founder or an Authorized_Approver, never an Internal_Agent
    - _Requirements: 68.1, 68.2, 68.3, 68.11_
  - [ ] 82.2 Implement guarded execution
    - Execute only with content whose hash equals the approved hash; a content change after approval sets Invalidated and executes nothing; Rejected, Expired, or Invalidated sets the Agent_Task to Cancelled; an action attempted without a matching Approved request is blocked with an Audit_Log entry; approved external communications logged with the Approval_Request reference
    - _Requirements: 68.4, 68.5, 68.6, 68.9, 68.10_
  - [ ] 82.3 Deny agent commercial commitments
    - No agent permission to accept, sign, or confirm a commitment or to create or change a quotation, price, or Commercial_Record amount; such requests return HTTP 403, change no record, and write an Audit_Log entry
    - _Requirements: 68.7, 68.8_
  - [ ]* 82.4 Extend the approved execution property test to agent-originated actions
    - **Property 30: Approved execution**
    - Generate agent proposals, decisions, content edits after approval, and execution attempts; assert every executed agent action has an Approved request with a hash equal to the executed content hash
    - **Validates: Requirements 68.12**
  - [ ]* 82.5 Write unit tests for agent approvals
    - Hold while Pending, hash mismatch blocks, edit after approval invalidates, Internal_Agent decision rejected, 403 for price creation
    - _Requirements: 68.2, 68.3, 68.5, 68.8, 68.10_

- [ ] 83. Build the ops dashboard
  - [ ] 83.1 Implement the ops dashboard endpoints
    - Endpoints serving `/admin/ops` data only to the Founder and Administrators (403 for other authenticated principals, 401 for Guests); agent directory; task queue, running tasks, and history with filters by agent, status, and date range; token counts, model usage, estimated cost, and error counts computed from stored Agent_Task records; reject decisions require a non-empty reason (field-level error); agent configuration changes only by the Founder with an Audit_Log entry holding previous and new values
    - _Requirements: 69.1, 69.2, 69.3, 69.4, 69.5, 69.7, 69.8_
  - [ ] 83.2 Build the `/admin/ops` screen
    - Agent directory, queue, history with filters, metrics, pending agent-originated Approval_Requests with approve and reject controls shown only to the Founder and Authorized_Approvers, configuration editing for the Founder only, failed Agent_Task view showing the error, redacted input and output, and step timeline; loading, empty, and error-with-retry states; keyboard operable and announced status changes
    - _Requirements: 69.3, 69.4, 69.6, 69.8, 69.9_
  - [ ]* 83.3 Write property test for ops dashboard metric integrity
    - **Property 12: Count integrity**
    - Generate Agent_Task data sets, filters, and date ranges; assert every displayed metric equals the value computed from the matching stored records
    - **Validates: Requirements 69.10**
  - [ ]* 83.4 Write unit and component tests for the ops dashboard
    - 401 and 403 access, reject without reason, configuration change by non-Founder rejected, failed-task view content
    - _Requirements: 69.2, 69.7, 69.8, 69.9_

- [ ]* 84. Optional: Lead research and outreach assistance (R70)
  - [ ] 84.1 Implement approved sources and Lead Research limits
    - `approved_sources` list managed by the Founder; a source request outside the list denied with an Audit_Log entry; every Lead data item created by the agent stores a source reference and one without it is rejected with a field-level error; enabled only through an approved operational need under R65
    - _Requirements: 70.1, 70.2, 70.3, 70.4_
  - [ ] 84.2 Implement Outreach drafts and approved sends
    - Outreach messages stored as drafts only; sending only through an Approved R68 Approval_Request; a draft targeting a normalized email on the opt-out list is rejected for sending with a structured error and no Approval_Request
    - _Requirements: 70.5, 70.6, 70.7_
  - [ ]* 84.3 Extend the opt-out property test to outreach
    - **Property 17: Opt-out**
    - Generate outreach targets, opt-outs, drafts, and send attempts; assert no outgoing outreach message is recorded for an opted-out normalized email
    - **Validates: Requirements 70.8**
  - [ ]* 84.4 Write unit tests for lead research and outreach
    - Unlisted source denied, missing source reference rejected, send without approval blocked, opt-out draft rejected
    - _Requirements: 70.2, 70.4, 70.6, 70.7_

- [ ]* 85. Optional: Content and marketing assistance (R71)
  - [ ] 85.1 Implement `content_items` and the claim check
    - Content and Marketing agents create Drafts only (article, LinkedIn post, case-study draft, campaign plan); each factual claim references a verified project record under R11 or is flagged unsupported; transition to Approved rejected with a structured error listing unsupported claims; statuses and transitions from Appendix A.2.25 encoded as data; Audit_Log on every status change
    - _Requirements: 71.1, 71.2, 71.3, 71.4, 71.5, 71.7_
  - [ ] 85.2 Implement publishing through approvals
    - Publish only through an Approved R68 Approval_Request whose content hash equals the `content_hash` of the item
    - _Requirements: 71.6_
  - [ ]* 85.3 Write unit tests for content items
    - Unsupported claim blocks approval, publish without approval blocked, hash mismatch blocked, undefined transition rejected, every Published item's claims reference verified records
    - _Requirements: 71.4, 71.5, 71.6, 71.8_

- [ ]* 86. Optional: Engineering and project assistance (R72)
  - [ ] 86.1 Implement the Engineering Assistant
    - Drafts of implementation plans, documentation reviews, and progress summaries with references to the stored records used; reads only records of the Project named in the Agent_Task; every draft Internal_Only; no tool or permission for production credentials, secret values, or infrastructure control, with denial and Audit_Log on request; production infrastructure change proposals handled as Sensitive_Actions under R68
    - _Requirements: 72.1, 72.2, 72.3, 72.5, 72.6, 72.7_
  - [ ] 86.2 Gate client-visible summaries behind human approval
    - A progress summary proposed as a client update becomes Client_Visible only after human approval under R47
    - _Requirements: 72.4_
  - [ ]* 86.3 Write unit tests for the Engineering Assistant
    - Other-Project records not readable, credential request denied and audited, client summary hidden until approved, infrastructure proposal creates an Approval_Request
    - _Requirements: 72.2, 72.4, 72.6, 72.7, 72.8_

- [ ] 87. Implement platform configuration and Organization suspension
  - [ ] 87.1 Implement `system_configurations` and Feature_Flags management
    - Typed configuration values with validated type and range for usage limits, upload limits, AI model configuration, API configuration, per-day agent cost limit, and per-task token limit; Feature_Flag management including `feature_flag_organizations`; changes only by the Founder and Administrators Appendix A.3 permits; one Audit_Log entry per change with previous value, new value, actor, and time
    - _Requirements: 73.5, 73.6_
  - [ ] 87.2 Implement Organization suspension and reinstatement
    - Suspend requires a reason, sets status suspended, and writes an Audit_Log entry; while suspended every request from that Organization's users returns HTTP 403 with a structured error stating the Organization is suspended; reinstatement restores access and writes an Audit_Log entry; permitted roles only per Appendix A.3
    - _Requirements: 73.7, 73.8, 73.9_
  - [ ] 87.3 Implement deletion requests behind approvals
    - Staff deletion of customer data executes only with an Approved R43 Approval_Request whose content hash equals the hash of the deletion parameters; Client self-service Dataset deletion under R63.1 stays exempt (A-36); Audit_Log entry on execution
    - _Requirements: 73.10_
  - [ ]* 87.4 Write property test for configuration audit
    - **Property 9: Audit completeness**
    - Generate configuration changes, including rejected ones; assert each committed change has exactly one Audit_Log entry holding its previous and new values and rejected changes have none
    - **Validates: Requirements 73.14**
  - [ ]* 87.5 Write unit tests for configuration, suspension, and deletion
    - Out-of-range value rejected, non-permitted role denied, suspended user gets 403, reinstated user regains access, deletion without matching hash blocked, self-service Dataset delete exempt
    - _Requirements: 73.5, 73.7, 73.8, 73.9, 73.10_

- [ ] 88. Build the full Founder_Control_Center
  - [ ] 88.1 Implement the analytics and dashboard endpoints
    - `/api/v1/admin/analytics` overview, usage, and agents restricted per Appendix A.3; counts of customers, inquiries, Active_Engagements, processing Jobs, agent activity, pending approvals, and recorded operational expenses computed from stored records; pipeline success rate from Execution records only where the Playground is enabled; system health from monitoring data with an unavailable state and no health value when monitoring cannot be retrieved; Audit_Log search by actor, action, resource, and time range
    - _Requirements: 73.3, 73.4, 73.11, 73.12, 73.13_
  - [ ] 88.2 Build the complete section navigation
    - Sections for inquiries, Prospective_Clients, Clients and Organizations, Project_Opportunities, Technical_Assessments, Proposals, Active_Engagements, Project_Milestones, team assignments, Deliverables, Support_Requests, Maintenance_Engagements, Commercial_Records, Labs, internal workflows, OPS agents, pending approvals, usage and infrastructure cost, Audit_Log, and system configuration; each served only to the roles Appendix A.3 grants, with Founder, Administrator, Engineer, and Project_Manager kept separate
    - _Requirements: 73.1, 73.2_
  - [ ] 88.3 Build the dashboard, configuration, and Feature_Flags screens
    - Dashboard metrics and system health with the unavailable state; Organization screen with suspend (reason required) and reinstate; configuration and Feature_Flags screen with typed inputs, validation messages, and previous and new value history; deletion request screen showing the Approval_Request state; Audit_Log search form; loading, empty, and error-with-retry states
    - _Requirements: 73.3, 73.5, 73.7, 73.9, 73.10, 73.11, 73.12_
  - [ ]* 88.4 Write component and Playwright tests for the Founder_Control_Center
    - Section visibility per role, suspension requires a reason, configuration validation errors shown, health unavailable state, Audit_Log filters
    - _Requirements: 73.2, 73.7, 73.11, 73.12_

- [ ] 89. Implement the Phase 5 gate check
  - [ ] 89.1 Extend `phase_gate.py` with `--phase 5` and update affected docs
    - Confirms the ENGINE job type registry and idempotency, the R67 workflow completing without any Project status change, Approval_Requests blocking unapproved Sensitive_Actions, enforced cost limits, and the OPS dashboard; confirms Phase 0 to Phase 4 gates still pass and that Optional agents (R70 to R72) stay disabled unless an approved operational need is recorded; update `DATABASE.md`, `API.md`, `SECURITY.md`, `ENVIRONMENT.md`, `ARCHITECTURE.md`, `TESTING.md`, `IMPLEMENTATION_STATUS.md` in the same change set
    - _Requirements: 5.4, 5.5, 78.1, 78.3, 78.11_

- [ ] 90. Checkpoint: Phase 5 gate
  - Ensure all tests pass, ask the user if questions arise.
  - The Phase 5 gate (R78.11) passes, Phase 0 to Phase 4 features still work (R78.3), and the phase report is ready for Founder review before Phase 6 starts (R78.2).

### Phase 6: Hardening and Release Readiness (R74 to R78)

- [ ] 91. Implement security hardening (R74)
  - [ ] 91.1 Add security headers and the CORS origin list to the API
    - Middleware sets Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options, and frame protection on every response, error responses included; a cross-origin request from an origin outside the configured list is rejected with no CORS allow headers; the origin list comes from configuration
    - _Requirements: 74.7, 74.8_
  - [ ] 91.2 Encrypt the sensitive customer fields listed in `docs/SECURITY.md`
    - Field-level encryption for the listed fields through a key-provider interface with a local adapter (no AWS call); data migration that encrypts existing rows; ciphertext only in storage, plaintext only in service-layer reads
    - _Requirements: 74.6_
  - [ ] 91.3 Write infrastructure policy checks as code
    - Static checks over the IaC definitions, run locally and in CI without deploying: TLS enforced, encryption at rest for S3, RDS, and every queue in use, S3 buckets private with public access blocked, RDS in private subnets with no public endpoint, every data-access IAM permission scoped to named resources with no wildcard resource; a violation fails the check with the resource name
    - Writing these checks does not deploy anything. No AWS deployment without the Founder's written authorization (R3.6)
    - _Requirements: 74.1, 74.2, 74.3, 74.4, 74.5_
  - [ ] 91.4 Add the seeded-secret log scan to the test run
    - Test fixtures seed known sensitive values; a post-run scanner searches every log the suite produced; on a hit the run fails and reports the log location of the value; the scanner is wired into the default CI job
    - _Requirements: 74.9, 74.10_
  - [ ] 91.5 Add the dependency scan gate and the security review record
    - Script runs dependency vulnerability scanning for the Python and Node dependencies and fails on any unresolved critical finding; script writes the security review into `docs/SECURITY.md` from recorded test results for tenant isolation, Internal_Only separation, prompt-injection, tool-permission, and approval-enforcement tests, and never records a result that was not produced by a run
    - _Requirements: 74.11, 74.12_
  - [ ]* 91.6 Write property test for log redaction
    - **Property 53: Log redaction**
    - Generate requests, jobs, and agent runs that carry seeded sensitive values in inputs and errors; assert no captured log line contains a seeded value
    - **Validates: Requirements 74.13**
  - [ ]* 91.7 Write unit tests for hardening
    - Headers present on success and error responses, disallowed origin gets no CORS headers, wildcard-resource IAM policy fails the check, public bucket definition fails the check, a planted seeded value in a log fails the run with its location, ciphertext stored for each listed field
    - _Requirements: 74.1, 74.3, 74.5, 74.6, 74.7, 74.8, 74.10_

- [ ] 92. Implement monitoring, health, and recovery (R75)
  - [ ] 92.1 Implement the truthful health endpoint
    - `GET /health` runs a live check of each dependency (database, storage, queue if in use, scanner, model client) inside the request with a per-check timeout; a failed or timed-out check reports that dependency as unavailable; the body names dependencies only, never an address or secret value
    - _Requirements: 75.8, 75.9_
  - [ ] 92.2 Emit structured logs, metrics, and alarm definitions
    - Structured JSON logs and metrics for API errors, Job failures, agent failures, and cost thresholds through the existing metrics interface with a local adapter; alarm definitions in IaC for those metrics plus queue depth where a managed queue is in use; no deployment
    - _Requirements: 75.6, 75.7_
  - [ ] 92.3 Raise an alarm and a Founder-visible record on dead-letter creation
    - When a dead-letter record is created, emit the alarm metric and expose the record in the Founder_Control_Center list; the alarm and the record come from the same transaction event
    - _Requirements: 75.12_
  - [ ] 92.4 Implement backup, retention, and deletion-window controls
    - IaC settings for automated RDS backups with the retention period read from `docs/DEPLOYMENT.md`; S3 versioning only on buckets recorded in `docs/DEPLOYMENT.md`; purge job that removes a deleted customer object and every version within the documented deletion window; local-adapter tests only
    - _Requirements: 75.1, 75.2, 75.3_
  - [ ] 92.5 Write the restore test script and the deployment runbooks
    - Script restores a backup to a separate environment and verifies the restored data against recorded checksums or record counts, then records the result; add to `docs/DEPLOYMENT.md` the restore procedure, deployment process with rollback steps, retention period, deletion window, and a field for the RTO and RPO set by the Founder (A-31) that stays marked "pending Founder value" until set; the script runs against a local database by default and runs against AWS only with the Founder's written authorization (R3.6)
    - _Requirements: 75.4, 75.5, 75.10, 75.11_
  - [ ]* 92.6 Write property test for truthful health
    - **Property 54: Truthful health**
    - Generate dependency states (ok, failing, timing out) in every combination; assert a dependency is reported healthy only when its check succeeded in the same request
    - **Validates: Requirements 75.13**
  - [ ]* 92.7 Write unit and infrastructure tests for monitoring and recovery
    - Failing dependency reported unavailable, timeout reported unavailable, no secret or address in the body, dead-letter creation emits alarm and record, alarm definitions exist for each required metric, purge removes all versions, restore script flags a checksum mismatch
    - _Requirements: 75.3, 75.5, 75.6, 75.8, 75.9, 75.12_

- [ ] 93. Implement performance and cost review tooling (R76)
  - [ ] 93.1 Implement the load test harness
    - Script reads the Founder-set target values and the main endpoint list from `docs/DEPLOYMENT.md` and refuses to run when targets are missing; applies the documented load, measures p95 latency per listed endpoint, and writes the result to `docs/IMPLEMENTATION_STATUS.md`; default target is a local or non-production environment, and a production target requires the Founder's written authorization
    - _Requirements: 76.1, 76.2, 76.3_
  - [ ] 93.2 Implement the cost review and Appendix C check
    - Script compares recorded `usage_records` with AWS billing data for the same period per environment and writes the review; a check lists each AWS service present in the IaC and fails when it has no Appendix C justification, so the service is removed before Phase 6 acceptance; billing data comes from an exported file or a read-only adapter, with no AWS call unless the Founder authorizes it
    - _Requirements: 76.4, 76.5, 76.6_
  - [ ] 93.3 Implement the billable deployment authorization record and budget alarm verification
    - Record each Founder written authorization for a billable deployment (R3.6) and fail the release check when a billable deployment has none; verification script simulates spend at each R7.4 budget alarm threshold and records whether the alarm fires, with a local simulator by default
    - _Requirements: 76.7, 76.8_
  - [ ]* 93.4 Write unit tests for the performance and cost tooling
    - Load test refuses to run without targets, p95 recorded for each listed endpoint, unjustified service fails the Appendix C check, deployment without authorization fails the release check, a budget alarm that does not fire is recorded as failed
    - _Requirements: 76.1, 76.3, 76.6, 76.7, 76.8_

- [ ] 94. Close test coverage gaps (R77)
  - [ ] 94.1 Add the property coverage check to CI
    - Script lists every FOR ALL criterion in `requirements.md` and fails when no property-based test references its requirement ID and criterion number; confirm each property test carries the `Feature: neuropath-platform, Property N` tag and runs at least 100 iterations
    - _Requirements: 77.9, 77.13_
  - [ ] 94.2 Add the missing test categories and the CI suite structure
    - Verify and add where missing: Web_App component, form validation, navigation, responsive (360, 768, 1280 px), accessibility, and Playwright MVP flow tests; API unit, integration, authentication, authorization (Appendix A.3), tenant isolation, Internal_Only visibility, transition conformance (A.1, A.2), and migration up and down tests; Agent_Runtime tests for structured output, hallucination checks, prompt-injection, tool-permission, and approval enforcement; infrastructure tests for deployment validation, IAM, storage access, backup, and monitoring; Data_Engine tests for R56 to R63 only where the Playground is enabled
    - _Requirements: 77.1, 77.2, 77.3, 77.4, 77.5, 77.6, 77.7, 77.8_
  - [ ] 94.3 Enforce stubbed model calls and the Labs-disabled flow in CI
    - Default CI uses the stubbed `ModelClient` with recorded responses and fails when any Bedrock call is attempted; MVP project flow tests run with all Labs disabled
    - _Requirements: 77.10, 77.11_
  - [ ] 94.4 Record phase test results in `docs/IMPLEMENTATION_STATUS.md`
    - Script writes the results of the tests relevant to each phase from the recorded test run, and refuses to mark a phase complete without recorded results
    - _Requirements: 77.12_
  - [ ]* 94.5 Write unit tests for the coverage checks
    - Coverage check fails on an uncovered FOR ALL criterion, CI fails on a Bedrock call attempt, status script refuses a phase with no results
    - _Requirements: 77.9, 77.10, 77.12, 77.13_

- [ ] 95. Implement the MVP acceptance journey (R78)
  - [ ] 95.1 Implement the MVP acceptance check
    - Automated end-to-end check on one Project through the API with local adapters: visitor inquiry; Founder review and information request; client answer on the same inquiry; qualification; Technical_Assessment confirmed; architecture confirmed; Proposal drafted, priced by an Authorized_Approver, approved, and sent; client accepts; Agreement In Effect; Project activated; Project_Milestones, Tasks, and updates recorded; Deliverables shared; quality gate passed; deployment recorded and handover complete; client final acceptance; Project Completed; client raises a Support_Request; each step asserts stored records and writes an acceptance journey record, with no fabricated success state
    - _Requirements: 78.13, 78.4_
  - [ ] 95.2 Add the Playground and OPS acceptance checks
    - Include the R56 to R63 Playground acceptance tests only where the Founder recorded a go decision; always include the OPS acceptance checks of R67 and R68
    - _Requirements: 78.14, 78.15_
  - [ ]* 95.3 Write property test for phase order
    - **Property 55: Phase order**
    - Generate phase approval and start records in arbitrary order; assert a phase start is accepted only when its time is later than the recorded Founder approval of the previous phase report, for every phase n greater than 0
    - **Validates: Requirements 78.16**
  - [ ]* 95.4 Write unit tests for the acceptance journey
    - A missing step stops the journey with the failing step named, a skipped approval is not accepted, the Playground checks are skipped without a go decision, and the journey record lists each step with its stored record id
    - _Requirements: 78.13, 78.14, 78.15_

- [ ] 96. Implement the Phase 6 gate check
  - [ ] 96.1 Extend `phase_gate.py` with `--phase 6` and update affected docs
    - Confirms R74, R75, R76, and R77 are met from recorded results, that the restore test passed, that the security review is recorded in `docs/SECURITY.md`, that the MVP acceptance check passed, and that Phase 0 to Phase 5 gates still pass; the check requires the Founder-set load targets and RTO and RPO values and fails when they are missing; no AWS deployment happens without the Founder's written authorization (R3.6); update `DEPLOYMENT.md`, `SECURITY.md`, `TESTING.md`, `IMPLEMENTATION_STATUS.md`, `ARCHITECTURE.md`, `ENVIRONMENT.md`, `API.md`, `DATABASE.md` in the same change set, and generate the Phase 6 report listing requirement IDs, test results, known issues, open assumptions, and next steps
    - _Requirements: 78.1, 78.3, 78.12_

- [ ] 97. Checkpoint: Phase 6 gate
  - Ensure all tests pass, ask the user if questions arise.
  - The Phase 6 gate (R78.12) passes, the MVP acceptance check passes (R78.13), Phase 0 to Phase 5 features still work (R78.3), and the phase report is ready for Founder review (R78.2). Any AWS deployment still needs the Founder's written authorization (R3.6).

## Notes

- Tasks marked with `*` are optional tests and can be skipped for a faster MVP. Core implementation tasks are never optional.
- Property test tag convention: each property test sub-task names its design property as `Property N: <title>` and lists `Validates: Requirements x.y`.
- Each phase ends with a gate. The next phase starts only after the Founder's approval of the phase report is recorded.
- No AWS deployment and no billable resources are created without the Founder's written authorization (R3.6). IaC is authored and validated only.
- Phase 4B (Data Engineering Playground) starts only after a recorded go decision (A-04).
- R70 to R72 are Optional.
- Each task references specific requirements for traceability. Unit tests cover examples and edge cases; property tests cover universal properties.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "2.1", "3.1"] },
    { "id": 2, "tasks": ["1.3", "2.2", "3.2", "4.1", "6.1"] },
    { "id": 3, "tasks": ["1.4", "2.3", "3.3", "4.2", "5.1", "6.2"] },
    { "id": 4, "tasks": ["4.3", "4.4", "5.2", "6.3", "7.1"] },
    { "id": 5, "tasks": ["5.3", "5.4", "7.2"] },
    { "id": 6, "tasks": ["7.3", "8.1"] },
    { "id": 7, "tasks": ["10.1", "12.1"] },
    { "id": 8, "tasks": ["10.2", "10.3", "12.2"] },
    { "id": 9, "tasks": ["10.4", "11.1", "11.2", "12.3", "12.4"] },
    { "id": 10, "tasks": ["11.3", "12.5", "12.6"] },
    { "id": 11, "tasks": ["11.4", "12.7", "12.8", "12.9", "13.1"] },
    { "id": 12, "tasks": ["13.2", "14.1", "14.2"] },
    { "id": 13, "tasks": ["14.3", "14.4", "15.1"] },
    { "id": 14, "tasks": ["17.1", "18.1", "21.1"] },
    { "id": 15, "tasks": ["17.2", "17.3", "18.2", "21.2"] },
    { "id": 16, "tasks": ["18.3", "18.5"] },
    { "id": 17, "tasks": ["18.4", "18.6", "18.7", "19.1"] },
    { "id": 18, "tasks": ["19.2", "19.3", "19.4", "20.1", "22.1", "24.1", "26.1", "27.1"] },
    { "id": 19, "tasks": ["20.2", "22.2", "22.3", "23.1", "24.2", "25.1", "26.2", "27.2", "27.3"] },
    { "id": 20, "tasks": ["23.2", "25.2", "25.3", "28.1", "28.2"] },
    { "id": 21, "tasks": ["23.3", "23.4", "28.3", "29.1"] },
    { "id": 22, "tasks": ["23.5", "29.2", "29.4", "30.1", "30.2"] },
    { "id": 23, "tasks": ["29.3", "30.3", "30.4"] },
    { "id": 24, "tasks": ["30.5", "31.1"] },
    { "id": 25, "tasks": ["31.2"] },
    { "id": 26, "tasks": ["33.1", "33.2"] },
    { "id": 27, "tasks": ["33.3", "33.4", "33.5", "33.7"] },
    { "id": 28, "tasks": ["33.6", "33.8", "34.1", "35.1"] },
    { "id": 29, "tasks": ["34.2", "34.3", "35.2", "36.1"] },
    { "id": 30, "tasks": ["34.4", "34.5", "35.3", "36.2"] },
    { "id": 31, "tasks": ["35.4", "35.5", "36.3", "37.1"] },
    { "id": 32, "tasks": ["37.2"] },
    { "id": 33, "tasks": ["37.3", "38.1", "39.1"] },
    { "id": 34, "tasks": ["37.4", "37.5", "37.6", "38.2", "38.3", "39.2"] },
    { "id": 35, "tasks": ["38.4", "39.3", "39.5", "39.6"] },
    { "id": 36, "tasks": ["39.4", "39.8", "41.1", "41.2"] },
    { "id": 37, "tasks": ["39.7", "41.3", "41.4", "42.1"] },
    { "id": 38, "tasks": ["41.5", "42.2", "42.3", "42.4", "43.1"] },
    { "id": 39, "tasks": ["42.5", "43.2", "44.1"] },
    { "id": 40, "tasks": ["43.3", "43.4", "44.2", "45.1"] },
    { "id": 41, "tasks": ["44.3", "44.4", "45.2", "46.1"] },
    { "id": 42, "tasks": ["46.2", "47.1"] },
    { "id": 43, "tasks": ["46.3", "47.2", "48.1"] },
    { "id": 44, "tasks": ["47.3", "48.2"] },
    { "id": 45, "tasks": ["48.3"] },
    { "id": 46, "tasks": ["50.1"] },
    { "id": 47, "tasks": ["50.2", "51.1"] },
    { "id": 48, "tasks": ["51.2", "52.1", "53.1", "54.1", "58.1", "61.1"] },
    { "id": 49, "tasks": ["51.3", "52.2", "53.2", "54.2", "55.1", "58.2", "59.1", "60.1", "61.2"] },
    { "id": 50, "tasks": ["52.3", "55.2", "56.1", "59.2", "60.2", "61.3", "62.1"] },
    { "id": 51, "tasks": ["52.4", "56.2", "56.4", "62.2", "62.3", "63.1"] },
    { "id": 52, "tasks": ["56.3", "57.1", "63.2", "64.1"] },
    { "id": 53, "tasks": ["57.2", "63.3", "64.2"] },
    { "id": 54, "tasks": ["67.1"] },
    { "id": 55, "tasks": ["67.2", "68.1"] },
    { "id": 56, "tasks": ["68.2", "69.1"] },
    { "id": 57, "tasks": ["68.3", "69.2", "69.3", "69.4", "70.1"] },
    { "id": 58, "tasks": ["68.4", "68.5", "68.6", "68.7", "70.2", "70.3", "71.1"] },
    { "id": 59, "tasks": ["71.2", "73.1", "73.2"] },
    { "id": 60, "tasks": ["71.3", "71.4", "71.5", "71.6", "72.1", "73.3", "73.4"] },
    { "id": 61, "tasks": ["72.2", "72.3", "74.1", "74.2"] },
    { "id": 62, "tasks": ["74.3", "75.1"] },
    { "id": 63, "tasks": ["77.1"] },
    { "id": 64, "tasks": ["77.2", "78.1"] },
    { "id": 65, "tasks": ["78.2", "79.1"] },
    { "id": 66, "tasks": ["78.3", "79.2", "80.1"] },
    { "id": 67, "tasks": ["78.4", "79.3", "80.2", "87.1"] },
    { "id": 68, "tasks": ["78.5", "79.4", "79.5", "80.3", "80.4", "80.5", "81.1", "85.1", "87.2"] },
    { "id": 69, "tasks": ["78.6", "78.7", "81.2", "82.1", "84.1", "85.2", "86.1", "87.3"] },
    { "id": 70, "tasks": ["81.3", "82.2", "83.1", "84.2", "85.3", "86.2", "87.4", "87.5", "88.1"] },
    { "id": 71, "tasks": ["81.4", "81.5", "82.3", "83.2", "83.3", "84.3", "84.4", "86.3", "88.2"] },
    { "id": 72, "tasks": ["82.4", "82.5", "83.4", "88.3"] },
    { "id": 73, "tasks": ["88.4", "89.1"] },
    { "id": 74, "tasks": ["91.1", "91.2", "91.3", "92.1", "93.1"] },
    { "id": 75, "tasks": ["91.4", "91.5", "91.6", "91.7", "92.2", "92.4", "93.2"] },
    { "id": 76, "tasks": ["92.3", "92.5", "92.6", "92.7", "93.3", "93.4", "94.1"] },
    { "id": 77, "tasks": ["94.2", "95.1"] },
    { "id": 78, "tasks": ["94.3", "94.5", "95.2", "95.3", "95.4"] },
    { "id": 79, "tasks": ["94.4"] },
    { "id": 80, "tasks": ["96.1"] }
  ]
}
```
