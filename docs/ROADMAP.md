# Roadmap

Phases and requirement ranges from [the canonical requirements](../.kiro/specs/neuropath-platform/requirements.md). Requirement IDs are stable; R79 belongs to Phase 4 even though it is numbered after R78.

| Phase | Name | Requirements | Outcome |
|---|---|---|---|
| 0 | Foundation | R1 to R8 | A buildable, tested skeleton with no billable cloud resources unless authorized |
| 1 | Public Company Website | R9 to R15 | A website that accepts genuine project inquiries |
| 2 | Client Acquisition and Founder CRM | R16 to R30 | Inquiries can be received, reviewed, qualified and managed |
| 3 | Solution Discovery and Proposal | R31 to R43 | A qualified inquiry can move to an approved, versioned proposal that a client can accept |
| 4 | Project Delivery and Engineering Labs | R44 to R63, R79 (4A delivery and commercial records; 4B Labs, Playground R56 to R63 MVP-conditional) | Client projects can be delivered and supported on the platform |
| 5 | NEUROPATH OPS and ENGINE | R64 to R73 | Internal automation under Founder approval |
| 6 | Production Readiness | R74 to R78 | A platform that is reviewed, recoverable and supportable in production |

Priority order: public website, inquiry intake and Founder CRM, discovery and proposal, project delivery, Labs, OPS and ENGINE, production hardening.

## Phase gate rule (R78)

- When a phase is completed, a phase report lists the delivered requirement IDs, test results, known issues, open assumptions and the next phase plan.
- Work on the next phase starts only after a **recorded Founder review approval** of the previous phase report.
- Each completed phase builds and runs with all previously delivered features working.
- Each phase has a gate check defined in R78.5 to R78.11. The Phase 4 gate includes a recorded Founder go or no-go decision on the Data Engineering Playground (A-04).

## Current status

Phase 0 is in progress. See the spec task list at [tasks.md](../.kiro/specs/neuropath-platform/tasks.md).
