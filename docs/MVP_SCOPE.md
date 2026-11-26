# MVP Scope

Summary of the Scope Register in [the canonical requirements](../.kiro/specs/neuropath-platform/requirements.md). The register there is authoritative; this page does not change it.

## MVP

| Area | Requirements |
|---|---|
| Foundation, design system, documentation, data model governance, CI and cost control, status contract | R1 to R8 |
| Public website and project inquiry form | R9 to R15 |
| Authentication and invitation-based client onboarding | R16, R25 |
| Roles and permission matrix; tenant isolation; API conventions | R17, R18, R19 |
| Attachments with malware scanning | R20 |
| Inquiry review and qualification, Founder inquiry inbox; lead management with consent and opt-out | R21, R22, R23 |
| Project record and lifecycle statuses; basic client workspace; notifications; Founder dashboard | R24, R26, R27, R28 |
| Technical assessments; audit trail | R29, R34, R30 |
| AI Solution Architect integration, requirement analysis, clarification; solution architecture and diagram | R31 to R33, R35 |
| Proposals: drafting, versioning, pricing approval, client decision, agreement records, sending and export | R36 to R40 |
| Consultation and Engineering Service Requests; usage and cost tracking; approval requests | R41, R42, R43 |
| Project activation, milestones, tasks, communication, deliverables, testing, deployment and handover, final acceptance | R44 to R51 |
| Support requests and maintenance engagements; change requests and scope baselines | R52, R53, R54 |
| Labs module framework | R55 |
| Commercial and payment records (record-keeping only) | R79 |
| ENGINE job framework; agent architecture and task recording for the first workflow; first internal OPS workflow; OPS approvals; Ops dashboard | R64 to R69 |
| Full Founder Control Center | R73 |
| Security, reliability, performance and cost review, test coverage, phase gating | R74 to R78 |

## MVP-conditional

- **Data Engineering Playground (R56 to R63).** Conditional on A-04: the Founder records a go or no-go decision at the Phase 4 gate. The Playground stays disabled in production until a go decision is recorded (R55.11).

## Optional

Built only on an operational need approved by the Founder (A-28):

- Lead Research and Outreach agents (R70)
- Content and Marketing agents (R71)
- Engineering Assistant (R72)
- Per-user permission grants beyond delegation (R17.11)
- User email opt-in notifications (R27.10)

## Future

Invoice generation and billing integration, proprietary products and SaaS tiers, additional Labs, Parquet and JSONL upload, maintenance reporting dashboards, client-facing analytics, managed queue and orchestration services.

## Out of scope

Payment processing and billing, e-signature, and automatic acceptance or approval of any commercial engagement by AI.
