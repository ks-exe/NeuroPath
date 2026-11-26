# Requirements Document

**Version:** 2.0 (supersedes V1, archived unchanged at `docs/archive/REQUIREMENTS_V1.md`)
**Status:** Draft for Founder review. No implementation, AWS deployment, or billable resource creation is authorized by this document.

## Introduction

NEUROPATH is a Technology Solutions & Engineering Company. Its tagline is "Technology. Engineered to Solve." Its working model is: clients bring problems, and NEUROPATH engineers solutions. NEUROPATH does not sell a fixed catalogue of products and does not ask clients to choose a technology before they describe their problem.

**Problems solved.** Organizations approach NEUROPATH with manual or fragmented processes, systems that do not exchange data, data that is collected but not usable, infrastructure that is hard to run or secure, software that needs to be built or modernized, or an idea whose technical form is not yet known.

**Customers.** Customers are organizations and individuals that need engineering capacity or technical direction: operational teams with manual processes, businesses that need an AI-enabled application, teams with scattered data, and organizations modernizing legacy systems or moving to cloud infrastructure. This document names no existing customers.

**Engineering capabilities.** NEUROPATH offers six capability groups: AI & ML Engineering; Data Engineering & Analytics; Cloud & DevOps; Custom Software Engineering; Intelligent Automation & Integration; and Technical Consulting & Architecture. These are capabilities, not a commitment to accept every project. Each project is assessed for feasibility, required skills, available resources, risk, and scope.

**How clients engage.** A client submits a project inquiry that describes a problem and a desired outcome. The client may attach supporting files, and may answer follow-up questions against the same inquiry. Engagement forms are technical consulting, project-based engineering, custom software delivery, architecture and implementation, cloud deployment, and ongoing maintenance and support.

**How projects are delivered.** Every project follows one journey: Client Problem, Discovery, Requirement Analysis, Solution Architecture, Proposal, Agreement, Engineering, Testing, Deployment, Handover, Maintenance. A NEUROPATH reviewer qualifies each inquiry. AI tools may draft analysis, architecture, and proposals. A named authorized human reviews and approves every proposal, price, and external commitment. An inquiry is never an accepted commercial project until a client accepts an approved proposal version.

**Proprietary products.** NEUROPATH may later offer proprietary products, reusable platforms, or software-as-a-service subscriptions built from its engineering work. These are secondary to services, are not part of the first release, and require a separate Founder decision.

**The platform.** NEUROPATH is an engineering company supported by its own digital platform. The platform is not primarily a SaaS product. It consists of a public company website, a client workspace for tracking projects, a Founder Control Center for managing the business, optional supporting Labs (Data Engineering Playground, AI Solution Architect, Engineering Service Request), an internal execution layer (ENGINE), and internal operational support (OPS). Clients are never required to use a Lab.

### Delivery Phases

Each phase ends with a working application. Work on a phase starts only after the Founder has reviewed the previous phase report. The platform is designed for a small founding team: each phase delivers value that is usable before the next phase starts.

| Phase | Name | Scope | Real-world outcome |
|---|---|---|---|
| 0 | Foundation | Monorepo, development environment, architecture decisions, database baseline, documentation, CI/CD foundation, cost controls | A buildable, tested skeleton with no billable cloud resources unless authorized |
| 1 | Public Company Website | Brand, homepage, Services, Solutions, Projects, How We Work, About, Insights, Contact, project inquiry form, responsive layout, SEO | A website that accepts genuine project inquiries |
| 2 | Client Acquisition and Founder CRM | Authentication, users and organizations, inquiry management, leads, inquiry review, Founder dashboard, internal assessment records, notifications, basic client workspace | NEUROPATH can receive, review, qualify, and manage real opportunities |
| 3 | Solution Discovery and Proposal | AI Solution Architect, requirement analysis, clarification workflow, architecture diagrams, technical assessments, proposal drafting, review and approval, consultation workflow | NEUROPATH can move a qualified inquiry to an approved, versioned proposal that a client can accept |
| 4 | Project Delivery and Engineering Labs | Project activation, status management, milestones, tasks, team assignment, client communication, deliverables, testing records, deployment records, handover, support requests; Data Engineering Playground and other Labs as independent modules | NEUROPATH can deliver and support client projects on the platform |
| 5 | NEUROPATH OPS and ENGINE | Internal workflow engine, inquiry automation, agent orchestration, internal task automation, content assistance, lead research, engineering assistance, approvals, cost monitoring | Internal automation that reduces repeated manual work, under Founder approval |
| 6 | Production Readiness | Security review, performance, reliability, backups, monitoring, disaster recovery, cost optimization, deployment documentation, operational readiness | A platform that is reviewed, recoverable, and supportable in production |

Priority order: public website, inquiry intake and Founder CRM, discovery and proposal, project delivery, Labs, OPS and ENGINE, production hardening.

### How to Read This Document

Each requirement carries a compact metadata block:

- **ID** is the unique requirement identifier (NP-Rnn). **Phase** is the delivery phase. **Scope** is one of MVP, MVP-conditional (Founder go/no-go at the phase gate), Future, Optional, or Out-of-scope.
- **Roles** lists the roles that act in the requirement. **Depends** lists prerequisite requirement IDs. **V1** maps to the archived V1 requirement number.
- **Entities**, **Failures**, **Validation**, and **Security** are present where they apply.
- **Assumes** references an assumption in the Founder Review Assumptions table.
- Requirement IDs are stable identifiers. An ID is never renumbered, even when requirements are added, moved, or removed.
- R79 (Commercial and Payment Records) is a Phase 4 requirement. R79 is numbered after R78 because R79 was added after R78 was numbered.
- The appendices are Appendix A (A.1 Project status model, A.2 other entity status tables, A.3 permission matrix), Appendix B (data model decisions), Appendix C (infrastructure service necessity), Appendix D (V1 to V2 mapping), Appendix E (self-review), and Appendix F (completeness report).
- Appendix entries marked "(proposed, Founder review)" or "(decision, design phase may revise)" are not confirmed decisions. A "(proposed, Founder review)" entry stays a proposal until the Founder confirms it, and the design phase confirms or revises each "(decision, design phase may revise)" entry.
- Assumptions marked "(Founder decision, default)" in the Founder Review Assumptions table are defaults that the Founder may change.

## Founder Review Assumptions

The following items are working assumptions that the Founder must confirm or change. They are not business decisions.

| ID | Assumption | Affects |
|---|---|---|
| A-01 | A Project record is created at the moment an inquiry is submitted, one Project per Project_Inquiry. The Project status model governs the whole journey from Submitted to Completed. | R14, R21, R24 |
| A-02 | A visitor may submit an inquiry without an account. The Prospective_Client is stored as a Lead. A Client account is created by invitation after the inquiry is reviewed. | R14, R16, R25 |
| A-03 | Inquiry attachments are delivered in Phase 2, not Phase 1, because they require private storage and malware scanning. The Phase 1 form has no attachment control. | R14, R20 |
| A-04 | The Data Engineering Playground (R56 to R63) is MVP-conditional. The Founder decides at the Phase 4 gate whether it ships in the first release, based on available resources. | R55 to R63 |
| A-05 | V1 Registered_Customer and Premium_Customer map to the single role Client. A `tier` attribute is reserved on the Organization for a future opportunity and has no effect in MVP. | R17, R42 |
| A-06 | Only the Founder may approve commercial pricing and send proposals to clients. The Founder may delegate each permission to a named user. | R37, R43 |
| A-07 | The default permission matrix in Appendix A.3 is a starting point for Engineer and Project_Manager roles. | R17 |
| A-08 | No configured limit or period is fixed in this document: retention periods, attachment size limits, upload limits, approval expiry periods, the invitation expiry period, the Guest Lab usage limit, the Recommendation sample size bound, AI cost limits (per-Organization, global, and per-day agent cost), and the per-task token limit. The Founder sets each value in configuration before the phase that uses it is accepted. | R20, R25, R31, R32, R42, R43, R58, R63, R64, R66, R73, R74, R75, R76, R78 |
| A-09 | NEUROPATH does not send an automatic acknowledgement email to an inquiry submitter. The confirmation is shown on screen. Email to external parties requires Founder approval. | R14, R27 |
| A-10 | The Infrastructure as code tool (CDK or Terraform) is selected once during Phase 0 and recorded as an architecture decision. | R2 |
| A-11 | The consent wording for contact and for AI-assisted processing of inquiry content requires legal review by the Founder before launch. This document makes no compliance claim. | R14, R32, R33 |
| A-12 | No service-level agreement, support response time, or uptime commitment is defined. Support requests are recorded and handled without a promised response time. | R52 |
| A-13 | Agreement records in MVP store status, parties, effective dates, and a reference to a signed document that NEUROPATH uploads. No e-signature or payment integration exists. | R39 |
| A-14 | A Maintenance_Engagement is a separate record linked to the originating Project, with its own scope, status, and Agreement. | R53 |
| A-15 | The website and platform are English-only in MVP. | R9 to R15 |
| A-16 | The domain name, transactional email provider, and malware scanning product are not yet chosen. Each stays behind an interface until chosen. | R3, R14, R20 |
| A-17 | Insights, Projects, and case-study content come from structured content files maintained by NEUROPATH in the repository, not from a content management system. | R11, R13 |
| A-18 | A defect has a severity of Blocker, Critical, Major, or Minor. A Project may enter Awaiting Client Acceptance only with no open Blocker or Critical defect. | R49 |
| A-19 | Client acceptance of a proposal or delivery is recorded in the platform by an authorized member of the Client's Organization, and the Founder may record an acceptance received outside the platform together with an evidence reference. | R38, R51 |
| A-20 | A Client Organization has two member roles, Owner and Member. The first Client of a new Organization becomes Owner, and an Owner may invite people into the Owner's own Organization only. Member decision rights follow Appendix A.3. | R25, R38, R51 |
| A-21 | The project roles on a Project are Project Lead, Engineer, and Reviewer. A project role is separate from the platform role of R17 and is held through a Project_Member record. | R44, R46, R49, R50 |
| A-22 | A Client sees the display name and project role of each Project_Member. No other internal contact field is Client_Visible until the Founder configures the field as Client_Visible. | R44 |
| A-23 | The Deliverable approval permission ("Approved for Client") is held by the Founder and by a Project_Manager who is a current Project_Member of the Project (Appendix A.3, note 6). | R48 |
| A-24 | Test activity types are a configurable list maintained by the Founder. No fixed list of test types or minimum test coverage per Project is defined in this document. | R49 |
| A-25 | A Change_Request with no timeline or cost impact is approved by the Founder or a Project_Manager without an Approval_Request. The client Acceptance_Record is still required. | R54 |
| A-26 | Client access to a Lab in status client beta is granted per Organization through the Lab's Feature_Flag configuration, which the Founder maintains. | R55, Appendix A.3 |
| A-27 | ENGINE uses an in-process queue and worker behind one interface until Appendix C records a need for Amazon SQS, AWS Step Functions, Amazon EventBridge, or AWS Lambda. | R64, R65, R75, R76, Appendix C |
| A-28 | R67 is the only MVP OPS workflow. Every other agent or workflow is Optional and is enabled only on an operational need that the Founder approved. | R65, R67, R70, R71, R72 |
| A-29 | The Founder sets the CPU, memory, and time limits and the retry backoff for each job type before Phase 5 acceptance. | R64 |
| A-30 | In MVP at most one Agent_Task is in status Running at a time, and the per-day agent cost limit is checked before each Agent_Task starts. | R66 |
| A-31 | The Founder sets the recovery time objective (RTO) and recovery point objective (RPO) before Phase 6 acceptance. | R75, R78 |
| A-32 | The Founder sets the load test target values and the list of main API endpoints before Phase 6 acceptance. | R76, R78 |
| A-33 | The Founder records the list of sensitive fields and the seeded values used by the log scan in `docs/SECURITY.md`. The security review is an internal review and makes no compliance claim. | R74 |
| A-34 | The secret detection patterns (R50.3) and the card number and bank credential detection patterns (R79.12) are proposed lists that the Founder approves before Phase 4 acceptance. | R50, R79 |
| A-35 | (Founder decision, default) The Project status Accepted and transition T18 are enabled in Phase 3, so a client acceptance at the Phase 3 gate moves the Project to Accepted. Activation to In Progress waits for Phase 4. | R38, R44, R78, Appendix A.1 |
| A-36 | (Founder decision, default) Client self-service Dataset deletion under R63.1 does not require an Approval_Request. R73.10 applies to staff-initiated deletion requests for customer data. | R63, R73, Appendix A.3 |
| A-37 | (Founder decision, default) "Awaiting Client Acceptance" is the handover-preparation status before Delivered, and the Client decides while the Project is Delivered. The Founder may rename the status. | R44, R49, R50, R51, Appendix A.1 |

## Scope Register

| Class | Item | Requirements |
|---|---|---|
| MVP | Foundation, design system, documentation, data model governance, CI and cost control, status contract | R1 to R8 |
| MVP | Public website and project inquiry form | R9 to R15 |
| MVP | Authentication and invitation-based client onboarding | R16, R25 |
| MVP | Roles and permission matrix | R17 |
| MVP | Tenant isolation | R18 |
| MVP | API conventions | R19 |
| MVP | Attachments with malware scanning | R20 |
| MVP | Inquiry review and qualification, Founder inquiry inbox | R21, R23 |
| MVP | Lead management with consent and opt-out | R22 |
| MVP | Project record and lifecycle statuses | R24 |
| MVP | Basic client workspace | R26 |
| MVP | Notifications | R27 |
| MVP | Founder dashboard | R28 |
| MVP | Technical assessments | R29, R34 |
| MVP | Audit trail | R30 |
| MVP | AI Solution Architect integration, requirement analysis, clarification | R31 to R33 |
| MVP | Solution architecture and diagram | R35 |
| MVP | Proposal drafting and versioning, pricing approval, client decision, agreement records, sending and export | R36 to R40 |
| MVP | Consultation request and Engineering Service Request | R41 |
| MVP | Usage and cost tracking | R42 |
| MVP | Approval requests | R43 |
| MVP | Project activation, milestones, tasks, communication, deliverables, testing, deployment and handover, final acceptance | R44 to R51 |
| MVP | Support requests and maintenance engagements | R52, R53 |
| MVP | Change requests and scope baselines | R54 |
| MVP | Labs module framework | R55 |
| MVP | Commercial and payment records, record-keeping only | R79 |
| MVP | ENGINE job framework | R64 |
| MVP | Agent architecture and task recording for the first workflow | R65, R66 |
| MVP | First internal OPS workflow | R67 |
| MVP | OPS approvals | R68 |
| MVP | Ops dashboard | R69 |
| MVP | Full Founder Control Center | R73 |
| MVP | Security, reliability, performance and cost review, test coverage, phase gating | R74 to R78 |
| MVP-conditional | Data Engineering Playground (Founder go or no-go at the Phase 4 gate) | R56 to R63, A-04 |
| Optional | Per-user permission grants beyond delegation | R17.11 |
| Optional | Lead Research and Outreach agents | R70 |
| Optional | Content and Marketing agents | R71 |
| Optional | Engineering Assistant | R72 |
| Optional | User email opt-in notifications | R27.10 |
| Future | Invoice generation and billing integration | beyond R79 |
| Future | Proprietary products and SaaS tiers | A-05 |
| Future | Additional Labs | R55.10 |
| Future | Parquet and JSONL upload | R56.4 |
| Future | Maintenance reporting dashboards | none |
| Future | Client-facing analytics | none |
| Future | Managed queue and orchestration services | Appendix C |
| Out-of-scope | Payment processing and billing | none |
| Out-of-scope | E-signature | A-13 |
| Out-of-scope | Automatic acceptance or approval of any commercial engagement by AI | R21.8, R68.7 |
| Out-of-scope | A universal engine that runs model-generated code | R58.7, R64.4 |
| Out-of-scope | Customer-facing OPS | none |
| Out-of-scope | Multi-language support | A-15 |
| Out-of-scope | Native mobile apps | none |
| Out-of-scope | Training of models on customer data without recorded explicit consent | R63.3 |

Every MVP and MVP-conditional item maps to at least one requirement with testable acceptance criteria.

## Glossary

- **Platform**: The complete NEUROPATH system comprising Web_App, API, Data_Engine, Agent_Runtime, ENGINE, OPS, and Infrastructure.
- **Public_Site**: The set of public pages in Web_App that require no authentication.
- **Web_App**: The Next.js, React, TypeScript, Tailwind, and shadcn/ui frontend in `apps/web`.
- **API**: The FastAPI backend in `apps/api`, exposed under the `/api/v1` path prefix.
- **Client_Workspace**: The authenticated, project-focused area of Web_App used by Clients.
- **Founder_Control_Center**: The authenticated internal area of Web_App for NEUROPATH staff, reachable under `/admin`.
- **Data_Engine**: The Python package in `data_engine/` that performs profiling, validation, transformation, feature engineering, and reporting for the Data Playground.
- **Agent_Runtime**: The Strands Agents and Amazon Bedrock runtime in `agents/` that hosts AI components used by Labs, discovery tools, and OPS.
- **ENGINE**: The modular internal execution layer for data processing, pipeline execution, build and deploy workflows, scheduled jobs, AI processing tasks, internal engineering automation, and execution tracking. It runs only allowlisted operations.
- **OPS**: The internal operational support module, reachable only by NEUROPATH staff, in which AI agents assist staff. OPS is not a customer-facing product.
- **Infrastructure**: AWS resources defined as code in `infrastructure/`.
- **Auth_Service**: Amazon Cognito user pools and the API components that verify Cognito tokens.
- **Guest**: An unauthenticated visitor.
- **Client**: An authenticated, email-verified external user who belongs to an Organization. Replaces V1 Registered_Customer and Premium_Customer (A-05).
- **Founder**: The highest-privilege role. The Founder holds every permission of every other role and has visibility across the whole business.
- **Administrator**: An authenticated NEUROPATH staff member with administrative permissions.
- **Engineer**: An authenticated NEUROPATH staff member who performs assessments, design, and delivery work.
- **Project_Manager**: An authenticated NEUROPATH staff member who coordinates inquiries, projects, milestones, and client communication.
- **Internal_Agent**: A non-human principal that may call only the API operations explicitly authorized for that agent.
- **Authorized_Reviewer**: An internal user who holds the permission needed for a given review action under Appendix A.3.
- **Authorized_Approver**: An internal user who holds the permission to approve a proposal or commercial terms. By default the Founder only (A-06).
- **Organization**: A tenant that owns users, projects, inquiries, communications, deliverables, and Lab data. An Organization has status active or suspended (R73). NEUROPATH itself is the internal organization.
- **Organization status**: The status of an Organization, either active or suspended. The Founder changes the status in the Founder_Control_Center (R73).
- **Organization_Member**: The record that links one user to one Organization. In a Client Organization the record holds one member role, Owner or Member (R25.5, A-20).
- **Prospective_Client**: A person or organization that has submitted an inquiry or been identified as a possible client, and has no Client account. Stored as a Lead.
- **Lead**: The stored record of a Prospective_Client, created from an inquiry or from Lead Research.
- **Project_Inquiry**: The submitted description of a problem, with desired outcome, existing systems, constraints, and optional attachments. An inquiry is a request for review. It is not a commercial project.
- **Inquiry_Question**: A follow-up question attached to a Project_Inquiry, with status Draft, Open, Answered, or Withdrawn (Appendix A.2.2).
- **Project**: The record that carries a Project_Inquiry through the lifecycle. It has one status from the Project Status Model (Appendix A.1) and is created at inquiry submission (A-01).
- **Project_Opportunity**: A Project that a reviewer has qualified and that has not yet been accepted by the Client. Statuses Qualified through Awaiting Client Decision.
- **Active_Engagement**: A Project with an accepted Proposal_Version and an Agreement in effect, in status In Progress, Testing, Awaiting Client Acceptance, or Delivered.
- **Project_Requirements**: The structured set of business, functional, non-functional, technical, data, integration, security, and scalability requirements recorded for a Project.
- **Technical_Assessment**: An internal record of feasibility, risks, dependencies, missing information, and recommended engineering disciplines for a Project.
- **Solution_Architecture**: A versioned, validated, structured description of the proposed architecture, technology stack, and technical decisions for a Project, renderable as a diagram.
- **Solution_Architect**: The AI Solution Architect, a supporting tool inside discovery that drafts Technical_Assessments, Solution_Architectures, and Proposal drafts. Its output is a draft until a human approves it.
- **Proposal**: The container for all versions of NEUROPATH's offer to a Client for one Project.
- **Proposal_Version**: One immutable-after-approval version of a Proposal, with status Draft, In Review, Approved, Sent, Superseded, or Withdrawn.
- **Agreement**: The record of the contractual status between NEUROPATH and a Client for a Project or Maintenance_Engagement. In MVP it holds metadata and a document reference only (A-13).
- **Project_Milestone**: A dated, named group of work and deliverables within a Project.
- **Task**: A unit of work within a Project_Milestone, with an assignee, due date, and status.
- **Deliverable**: A document, report, diagram, source-code handover reference, deployment document, or other file that NEUROPATH shares with a Client.
- **Communication**: A message in a project thread. A Communication is either Client_Visible or Internal_Only.
- **Client_Visible**: Data that the owning Client Organization may see.
- **Internal_Only**: Data that only NEUROPATH internal roles may see.
- **Acceptance_Record**: An append-only record of a decision by a Client on a Proposal_Version, a milestone deliverable, or final delivery, with user identity, timestamp, and the accepted version.
- **Defect**: A recorded fault found in testing, with severity, status, and resolution.
- **Deployment_Record**: A record of a deployment to an environment, with status and notes, and without secret values.
- **Handover_Checklist**: The list of items that must be completed to transfer a delivered solution to the Client.
- **Support_Request**: A request, bug report, or improvement request raised by a Client for an active or completed Project.
- **Maintenance_Engagement**: A separate engagement that provides ongoing maintenance for a delivered Project under its own scope and Agreement.
- **Commercial_Record**: A record-keeping entry of type Quotation Reference, Milestone Payment Schedule Entry, Invoice Reference, or Payment Status for a Project (R79). It performs no payment processing.
- **Lab**: An optional supporting tool: Data Engineering Playground, AI Solution Architect, or Engineering Service Request.
- **Engineering_Service_Request**: The structured entry form for a general engineering challenge. It creates a Project_Inquiry and does not require choosing a Lab or a technology.
- **Dataset**: A user-uploaded file in CSV, XLSX, or JSON format and its metadata.
- **Profile**: The computed statistical and quality description of a Dataset.
- **Pipeline**: An ordered list of allowlisted Operations applied to a Dataset.
- **Operation**: A deterministic, allowlisted, parameterized transformation implemented in the Data_Engine.
- **Recommendation**: An AI-suggested Operation list that is a proposal only and is not executed until a user approves it.
- **Execution**: One run of a Pipeline, with per-Operation status, timing, counts, warnings, errors, and logs.
- **Job**: An asynchronous unit of long-running work identified by a job ID.
- **Agent_Task**: A unit of work assigned to an OPS agent.
- **Approval_Request**: A recorded request for a decision by an Authorized_Approver on a proposal, commercial term, or Sensitive_Action.
- **Sensitive_Action**: Any of: sending external emails, contacting prospects, publishing content, issuing commercial quotations, making purchases, spending on advertising, modifying production infrastructure, deleting customer information, sharing confidential information.
- **Audit_Log**: An append-only record of who did what, to which resource, and when.
- **Presigned_URL**: A short-lived Amazon S3 URL scoped to a single object and operation.
- **Feature_Flag**: A runtime switch that enables or disables a capability.
- **Design_System**: The "Editorial Brutalism x Engineering Journal" visual language defined in Requirement 4.
- **Real_Result**: A value derived from actual execution of code or a persisted record, never from placeholder or invented data.
- **Project_Member**: The record that assigns one internal user to one Project with one project role (A-21).
- **Project role**: The role a Project_Member holds on one Project: Project Lead, Engineer, or Reviewer. A project role is separate from the platform role of R17 (A-21).
- **Project Lead**: The project role that leads delivery on a Project (A-21).
- **Engineer (project role)**: The project role that performs engineering work on a Project. A user holding this project role need not hold the platform role Engineer (A-21).
- **Reviewer (project role)**: The project role that reviews work on a Project (A-21).
- **Client Owner**: The Organization_Member role in a Client Organization that may invite people into the Owner's own Organization and holds the Owner decision rights of Appendix A.3 (A-20).
- **Client Member**: The Organization_Member role in a Client Organization with the Member decision rights of Appendix A.3 (A-20).
- **Invitation**: A record that binds one email address to one Organization, expires after the configured period, and is accepted at most once (R25).
- **Scope_Baseline**: A versioned record of the agreed scope of a Project. Version 1 copies the accepted Proposal_Version, and each later version references one Approved Change_Request (R54).
- **Change_Request**: A recorded request to change the scope, timeline, or cost of a Project, with its own status and client Acceptance_Record (R54).
- **Delivery reference**: The record computed when a Project enters Delivered. It lists the Approved for Client Deliverable versions and the Handover_Checklist item statuses of the Project, with a content hash. Final acceptance is recorded against it (R51.2, R51.5).
- **Milestone acceptance criterion**: A verifiable condition recorded on a Project_Milestone that the Client checks when deciding on the milestone. Each acceptance criterion has status Met or Not Met (R45, R49).
- **Test activity**: A recorded test run on a Project, with a type from the configurable list, result, and date (R49, A-24).
- **Solution_Architect_Draft**: An output of the Solution_Architect that stays a draft until a human approves the output (R31, R32).
- **Project_Requirements_Version**: One immutable version of the Project_Requirements of a Project.
- **Technical_Assessment_Version**: One immutable version of a Technical_Assessment.
- **Solution_Architecture_Version**: One immutable version of a Solution_Architecture.
- **Price_Entry**: A price line in a Proposal_Version that requires approval by an Authorized_Approver (R37).
- **Cost_Estimate**: An internal estimate of the cost of delivering a Project or of AI usage, which is not a client price (R37, R42).
- **Lab registration**: The record that registers a Lab with the Labs module framework, with its status and Feature_Flag (R55).
- **Operational need record**: A Founder-approved record that justifies enabling an Optional agent or workflow (A-28).
- **Agent registration**: The record that registers an OPS agent with its allowed API operations and limits (R65).
- **Job type registry**: The allowlist of job types that ENGINE may run. Each entry names the handler and the configured limits and retry policy of the job type (R64, A-29).
- **Dead-letter record**: The record of a Job or Agent_Task that failed after the final retry (R64).
- **Approved source list**: The Founder-approved list of sources that an agent may read (R70).
- **Usage record**: A row in the `usage_records` table that records AI or compute usage with tokens, cost, Organization, and timestamp (R42).
- **Consent_Record**: An append-only record of the consent a Lead or Client gave, with wording version and timestamp (R22).
- **Opt_Out_Entry**: A record that a person opted out of contact, checked before any outreach (R22).
- **System**: The API acting on a recorded event under the Platform principal, as used in status transition tables. The System is never an Internal_Agent or Agent_Runtime principal (Appendix A).

### Entity Relationships

- A Prospective_Client (Lead) submits zero or more Project_Inquiries. A Client belongs to one or more Organizations.
- One Project_Inquiry has exactly one Project (A-01). One Project has zero or more Inquiry_Questions, Technical_Assessments, Solution_Architecture versions, and Proposals (typically one), and zero or more Project_Milestones.
- One Proposal has one or more Proposal_Versions. At most one Proposal_Version is accepted. An accepted Proposal_Version yields at most one Agreement for the Project.
- One Project_Milestone has zero or more Tasks and Deliverables. One Project has zero or more Communications, Defects, Deployment_Records, Acceptance_Records, and one Handover_Checklist.
- One Project has zero or more Support_Requests. A Maintenance_Engagement references one originating Project and one Agreement.
- An Invitation binds one email address to one Organization and is accepted at most once. An Organization has zero or more Organization_Members, and each Organization_Member of a Client Organization has the role Owner or Member.
- A Project has zero or more Project_Members, each with one project role (Project Lead, Engineer, or Reviewer).
- An accepted Proposal_Version yields Scope_Baseline version 1 at activation. Each later Scope_Baseline version references one approved Change_Request.
- A Change_Request belongs to one Project.
- A Commercial_Record references one Project and optionally one Proposal_Version, Agreement, Project_Milestone, Maintenance_Engagement, or Change_Request of that Project.
- A Project has one delivery reference when the Project enters Delivered, and final acceptance is recorded against that delivery reference.

### Engagement Stage Definitions

| Stage | Meaning | Project statuses |
|---|---|---|
| Inquiry | Submitted for review. No commercial standing. | Draft, Submitted, Under Review, Awaiting Information |
| Qualified project (opportunity) | NEUROPATH has judged the project suitable. No offer exists or is accepted. | Qualified, Assessment in Progress, Solution Designed |
| Proposal stage | An offer is being drafted, reviewed, or awaits the client. | Proposal Draft, Proposal Under Review, Proposal Sent, Awaiting Client Decision |
| Approved and accepted | The client has accepted an approved Proposal_Version. | Accepted |
| Active engagement | Engineering and delivery are underway under an Agreement in effect. | In Progress, Testing, Awaiting Client Acceptance, Delivered |
| Closed | No further work on this Project record. | Completed, Rejected, Cancelled |
| Paused | Work is suspended with a recorded reason. | On Hold |


## Requirements

## Phase 0: Foundation

### Requirement 1: Monorepo Structure

**User Story:** As a developer, I want a documented monorepo layout, so that every module has a predictable home and can be built and tested independently.

**ID:** NP-R01 | **Phase:** 0 | **Scope:** MVP | **Roles:** Engineer | **V1:** 1 | **Depends:** none

#### Acceptance Criteria

1. THE Platform repository SHALL contain the top-level directories `apps/web`, `apps/api`, `packages`, `infrastructure`, `docs`, and `scripts`.
2. THE `apps/api` directory SHALL contain the subdirectories `api`, `core`, `models`, `schemas`, `services`, `repositories`, `workers`, and `tests`.
3. THE Platform repository SHALL create the directories `data_engine` (with `profiling`, `validation`, `transformations`, `feature_engineering`, `reporting`) and `agents` (with one subdirectory per OPS agent) in the phase that first needs them, and SHALL NOT create empty placeholder modules earlier.
4. THE Platform repository SHALL isolate each Lab as an independent module so that a Lab can be added, disabled, or removed without changing the core inquiry, project, or proposal modules.
5. IF the implemented structure deviates from this layout, THEN THE Platform SHALL document each deviation and its rationale in `docs/ARCHITECTURE.md`.

### Requirement 2: Technology Stack and Architecture Decisions

**User Story:** As a developer, I want a fixed, minimal technology stack with recorded decisions, so that the platform stays modular and avoids unneeded services.

**ID:** NP-R02 | **Phase:** 0 | **Scope:** MVP | **Roles:** Engineer, Founder | **V1:** 2 | **Assumes:** A-10 | **Security:** Web_App holds no secrets

#### Acceptance Criteria

1. THE Web_App SHALL be implemented with Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, and React Flow.
2. THE API SHALL be implemented with Python, FastAPI, Pydantic, SQLAlchemy, and Alembic.
3. THE Platform SHALL use PostgreSQL on Amazon RDS for relational data and Amazon S3 for file storage.
4. THE Data_Engine SHALL use Pandas, Polars, and PyArrow, and THE Agent_Runtime SHALL use Amazon Bedrock models and Strands Agents with structured outputs.
5. THE Infrastructure SHALL use AWS Cognito, Lambda, ECS on Fargate, SQS, Step Functions, EventBridge, CloudWatch, and Secrets Manager only for a component whose purpose is recorded in `docs/ARCHITECTURE.md` and required by a requirement in this document.
6. THE Infrastructure SHALL be defined as code in either CDK or Terraform, selected once and recorded in `docs/ARCHITECTURE.md`.
7. WHEN an architectural decision is made, THE Platform SHALL record the decision, alternatives considered, and rationale in `docs/ARCHITECTURE.md`.
8. THE Web_App SHALL NOT call privileged AWS services and SHALL NOT contain secrets or AWS credentials.

### Requirement 3: Local Development and External Service Fallbacks

**User Story:** As a developer, I want to run the Platform locally without every AWS service available, so that development continues when a credential or service is unavailable.

**ID:** NP-R03 | **Phase:** 0 | **Scope:** MVP | **Roles:** Engineer, Founder | **V1:** 3 | **Assumes:** A-16 | **Failures:** missing credential or service | **Security:** no hardcoded secrets

#### Acceptance Criteria

1. THE Platform SHALL provide documentation that lists every environment variable, its purpose, and whether it is a secret, and the documentation SHALL be created in the phase that first introduces a variable.
2. THE Platform SHALL load secrets from environment variables locally and from AWS Secrets Manager in deployed environments.
3. IF a required credential or external service is unavailable, THEN THE Platform SHALL use a documented integration interface together with a safe local implementation.
4. IF a local implementation substitutes for an external service, THEN THE Platform SHALL identify the substitution in the implementation status record and SHALL return no fabricated success result to callers.
5. THE Platform SHALL keep each external integration (Bedrock, S3, Cognito, malware scanner, email, notification channel) behind an interface so that the implementation is replaceable without changing callers.
6. THE Infrastructure SHALL NOT create billable AWS resources until the Founder has explicitly authorized the specific deployment in writing.
7. THE Platform repository SHALL contain no hardcoded secrets, and a secret scanning check SHALL run in the continuous integration pipeline.

### Requirement 4: Design System

**User Story:** As a visitor, I want a distinctive, consistent interface, so that NEUROPATH reads as a serious engineering company.

**ID:** NP-R04 | **Phase:** 0 (tokens), applied in every UI phase | **Scope:** MVP | **Roles:** all | **V1:** 4

#### Acceptance Criteria

1. THE Web_App SHALL implement the Design_System "Editorial Brutalism x Engineering Journal" through shared design tokens.
2. THE Web_App SHALL use the colors #762B3B (primary), #F4F0E9 (background), #171515 (dark), #D9D0C6 (secondary), and #A76C58 (accent).
3. THE Web_App SHALL use Playfair Display for headings, Manrope for body text, and IBM Plex Mono for code, labels, and technical text.
4. THE Web_App SHALL use no gradients other than a flat two-stop gradient required by a functional chart, no glassmorphism, no robot imagery, and border radii no larger than 4 px on cards.
5. THE Web_App SHALL limit motion to transitions of 300 ms or less.
6. WHILE the user's operating system reports a reduced-motion preference, THE Web_App SHALL disable non-essential animation.
7. THE Web_App SHALL render without horizontal scrolling at viewport widths of 360 px, 768 px, 1280 px, and 1920 px.

### Requirement 5: Documentation Set

**User Story:** As a stakeholder, I want current documentation after every phase, so that status and decisions are always visible.

**ID:** NP-R05 | **Phase:** 0 and every phase | **Scope:** MVP | **Roles:** Engineer, Founder | **V1:** 5

#### Acceptance Criteria

1. THE Platform repository SHALL contain `README.md` and, in `docs/`, the documents REQUIREMENTS_V2, CHANGELOG_V1_TO_V2, ARCHITECTURE, ROADMAP, MVP_SCOPE, and AI_AGENT_INSTRUCTIONS from Phase 0.
2. THE Platform SHALL create each of the documents DATABASE, API, SECURITY, DEVELOPMENT, ENVIRONMENT, DEPLOYMENT, TESTING, and IMPLEMENTATION_STATUS in the first phase whose deliverables the document describes, and SHALL NOT create the document with placeholder content earlier.
3. THE implementation status document SHALL list completed work, incomplete work, known bugs, technical debt, blockers, tests run with results, and next tasks.
4. WHEN a phase is completed, THE Platform SHALL update every affected document in the same change set as the phase deliverables.
5. THE Platform SHALL mark a feature as complete in the implementation status document only when automated tests covering the feature exist and pass.
6. THE `.kiro/specs/neuropath-platform/requirements.md` file SHALL be the single canonical requirements source, and `docs/REQUIREMENTS_V2.md` SHALL point to it without duplicating its text.

### Requirement 6: Data Model Governance

**User Story:** As a developer, I want a migration-managed, documented relational schema, so that data is consistent and tenant-isolated and tables exist only when needed.

**ID:** NP-R06 | **Phase:** 0 (baseline), every phase | **Scope:** MVP | **Roles:** Engineer | **V1:** 6 | **Depends:** R2 | **Security:** tenant ownership on every tenant table

#### Acceptance Criteria

1. THE API SHALL implement the tables listed for each phase in Appendix B, after the design phase has confirmed or revised each table's decision recorded in Appendix B.
2. THE API SHALL apply every schema change through an Alembic migration.
3. THE API SHALL create the tables required by a phase in a migration delivered in that phase or an earlier phase, and SHALL NOT create a table for a later phase.
4. THE API SHALL define foreign keys, unique constraints, and indexes for every relationship and every column used for tenant filtering or lookup.
5. THE API SHALL include an `organization_id` column on each tenant-owned table.
6. THE API SHALL exclude from each tenant-scoped repository method any query that omits an organization filter, except for methods restricted to Founder or Administrator callers.
7. WHEN a migration is applied and then reverted on an empty database, THE API SHALL leave the database schema equal to its starting state.
8. THE database documentation SHALL describe each table, column, relationship, tenant ownership rule, retention rule, and the migration strategy for the phase.
9. THE API SHALL store each Proposal_Version, Acceptance_Record, and Audit_Log entry in a table that has no update or delete operation exposed by the API, except status transitions under R8 and, for a Proposal_Version, content edits while the status is Draft or In Review.

### Requirement 7: Continuous Verification and Cost Control

**User Story:** As the Founder, I want automated checks and cost guardrails, so that quality and spending stay under control.

**ID:** NP-R07 | **Phase:** 0 | **Scope:** MVP | **Roles:** Engineer, Founder | **V1:** 7 | **Depends:** R2, R3

#### Acceptance Criteria

1. THE Platform SHALL provide one documented command for each of: lint, type check, unit tests, and build, for each of Web_App and API.
2. WHEN a change is pushed, THE continuous integration pipeline SHALL run lint, type check, tests, and secret scanning.
3. THE Infrastructure SHALL tag every AWS resource with project, environment, and owner tags.
4. THE Infrastructure SHALL define an AWS budget alarm for each deployed environment before any other resource in that environment is created.
5. WHERE a new AWS service not listed in Requirement 2 is proposed, THE Platform SHALL record a justification in `docs/ARCHITECTURE.md` before the service is provisioned.

### Requirement 8: Domain Model and Status Transition Contract

**User Story:** As a developer, I want one authoritative definition of statuses and transitions, so that code, tests, and documents cannot diverge.

**ID:** NP-R08 | **Phase:** 0 (definition), enforced from Phase 2 | **Scope:** MVP | **Roles:** Engineer | **V1:** new (extends 19.2, 19.3) | **Depends:** R6 | **Entities:** all status-bearing entities

#### Acceptance Criteria

1. THE Platform SHALL define each status set and transition table in Appendix A as machine-readable data in one source file per entity in the API.
2. THE API SHALL reject any status change for which no row in the transition table exists for the current status, target status, and acting role.
3. THE API SHALL reject any status change whose guard condition in the transition table is not satisfied, and SHALL return a structured error that names the failed guard.
4. WHEN a status change is accepted, THE API SHALL write an Audit_Log entry with the previous status, new status, actor, timestamp, and reason.
5. THE API SHALL provide no endpoint that sets a status without passing the transition check.
6. WHILE the entity required by a guard is not yet delivered by the current phase, THE API SHALL treat each transition that depends on that guard as disabled.
7. FOR ALL pairs of statuses (s1, s2) and roles, THE API SHALL accept the change from s1 to s2 if and only if a matching row exists in the transition table (status transition validity property).

## Phase 1: Public Company Website

### Requirement 9: Global Navigation and Layout

**User Story:** As a visitor, I want consistent navigation, so that I can find any section from any page.

**ID:** NP-R09 | **Phase:** 1 | **Scope:** MVP | **Roles:** Guest | **V1:** 8 | **Depends:** R4 | **Assumes:** A-15

#### Acceptance Criteria

1. THE Web_App SHALL display the primary navigation links Home, Services, Solutions, Projects, How We Work, About, Insights, and Contact on every public page.
2. THE Web_App SHALL display the primary call to action "Start a Project" in the header on every public page, and SHALL link it to the project inquiry form.
3. THE Web_App SHALL display a Sign In link in the header only in a phase in which the Auth_Service is enabled.
4. WHEN the viewport width is below 768 px, THE Web_App SHALL replace the navigation links with a menu control that opens and closes the full navigation.
5. THE Web_App SHALL set `aria-current="page"` on the navigation item for the current page.
6. THE Web_App SHALL display a footer on every public page containing links to all navigation destinations and the tagline "Technology. Engineered to Solve."
7. WHILE a Guest views a public page, THE Web_App SHALL operate without requiring authentication.

### Requirement 10: Homepage

**User Story:** As a visitor with a problem, I want a homepage that shows I can bring the problem without knowing the solution, so that I decide to start a project.

**ID:** NP-R10 | **Phase:** 1 | **Scope:** MVP | **Roles:** Guest | **V1:** 9 | **Depends:** R9, R11

#### Acceptance Criteria

1. THE Web_App SHALL render the homepage with these sections in order: Hero, What We Solve, Engineering Capabilities, Industries and Business Use Cases, Selected Projects and Case Studies, How We Work, Why NEUROPATH, and Final Project Inquiry CTA.
2. THE Hero section SHALL display the heading "Bring us your problem. We'll engineer the solution." and the tagline "Technology. Engineered to Solve."
3. THE Hero section SHALL display the primary call to action "Start a Project" and the secondary call to action "Explore Our Capabilities".
4. WHEN a visitor activates "Start a Project", THE Web_App SHALL navigate to the project inquiry form.
5. WHEN a visitor activates "Explore Our Capabilities", THE Web_App SHALL navigate to the Services page.
6. THE What We Solve section SHALL state that a client may come with a manual process, an AI application need, workflow automation, system integration, a data pipeline or analytics need, cloud infrastructure, custom software, modernization, or an idea without knowing the technology.
7. THE Engineering Capabilities section SHALL present the six service groups defined in Requirement 12.
8. THE How We Work section SHALL present the journey steps Discovery, Requirement Analysis, Solution Architecture, Proposal, Agreement, Engineering, Testing, Deployment, Handover, and Maintenance in that order.
9. THE Web_App SHALL present the Data Engineering Playground and the AI Solution Architect only as supporting capabilities, and SHALL NOT place either in the Hero section.
10. THE Final Project Inquiry CTA section SHALL link to the project inquiry form.
11. THE Web_App SHALL NOT display the V1 tagline "Engineering Intelligence. Enabling Growth." on any page.

### Requirement 11: Truthful Content

**User Story:** As the Founder, I want the website to contain only true claims, so that NEUROPATH's credibility is protected.

**ID:** NP-R11 | **Phase:** 1 | **Scope:** MVP | **Roles:** Founder, Guest | **V1:** 10 | **Assumes:** A-17 | **Validation:** verification flag

#### Acceptance Criteria

1. THE Selected Projects and Case Studies section SHALL display only projects that exist in a content source maintained by NEUROPATH and marked verified by the Founder.
2. THE Web_App SHALL NOT display invented customers, results, metrics, testimonials, pricing, or certifications.
3. IF no verified project exists, THEN THE Selected Projects and Case Studies section SHALL state that case studies are being prepared, without placeholder entries.
4. THE Web_App SHALL render each project entry from structured content that includes title, description, technologies, and a verification flag.
5. THE Web_App SHALL omit any project entry whose verification flag is not set to verified.
6. THE Why NEUROPATH section SHALL contain only statements about NEUROPATH's working method that the Founder has confirmed in the content source.

### Requirement 12: Services Pages

**User Story:** As a prospective client, I want clear descriptions of what NEUROPATH engineers, so that I can see my problem is within reach without having to name a technology.

**ID:** NP-R12 | **Phase:** 1 | **Scope:** MVP | **Roles:** Guest | **V1:** 11 | **Depends:** R11 | **Security/Legal:** scraping compliance statement

#### Acceptance Criteria

1. THE Services page SHALL list six service groups, each linking to a detail section or page: A. AI & ML Engineering; B. Data Engineering & Analytics; C. Cloud & DevOps; D. Custom Software Engineering; E. Intelligent Automation & Integration; F. Technical Consulting & Architecture.
2. THE detail content of group A SHALL list custom AI applications, LLM integrations, RAG systems, AI agents and agentic workflows, intelligent automation, predictive analytics, machine learning model development, AI decision support, and model integration and deployment.
3. THE detail content of group B SHALL list data pipelines, ETL and ELT, data ingestion and processing, data warehousing, data transformation, data quality engineering, business intelligence, analytics dashboards, and data architecture.
4. THE detail content of group C SHALL list cloud architecture, AWS infrastructure, infrastructure as code, CI/CD, containerization, deployment, monitoring and observability, cloud optimization, and reliability and security engineering.
5. THE detail content of group D SHALL list custom web applications, backend systems, APIs, database architecture, internal business platforms, modernization, third-party integrations, and full-stack development.
6. THE detail content of group E SHALL list workflow automation, internal operational automation, AI-assisted processes, system-to-system integration, document processing, data synchronization, and operational efficiency.
7. THE detail content of group F SHALL list technical discovery, feasibility analysis, system architecture, technology selection, cloud architecture consulting, technical audits, project planning, and engineering roadmaps.
8. THE Services page SHALL state that each service group is a capability and that each project is assessed for feasibility, required skills, resources, risk, and scope before NEUROPATH accepts it.
9. WHEN content under group B or group E describes web scraping or automated data collection, THE content SHALL state that engagements respect applicable laws, website terms of service, access controls, and privacy requirements.
10. THE detail content for each service group SHALL describe typical engagements, deliverables, and technologies, and SHALL contain no unverifiable performance claims.
11. THE Web_App SHALL display on each service detail the call to action "Start a Project", and SHALL pass the service group to the inquiry form only as an optional hint that the visitor may change or clear.

### Requirement 13: Additional Public Pages

**User Story:** As a visitor, I want pages for Solutions, Projects, How We Work, About, and Insights, so that I can learn about the company and its method.

**ID:** NP-R13 | **Phase:** 1 | **Scope:** MVP | **Roles:** Guest | **V1:** 12 | **Depends:** R11 | **Assumes:** A-17

#### Acceptance Criteria

1. THE Web_App SHALL provide public pages for Solutions, Projects, How We Work, About, and Insights.
2. THE Solutions page SHALL describe problem-oriented solution areas and SHALL describe the Data Engineering Playground, the AI Solution Architect, and the Engineering Service Request as optional supporting capabilities, each with its availability status.
3. THE Projects page SHALL apply the truthful content rules in Requirement 11.
4. THE How We Work page SHALL describe each journey step from Discovery to Maintenance, what the client provides, and what NEUROPATH delivers at that step, and SHALL state that AI-drafted material is reviewed by a NEUROPATH engineer before it reaches a client.
5. THE About page SHALL describe the company as a Technology Solutions & Engineering Company and SHALL contain only statements confirmed by the Founder.
6. THE Insights page SHALL list only published articles from a structured content source, and IF no article is published, THEN THE Insights page SHALL state that articles are forthcoming.
7. THE Web_App SHALL return a styled 404 page with navigation for any unknown public route.

### Requirement 14: Project Inquiry Form

**User Story:** As a prospective client, I want to describe my problem without choosing a technology, so that NEUROPATH can review it and respond.

**ID:** NP-R14 | **Phase:** 1 | **Scope:** MVP | **Roles:** Guest | **V1:** 13 | **Depends:** R6, R31 | **Assumes:** A-01, A-02, A-03, A-09, A-11 | **Entities:** Lead, Project_Inquiry, Project | **Failures:** validation error, rate limit, honeypot, API failure | **Validation:** see criteria | **Security:** sanitized text, rate limit, consent record

#### Acceptance Criteria

1. THE inquiry form SHALL provide fields for name, email, company or organization, project title, problem description, desired outcome, existing systems, relevant data or integrations, expected users, additional constraints, optional budget range, optional preferred timeline, and a consent checkbox for contact and data processing.
2. THE inquiry form SHALL NOT require the visitor to select an AI, Data, DevOps, or Software category, and SHALL display an optional service hint field that the visitor may leave empty.
3. WHEN a visitor submits the form with name, a syntactically valid email, a problem description of at least 20 characters, a project title, and consent given, THE API SHALL store a Lead, a Project_Inquiry, and a Project in status Submitted, and SHALL return a success response.
4. IF a required field is empty, an email is syntactically invalid, or consent is not given, THEN THE Web_App SHALL show a field-specific error message next to the offending field and SHALL NOT submit the form.
5. IF the API rejects a submission, THEN THE Web_App SHALL display the error and preserve the entered values.
6. WHEN a submission succeeds, THE Web_App SHALL display a confirmation message and clear the form.
7. THE API SHALL limit anonymous form submissions to 5 per client IP address per 10 minutes and SHALL return a rate-limit error beyond that limit.
8. THE API SHALL include a honeypot field check and reject submissions that fill it.
9. THE API SHALL sanitize submitted text before storage and rendering, and SHALL limit each free-text field to a configured maximum length.
10. THE API SHALL record the consent text version, consent timestamp, and a separate flag for permission to process the inquiry content with AI-assisted analysis.
11. THE API SHALL write an Audit_Log entry for each stored Project_Inquiry.
12. THE Platform SHALL notify NEUROPATH internal users of each new Project_Inquiry through the notification interface, and SHALL NOT send email to the submitter without Founder approval.
13. WHILE the form request is pending, THE Web_App SHALL disable the submit control and show a loading state.
14. FOR ALL submissions that the API accepts, THE API SHALL store exactly one Project_Inquiry and one Project, and a repeated delivery of the same submission token SHALL NOT create a second Project_Inquiry (idempotence).

### Requirement 15: SEO, Performance, and Accessibility of the Public Site

**User Story:** As the Founder, I want the website to be discoverable and accessible, so that more qualified visitors reach it.

**ID:** NP-R15 | **Phase:** 1 | **Scope:** MVP | **Roles:** Guest | **V1:** 14 | **Depends:** R9 to R14

#### Acceptance Criteria

1. THE Web_App SHALL set a unique title, meta description, canonical URL, and Open Graph metadata on every public page.
2. THE Web_App SHALL generate a sitemap and a robots file.
3. THE Web_App SHALL render exactly one h1 element per public page and a logical heading hierarchy.
4. THE Web_App SHALL provide text alternatives for every meaningful image.
5. THE Web_App SHALL meet WCAG 2.2 level AA contrast for text and interactive controls, including focus indicators.
6. THE Web_App SHALL allow every interactive element to be operated with the keyboard alone.
7. THE Web_App SHALL associate every form control with a visible label.
8. WHEN an error or status message appears, THE Web_App SHALL announce the message to screen readers through a live region or focus move.
9. THE public homepage SHALL achieve Lighthouse scores of at least 90 for Performance, Accessibility, Best Practices, and SEO on a mobile profile in a production build.
10. THE Web_App SHALL load only the fonts and scripts required by each page.

## Phase 2: Client Acquisition and Founder CRM

### Requirement 16: Registration, Sign-In, and Account Recovery

**User Story:** As a client or NEUROPATH staff member, I want secure account management, so that I can access my projects and data safely.

**ID:** NP-R16 | **Phase:** 2 | **Scope:** MVP | **Roles:** Guest, Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 15 | **Depends:** R3, R6, R14 | **Assumes:** A-02, A-16 | **Entities:** User, Organization, Organization_Member, Invitation | **Failures:** unverified email, expired or used invitation, failed sign-in, lockout, Cognito unavailable | **Validation:** email syntax, password policy, invitation token | **Security:** Cognito-only credentials, enumeration-safe recovery, HTTP-only cookies

#### Acceptance Criteria

1. THE Auth_Service SHALL perform authentication through Amazon Cognito, and THE Platform SHALL NOT store or process passwords outside Cognito.
2. WHEN an Authorized_Reviewer converts a reviewed Project_Inquiry into a Client invitation, THE API SHALL create an Invitation bound to the Lead email and to the Organization that owns the Project.
3. WHEN an invited person registers with a valid, unused, unexpired Invitation and a password that meets the policy, THE Auth_Service SHALL create an unverified account and send a verification message.
4. IF a registration request carries no Invitation, or an Invitation that is expired, already used, or bound to a different email, THEN THE API SHALL reject the registration with a structured error and SHALL create no account.
5. WHEN the Founder creates a staff account, THE API SHALL create the account with the role selected by the Founder and send a verification message.
6. IF an account email is not verified, THEN THE Auth_Service SHALL deny sign-in until verification is completed.
7. WHEN a user requests password recovery, THE Auth_Service SHALL send a reset code to the registered email, and THE API SHALL return an identical response body, status code, and response timing class whether or not the email is registered.
8. THE Auth_Service SHALL enforce a password policy of at least 12 characters.
9. IF five consecutive failed sign-in attempts occur for one account, THEN THE Auth_Service SHALL apply a temporary lockout to that account.
10. THE API SHALL provide endpoints `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/logout`, and `/api/v1/auth/me`.
11. WHEN a user registers through an Invitation, THE API SHALL create a user record and an Organization_Member record that links the user to the Invitation's Organization with the Client role.
12. WHEN a user signs out, THE API SHALL invalidate the session, including revocation of the refresh token, and THE Web_App SHALL clear client session state.
13. IF a request presents a session token that has been invalidated, THEN THE API SHALL return HTTP 401 with a structured error.
14. THE Web_App SHALL store session tokens only in HTTP-only, secure, same-site cookies.
15. IF the Auth_Service is unavailable, THEN THE API SHALL return a structured error that states authentication is temporarily unavailable and SHALL grant no session.
16. THE API SHALL write an Audit_Log entry for each account creation, Invitation creation, Invitation use, sign-in lockout, and staff account creation.

### Requirement 17: Roles and Permissions

**User Story:** As the Founder, I want strict role-based access, so that users and agents only do what they are permitted to do.

**ID:** NP-R17 | **Phase:** 2 | **Scope:** MVP (per-user grants: Optional) | **Roles:** Guest, Client, Founder, Administrator, Engineer, Project_Manager, Internal_Agent | **V1:** 16 | **Depends:** R16 | **Assumes:** A-05, A-06, A-07 | **Entities:** Role, Permission, Role_Assignment | **Failures:** unauthenticated, unauthorized | **Security:** deny by default, server-side enforcement

#### Acceptance Criteria

1. THE API SHALL support the roles Guest, Client, Founder, Administrator, Engineer, Project_Manager, and Internal_Agent.
2. THE API SHALL grant each role exactly the permissions defined for that role in the permission matrix in Appendix A.3.
3. THE API SHALL treat the Founder as holding every permission defined in Appendix A.3.
4. THE API SHALL check authentication and authorization on every endpoint other than public endpoints, and SHALL deny any action that no permission explicitly grants.
5. IF a request to a non-public endpoint lacks valid authentication, THEN THE API SHALL return HTTP 401 with a structured error.
6. IF an authenticated principal lacks the permission required by the endpoint, THEN THE API SHALL return HTTP 403 with a structured error.
7. THE API SHALL grant an Internal_Agent access only to the operations listed in that agent's explicit permission set.
8. IF a role assignment would give an Internal_Agent the Administrator role, the Founder role, or unrestricted administrative access, THEN THE API SHALL reject the assignment with a structured error.
9. THE Web_App SHALL hide controls that the current user lacks permission to use, and THE API SHALL enforce the same restrictions independently of the Web_App.
10. WHEN a role is assigned, changed, or removed, THE API SHALL write an Audit_Log entry with actor, target user, previous role, new role, and time.
11. WHERE per-user permission grants are enabled, THE API SHALL allow the Founder to grant or revoke an individual permission from Appendix A.3 for a named user and SHALL write an Audit_Log entry for each grant and revocation.
12. FOR ALL roles other than Founder and all endpoints, THE API SHALL return a success status only when Appendix A.3 grants that role the endpoint's permission (matrix conformance property).

### Requirement 18: Tenant Isolation

**User Story:** As a client, I want my organization's data visible only to my organization and authorized NEUROPATH staff, so that confidential information remains private.

**ID:** NP-R18 | **Phase:** 2 | **Scope:** MVP | **Roles:** Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 17 | **Depends:** R6, R17 | **Entities:** Organization, Organization_Member, all tenant-owned records | **Failures:** cross-organization access attempt | **Security:** organization-scoped queries, S3 prefix verification, Internal_Only filtering

#### Acceptance Criteria

1. THE API SHALL scope every query for tenant-owned data issued on behalf of a Client to the Organizations in which the Client holds membership.
2. IF a Client requests a resource that belongs to an Organization in which the Client holds no membership, THEN THE API SHALL return HTTP 404 and SHALL NOT disclose whether the resource exists.
3. THE API SHALL store tenant objects in S3 under keys prefixed by the owning organization identifier.
4. WHEN a Presigned_URL is requested, THE API SHALL verify that the object key begins with the prefix of an Organization the caller may access before issuing the Presigned_URL.
5. THE API SHALL exclude every Internal_Only record and field from responses to principals that hold the Client role.
6. THE API SHALL provide endpoints for current user and Organization data at `/api/v1/users/me` and `/api/v1/organizations`.
7. FOR ALL pairs of distinct Organizations A and B, no API response to a Client of A SHALL contain any record owned by B (isolation property).
8. FOR ALL API responses to a principal holding the Client role, the response SHALL contain no Internal_Only record or field (visibility property).

### Requirement 19: API Conventions

**User Story:** As a developer, I want uniform API behavior, so that clients handle success and failure predictably.

**ID:** NP-R19 | **Phase:** 2 | **Scope:** MVP | **Roles:** all | **V1:** 21 | **Depends:** R2 | **Failures:** validation error, rate limit, long-running work | **Validation:** Pydantic schemas on every input | **Security:** per-principal and per-IP rate limits

#### Acceptance Criteria

1. THE API SHALL validate every request body, query parameter, and path parameter with Pydantic schemas.
2. IF validation fails, THEN THE API SHALL return HTTP 422 with an error body that contains a machine-readable code, a human-readable message, and the list of offending fields.
3. THE API SHALL return every error in one documented structured error format that includes a machine-readable code, a human-readable message, and a request identifier.
4. THE API SHALL include the request identifier of each request in the corresponding log entries.
5. THE API SHALL apply per-principal and per-IP rate limits with limit values held in configuration.
6. IF a rate limit is exceeded, THEN THE API SHALL return HTTP 429 with a `Retry-After` header.
7. WHEN an endpoint starts long-running work, THE API SHALL return HTTP 202 with a job ID.
8. THE API SHALL provide an endpoint that returns the status of a Job by job ID, scoped to the principal permitted to see that Job.
9. THE API SHALL expose an OpenAPI description, and the continuous integration pipeline SHALL fail when the OpenAPI description and `docs/API.md` disagree on paths, methods, or schemas.

### Requirement 20: Secure Inquiry and Project Attachments

**User Story:** As a client, I want to share supporting files safely, so that NEUROPATH can understand my problem without exposing my documents.

**ID:** NP-R20 | **Phase:** 2 | **Scope:** MVP | **Roles:** Guest, Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 23.7 to 23.11 | **Depends:** R3, R14, R17, R18 | **Assumes:** A-03, A-08, A-16 | **Entities:** Attachment, Project_Inquiry, Project | **Failures:** disallowed type, content-type mismatch, size above limit, malware detected, scanner unavailable, missing object | **Validation:** extension, real content type, size | **Security:** private bucket, encryption at rest, short-lived scoped URLs, malware scan, audited downloads

#### Acceptance Criteria

1. THE Infrastructure SHALL store attachments in a private S3 bucket that blocks public access and encrypts objects at rest.
2. WHEN an upload is requested, THE API SHALL return a Presigned_URL valid for no more than 10 minutes and scoped to one object key under the owning Organization's prefix.
3. WHEN an upload finishes, THE API SHALL accept a complete-upload request and create an Attachment record only after verifying that the object exists.
4. THE API SHALL validate on the server both the file extension and the real content type by inspecting file content.
5. THE API SHALL accept only file types on an allowlist documented in `docs/SECURITY.md`.
6. THE API SHALL enforce a maximum attachment size held in configuration and set by the Founder (A-08).
7. IF a file has an extension outside the allowlist, a content type that does not match its extension, or a size above the configured limit, THEN THE API SHALL reject the file, delete the stored object, and return a structured error that names the reason.
8. THE API SHALL scan each uploaded attachment for malware before marking the Attachment as available.
9. IF the malware scan detects malware or the scanner is unavailable, THEN THE API SHALL mark the Attachment as quarantined, SHALL issue no download Presigned_URL for the Attachment, and SHALL notify an internal user through the notification interface.
10. WHEN a download is requested for an available Attachment, THE API SHALL issue a Presigned_URL valid for no more than 10 minutes only to a member of the owning Organization or to an internal role that Appendix A.3 permits to read attachments.
11. WHEN a download Presigned_URL is issued, THE API SHALL write an Audit_Log entry with actor, Attachment identifier, and time.
12. FOR ALL Attachments, THE API SHALL issue a download Presigned_URL only when the Attachment status is available (quarantine property).

### Requirement 21: Inquiry Review and Qualification

**User Story:** As a NEUROPATH reviewer, I want to review, question, qualify, or reject inquiries, so that only suitable opportunities move forward.

**ID:** NP-R21 | **Phase:** 2 | **Scope:** MVP | **Roles:** Founder, Administrator, Engineer, Project_Manager | **Depends:** R8, R14, R17 | **Assumes:** A-01, A-07 | **Entities:** Project_Inquiry, Project, Inquiry_Question, Project_Opportunity, Audit_Log | **Failures:** disallowed transition, missing reason, unauthorized reviewer | **Validation:** transition table in Appendix A.1, reason required for rejection | **Security:** human-only decisions

#### Acceptance Criteria

1. THE API SHALL allow an Authorized_Reviewer to list and view Project_Inquiries according to the permissions in Appendix A.3.
2. WHEN an Authorized_Reviewer requests more information on a Project_Inquiry, THE API SHALL create one or more Inquiry_Questions with status Open and move the Project to status Awaiting Information.
3. WHEN an Authorized_Reviewer rejects a Project_Inquiry with a recorded reason, THE API SHALL move the Project to status Rejected and store the reason.
4. IF a rejection request contains no reason, THEN THE API SHALL reject the request with a structured error.
5. WHEN an Authorized_Reviewer qualifies a Project_Inquiry, THE API SHALL move the Project to status Qualified, which makes the Project a Project_Opportunity.
6. WHEN an Authorized_Reviewer assigns a technical reviewer, THE API SHALL record the assigned Engineer on the Project.
7. THE API SHALL accept only Project status transitions defined in Appendix A.1, and IF a requested transition is not defined, THEN THE API SHALL return a structured error and leave the status unchanged.
8. THE API SHALL accept a qualify, reject, or approve decision on a Project_Inquiry or engagement only from a human principal, and SHALL reject such a decision from an Internal_Agent or from the Agent_Runtime.
9. WHERE AI-generated analysis exists for a Project_Inquiry, THE Web_App SHALL label the analysis as AI-generated and advisory.
10. WHEN a review decision is recorded, THE API SHALL write an Audit_Log entry with actor, time, previous status, new status, and reason.
11. FOR ALL sequences of review requests, every recorded Project status change SHALL correspond to a transition defined in Appendix A.1 (transition conformance property).

### Requirement 22: Lead Management

**User Story:** As the Founder, I want a lawful, de-duplicated record of prospective clients, so that NEUROPATH contacts the right people with valid consent.

**ID:** NP-R22 | **Phase:** 2 | **Scope:** MVP | **Roles:** Founder, Administrator, Project_Manager | **V1:** 13, 43.2, 43.5 | **Depends:** R14, R17 | **Assumes:** A-11 | **Entities:** Lead, Lead_Source, Consent_Record, Opt_Out_Entry | **Failures:** duplicate email, contact attempt to opted-out person, disallowed status transition | **Validation:** normalized email, statuses in Appendix A.2 | **Security:** consent evidence, opt-out enforcement

#### Acceptance Criteria

1. WHEN a Project_Inquiry is stored, THE API SHALL create or link a Lead for the submitter.
2. THE API SHALL store, for each Lead data item, the source from which the item was obtained.
3. THE API SHALL assign each Lead one status defined in Appendix A.2 and SHALL accept only the Lead status transitions defined in Appendix A.2.
4. THE API SHALL compute a normalized email for each Lead by trimming surrounding whitespace and converting the email to lowercase.
5. WHEN a new Lead has the same normalized email as an existing Lead, THE API SHALL flag both Leads as a possible duplicate.
6. WHEN an Authorized_Reviewer approves a merge of flagged Leads, THE API SHALL merge the Leads, preserve every source and consent record, and write an Audit_Log entry; THE API SHALL perform no merge without that approval.
7. THE API SHALL record each consent with timestamp and consent wording version.
8. WHEN a person requests opt-out, THE API SHALL add the normalized email to the opt-out list and write an Audit_Log entry.
9. IF a contact action targets a Lead whose normalized email is on the opt-out list, THEN THE API SHALL reject the action with a structured error.
10. FOR ALL emails, normalizing an already normalized email SHALL return the same value (idempotence property).
11. FOR ALL Leads whose normalized email is on the opt-out list, THE API SHALL record no outgoing contact (opt-out property).

### Requirement 23: Founder Inquiry Inbox

**User Story:** As the Founder, I want an inbox of inquiries, so that I can see and act on every opportunity in one place.

**ID:** NP-R23 | **Phase:** 2 | **Scope:** MVP | **Roles:** Founder, Administrator, Engineer, Project_Manager | **Depends:** R17, R20, R21, R22 | **Entities:** Project_Inquiry, Project, Attachment, Inquiry_Question, Audit_Log | **Failures:** loading failure | **Security:** permission-filtered listing

#### Acceptance Criteria

1. THE Founder_Control_Center SHALL provide an inquiry inbox that lists Project_Inquiries visible to the current user under Appendix A.3.
2. THE inquiry inbox SHALL provide filters by Project status, submission date range, and assigned reviewer, and THE API SHALL apply the filters on the server.
3. WHEN a user opens a Project_Inquiry from the inbox, THE Founder_Control_Center SHALL show the inquiry fields, Attachments with their scan status, Inquiry_Questions with answers, and the status and decision history.
4. THE inquiry inbox SHALL display counts per Project status computed only from stored records.
5. WHILE inbox data is loading, THE Founder_Control_Center SHALL show a loading state.
6. IF no Project_Inquiry matches the current filters, THEN THE Founder_Control_Center SHALL show an empty state that states no inquiries match.
7. IF loading inbox data fails, THEN THE Founder_Control_Center SHALL show an error state with a retry control.
8. FOR ALL filter combinations, the count displayed for a status SHALL equal the number of stored Project_Inquiries that match the filters and have that status (count integrity property).

### Requirement 24: Project Record and Early Lifecycle Statuses

**User Story:** As the Founder, I want every inquiry carried by one Project with a controlled status, so that each opportunity has a single, traceable state.

**ID:** NP-R24 | **Phase:** 2 | **Scope:** MVP | **Roles:** Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 19.2-19.5 | **Depends:** R8, R14, R21 | **Assumes:** A-01 | **Entities:** Project, Project_Inquiry, Inquiry_Question, Audit_Log, Notification | **Failures:** disallowed transition, transition to a status not enabled in the current phase, On Hold without reason, client cancellation after Accepted | **Validation:** transition table in Appendix A.1 | **Security:** role-checked transitions, client-facing labels only

#### Acceptance Criteria

1. WHEN a Project_Inquiry is submitted, THE API SHALL create exactly one Project linked to that Project_Inquiry with status Submitted.
2. THE API SHALL assign each Project one status from the Project Status Model in Appendix A.1.
3. WHILE the Platform is in Phase 2, THE API SHALL enable the statuses Draft, Submitted, Under Review, Awaiting Information, Qualified, Rejected, Cancelled, and On Hold.
4. IF a requested transition targets a status that is not enabled in the current phase, THEN THE API SHALL reject the transition with a structured error that names the status as disabled.
5. IF a requested transition is not defined in Appendix A.1, THEN THE API SHALL reject the transition with a structured error.
6. THE Client_Workspace SHALL display each Project status to a Client using the client-facing label defined in Appendix A.1.
7. WHEN a Client answers the last Open Inquiry_Question of a Project in status Awaiting Information, THE API SHALL move the Project to Under Review.
8. IF a transition to On Hold is requested without a reason, THEN THE API SHALL reject the transition with a structured error.
9. WHEN a Project moves to On Hold, THE API SHALL store the reason and the prior status.
10. WHEN an Authorized_Reviewer resumes a Project from On Hold, THE API SHALL move the Project to the stored prior status.
11. WHEN a Client requests cancellation of a Project whose status precedes Accepted in Appendix A.1, THE API SHALL move the Project to Cancelled.
12. IF a Client requests cancellation of a Project in status Accepted or a later status, THEN THE API SHALL reject the request with a structured error.
13. WHEN a Project status changes, THE API SHALL write an Audit_Log entry with prior status, new status, actor, and reason, and SHALL create a Notification for the Project owner.
14. FOR ALL sequences of transition requests, every stored Project status SHALL be reachable from Submitted through transitions defined in Appendix A.1 and enabled in the phase in which each transition occurred (transition integrity property).
15. FOR ALL Project_Inquiries, THE API SHALL hold exactly one linked Project (one-to-one invariant).

### Requirement 25: Client Invitation and Organization Onboarding

**User Story:** As the Founder, I want to invite a reviewed Prospective_Client into a Client Organization, so that only reviewed people get platform access.

**ID:** NP-R25 | **Phase:** 2 | **Scope:** MVP | **Roles:** Founder, Administrator, Project_Manager, Client | **Depends:** R16, R17, R18, R22 | **Assumes:** A-02, A-08, A-20 | **Entities:** Invitation, Organization, Organization_Member, Lead, User, Audit_Log | **Failures:** expired invitation, reused invitation, revoked invitation, email mismatch, invitation to another Organization | **Validation:** normalized email match, Organization name required | **Security:** single-use token bound to email, organization-scoped inviting

#### Acceptance Criteria

1. WHEN an Authorized_Reviewer invites a Prospective_Client linked to a Project_Inquiry, THE API SHALL create an Invitation bound to the Lead's normalized email and to a new or existing Organization.
2. WHEN THE API creates a new Organization for an Invitation, THE API SHALL set the Organization name from the inquiry company field and SHALL allow the Authorized_Reviewer to edit the name before sending.
3. THE API SHALL set each Invitation expiry from the configured invitation expiry period.
4. WHEN an invited person completes registration through a valid Invitation with the bound email, THE API SHALL convert the Lead to a Client, add the Client to the Organization as an Organization_Member, and link the Organization to the Project.
5. THE API SHALL assign each Organization_Member of a Client Organization one role of Owner or Member.
6. WHEN the first Client of a new Organization accepts an Invitation, THE API SHALL assign that Client the Owner role.
7. WHEN an Organization_Member with role Owner invites a person, THE API SHALL create an Invitation bound to the invitee's email and to the Owner's Organization only.
8. IF an Invitation request names an Organization in which the inviting Client is not an Owner, THEN THE API SHALL reject the request with HTTP 404 and a structured error.
9. IF an Invitation is presented after expiry, after revocation, or after a prior acceptance, THEN THE API SHALL reject the Invitation with a structured error.
10. IF the registering email does not match the Invitation's bound email after normalization, THEN THE API SHALL reject the registration with a structured error.
11. WHEN an Authorized_Reviewer or the issuing Owner revokes an Invitation that has not been accepted, THE API SHALL mark the Invitation revoked.
12. WHEN an Invitation is created, sent, accepted, rejected, or revoked, THE API SHALL write an Audit_Log entry.
13. FOR ALL Invitations, THE API SHALL record at most one acceptance (single-use property).

### Requirement 26: Basic Client Workspace

**User Story:** As a Client, I want a project-focused workspace, so that I can follow my inquiries and answer NEUROPATH's questions.

**ID:** NP-R26 | **Phase:** 2 | **Scope:** MVP | **Roles:** Client | **V1:** 18 | **Depends:** R17, R18, R24, R27 | **Entities:** Project, Project_Inquiry, Inquiry_Question, Communication, Notification | **Failures:** loading failure, unauthenticated access, answer to a non-Open question | **Validation:** answer text required | **Security:** Organization-scoped data, Client_Visible data only

#### Acceptance Criteria

1. THE Client_Workspace SHALL provide an authenticated, project-focused dashboard at `/dashboard`.
2. WHILE the Platform is in Phase 2, THE Client_Workspace SHALL show the Client's Project_Inquiries and Projects with status, Open Inquiry_Questions, recent Client_Visible updates, and Notifications.
3. WHEN a Client submits an answer to an Open Inquiry_Question from the dashboard, THE API SHALL store the answer, set the Inquiry_Question to Answered, and apply the status rule in Requirement 24.
4. IF a Client submits an answer to an Inquiry_Question that is not Open, THEN THE API SHALL reject the answer with a structured error.
5. THE API SHALL return to the Client_Workspace only records owned by Organizations in which the Client is an Organization_Member, and only Client_Visible data.
6. THE Client_Workspace SHALL compute every displayed value from stored records.
7. WHILE dashboard data is loading, THE Client_Workspace SHALL show a loading state.
8. IF the Client has no records of a displayed type, THEN THE Client_Workspace SHALL show an empty state that states the next action.
9. IF loading dashboard data fails, THEN THE Client_Workspace SHALL show an error state with a retry control.
10. WHEN an unauthenticated user requests a `/dashboard` route, THE Web_App SHALL redirect the user to Sign In and return the user to the requested route after sign-in.
11. THE Phase 4 Client Workspace requirements SHALL extend this dashboard with proposals, milestones, deliverables, and support content.
12. FOR ALL Clients, every record shown in the Client_Workspace SHALL belong to an Organization of that Client and be Client_Visible (workspace isolation property).

### Requirement 27: Notifications

**User Story:** As a user, I want in-app notifications for events that concern me, so that I can act without polling every page.

**ID:** NP-R27 | **Phase:** 2 | **Scope:** MVP | **Roles:** Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 18.4-18.6, 13.10 | **Depends:** R3, R17, R24 | **Assumes:** A-09, A-16 | **Entities:** Notification, Notification_Preference, User | **Failures:** email provider unavailable, email to external party without approval | **Security:** recipient-scoped notifications, external email approval

#### Acceptance Criteria

1. WHEN a Project_Inquiry is stored, THE Platform SHALL create an in-app Notification for each internal user permitted to review inquiries under Appendix A.3.
2. WHEN an Inquiry_Question is asked, THE Platform SHALL create an in-app Notification for the Client Organization_Members of the Project.
3. WHEN an Inquiry_Question is answered, THE Platform SHALL create an in-app Notification for the internal user who asked the Inquiry_Question.
4. WHEN a Project status changes, THE Platform SHALL create an in-app Notification for the Project owner.
5. WHEN an Attachment is quarantined, THE Platform SHALL create an in-app Notification for internal users permitted to review inquiries.
6. WHERE the phase that delivers proposals, milestones, deliverables, or support is enabled, THE Platform SHALL create in-app Notifications for proposal sent, milestone, deliverable, and support events.
7. WHILE the phase that delivers an event type is not enabled, THE Platform SHALL keep Notifications for that event type disabled.
8. THE Web_App SHALL display the current user's unread Notification count and SHALL allow the user to mark a Notification as read.
9. THE API SHALL return to each user only Notifications addressed to that user.
10. WHEN an event occurs for which a user has opted into email, THE Platform SHALL send an email Notification to that user through the notification interface.
11. IF an email Notification targets an external party and is not a Cognito authentication or verification message, THEN THE Platform SHALL send the email only after Founder approval.
12. THE Platform SHALL deliver Notifications through a notification interface with a local implementation, as required by Requirement 3.
13. IF the email provider is unavailable, THEN THE Platform SHALL keep the in-app Notification, record the email failure, and report no email success.
14. FOR ALL users with no email opt-in for an event type, THE Platform SHALL send no email for that event type (opt-in property).

### Requirement 28: Founder Dashboard (Phase 2)

**User Story:** As the Founder, I want a dashboard of real pipeline metrics, so that I can see the state of the business at a glance.

**ID:** NP-R28 | **Phase:** 2 | **Scope:** MVP | **Roles:** Founder, Administrator | **V1:** 20.1-20.2, 42.1 (partial) | **Depends:** R17, R22, R23, R24 | **Entities:** Project, Project_Inquiry, Inquiry_Question, Lead, Organization, Audit_Log | **Failures:** loading failure, invalid date range | **Validation:** date range start not after end | **Security:** Founder and Administrator only per Appendix A.3

#### Acceptance Criteria

1. THE Founder_Control_Center SHALL provide a Founder dashboard accessible only to roles permitted under Appendix A.3, which by default are Founder and Administrator.
2. THE Founder dashboard SHALL show counts of Project_Inquiries per Project status, new Project_Inquiries in a selected date range, Qualified Projects, Rejected Projects, Projects in Awaiting Information, Open Inquiry_Questions, Leads, Client Organizations, and Clients.
3. THE Founder dashboard SHALL show recent activity drawn from the Audit_Log.
4. THE API SHALL compute every Founder dashboard metric from stored records and SHALL return no placeholder values.
5. IF a selected date range has a start after its end, THEN THE API SHALL reject the request with HTTP 422.
6. WHILE Founder dashboard data is loading, THE Founder_Control_Center SHALL show a loading state.
7. IF no records exist for a metric, THEN THE Founder dashboard SHALL show zero for that metric and an empty state for recent activity when no activity exists.
8. IF loading Founder dashboard data fails, THEN THE Founder_Control_Center SHALL show an error state with a retry control.
9. FOR ALL stored data sets and date ranges, each displayed count SHALL equal the number of stored records that match the metric definition (count integrity property).

### Requirement 29: Internal Technical Assessment Records

**User Story:** As an Engineer, I want to record a structured Technical_Assessment for a qualified Project, so that feasibility and risk are documented before solution design.

**ID:** NP-R29 | **Phase:** 2 | **Scope:** MVP | **Roles:** Engineer, Founder | **Depends:** R17, R24, R30 | **Assumes:** A-07 | **Entities:** Technical_Assessment, Technical_Assessment_Version, Project, Audit_Log | **Failures:** assessment on a non-Qualified Project, missing complexity justification, invalid feasibility value, Client access attempt | **Validation:** enumerated feasibility and complexity values, disciplines from the six service groups | **Security:** Internal_Only

#### Acceptance Criteria

1. WHEN an Engineer or the Founder starts a Technical_Assessment for a Project in status Qualified, THE API SHALL create the Technical_Assessment and move the Project to Assessment in Progress.
2. IF a Technical_Assessment is started for a Project that is not in status Qualified, THEN THE API SHALL reject the request with a structured error.
3. THE Technical_Assessment SHALL record feasibility, required skills, resource availability, risks, dependencies, missing information, recommended engineering disciplines, complexity, and complexity justification.
4. THE API SHALL accept only Feasible, Feasible with conditions, Not feasible, or Unknown as the feasibility value.
5. THE API SHALL accept only Low, Medium, High, or Very High as the complexity value, and IF the complexity justification is empty, THEN THE API SHALL reject the Technical_Assessment with HTTP 422.
6. THE API SHALL accept as recommended engineering disciplines only values from the six service groups defined in this document.
7. THE API SHALL classify every Technical_Assessment as Internal_Only.
8. IF a Client requests a Technical_Assessment, THEN THE API SHALL return HTTP 404 and SHALL not disclose that the Technical_Assessment exists.
9. WHEN an Engineer or the Founder edits a Technical_Assessment, THE API SHALL store a new Technical_Assessment_Version and SHALL keep every prior version unchanged.
10. WHILE the Platform is in Phase 2, THE API SHALL enable the transition from Qualified to Assessment in Progress and SHALL keep the transition to Solution Designed disabled until Phase 3.
11. WHEN a Technical_Assessment is created or a new version is stored, THE API SHALL write an Audit_Log entry.
12. THE Phase 3 AI assessment drafting requirement (R34) SHALL extend this record with AI-drafted content.
13. FOR ALL sequences of edits, the stored version numbers of a Technical_Assessment SHALL be consecutive from 1 and every prior version SHALL remain equal to its original content (version history invariant).

### Requirement 30: Audit Logging Baseline

**User Story:** As the Founder, I want an append-only record of significant actions, so that I can reconstruct who did what and when.

**ID:** NP-R30 | **Phase:** 2 | **Scope:** MVP | **Roles:** Founder, Administrator | **V1:** 42.5-42.6, 20.6, 44.5 | **Depends:** R6, R17, R21 | **Entities:** Audit_Log | **Failures:** update or delete attempt on an entry, audit write failure | **Validation:** search filter values, time range start not after end | **Security:** append-only storage, redaction of secrets and raw customer data

#### Acceptance Criteria

1. THE API SHALL record each Audit_Log entry with actor type (user, agent, or system), actor identifier, action, resource type, resource identifier, Organization, timestamp, request identifier, and metadata.
2. THE API SHALL write an Audit_Log entry for authentication events, role changes, status changes, review decisions, Attachment access, consent and opt-out events, Invitation events, configuration changes, approvals, exports, external communications, and data deletion.
3. THE API SHALL apply the documented redaction policy to Audit_Log metadata so that metadata contains no secrets, tokens, passwords, or raw customer content.
4. THE API SHALL expose no operation that updates or deletes an Audit_Log entry, as required by Requirement 6.9.
5. IF an Audit_Log entry cannot be written for a state-changing request, THEN THE API SHALL roll back the state change and return a structured error.
6. THE Founder_Control_Center SHALL allow Founder and Administrator users to search the Audit_Log by actor, action, resource, and time range.
7. IF an Audit_Log search time range has a start after its end, THEN THE API SHALL reject the request with HTTP 422.
8. IF a user without Founder or Administrator permission requests Audit_Log search, THEN THE API SHALL return HTTP 403 with a structured error.
9. FOR ALL state-changing endpoints, each committed change SHALL produce exactly one Audit_Log entry (audit completeness property).
10. FOR ALL sequences of API operations, the set of Audit_Log entries after the sequence SHALL contain every entry that existed before the sequence, unchanged (append-only property).

## Phase 3: Solution Discovery and Proposal

### Requirement 31: Solution Architect Integration with Discovery

**User Story:** As an Authorized_Reviewer, I want to invoke the Solution_Architect on a Project, so that analysis and design drafts support human review without replacing it.

**ID:** NP-R31 | **Phase:** 3 | **Scope:** MVP | **Roles:** Authorized_Reviewer, Engineer, Founder, Guest, Client | **V1:** 31.1, 31.4, 35.9 | **Depends:** R14, R17, R25, R30 | **Assumes:** A-11 | **Entities:** Project, Project_Inquiry, Solution_Architect_Draft, Feature_Flag, Audit_Log | **Failures:** invocation on a Project in a disallowed status, invocation while Feature_Flag disabled, Guest over configured Lab limit, Guest save attempt without sign-in | **Validation:** Project status in Qualified or Under Review, configured Guest limit, free-text maximum lengths | **Security:** Internal_Only drafts, role check on invocation, untrusted input

#### Acceptance Criteria

1. WHEN an Authorized_Reviewer invokes the Solution_Architect on a Project in status Qualified or Under Review, THE API SHALL start a Job and store the result as a Solution_Architect_Draft linked to the Project.
2. IF the Solution_Architect is invoked on a Project in any status other than Qualified or Under Review, THEN THE API SHALL reject the request with HTTP 409 and a structured error.
3. IF a user without Authorized_Reviewer permission invokes the Solution_Architect on a Project, THEN THE API SHALL return HTTP 403 with a structured error.
4. THE API SHALL classify every Solution_Architect_Draft as Internal_Only until an Authorized_Reviewer publishes a specific part of the draft to the Client.
5. WHEN an Authorized_Reviewer publishes a part of a Solution_Architect_Draft, THE API SHALL make only that part visible in the Client_Workspace and write an Audit_Log entry naming the part.
6. THE Solution_Architect SHALL leave the Project status unchanged, and only a human status transition under R17 SHALL change the Project status.
7. WHERE the public Solution_Architect Lab is enabled, THE Web_App SHALL provide the Lab and THE API SHALL convert the Lab output into a Project_Inquiry draft.
8. WHILE a user is a Guest, THE API SHALL allow Lab analyses only up to the configured Guest limit and SHALL require sign-in before the Project_Inquiry draft is saved.
9. IF a Guest exceeds the configured Lab limit, THEN THE API SHALL return HTTP 429 with a structured error that states sign-in is required to continue.
10. WHERE the Solution_Architect Feature_Flag is disabled, THE API SHALL reject Solution_Architect invocations with HTTP 404 and THE Web_App SHALL hide the Lab and the staff invocation control.
11. THE Platform SHALL allow a Project_Inquiry to be submitted under R14 without use of the Lab, and R14 SHALL remain fully functional while the Solution_Architect Feature_Flag is disabled; R14 depends on R31 only for the optional "start from Solution Architect" path.
12. THE API SHALL provide Solution_Architect endpoints analyze, clarify, get, generate-architecture, generate-proposal, and export under `/api/v1/solutions`.
13. WHEN the Solution_Architect is invoked, THE API SHALL write an Audit_Log entry with the actor, Project, and Job identifier.
14. FOR ALL Solution_Architect invocations, the Project status before and after the Job SHALL be equal (status preservation property).

### Requirement 32: AI Requirement Analysis

**User Story:** As an Engineer, I want a structured AI analysis of a Project_Inquiry, so that scope, gaps, and risks are visible before assessment.

**ID:** NP-R32 | **Phase:** 3 | **Scope:** MVP | **Roles:** Authorized_Reviewer, Engineer, Founder | **V1:** 31.7-31.8, 32.1-32.2, 32.5-32.7 | **Depends:** R14, R31, R42 | **Assumes:** A-08, A-11 | **Entities:** Job, Project_Inquiry, Inquiry_Question, Attachment, Project_Requirements_Version, AI_Usage_Record | **Failures:** schema validation failure after retries, input above maximum length, attachment without AI-processing consent, attachment unavailable, AI provider error, prompt-injection attempt | **Validation:** Pydantic output schema, maximum input lengths, service group labels | **Security:** untrusted input, no tool access change from input, AI provider disclosure, Internal_Only output

#### Acceptance Criteria

1. WHEN AI analysis is requested for a Project, THE API SHALL start a Job and return HTTP 202 with the Job identifier.
2. THE Agent_Runtime SHALL send to the AI provider the Project_Inquiry fields and the answered Inquiry_Questions.
3. WHERE the AI-processing consent flag of R14.10 is set and the Attachment is available, THE Agent_Runtime SHALL include the extracted Attachment text in the analysis input.
4. IF the AI-processing consent flag is not set or the Attachment is unavailable, THEN THE Agent_Runtime SHALL exclude the Attachment text and record the exclusion reason in the Job result.
5. THE Web_App SHALL disclose, before the first analysis of a Project, which data categories are sent to the AI provider, consistent with A-11.
6. IF any input field exceeds its configured maximum length, THEN THE API SHALL reject the analysis request with HTTP 422 naming the field.
7. THE Agent_Runtime SHALL produce structured output covering business problem, functional requirements, non-functional requirements, technical requirements, data requirements, integration requirements, security and privacy requirements, scalability requirements, feasibility, dependencies, risks, missing information, and recommended engineering disciplines.
8. THE Agent_Runtime SHALL accept as recommended engineering disciplines only values from the six service groups, and SHALL mark each statement that is an assumption as an assumption.
9. THE API SHALL validate every model output against the Pydantic analysis schema before storing the output.
10. IF the model output fails schema validation, THEN THE Agent_Runtime SHALL retry at most 2 times and then mark the Job failed with a structured error and store no analysis output.
11. THE Agent_Runtime SHALL treat all inquiry fields, answers, and Attachment text as untrusted input, and an instruction embedded in that input SHALL leave the Agent_Runtime configured behavior and tool access unchanged.
12. WHEN a model call completes, THE Agent_Runtime SHALL record the input tokens, output tokens, model identifier, and cost of the call under R42.
13. WHEN validated output is produced, THE API SHALL store the output as a new Project_Requirements_Version in Draft status, marked AI-generated and Internal_Only.
14. FOR ALL analysis inputs containing embedded instructions, the set of tools available to the Agent_Runtime during the Job SHALL equal the configured tool set (prompt-injection invariant).
15. FOR ALL failed analysis Jobs, the number of stored Project_Requirements_Versions SHALL equal the number before the Job (no partial output property).

### Requirement 33: Clarification Workflow

**User Story:** As an Authorized_Reviewer, I want to send approved clarification questions to the client, so that missing information is collected on the same inquiry.

**ID:** NP-R33 | **Phase:** 3 | **Scope:** MVP | **Roles:** Authorized_Reviewer, Founder, Client | **V1:** 31.2, 31.5 | **Depends:** R14, R25, R30, R32 | **Assumes:** A-09, A-11 | **Entities:** Inquiry_Question, Project_Inquiry, Client_Workspace, Invitation, Audit_Log | **Failures:** unapproved question send attempt, answer to a Withdrawn question, answer by a non-owner, Guest inquiry without Invitation or approved email | **Validation:** question status values per Appendix A.2, answer maximum length | **Security:** tenant isolation, reviewer approval gate

#### Acceptance Criteria

1. WHEN an analysis lists missing information, THE Agent_Runtime SHALL generate draft Inquiry_Questions linked to the Project_Inquiry, and an Authorized_Reviewer SHALL be able to add draft Inquiry_Questions manually.
2. THE API SHALL send an Inquiry_Question to the Client only after an Authorized_Reviewer approves that Inquiry_Question.
3. IF a send is requested for an Inquiry_Question that has no recorded approval, THEN THE API SHALL reject the request with HTTP 409.
4. THE API SHALL allow Inquiry_Question statuses Open, Answered, and Withdrawn with the transitions defined in Appendix A.2.
5. WHEN a Client answers an Open Inquiry_Question in the Client_Workspace, THE API SHALL attach the answer to the same Project_Inquiry, set the status to Answered, and create no new Project_Inquiry.
6. IF a Client answers a Withdrawn Inquiry_Question or an Inquiry_Question of another Organization, THEN THE API SHALL reject the answer with HTTP 409 or HTTP 404 respectively.
7. WHEN an Authorized_Reviewer requests re-analysis after answers are recorded, THE API SHALL run R32 and store a new Project_Requirements_Version, keeping prior versions unchanged.
8. WHILE a Project_Inquiry was submitted by a Guest without an account, THE API SHALL deliver approved Inquiry_Questions only after the Invitation of R25 is accepted or through a Founder-approved email under A-09.
9. WHEN an Inquiry_Question is created, approved, sent, answered, or withdrawn, THE API SHALL write an Audit_Log entry.
10. FOR ALL Inquiry_Questions delivered to a Client, a recorded reviewer approval SHALL exist with a timestamp earlier than the delivery (approval-before-send property).
11. FOR ALL answer sequences on a Project, the count of Project_Inquiry records for the Project SHALL remain unchanged (same-inquiry invariant).

### Requirement 34: Technical Assessment Drafting and Classification

**User Story:** As an Engineer, I want an AI-drafted Technical_Assessment that I confirm, so that assessment is faster while remaining a human decision.

**ID:** NP-R34 | **Phase:** 3 | **Scope:** MVP | **Roles:** Engineer, Founder | **V1:** 32.3-32.4 | **Depends:** R29, R32, R35 | **Entities:** Technical_Assessment, Technical_Assessment_Version, Project, Audit_Log | **Failures:** label outside the six service groups, missing complexity justification, transition attempt without Confirmed assessment, confirmation by a non-Engineer | **Validation:** service group labels, complexity enumeration, non-empty justification | **Security:** Internal_Only, human confirmation gate

#### Acceptance Criteria

1. WHEN an Engineer requests an AI draft for a Project with a stored analysis, THE Agent_Runtime SHALL create a Technical_Assessment_Version with the structure defined in R29.
2. THE API SHALL accept discipline labels only from the six service groups and SHALL reject a draft containing any other label with a structured error.
3. THE Agent_Runtime SHALL assign complexity of exactly one of Low, Medium, High, or Very High with a non-empty justification.
4. THE API SHALL mark every AI-drafted Technical_Assessment_Version as AI-generated and unconfirmed.
5. WHEN an Engineer or the Founder reviews an AI-drafted version and confirms the version or saves an edited version, THE API SHALL mark that version Confirmed and record the confirming user and timestamp.
6. IF a user other than an Engineer or the Founder attempts to confirm a Technical_Assessment_Version, THEN THE API SHALL return HTTP 403.
7. IF a transition to Solution Designed is requested for a Project without a Confirmed Technical_Assessment_Version and a confirmed Solution_Architecture_Version under R35, THEN THE API SHALL reject the transition with HTTP 409 and a structured error.
8. WHEN a Technical_Assessment_Version is drafted or confirmed, THE API SHALL write an Audit_Log entry.
9. FOR ALL Projects in status Solution Designed, a Confirmed Technical_Assessment_Version and a confirmed Solution_Architecture_Version SHALL exist (transition guard invariant).

### Requirement 35: Solution Architecture and Diagram

**User Story:** As an Engineer, I want a validated, versioned architecture graph, so that the proposed solution is reviewable and renders correctly.

**ID:** NP-R35 | **Phase:** 3 | **Scope:** MVP | **Roles:** Engineer, Founder, Client (approved content only) | **V1:** 34 | **Depends:** R31, R34, R36 | **Entities:** Solution_Architecture, Solution_Architecture_Version, Proposal_Version, Audit_Log | **Failures:** edge to missing node, duplicate node identifier, node type outside allowed list, empty rationale, Client access to unapproved version | **Validation:** graph schema, allowed node and edge types listed in Appendix B | **Security:** Internal_Only until included in an approved Proposal_Version

#### Acceptance Criteria

1. THE Agent_Runtime SHALL produce each Solution_Architecture_Version as structured graph data with typed nodes and typed edges validated against the graph schema.
2. IF graph data contains an edge referencing a missing node, a duplicate node identifier, or a node type or edge type outside the allowed list in Appendix B, THEN THE API SHALL reject the graph with HTTP 422 naming each violation.
3. THE Solution_Architecture_Version SHALL record a technology stack with a non-empty rationale per item and technical decisions each with the decision, the alternatives considered, and the rationale.
4. WHEN a Solution_Architecture is changed, THE API SHALL store a new Solution_Architecture_Version and keep every prior version unchanged.
5. THE Web_App SHALL render the diagram with React Flow from validated graph data only.
6. THE Web_App SHALL provide a text alternative listing the nodes and connections of each diagram.
7. WHEN an export is requested, THE API SHALL return the Solution_Architecture_Version as JSON.
8. WHEN an Engineer or the Founder confirms a Solution_Architecture_Version, THE API SHALL mark the version confirmed and write an Audit_Log entry.
9. THE API SHALL classify every Solution_Architecture_Version as Internal_Only until the version is included in an Approved Proposal_Version.
10. IF a Client requests a Solution_Architecture_Version that is not included in an Approved Proposal_Version, THEN THE API SHALL return HTTP 404.
11. FOR ALL valid graphs, serializing to JSON and parsing the result SHALL produce an equal graph (round-trip property).
12. FOR ALL accepted graphs, every edge endpoint SHALL reference an existing node identifier and all node identifiers SHALL be unique (graph integrity invariant).

### Requirement 36: Proposal Drafting and Versioning

**User Story:** As the Founder, I want versioned proposals with immutable approved content, so that what the client receives is controlled and traceable.

**ID:** NP-R36 | **Phase:** 3 | **Scope:** MVP | **Roles:** Engineer, Authorized_Approver, Founder, Client (Sent versions only) | **V1:** 33.1, 33.4-33.6, 35.1-35.2, 35.4 | **Depends:** R30, R34, R35, R37 | **Entities:** Proposal, Proposal_Version, Solution_Architecture_Version, Audit_Log | **Failures:** edit of an Approved version, invalid status transition, architecture from an unconfirmed version, missing preliminary statement | **Validation:** Proposal_Version status per Appendix A.2, required sections | **Security:** Internal_Only until Sent, content hash on approval

#### Acceptance Criteria

1. THE API SHALL maintain one Proposal per Project and one or more Proposal_Versions per Proposal.
2. THE API SHALL allow Proposal_Version statuses Draft, In Review, Approved, Sent, Superseded, and Withdrawn with the transitions defined in Appendix A.2.
3. THE Proposal_Version SHALL contain overview, problem understanding, business objectives, functional and non-functional requirements, proposed solution, engineering disciplines, architecture, technology stack, infrastructure, integrations, security, roadmap, milestones, deliverables, risks and assumptions, complexity, preliminary timeline, and indicative cost.
4. THE API SHALL accept as the architecture section only a confirmed Solution_Architecture_Version under R35, and IF an unconfirmed version is referenced, THEN THE API SHALL reject the Proposal_Version with HTTP 422.
5. THE API SHALL populate the indicative cost section only through R37.
6. WHEN AI drafting is requested, THE Agent_Runtime SHALL create a new Proposal_Version in Draft status marked AI-generated.
7. THE Proposal_Version SHALL state that the content is preliminary and is not a contract, quotation, or commitment until an Agreement exists.
8. THE Agent_Runtime SHALL present no fabricated customers, benchmarks, or guarantees in a Proposal_Version.
9. WHEN a Proposal_Version is Approved, THE API SHALL compute and store a content hash and treat the content as immutable.
10. IF a change is requested to an Approved, Sent, Superseded, or Withdrawn Proposal_Version, THEN THE API SHALL reject the change and require a new Proposal_Version.
11. WHEN a Proposal_Version is exported, THE API SHALL return a downloadable document and write an Audit_Log entry.
12. WHEN a Proposal_Version status changes, THE API SHALL write an Audit_Log entry.
13. FOR ALL Approved Proposal_Versions, the recomputed content hash SHALL equal the stored content hash at every later time (immutability property).

### Requirement 37: Commercial Pricing and Cost Estimates

**User Story:** As the Founder, I want every price to be human-approved, so that NEUROPATH never sends invented pricing.

**ID:** NP-R37 | **Phase:** 3 | **Scope:** MVP | **Roles:** Authorized_Approver, Founder, Engineer | **V1:** 33.2-33.3 | **Depends:** R30, R36 | **Assumes:** A-06 | **Entities:** Price_Entry, Cost_Estimate, Proposal_Version, Audit_Log | **Failures:** price without approval, AI estimate without grounded inputs, combined cloud and service figure, non-approver price entry | **Validation:** currency and amount format, required assumptions list, separated cost categories | **Security:** Internal_Only AI estimates until approval, approval role check

#### Acceptance Criteria

1. THE API SHALL include a price in a Proposal_Version only when an Authorized_Approver entered or approved that price.
2. THE Platform SHALL treat the Founder as the default Authorized_Approver and SHALL allow the Founder to delegate approval under A-06.
3. IF a user who is not an Authorized_Approver enters or approves a price, THEN THE API SHALL return HTTP 403.
4. WHERE grounded inputs for an estimate exist, THE Agent_Runtime SHALL produce a Cost_Estimate that separates estimated cloud infrastructure cost from NEUROPATH service fees and states the assumptions behind each figure.
5. IF grounded inputs for an estimate are missing, THEN THE Agent_Runtime SHALL state that no estimate is provided and list the missing information.
6. THE API SHALL label every AI Cost_Estimate as indicative and classify the estimate as Internal_Only until an Authorized_Approver approves the estimate.
7. THE Agent_Runtime SHALL derive every figure from the stored grounded inputs, and IF a figure has no traceable input, THEN THE API SHALL reject the Cost_Estimate with a structured error.
8. WHEN a price is entered, edited, or approved, THE API SHALL write an Audit_Log entry with the actor, amount, currency, and Proposal_Version.
9. FOR ALL Proposal_Versions with status Sent, every price in the version SHALL have a recorded Authorized_Approver approval (approved pricing property).

### Requirement 38: Client Proposal Decision

**User Story:** As a Client, I want to accept, decline, or question a proposal I have received, so that my decision is recorded against the exact version I reviewed.

**ID:** NP-R38 | **Phase:** 3 | **Scope:** MVP | **Roles:** Client (Owner; Member per Appendix A.3), Founder | **V1:** 19.4 | **Depends:** R6, R17, R36, R40 | **Assumes:** A-19, A-20, A-35 | **Entities:** Proposal, Proposal_Version, Acceptance_Record, Communication, Project, Audit_Log | **Failures:** decision on a Superseded or Withdrawn version, second acceptance on one Proposal, Client access to a version not Sent, decision by a user without permission, off-platform acceptance without evidence reference | **Validation:** decision type in {Accept, Decline, Request Clarification}, optional decline reason length limit, required evidence reference for Founder-recorded acceptance | **Security:** own Organization only, Acceptance_Record append-only

#### Acceptance Criteria

1. THE API SHALL return to a Client only the Proposal_Versions with status Sent that belong to a Project of the Client's own Organization.
2. IF a Client requests a Proposal_Version with status Draft, In Review, or Approved, or a Proposal_Version of another Organization, THEN THE API SHALL return HTTP 404.
3. WHILE a Proposal_Version has status Sent, THE API SHALL allow a Client Owner, and a Client Member where Appendix A.3 grants the permission, to Accept, Decline, or Request Clarification on that Proposal_Version.
4. IF a Client user without the decision permission under Appendix A.3 submits a decision, THEN THE API SHALL return HTTP 403.
5. WHEN a Client accepts a Proposal_Version, THE API SHALL create an Acceptance_Record containing the user identifier, the Organization, the timestamp, the Proposal_Version identifier, and the content hash of the accepted Proposal_Version.
6. WHEN a Client declines a Proposal_Version, THE API SHALL record the decline with the user identifier, timestamp, and the optional reason supplied by the Client.
7. WHEN a Client requests clarification on a Proposal_Version, THE API SHALL create a Client_Visible Communication linked to the Proposal_Version and keep the Project in status Awaiting Client Decision.
8. WHEN the Founder records an acceptance received outside the platform, THE API SHALL create an Acceptance_Record that marks the source as off-platform and stores the Founder identity and the evidence reference (A-19).
9. IF the Founder records an off-platform acceptance without an evidence reference, THEN THE API SHALL reject the record with HTTP 422.
10. IF a decision is submitted on a Proposal_Version with status Superseded or Withdrawn, THEN THE API SHALL return HTTP 409 and record no decision.
11. IF an acceptance is submitted on a Proposal that already has an accepted Proposal_Version, THEN THE API SHALL return HTTP 409 and record no Acceptance_Record.
12. WHEN a Proposal_Version is accepted, THE API SHALL set every other Proposal_Version of the same Proposal with status Sent to Superseded.
13. THE API SHALL move a Project from Awaiting Client Decision to Accepted only when an Acceptance_Record exists for a Proposal_Version of that Project's Proposal.
14. THE API SHALL store Acceptance_Records as append-only under R6.9.
15. WHEN a decision is recorded, THE API SHALL write an Audit_Log entry and send a Notification to the Founder.
16. FOR ALL Acceptance_Records, the stored content hash SHALL equal the content hash stored when the Proposal_Version was Approved (accepted-equals-approved property).
17. FOR ALL Proposals, at most one Proposal_Version SHALL have an Acceptance_Record with decision accept (single acceptance invariant).

### Requirement 39: Agreement Records

**User Story:** As the Founder, I want an Agreement record for each accepted engagement, so that delivery starts only under a recorded contractual status.

**ID:** NP-R39 | **Phase:** 3 (records), 4 (activation guard) | **Scope:** MVP | **Roles:** Founder, Administrator, Client (read only) | **V1:** none (new) | **Depends:** R20, R38 | **Assumes:** A-13, A-14 | **Entities:** Agreement, Attachment, Project, Maintenance_Engagement, Proposal_Version, Acceptance_Record, Audit_Log | **Failures:** Agreement without an accepted Proposal_Version, end date before effective date, invalid status transition, In Progress transition without an Agreement In Effect, creation by an unauthorized role | **Validation:** Agreement status per Appendix A.2, date order, Attachment rules of R20 | **Security:** Internal_Only notes, Client sees status and approved document only

#### Acceptance Criteria

1. WHEN a Proposal_Version has an Acceptance_Record, THE API SHALL allow the Founder or an Administrator to create an Agreement for the Project or Maintenance_Engagement.
2. IF an Agreement is created for a Project without an accepted Proposal_Version, THEN THE API SHALL return HTTP 422.
3. IF a user other than the Founder or an Administrator creates or changes an Agreement, THEN THE API SHALL return HTTP 403.
4. THE Agreement SHALL record the parties, the Project or Maintenance_Engagement reference, the accepted Proposal_Version reference, the effective date, an optional end date, and a status.
5. IF an Agreement end date is earlier than the effective date, THEN THE API SHALL reject the Agreement with HTTP 422.
6. THE API SHALL allow Agreement statuses Draft, Pending Signature, In Effect, Expired, and Terminated with the transitions defined in Appendix A.2, and IF an undefined transition is requested, THEN THE API SHALL return HTTP 409.
7. THE API SHALL store the uploaded signed document as an Attachment under the rules of R20.
8. THE Platform SHALL provide no e-signature and no payment function for Agreements (A-13).
9. WHERE the Phase 4 activation guard is enabled, THE API SHALL move a Project from Accepted to In Progress only when the Project has an Agreement with status In Effect.
10. THE API SHALL classify Agreement notes as Internal_Only.
11. THE API SHALL return to a Client of the owning Organization only the Agreement status and the signed document that NEUROPATH marked as approved for the Client.
12. WHEN an Agreement is created, changed, or changes status, or a document is attached, THE API SHALL write an Audit_Log entry.
13. FOR ALL Projects with status In Progress after the activation guard is enabled, the Project SHALL have an Agreement with status In Effect at the time of the transition (activation guard property).

### Requirement 40: Proposal Sending and Export

**User Story:** As the Founder, I want to send and export only approved proposal versions, so that clients receive exactly the content NEUROPATH approved.

**ID:** NP-R40 | **Phase:** 3 | **Scope:** MVP | **Roles:** Authorized_Approver, Founder, Engineer, Project_Manager, Client (Sent versions only) | **V1:** 35.3-35.4 | **Depends:** R26, R27, R36, R37, R43 | **Assumes:** A-06, A-09 | **Entities:** Proposal_Version, Approval_Request, Notification, Project, Audit_Log | **Failures:** send of a version not Approved, send without an Approved Approval_Request, content hash mismatch, export of a Draft or In Review version, external email outside the R27 path | **Validation:** Proposal_Version status, Approval_Request hash match, preliminary statement present in export | **Security:** Sensitive_Action approval under R43, visibility limited to the owning Organization

#### Acceptance Criteria

1. THE API SHALL allow a Proposal_Version to be Sent only when the Proposal_Version has status Approved.
2. IF a send is requested for a Proposal_Version with a status other than Approved, THEN THE API SHALL return HTTP 409.
3. THE API SHALL execute a send only with an Approval_Request under R43 for the Sensitive_Actions "issuing commercial quotations" and "sharing confidential information" that an Authorized_Approver approved and whose content hash equals the Proposal_Version content hash.
4. IF a send is requested without a matching Approved Approval_Request, THEN THE API SHALL block the send, return HTTP 403, and write an Audit_Log entry.
5. WHEN a Proposal_Version is Sent, THE API SHALL set the status to Sent, make the Proposal_Version visible in the Client_Workspace of the owning Organization, and create a Notification for the Client.
6. THE Platform SHALL send external email about a Proposal_Version only through the Founder-approved path of R27.
7. WHEN a new Proposal_Version is Sent, THE API SHALL set the previously Sent Proposal_Version of the same Proposal to Superseded.
8. WHEN a Proposal_Version is Sent, THE API SHALL move the Project from Proposal Under Review to Proposal Sent and then to Awaiting Client Decision per Appendix A.1.
9. WHEN an export is requested for a Proposal_Version with status Approved or Sent, THE API SHALL return a PDF or document file that contains the statement that the content is preliminary and is not a contract.
10. IF an export is requested for a Proposal_Version with status Draft or In Review by a Client, THEN THE API SHALL return HTTP 404.
11. WHEN a Proposal_Version is Sent or exported, THE API SHALL write an Audit_Log entry with the actor, the Proposal_Version identifier, and the content hash.
12. FOR ALL Proposals, at most one Proposal_Version SHALL have status Sent at any time (single sent version invariant).
13. FOR ALL Sent Proposal_Versions, the exported file SHALL be generated from content whose hash equals the stored approved content hash (export fidelity property).

### Requirement 41: Consultation Requests and Engineering Service Request

**User Story:** As a prospective client, I want a structured way to describe an engineering challenge or discuss a Lab result, so that NEUROPATH can review my request without me choosing a technology first.

**ID:** NP-R41 | **Phase:** 3 | **Scope:** MVP | **Roles:** Guest, Client, Founder, Project_Manager | **V1:** 35.5-35.8, 35.10, 36 | **Depends:** R14, R16, R21, R31 | **Assumes:** A-01, A-02, A-11 | **Entities:** Engineering_Service_Request, Project_Inquiry, Project, Lead, Task, Audit_Log | **Failures:** validation failure, rate limit exceeded, missing consent, duplicate submission, save without sign-in, submission linked to another Organization | **Validation:** R14 inquiry validation, required problem and desired outcome, optional service hint | **Security:** R14 rate limit and consent, own Organization linkage only

#### Acceptance Criteria

1. THE Web_App SHALL provide the Engineering_Service_Request form with fields for the problem, the desired outcome, the systems and data involved, the constraints, and an optional service hint.
2. THE Web_App SHALL allow submission of an Engineering_Service_Request with the service hint left empty.
3. WHEN an Engineering_Service_Request is submitted, THE API SHALL create a Project_Inquiry through the R14 path with the same validation, rate limit, consent, and idempotence rules.
4. WHEN a signed-in Client submits an Engineering_Service_Request from the Client_Workspace, THE API SHALL link the Project_Inquiry to the Client's own Organization.
5. THE Web_App SHALL display a "Discuss This Solution With NEUROPATH" control on Solution_Architect Lab output that offers request consultation, submit inquiry, request detailed proposal, and save solution.
6. WHEN a user selects request consultation or submit inquiry, THE API SHALL create a Project_Inquiry, a Project with status Submitted, and a Lead under R14 and R16.
7. WHEN a user selects request detailed proposal, THE API SHALL create an Internal_Only Task or note for NEUROPATH review and SHALL create no Proposal_Version, price, or quotation.
8. IF a Guest selects save solution, THEN THE Web_App SHALL require sign-in before the API stores the solution.
9. WHEN a consultation, inquiry, detailed proposal request, or save action completes, THE API SHALL write an Audit_Log entry.
10. FOR ALL repeated submissions with the same idempotence key, THE API SHALL create exactly one Project_Inquiry and one Project (idempotence property).

### Requirement 42: Usage and Cost Tracking

**User Story:** As the Founder, I want usage and AI cost recorded per Organization with enforced limits, so that platform spend stays visible and bounded.

**ID:** NP-R42 | **Phase:** 3 | **Scope:** MVP (billing Out-of-scope) | **Roles:** Founder, Administrator | **V1:** 22, 38.6 (partial) | **Depends:** R6, R26, R28 | **Assumes:** A-05, A-08 | **Entities:** usage_records, Organization, Job, Notification, Audit_Log | **Failures:** per-Organization limit exceeded, global limit exceeded, missing cost data for a call | **Validation:** non-negative token counts and costs, configured limit values | **Security:** usage data Internal_Only

#### Acceptance Criteria

1. THE API SHALL record, per Organization, usage of uploads, storage, Jobs, and AI calls in usage_records.
2. WHEN an AI call completes, THE API SHALL record the token counts, the model identifier, and the estimated cost of the call.
3. WHEN a Job completes, THE API SHALL record the estimated cost of the Job.
4. THE Platform SHALL provide configurable per-Organization and global AI cost limits whose values the Founder sets in configuration (A-08).
5. IF an AI call would exceed a per-Organization or global AI cost limit, THEN THE API SHALL reject the call with a structured error that names the exceeded limit and send a Notification to the Founder.
6. THE API SHALL apply no behavior based on the reserved Organization `tier` attribute in MVP (A-05).
7. THE Platform SHALL provide no billing and no payment processing, and billing enablement SHALL require a future Founder decision.
8. THE Founder_Control_Center SHALL display usage and estimated cost per Organization and in total for a selected period.
9. FOR ALL periods and Organizations, the sum of the recorded per-call estimated costs SHALL equal the reported total estimated cost for that period (cost aggregation property).

### Requirement 43: Approval Requests for Commercial and Sensitive Actions

**User Story:** As the Founder, I want every commercial and Sensitive_Action to require an approval of the exact content, so that nothing leaves NEUROPATH without a named human decision.

**ID:** NP-R43 | **Phase:** 3 (reused in Phase 5) | **Scope:** MVP | **Roles:** Authorized_Approver, Founder, Engineer, Project_Manager, Internal_Agent (requester only) | **V1:** 40 | **Depends:** R6, R17, R26 | **Assumes:** A-06, A-08 | **Entities:** Approval_Request, Audit_Log, Notification | **Failures:** decision by a non-approver, decision by an Internal_Agent, execution with a hash mismatch, content change after approval, expired request, Sensitive_Action without an Approved request | **Validation:** Approval_Request status per Appendix A.2, required action type, target, content or parameters, rationale | **Security:** content hash binding, approver role check, append-only decision audit

#### Acceptance Criteria

1. THE Approval_Request SHALL record the action type, the target, the exact content or parameters with a content hash, the requester (user or Internal_Agent), the rationale, and a status.
2. THE API SHALL allow Approval_Request statuses Pending, Approved, Rejected, Expired, and Invalidated with the transitions defined in Appendix A.2.
3. THE API SHALL accept an Approval_Request decision only from an Authorized_Approver, with the Founder as the default and delegation under A-06.
4. IF an Internal_Agent or a user who is not an Authorized_Approver submits a decision, THEN THE API SHALL return HTTP 403 and write an Audit_Log entry.
5. THE API SHALL execute an approved action only with content whose hash equals the content hash of the Approved Approval_Request.
6. WHEN the content or parameters of an Approved Approval_Request change before execution, THE API SHALL set the Approval_Request to Invalidated.
7. WHEN a Pending Approval_Request reaches the configured expiry period (A-08), THE API SHALL set the Approval_Request to Expired and block the action.
8. IF a Sensitive_Action is attempted without an Approved Approval_Request with a matching content hash, THEN THE API SHALL block the action and write an Audit_Log entry.
9. WHEN an Approval_Request is decided, THE API SHALL write an Audit_Log entry with the approver, the time, the decision, and the reason.
10. THE Platform SHALL apply Approval_Requests to proposal sending, price approval, and external email from Phase 3, to Commercial_Record issue from Phase 4, and to staff-initiated deletion of customer data under R73.10.
11. THE Phase 5 OPS approval requirements SHALL reuse the Approval_Request mechanism defined in this requirement.
12. FOR ALL executed Sensitive_Actions, an Approval_Request with status Approved SHALL exist whose content hash equals the hash of the executed content (approved execution property).

## Phase 4: Project Delivery and Engineering Labs

Phase 4A covers delivery; Phase 4B covers Labs.

### Requirement 44: Project Activation and Team Assignment

**User Story:** As the Founder, I want a Project to start delivery only under an Agreement in effect and with a named team, so that engineering work is authorized and accountable.

**ID:** NP-R44 | **Phase:** 4 | **Scope:** MVP | **Roles:** Founder, Project_Manager, Administrator, Engineer, Client | **V1:** none (new) | **Depends:** R17, R18, R24, R26, R30, R39 | **Assumes:** A-07, A-21, A-22, A-35, A-37 | **Entities:** Project, Agreement, Project_Member, Audit_Log | **Failures:** activation without an Agreement In Effect, assignment of a non-staff user, write by an unassigned user | **Validation:** project role in {Project Lead, Engineer, Reviewer}, status transition per Appendix A.1 | **Security:** assignment-scoped write access, Client sees names and project roles only

#### Acceptance Criteria

1. THE API SHALL enable the Project statuses In Progress, Testing, Awaiting Client Acceptance, Delivered, and Completed in Phase 4 with the transitions defined in Appendix A.1; the status Accepted is enabled in Phase 3 (A-35).
2. WHEN a user requests the transition of a Project from Accepted to In Progress, THE API SHALL apply the transition only if the Project has an Agreement with status In Effect under the R39 guard.
3. IF a transition from Accepted to In Progress is requested without an Agreement In Effect, THEN THE API SHALL reject the request with a structured error and write an Audit_Log entry.
4. WHEN the Founder or a Project_Manager assigns an internal user to a Project, THE API SHALL create a Project_Member record with the user, the Project, and one project role of Project Lead, Engineer, or Reviewer.
5. THE API SHALL accept a write to a Project's milestones, Tasks, Communications, Deliverables, test records, and Defects only from a current Project_Member of that Project, the Founder, or an Administrator.
6. THE API SHALL limit Engineer access to Projects on which the Engineer is a current Project_Member, according to Appendix A.3.
7. WHEN a Client requests the team of a Project of the Client's own Organization, THE API SHALL return each Project_Member's display name and project role, and only those internal contact fields that the Founder has configured as Client_Visible.
8. WHEN a Project_Member is unassigned, THE API SHALL record the end of the assignment and retain the Project_Member history.
9. WHEN a Project_Member is assigned, has a role changed, or is unassigned, THE API SHALL write an Audit_Log entry with the actor, the user, the project role, and the time.
10. FOR ALL writes to delivery records of a Project, the writer SHALL be a current Project_Member of that Project, the Founder, or an Administrator at the time of the write (assigned-writer property).

### Requirement 45: Project Milestones

**User Story:** As a Project_Manager, I want dated milestones with computed progress and client acceptance, so that the Client sees honest delivery status.

**ID:** NP-R45 | **Phase:** 4 | **Scope:** MVP | **Roles:** Project_Manager, Founder, Project_Member, Client | **V1:** none (new) | **Depends:** R18, R24, R26, R27, R30, R44 | **Assumes:** A-19 | **Entities:** Project_Milestone, Task, Acceptance_Record, Notification, Audit_Log | **Failures:** due date before planned start, client decision on a milestone not in Ready for Review, rejection without a reason, manual progress input | **Validation:** required name and dates, milestone status per Appendix A.2 | **Security:** Client sees only Client_Visible milestones of the Client's own Organization

#### Acceptance Criteria

1. THE API SHALL store each Project_Milestone with a name, a description, a planned start date, a due date, a list of expected deliverables, a status, and a Client_Visible flag.
2. THE API SHALL allow Project_Milestone statuses Planned, In Progress, Ready for Review, Accepted, and Rejected with the transitions defined in Appendix A.2.
3. IF a Project_Milestone due date is earlier than the planned start date, THEN THE API SHALL reject the create or edit request with a field-level validation error.
4. WHEN an authorized member of the Client's Organization accepts a Client_Visible Project_Milestone in status Ready for Review, THE API SHALL set the status to Accepted and create an Acceptance_Record.
5. WHEN an authorized member of the Client's Organization rejects a Client_Visible Project_Milestone in status Ready for Review with a reason, THE API SHALL set the status to Rejected and create an Acceptance_Record that contains the reason.
6. IF a Client submits a decision on a Project_Milestone that is not in status Ready for Review, or a rejection without a reason, THEN THE API SHALL reject the request with a structured error.
7. THE API SHALL compute Project_Milestone progress as the number of Tasks with status Done divided by the number of Tasks with a status other than Cancelled, multiplied by 100, and as 0 when no such Task exists.
8. THE API SHALL accept no progress value supplied by a client of the API.
9. THE Client_Workspace SHALL display the upcoming Client_Visible Project_Milestones of the Client's Projects with name, due date, status, and computed progress.
10. WHEN a Project_Milestone is created, changes status, or receives a client decision, THE API SHALL write an Audit_Log entry and send Notifications under R27.
11. FOR ALL Project_Milestones, the computed progress SHALL lie in the range 0 to 100 inclusive and SHALL equal the progress formula of criterion 7 (progress computation property).

### Requirement 46: Tasks and Assignment

**User Story:** As a Project Lead, I want tasks assigned to project team members with tracked status, so that delivery work is visible and owned.

**ID:** NP-R46 | **Phase:** 4 | **Scope:** MVP | **Roles:** Project_Member, Project_Manager, Founder, Client (read only) | **V1:** none (new) | **Depends:** R18, R30, R44, R45 | **Entities:** Task, Project_Milestone, Project_Member, Audit_Log | **Failures:** assignee not a current Project_Member, Blocked without a reason, Client write attempt | **Validation:** required title, priority, Task status per Appendix A.2 | **Security:** Task Internal_Only by default, no Client write

#### Acceptance Criteria

1. THE API SHALL store each Task within one Project_Milestone with a title, a description, an assignee, a due date, a priority, a status, and a Client_Visible flag that defaults to Internal_Only.
2. THE API SHALL allow Task statuses To Do, In Progress, Blocked, Done, and Cancelled with the transitions defined in Appendix A.2.
3. IF a Task assignee is not a current Project_Member of the Task's Project at the time of assignment, THEN THE API SHALL reject the assignment with a structured error.
4. IF a Task is set to Blocked without a reason, THEN THE API SHALL reject the request with a field-level validation error.
5. WHEN a Task assignee changes, THE API SHALL write an Audit_Log entry with the previous assignee, the new assignee, the actor, and the time.
6. THE API SHALL derive a Task as overdue when the due date has passed and the status is neither Done nor Cancelled.
7. IF a Client submits a create, edit, or status change request for a Task, THEN THE API SHALL return HTTP 403.
8. WHEN a Client requests Tasks, THE API SHALL return only Client_Visible Tasks of Projects of the Client's own Organization.
9. FOR ALL Task assignments, the assignee SHALL be a current Project_Member of the Task's Project at the time of assignment (valid assignee property).

### Requirement 47: Project Communication and Client Updates

**User Story:** As a Client, I want one project thread and clear status updates, so that I can communicate with NEUROPATH without seeing internal discussion.

**ID:** NP-R47 | **Phase:** 4 | **Scope:** MVP | **Roles:** Project_Member, Project_Manager, Founder, Client | **V1:** none (new) | **Depends:** R18, R20, R26, R27, R30, R44 | **Entities:** Communication, Attachment, Notification, Audit_Log | **Failures:** Internal_Only message in a Client response, AI-drafted update published without approval, edit without history | **Validation:** required message body, explicit visibility on staff messages, sanitized text | **Security:** Internal_Only excluded from Client responses, server-side sanitization

#### Acceptance Criteria

1. THE API SHALL provide one Communication thread per Project.
2. WHEN a staff member posts a Communication, THE API SHALL record the visibility chosen by the staff member as Client_Visible or Internal_Only, with Internal_Only as the default.
3. WHEN a Client posts a Communication, THE API SHALL record the Communication as Client_Visible.
4. WHEN a Client requests a Project thread, THE API SHALL return only Client_Visible Communications of Projects of the Client's own Organization.
5. THE API SHALL accept Communication attachments only through the R20 attachment path.
6. THE API SHALL accept Client_Visible project updates with a status summary only from a staff member who is a current Project_Member, the Founder, or a Project_Manager.
7. WHERE a project update is drafted by an AI component in Phase 5, THE API SHALL set the update to Client_Visible only after a named human staff member approves the update.
8. WHEN a Communication is edited, THE API SHALL retain every previous version with the editor and the time.
9. THE API SHALL sanitize Communication text on the server before storage and before rendering.
10. WHEN a Client_Visible Communication or project update is posted, THE API SHALL send Notifications under R27 and write an Audit_Log entry.
11. FOR ALL API responses to a Client, the response SHALL contain no Internal_Only Communication (communication isolation property).

### Requirement 48: Deliverables

**User Story:** As a Client, I want versioned deliverables that NEUROPATH has approved for me, so that I receive only reviewed outputs and can accept or reject them.

**ID:** NP-R48 | **Phase:** 4 | **Scope:** MVP | **Roles:** Project_Member, Project_Manager, Founder, Client | **V1:** none (new) | **Depends:** R18, R20, R26, R30, R44, R45 | **Assumes:** A-19, A-23 | **Entities:** Deliverable, Deliverable version, Project_Milestone, Acceptance_Record, Audit_Log | **Failures:** Client access to a non-approved Deliverable, credentials in a handover reference, unscanned file, decision without a reason on rejection | **Validation:** Deliverable type, repository URL format, commit or tag reference | **Security:** malware scan and Presigned_URLs per R20, no credentials stored, download audit

#### Acceptance Criteria

1. THE API SHALL store each Deliverable with one type of Document, Report, Architecture Diagram, Source-Code Handover Reference, Deployment Documentation, or Other, and an optional link to one Project_Milestone.
2. WHEN a Deliverable is revised, THE API SHALL create a new Deliverable version and retain every previous version.
3. THE API SHALL store a Source-Code Handover Reference as a repository URL and a commit or tag reference.
4. IF a Source-Code Handover Reference contains embedded credentials or a token, THEN THE API SHALL reject the request with a field-level validation error.
5. THE API SHALL store Deliverable files only through the R20 path, including malware scanning and Presigned_URL access.
6. WHEN a staff member who holds the Deliverable approval permission under Appendix A.3 marks a Deliverable version Approved for Client, THE API SHALL make the version available to the Client's Organization.
7. WHEN a Client downloads a Deliverable version, THE API SHALL write an Audit_Log entry with the user, the Deliverable version, and the time.
8. WHEN an authorized member of the Client's Organization accepts or rejects an Approved for Client Deliverable version, THE API SHALL create an Acceptance_Record, and SHALL require a reason for a rejection.
9. FOR ALL Client download requests, THE API SHALL serve only Deliverable versions marked Approved for Client that belong to Projects of the Client's own Organization (deliverable access property).

### Requirement 49: Testing and Quality Assurance Records

**User Story:** As a Project Lead, I want test activities, acceptance criteria, and defects recorded, so that a Project reaches client acceptance only when quality gates are met.

**ID:** NP-R49 | **Phase:** 4 | **Scope:** MVP | **Roles:** Project_Member, Project_Manager, Founder, Client | **V1:** none (new) | **Depends:** R18, R20, R24, R30, R44, R45 | **Assumes:** A-18, A-21, A-24, A-37 | **Entities:** test activity, milestone acceptance criterion, Defect, Communication, Project, Audit_Log | **Failures:** transition to Awaiting Client Acceptance with an open Blocker or Critical Defect or an unmet criterion, Resolved or Won't Fix without a resolution note, Won't Fix on Blocker or Critical without Founder approval | **Validation:** test result in {Pass, Fail, Blocked}, criterion status in {Met, Not Met}, Defect severity per A-18, Defect status per Appendix A.2 | **Security:** test records Internal_Only unless marked Client_Visible

#### Acceptance Criteria

1. THE API SHALL store each test activity with a type, a scope, the executing user, a date, a result of Pass, Fail, or Blocked, and an optional evidence attachment through R20.
2. THE API SHALL store acceptance criteria per Project_Milestone, each with a status of Met or Not Met.
3. THE API SHALL store each Defect with a severity of Blocker, Critical, Major, or Minor (A-18) and a status of Open, In Progress, Resolved, Verified, Closed, or Won't Fix with the transitions defined in Appendix A.2.
4. IF a Defect is set to Resolved or Won't Fix without a resolution note, THEN THE API SHALL reject the request with a field-level validation error.
5. IF a Defect with severity Blocker or Critical is set to Won't Fix without Founder approval, THEN THE API SHALL reject the request and write an Audit_Log entry.
6. WHEN a Client submits feedback on testing, THE API SHALL record the feedback as a Client_Visible entry linked to the Project.
7. WHEN a Project Lead requests the transition of a Project from In Progress to Testing, THE API SHALL apply the transition.
8. WHEN a user requests the transition of a Project from Testing to Awaiting Client Acceptance, THE API SHALL apply the transition only if the Project has no Defect with severity Blocker or Critical in a status other than Verified, Closed, or Won't Fix, and every acceptance criterion of every Project_Milestone has status Met.
9. IF the guard of criterion 8 fails, THEN THE API SHALL reject the transition with a structured error that lists the blocking Defects and unmet criteria.
10. WHEN a test activity, criterion status, or Defect status changes, THE API SHALL write an Audit_Log entry.
11. FOR ALL Project transitions from Testing to Awaiting Client Acceptance, the guard of criterion 8 SHALL hold at the time of the transition (quality gate property).

### Requirement 50: Deployment Records and Handover

**User Story:** As a Project Lead, I want deployments and handover items recorded without secrets, so that the Client receives a traceable, complete handover.

**ID:** NP-R50 | **Phase:** 4 | **Scope:** MVP | **Roles:** Project_Member, Project_Manager, Founder, Client (read only) | **V1:** none (new) | **Depends:** R18, R20, R24, R30, R44, R48 | **Assumes:** A-16, A-34 | **Entities:** Deployment_Record, Handover_Checklist, Handover_Checklist item, Attachment, Project, Audit_Log | **Failures:** secret value or plaintext credential in a record, invalid Deployment_Record transition, transition to Delivered with an incomplete mandatory checklist item, item marked Done without evidence, Client write attempt | **Validation:** environment type in {dev, staging, production}, Deployment_Record status per Appendix A.2, required version or commit reference, configured secret detection patterns | **Security:** no secret storage, environment details Internal_Only by default

#### Acceptance Criteria

1. THE API SHALL store each Deployment_Record with an environment name, an environment type of dev, staging, or production, a version or commit reference, a status, notes, the actor, and the time.
2. THE API SHALL allow Deployment_Record statuses Planned, In Progress, Succeeded, Failed, and Rolled Back with the transitions defined in Appendix A.2, and IF an undefined transition is requested, THEN THE API SHALL return HTTP 409.
3. IF a Deployment_Record or Handover_Checklist field contains a value that matches a configured secret detection pattern, THEN THE API SHALL reject the request with a field-level validation error and store no part of the value.
4. THE API SHALL record a credential handover only as a reference to a secret store entry or to a named out-of-band handover process.
5. THE API SHALL classify Deployment_Records as Internal_Only unless a Project_Member, a Project_Manager, or the Founder marks a Deployment_Record as Client_Visible.
6. THE API SHALL store one Handover_Checklist per Project, and each Handover_Checklist item SHALL have a description, a mandatory flag, a status of Open or Done, and an optional evidence Attachment through R20.
7. IF a mandatory Handover_Checklist item is set to Done without an evidence Attachment or an evidence note, THEN THE API SHALL reject the request with a field-level validation error.
8. WHEN a user requests the transition of a Project from Awaiting Client Acceptance to Delivered, THE API SHALL apply the transition only if every mandatory Handover_Checklist item of the Project has status Done.
9. IF the guard of criterion 8 fails, THEN THE API SHALL reject the transition with a structured error that lists the open mandatory items.
10. IF a Client submits a create, edit, or status change request for a Deployment_Record or a Handover_Checklist item, THEN THE API SHALL return HTTP 403.
11. WHEN a Deployment_Record or a Handover_Checklist item is created or changes status, THE API SHALL write an Audit_Log entry.
12. FOR ALL Project transitions to Delivered, every mandatory Handover_Checklist item of the Project SHALL have status Done at the time of the transition (handover gate property).
13. FOR ALL stored Deployment_Records and Handover_Checklist items, no field SHALL match a configured secret detection pattern (no stored secrets property).

### Requirement 51: Final Delivery Acceptance

**User Story:** As a Client, I want to accept or reject the final delivery against a recorded delivery reference, so that a Project closes only on my recorded decision.

**ID:** NP-R51 | **Phase:** 4 | **Scope:** MVP | **Roles:** Client (Owner; Member per Appendix A.3), Founder, Project_Manager | **V1:** none (new) | **Depends:** R6, R17, R18, R24, R27, R30, R45, R48, R50 | **Assumes:** A-19, A-20, A-37 | **Entities:** Acceptance_Record, Project, Deliverable version, Handover_Checklist, Notification, Audit_Log | **Failures:** decision on a Project not in Delivered, rejection without a reason, decision by a user without permission, off-platform acceptance without an evidence reference, second final acceptance | **Validation:** decision type in {Accept, Reject}, required rejection reason, required evidence reference for Founder-recorded acceptance | **Security:** own Organization only, Acceptance_Record append-only

#### Acceptance Criteria

1. THE API SHALL record client decisions on milestone deliverables under R45 and R48, and SHALL record the client decision on final delivery under this requirement.
2. WHEN a Project enters Delivered, THE API SHALL compute a delivery reference that lists the Approved for Client Deliverable versions and the Handover_Checklist item statuses of the Project, together with the content hash of the delivery reference.
3. WHILE a Project has status Delivered, THE API SHALL allow a Client Owner, and a Client Member where Appendix A.3 grants the permission, of the owning Organization to accept or reject the final delivery.
4. IF a Client user without the decision permission under Appendix A.3, or a user of another Organization, submits a final delivery decision, THEN THE API SHALL return HTTP 403 or HTTP 404 respectively and record no decision.
5. WHEN a Client accepts the final delivery, THE API SHALL create an Acceptance_Record containing the user identifier, the Organization, the timestamp, the delivery reference, and the content hash of the delivery reference.
6. WHEN a final acceptance is recorded, THE API SHALL move the Project from Delivered to Completed per Appendix A.1.
7. WHEN a Client rejects the final delivery with a reason, THE API SHALL create an Acceptance_Record that contains the reason and move the Project to the status that Appendix A.1 defines for a rejected delivery, In Progress or Testing.
8. IF a Client rejects the final delivery without a reason, THEN THE API SHALL reject the request with a field-level validation error.
9. WHEN the Founder records a final acceptance received outside the platform, THE API SHALL create an Acceptance_Record that marks the source as off-platform and stores the Founder identity and the evidence reference (A-19).
10. IF the Founder records an off-platform final acceptance without an evidence reference, THEN THE API SHALL reject the record with HTTP 422.
11. IF a final delivery decision is submitted for a Project with a status other than Delivered, THEN THE API SHALL return HTTP 409 and record no Acceptance_Record.
12. WHEN a final delivery decision is recorded, THE API SHALL write an Audit_Log entry and send Notifications under R27 to the Founder and the Project Lead.
13. FOR ALL Projects with status Completed, an Acceptance_Record of type final acceptance SHALL exist for that Project (completion property).
14. FOR ALL final acceptance Acceptance_Records, the stored content hash SHALL equal the content hash of the delivery reference computed when the Project entered Delivered (accepted-equals-delivered property).

### Requirement 52: Support Requests

**User Story:** As a Client, I want to raise support requests on my active or completed projects, so that bugs, questions, improvements, and incidents are recorded and tracked.

**ID:** NP-R52 | **Phase:** 4 | **Scope:** MVP | **Roles:** Client, Project_Member, Project_Manager, Founder | **V1:** none (new) | **Depends:** R18, R20, R26, R27, R30, R44 | **Assumes:** A-12 | **Entities:** Support_Request, support_comments, Attachment, Project, Maintenance_Engagement, Notification, Audit_Log | **Failures:** request on another Organization's Project, request on a Project not in an eligible status, invalid status transition, Internal_Only comment in a Client response | **Validation:** type in {bug, question, improvement, incident}, required title and description, Support_Request status per Appendix A.2, explicit visibility on staff comments | **Security:** own Organization only, Internal_Only comments excluded from Client responses, server-side sanitization

#### Acceptance Criteria

1. WHEN a Client submits a Support_Request with a type of bug, question, improvement, or incident, a title, and a description for a Project of the Client's own Organization with status In Progress, Testing, Awaiting Client Acceptance, Delivered, or Completed, THE API SHALL create the Support_Request with status New.
2. IF a Client submits a Support_Request for a Project of another Organization, THEN THE API SHALL return HTTP 404 and create no Support_Request.
3. IF a Client submits a Support_Request for a Project whose status is not listed in criterion 1, THEN THE API SHALL reject the request with a structured error.
4. THE API SHALL allow Support_Request statuses New, Triaged, In Progress, Awaiting Client, Resolved, and Closed with the transitions defined in Appendix A.2, and IF an undefined transition is requested, THEN THE API SHALL return HTTP 409.
5. WHEN a staff member posts a support comment, THE API SHALL record the visibility chosen by the staff member as Client_Visible or Internal_Only, with Internal_Only as the default.
6. WHEN a Client posts a support comment, THE API SHALL record the support comment as Client_Visible.
7. THE API SHALL accept Support_Request attachments only through the R20 attachment path and SHALL sanitize Support_Request and support comment text on the server.
8. THE Platform SHALL display no response-time or resolution-time commitment for a Support_Request (A-12).
9. THE Client_Workspace SHALL list the Support_Request history of each Project of the Client's own Organization with type, title, status, and the time of the last status change.
10. WHEN a Support_Request is created, changes status, or receives a Client_Visible comment, THE API SHALL write an Audit_Log entry and send Notifications under R27.
11. FOR ALL Support_Request creation requests by a Client, the API SHALL create a Support_Request only when the target Project belongs to the Client's own Organization (support tenancy property).
12. FOR ALL API responses to a Client, the response SHALL contain no Internal_Only support comment (support comment isolation property).

### Requirement 53: Maintenance Engagements

**User Story:** As the Founder, I want ongoing maintenance recorded as its own engagement, so that post-delivery work has its own scope and Agreement.

**ID:** NP-R53 | **Phase:** 4 | **Scope:** MVP | **Roles:** Founder, Administrator, Project_Manager, Project_Member, Client (read only) | **V1:** none (new) | **Depends:** R18, R30, R39, R44, R46, R52 | **Assumes:** A-14 | **Entities:** Maintenance_Engagement, Agreement, Commercial_Record, Task, Support_Request, Project, Audit_Log | **Failures:** start without an Agreement In Effect, originating Project of another Organization, suspension without a reason, invalid status transition, Client write attempt | **Validation:** required scope description, Maintenance_Engagement status per Appendix A.2 | **Security:** own Organization only, Client read access limited to status and Client_Visible scope

#### Acceptance Criteria

1. WHEN the Founder, an Administrator, or a Project_Manager creates a Maintenance_Engagement, THE API SHALL store the Maintenance_Engagement linked to exactly one originating Project of the same Organization, with a scope description and status Proposed.
2. THE API SHALL allow Maintenance_Engagement statuses Proposed, Active, Suspended, and Ended with the transitions defined in Appendix A.2, and IF an undefined transition is requested, THEN THE API SHALL return HTTP 409.
3. WHEN a user requests the transition of a Maintenance_Engagement from Proposed to Active, THE API SHALL apply the transition only if the Maintenance_Engagement has an Agreement under R39 with status In Effect.
4. IF a transition to Active is requested without an Agreement In Effect, THEN THE API SHALL reject the request with a structured error and write an Audit_Log entry.
5. IF a Maintenance_Engagement is set to Suspended or Ended without a reason, THEN THE API SHALL reject the request with a field-level validation error.
6. THE API SHALL allow optional Commercial_Records to reference a Maintenance_Engagement.
7. THE API SHALL store maintenance tasks linked to the Maintenance_Engagement with the fields, statuses, and assignee rule of R46.
8. WHEN a Project_Member or a Project_Manager links a Support_Request to a Maintenance_Engagement, THE API SHALL accept the link only if the Support_Request belongs to the originating Project of that Maintenance_Engagement.
9. WHEN a Client requests a Maintenance_Engagement of the Client's own Organization, THE API SHALL return the status, the Client_Visible scope, and the Agreement status.
10. WHEN a Maintenance_Engagement is created or changes status, THE API SHALL write an Audit_Log entry.
11. FOR ALL Maintenance_Engagement transitions to Active, the Maintenance_Engagement SHALL have an Agreement with status In Effect at the time of the transition (maintenance activation guard property).

### Requirement 54: Change Requests and Scope Baselines

**User Story:** As the Founder, I want scope changes on an active project handled through approved change requests against a versioned baseline, so that the agreed scope is never edited silently.

**ID:** NP-R54 | **Phase:** 4 | **Scope:** MVP | **Roles:** Client, Project_Member, Project_Manager, Founder, Authorized_Approver | **V1:** none (new) | **Depends:** R6, R18, R27, R30, R36, R38, R43, R44, R45 | **Assumes:** A-06, A-19, A-25 | **Entities:** Change_Request, Scope_Baseline, Proposal_Version, Project_Milestone, Deliverable, Approval_Request, Acceptance_Record, Audit_Log | **Failures:** change request on a Project outside an Active_Engagement status, impact entered by an Internal_Agent, cost or timeline change without an Approved Approval_Request, approval without a client Acceptance_Record, edit of an existing Scope_Baseline, invalid status transition | **Validation:** required description and reason, impact fields for scope, timeline, and cost, Change_Request status per Appendix A.2 | **Security:** content hash binding through R43, Scope_Baseline append-only, own Organization only

#### Acceptance Criteria

1. WHEN a Project moves from Accepted to In Progress, THE API SHALL create Scope_Baseline version 1 that copies the scope, Project_Milestones, and Deliverables of the accepted Proposal_Version.
2. THE API SHALL store Scope_Baselines as append-only under R6.9.
3. WHILE a Project has an Active_Engagement status, THE API SHALL allow a Client of the owning Organization or a Project_Member to submit a Change_Request with a description, a reason, and the scope, timeline, and cost impact, with status Submitted.
4. IF an Internal_Agent submits or edits the impact fields of a Change_Request, THEN THE API SHALL return HTTP 403 and write an Audit_Log entry.
5. THE API SHALL allow Change_Request statuses Submitted, Under Review, Approved, Rejected, Withdrawn, and Implemented with the transitions defined in Appendix A.2, and IF an undefined transition is requested, THEN THE API SHALL return HTTP 409.
6. WHEN a Change_Request with a timeline or cost impact is approved, THE API SHALL require an Approval_Request under R43 that an Authorized_Approver approved and whose content hash equals the Change_Request content hash.
7. WHEN a Change_Request without a timeline or cost impact is approved, THE API SHALL require the decision of the Founder or a Project_Manager (A-25).
8. THE API SHALL set a Change_Request to Approved only when an Acceptance_Record from an authorized member of the Client's Organization, or a Founder-recorded off-platform acceptance with an evidence reference, exists for the Change_Request content hash.
9. WHEN an Approved Change_Request is implemented, THE API SHALL create a new Scope_Baseline version that references the Change_Request, set the Change_Request to Implemented, and leave every earlier Scope_Baseline version unchanged.
10. IF an edit or deletion of an existing Scope_Baseline version is requested, THEN THE API SHALL return HTTP 405 or HTTP 409 and change no Scope_Baseline.
11. WHEN a Change_Request is created or changes status, THE API SHALL write an Audit_Log entry and send Notifications under R27 to the Founder, the Project Lead, and the Client.
12. FOR ALL sequences of API operations, every Scope_Baseline version that existed before the sequence SHALL exist unchanged after the sequence (baseline immutability property).
13. FOR ALL Scope_Baseline versions with a version number greater than 1, the version SHALL reference exactly one Change_Request that was Approved before the version was created (baseline provenance property).

### Requirement 55: Labs Module Framework

**User Story:** As the Founder, I want Labs to be optional, independently switchable modules, so that new Labs can be added or disabled without affecting inquiries or project delivery.

**ID:** NP-R55 | **Phase:** 4 | **Scope:** MVP (framework); Data Engineering Playground MVP-conditional | **Roles:** Founder, Administrator, Guest, Client | **V1:** none (new) | **Depends:** R14, R17, R30, R41, R77, R78 | **Assumes:** A-04, A-26 | **Entities:** Lab registration, Feature_Flag, Audit_Log | **Failures:** request to a disabled Lab route, Lab status change by a non-Founder, core module dependency on a Lab module, Lab registration without owned routes | **Validation:** unique Lab id, Lab status in {disabled, internal, client beta, available}, owned route prefixes without overlap | **Security:** route access enforced by Lab status and R17 roles, Feature_Flag changes audited

#### Acceptance Criteria

1. THE Platform SHALL register each Lab with a unique id, a name, a status of disabled, internal, client beta, or available, a controlling Feature_Flag, and the list of routes that the Lab owns.
2. THE Platform SHALL register the Data Engineering Playground, the AI Solution Architect, and the Engineering Service Request as Labs.
3. IF a request targets a route owned by a Lab with status disabled, THEN THE API and THE Web_App SHALL return HTTP 404.
4. WHILE a Lab has status disabled, THE Web_App SHALL display no navigation entry for that Lab.
5. WHILE a Lab has status internal, THE API SHALL return HTTP 404 to Guests and Clients for routes owned by that Lab.
6. WHILE a Lab has status client beta, THE API SHALL serve routes owned by that Lab to NEUROPATH staff and to Clients of Organizations that the Lab's Feature_Flag configuration enables (A-26), and SHALL return HTTP 404 to every other principal.
7. THE API SHALL accept a Lab status change only from the Founder or an Administrator delegated by the Founder, and WHEN a Lab status changes, THE API SHALL write an Audit_Log entry.
8. THE Web_App and THE API SHALL accept a Project_Inquiry through R14 and SHALL run every Project flow of R24 and R44 to R54 without requiring the use of any Lab.
9. THE continuous integration pipeline SHALL fail when a core project, inquiry, or authentication module imports a Lab module.
10. THE Platform SHALL add a new Lab by registering a new module, with no change to the core project, inquiry, or authentication modules.
11. THE Data Engineering Playground (R56 to R63) SHALL remain disabled in production until the Founder records a go decision at the Phase 4 gate under R78 (A-04).
12. FOR ALL configurations in which every Lab has status disabled, the MVP project flow tests of R77 SHALL pass (Lab independence property).

Phase 4B: Data Engineering Playground (MVP-conditional, A-04).

### Requirement 56: Dataset Upload

**User Story:** As a Client, I want to upload a data file safely to the optional Data Engineering Playground, so that I can analyze and prepare the data.

**ID:** NP-R56 | **Phase:** 4 | **Scope:** MVP-conditional (A-04) | **Roles:** Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 23 | **Depends:** R17, R18, R19, R20, R30, R55, R64 | **Assumes:** A-04, A-08, A-16 | **Entities:** Dataset, Organization, Project, Job, Audit_Log | **Failures:** Guest upload attempt, disallowed extension, content type that does not match the extension, size above the limit, malformed structure, row count above the limit, malware detected, scanner unavailable, missing object on complete-upload, Project link to another Organization, request while the Lab is disabled | **Validation:** extension in {csv, xlsx, json}, content type inspected from file content, configured size, row, and time limits per role, permission confirmation recorded | **Security:** signed-in users only, Presigned_URL valid for at most 10 minutes and scoped to one key under the Organization prefix, malware scan before processing, isolated processing

#### Acceptance Criteria

1. THE Web_App SHALL provide the Data Engineering Playground at `/labs/data-playground` as a route owned by the Data Engineering Playground Lab registration of R55.
2. THE Web_App and THE API SHALL accept a Project_Inquiry and run every Project flow without requiring the creation of a Dataset.
3. IF a Guest requests an upload URL, a complete-upload, or any other dataset endpoint, THEN THE API SHALL return HTTP 401 and store no object.
4. THE Data_Engine SHALL accept CSV, XLSX, and JSON files, and THE Data_Engine SHALL isolate format handling behind an interface so that Parquet and JSONL can be added in a future phase.
5. THE Platform SHALL read the maximum file size, the maximum row count, and the maximum processing time from configuration per role, with values that the Founder sets (A-08).
6. THE Web_App SHALL provide drag-and-drop upload and file-picker upload, with client-side validation of extension and size before the upload begins.
7. WHILE an upload is in progress, THE Web_App SHALL display a progress indicator and a control that cancels the upload.
8. WHEN a user starts an upload, THE Web_App SHALL require the user to confirm permission to process the file, and THE API SHALL record the confirmation with the user identifier and the time.
9. WHEN an upload URL is requested, THE API SHALL issue a Presigned_URL through the R20 storage path that is valid for no more than 10 minutes and scoped to one object key under the prefix of the requesting user's Organization.
10. WHEN an upload finishes, THE API SHALL accept a complete-upload request and create a Dataset record only after verifying that the object exists.
11. WHERE a user links a Dataset to a Project, THE API SHALL accept the link only if the Project belongs to the same Organization as the Dataset.
12. IF a user links a Dataset to a Project of another Organization, THEN THE API SHALL return HTTP 404 and store no link.
13. THE API SHALL validate on the server both the file extension and the content type inspected from the file content.
14. IF a file has a disallowed extension, a content type that does not match the extension, a size above the configured limit, a malformed structure, or a row count above the configured limit, THEN THE API SHALL reject the file, delete the stored object, and return a structured error that names the reason.
15. THE API SHALL scan each uploaded file for malware through the R20 scanning path before processing, and IF the scan detects malware or the scanner is unavailable, THEN THE API SHALL quarantine the file and SHALL NOT process the file.
16. THE API SHALL enforce the size, row, and time limits for each file on the server, independently of client-side checks.
17. THE API SHALL provide the dataset endpoints upload-url, complete-upload, list, get, delete, and profile under `/api/v1/datasets`.
18. THE ENGINE SHALL process uploaded files through the job framework of R64 in an isolated environment with CPU, memory, and time limits and with no access to data of other Organizations.
19. WHEN a Dataset is created, rejected, or quarantined, THE API SHALL write an Audit_Log entry.
20. FOR ALL Dataset records, the stored object SHALL have passed the extension check, the content type check, the size and row limits, and the malware scan before the Dataset became available for processing (upload gate property).

### Requirement 57: Data Profiling

**User Story:** As a Client, I want accurate profiling of my data, so that I understand the data quality before changing the data.

**ID:** NP-R57 | **Phase:** 4 | **Scope:** MVP-conditional (A-04) | **Roles:** Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 24 | **Depends:** R18, R19, R56, R64 | **Assumes:** A-04, A-08 | **Entities:** Dataset, Profile, dataset_profiles, Job | **Failures:** unparseable file, profiling of another Organization's Dataset, time or resource limit exceeded | **Validation:** Job status in {queued, running, completed, failed} | **Security:** own Organization only, no partial Profile stored on failure

#### Acceptance Criteria

1. WHEN profiling is requested for a Dataset, THE API SHALL create a Job through R64 and return HTTP 202 with the job ID under the R19 asynchronous job pattern.
2. THE Data_Engine SHALL compute, from the actual file contents, the row count, the column count, the inferred type per column, the missing-value count and percentage per column, and the duplicate-row count.
3. THE Data_Engine SHALL compute for numeric columns the mean, median, standard deviation, minimum, and maximum, and for categorical columns the unique-value count and the value frequencies.
4. THE Data_Engine SHALL detect invalid values, outliers, inconsistent formats, wrong types, and leakage indicators, and SHALL report for each finding the column, the count of affected rows, and the detection rule used.
5. WHEN profiling completes, THE Data_Engine SHALL store the resulting Profile in the dataset_profiles table.
6. THE Web_App SHALL display the Profile at `/dashboard/datasets/[datasetId]` in an interactive dashboard with sortable column summaries, distribution charts, and a list of quality issues.
7. IF the file cannot be parsed, THEN THE Data_Engine SHALL mark the profiling Job failed with an error message and store no partial Profile.
8. THE Web_App SHALL display the profiling status as queued, running, completed, or failed and announce each status change to screen readers.
9. IF a user requests profiling of a Dataset of another Organization, THEN THE API SHALL return HTTP 404 and create no Job.
10. FOR ALL Datasets, the Profile row count SHALL equal the number of data rows in the file (row-count invariant).
11. FOR ALL Datasets, profiling the same file twice SHALL produce identical Profiles (idempotence property).

### Requirement 58: AI Recommendations for Data Operations

**User Story:** As a Client, I want suggested cleaning steps, so that I can improve my data without deep data engineering expertise.

**ID:** NP-R58 | **Phase:** 4 | **Scope:** MVP-conditional (A-04) | **Roles:** Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 25 | **Depends:** R18, R19, R42, R57, R59, R64 | **Assumes:** A-04, A-08, A-11 | **Entities:** Recommendation, Profile, Operation, AI_Usage_Record, Job | **Failures:** schema validation failure after 2 retries, Operation outside the allowlist, invalid parameters, AI cost limit exceeded, instruction embedded in Dataset values, request before a completed Profile | **Validation:** Pydantic schema for Recommendation output, allowlist of R59, per-Operation parameter schema, configured sample size bound | **Security:** bounded sample only, Dataset contents treated as untrusted input, no execution of generated code, data disclosure shown before the first request

#### Acceptance Criteria

1. WHEN a Profile is complete and the user requests Recommendations, THE Agent_Runtime SHALL return a list of Recommendations as structured output validated against a Pydantic schema.
2. THE Agent_Runtime SHALL send to the model only the Profile statistics and a bounded sample of values whose size the Founder sets in configuration (A-08), and SHALL exclude every raw row beyond that sample.
3. WHEN a user requests Recommendations for the first time, THE Web_App SHALL disclose which data is sent to the AI provider before the request is sent.
4. IF the model output fails schema validation, THEN THE Agent_Runtime SHALL retry at most 2 times and then return a structured error with no Recommendation.
5. THE API SHALL accept a Recommendation only if the Recommendation names an Operation in the R59 allowlist and the parameters pass the parameter schema of that Operation.
6. IF a Recommendation names an Operation outside the allowlist or has invalid parameters, THEN THE API SHALL discard the Recommendation and record the discard reason.
7. THE Platform SHALL NOT execute any code generated by a model.
8. THE Web_App SHALL display for each Recommendation the Operation, the parameters, the affected columns, and the reason, and SHALL label the Recommendation as AI-generated.
9. THE Agent_Runtime SHALL treat Dataset contents as untrusted input, and IF Dataset values contain an embedded instruction, THEN THE Agent_Runtime SHALL keep the instruction from altering Agent_Runtime behavior, the allowlist, or the output schema.
10. THE API SHALL add a Recommendation to a Pipeline only when a user approves the Recommendation under R59.
11. WHEN the Agent_Runtime makes an AI call for Recommendations, THE API SHALL record the usage and estimated cost under R42 and apply the per-Organization and global AI cost limits of R42.
12. FOR ALL accepted Recommendations, the named Operation SHALL be in the R59 allowlist and the parameters SHALL pass the parameter schema of that Operation (allowlist property).
13. FOR ALL Recommendation requests, the payload sent to the model SHALL contain no more raw values than the configured sample bound (bounded disclosure property).

### Requirement 59: Pipeline Builder

**User Story:** As a Client, I want a reviewable Pipeline, so that I control exactly what happens to my data.

**ID:** NP-R59 | **Phase:** 4 | **Scope:** MVP-conditional (A-04) | **Roles:** Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 26 | **Depends:** R18, R19, R30, R56, R57 | **Assumes:** A-04, A-08 | **Entities:** Pipeline, Pipeline version, Operation, Dataset, Audit_Log | **Failures:** Operation outside the allowlist, invalid parameters, reference to a missing column, incompatible Operation order, execution request without approval of the current version, destructive Operation without confirmation | **Validation:** allowlist, per-Operation parameter schema, column existence, Operation order compatibility | **Security:** own Organization only, original uploaded file read-only

#### Acceptance Criteria

1. THE API SHALL provide the pipeline endpoints create, list, get, patch, validate, and execute under `/api/v1/pipelines`, and an executions listing at `/api/v1/pipelines/{id}/executions`.
2. THE Web_App SHALL provide the pages `/dashboard/pipelines` and `/dashboard/pipelines/[pipelineId]` as routes owned by the Data Engineering Playground Lab registration of R55.
3. THE Web_App SHALL display a Pipeline as a visual graph of Operations that the user can inspect.
4. THE Web_App SHALL let the user enable or disable each Operation, edit the parameters of each Operation, and preview the effect on a bounded sample before execution.
5. THE Data_Engine SHALL compute each preview from the actual sample using the same Operation code that execution uses.
6. WHEN a user changes a Pipeline, THE API SHALL store a new Pipeline version and keep every prior Pipeline version unchanged.
7. WHEN validation is requested, THE API SHALL check that each Operation is in the allowlist, the parameters are valid, the referenced columns exist, and the Operation order is compatible, and SHALL return each problem with the Operation identifier.
8. THE API SHALL require a recorded user approval of the current Pipeline version before the Pipeline can be executed.
9. WHEN a Pipeline is changed after approval, THE API SHALL clear the approval.
10. IF an execution is requested for a Pipeline version without a recorded approval, THEN THE API SHALL return HTTP 409 and create no Job.
11. WHERE an Operation is destructive, THE Web_App SHALL require an explicit confirmation that names the Operation and the affected columns or row count before approval.
12. THE Data_Engine SHALL implement an allowlist that contains at least remove duplicates, drop columns, drop rows by condition, fill missing values, convert types, standardize formats, trim and normalize text, clip or remove outliers, rename columns, and filter rows.
13. THE Data_Engine SHALL leave the original uploaded file unchanged.
14. WHEN a Pipeline version is approved or an approval is cleared, THE API SHALL write an Audit_Log entry.
15. FOR ALL Pipeline previews and executions with identical Operations, parameters, and input rows, the preview result SHALL equal the execution result on those rows (preview fidelity property).
16. FOR ALL Pipeline executions, the content hash of the original uploaded file after the execution SHALL equal the content hash before the execution (original file immutability property).

### Requirement 60: Pipeline Execution and Logs

**User Story:** As a Client, I want a transparent execution record, so that I can trust and audit the results.

**ID:** NP-R60 | **Phase:** 4 | **Scope:** MVP-conditional (A-04) | **Roles:** Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 27 | **Depends:** R18, R19, R27, R30, R59, R64 | **Assumes:** A-04, A-08 | **Entities:** Execution, Pipeline version, Operation, Job, Notification, Audit_Log | **Failures:** Operation failure, time or resource limit exceeded, duplicate queue delivery, transient infrastructure failure after 3 retries, execution of an unapproved version | **Validation:** approved current Pipeline version, configured time and resource limits | **Security:** no raw data values or secrets in logs, isolated execution, own Organization only

#### Acceptance Criteria

1. WHEN execution of an approved Pipeline version is requested, THE API SHALL create a Job through R64 and return HTTP 202 with the job ID under the R19 asynchronous job pattern.
2. THE Data_Engine SHALL execute Operations in the Pipeline order using Pandas, Polars, PyArrow, and scikit-learn implementations that are deterministic for identical inputs and parameters.
3. THE Data_Engine SHALL record for each Operation the status, start time, end time, records processed, records affected, warnings, errors, and log lines.
4. IF an Operation fails, THEN THE Data_Engine SHALL stop the Execution, mark the Execution failed, preserve the logs, and mark no output as completed.
5. WHEN an Execution fails, THE Platform SHALL send a Notification under R27 to the user who requested the Execution.
6. THE Web_App SHALL display the live Execution status and let the user view the Execution logs.
7. THE Platform SHALL record in logs only counts, column names, and Operation names, and SHALL exclude raw data values and secrets from logs.
8. IF an Execution exceeds the configured time or resource limits, THEN THE ENGINE SHALL terminate the Execution and mark the Execution failed with the reason.
9. WHEN the queue delivers the same Job more than once, THE ENGINE SHALL process the Job once and ignore the duplicate deliveries.
10. IF a transient infrastructure failure occurs, THEN THE ENGINE SHALL retry the Job up to 3 times with backoff before marking the Job failed.
11. WHEN an Execution starts, completes, or fails, THE API SHALL write an Audit_Log entry.
12. FOR ALL pairs of Executions with identical input files, Pipeline versions, and parameters, the outputs SHALL be identical (determinism property).
13. FOR ALL Executions with a failed Operation, no Operation after the failed Operation SHALL have a start time and no output SHALL be marked completed (stop-on-failure property).
14. FOR ALL Execution log lines, no log line SHALL contain a cell value of the input Dataset (log redaction property).
15. FOR ALL Jobs delivered n times with n greater than or equal to 1, the ENGINE SHALL produce exactly one Execution result (idempotent delivery property).

### Requirement 61: Outputs, Downloads, and Completion Dashboard

**User Story:** As a Client, I want the processed data and a report, so that I can use and share my results.

**ID:** NP-R61 | **Phase:** 4 | **Scope:** MVP-conditional (A-04) | **Roles:** Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 28 | **Depends:** R18, R20, R55, R60, R62 | **Assumes:** A-04, A-08 | **Entities:** Execution, output dataset, quality report, transformation summary, pipeline configuration file, metadata, Dataset | **Failures:** download request by a user of another Organization, download of an output of a failed Execution, metric without a stored record | **Validation:** download format in {CSV, Parquet, JSON, XLSX} | **Security:** Presigned_URL valid for at most 10 minutes, issued only to members of the owning Organization and authorized staff

#### Acceptance Criteria

1. WHEN an Execution completes, THE Data_Engine SHALL produce a cleaned dataset, a quality report, a transformation summary, a pipeline configuration file, and metadata.
2. WHERE ML preparation is configured under R62, THE Data_Engine SHALL also produce a prepared-for-modeling dataset.
3. THE API SHALL provide downloads of output datasets as CSV, Parquet, JSON, and XLSX through Presigned_URLs issued through the R20 storage path, valid for no more than 10 minutes, and issued only to members of the owning Organization and to authorized NEUROPATH staff.
4. IF a user of another Organization requests a download, THEN THE API SHALL return HTTP 404 and issue no Presigned_URL.
5. THE Web_App SHALL display a completion dashboard at `/dashboard/reports/[reportId]` whose metrics (rows before and after, columns before and after, missing values before and after, duplicates removed, per-Operation counts, and duration) derive only from the recorded Execution.
6. THE Web_App SHALL provide the pages `/dashboard/datasets`, `/dashboard/datasets/[datasetId]`, and `/dashboard/reports/[reportId]` as routes owned by the Data Engineering Playground Lab registration of R55.
7. THE Web_App SHALL display only metrics that are backed by a stored record.
8. FOR ALL Executions, the output row count in the quality report SHALL equal the input row count minus the rows removed plus the rows added, as recorded by each Operation of the Execution (output-integrity property).
9. FOR ALL cleaned datasets, writing the dataset as CSV and then reading the CSV back SHALL produce a dataset equal to the written dataset (CSV round-trip property).
10. FOR ALL outputs, the CSV, Parquet, JSON, and XLSX files of one output SHALL represent the same rows and columns within the documented type limits of each format (cross-format equivalence property).
11. FOR ALL metrics displayed on the completion dashboard, each value SHALL equal the value computed from the stored Execution records (metrics-from-records property).

### Requirement 62: Machine Learning Preparation

**User Story:** As a Client, I want ML-oriented preparation without leakage, so that my train and test results are valid.

**ID:** NP-R62 | **Phase:** 4 | **Scope:** MVP-conditional (A-04) | **Roles:** Client, Founder, Administrator, Engineer, Project_Manager | **V1:** 29 | **Depends:** R57, R59, R60 | **Assumes:** A-04 | **Entities:** Operation, Pipeline, fitted transform metadata, train split, validation split, test split | **Failures:** ML preparation Operation without a target column, fit before split, leakage indicator kept without confirmation | **Validation:** required target column, random seed, split ratios summing to 1 | **Security:** own Organization only

#### Acceptance Criteria

1. THE Data_Engine SHALL provide Operations for categorical encoding, feature scaling, missing-value treatment, feature selection, feature engineering, and train, validation, and test splitting.
2. THE Web_App SHALL require the user to choose a target column before enabling any ML preparation Operation.
3. THE Data_Engine SHALL perform the split before fitting any encoder, scaler, imputer, or selector.
4. THE Data_Engine SHALL fit each encoder, scaler, imputer, and selector on the training split only and apply the fitted transform to the validation and test splits.
5. THE Data_Engine SHALL store the fitted transform metadata with the output so that the same transforms can be reapplied.
6. IF a candidate feature is flagged as a leakage indicator relative to the target column, THEN THE Web_App SHALL warn the user and require confirmation to keep the feature.
7. THE Data_Engine SHALL accept a random seed and produce the same split for the same input and the same seed.
8. THE Web_App SHALL describe the output as prepared for modeling and SHALL NOT claim that the data is ML-ready for every model or purpose.
9. FOR ALL inputs and seeds, two splits with the same input and the same seed SHALL be identical (seed determinism property).
10. FOR ALL splits, the train, validation, and test sets SHALL share no row identifier, and the combined row count SHALL equal the input row count (disjoint split property).
11. FOR ALL fitted transforms, the fitted parameters SHALL equal the parameters obtained by fitting on the training split alone (train-only fit property).

### Requirement 63: Dataset Lifecycle, Retention, and Privacy

**User Story:** As a Client, I want control over my data, so that I can delete the data and know how the data is used.

**ID:** NP-R63 | **Phase:** 4 | **Scope:** MVP-conditional (A-04) | **Roles:** Client, Founder, Administrator | **V1:** 30 | **Depends:** R18, R30, R56, R61, R64 | **Assumes:** A-04, A-08, A-36 | **Entities:** Dataset, Profile, output dataset, Pipeline, Execution, training consent record, Audit_Log | **Failures:** deletion of another Organization's Dataset, request for a deleted Dataset, model training without recorded consent | **Validation:** configured retention period (A-08) | **Security:** no public exposure of customer data, no training on customer data without recorded explicit consent

#### Acceptance Criteria

1. WHEN a user deletes a Dataset, THE API SHALL remove the stored object, the derived outputs, and the Profile, and write an Audit_Log entry.
2. THE Platform SHALL apply a retention period to Datasets and outputs whose value the Founder sets in configuration (A-08), and THE ENGINE SHALL delete expired items through a scheduled Job of R64.
3. THE Platform SHALL use customer data to train or fine-tune a model only when the owning Organization has given explicit, recorded consent.
4. THE Platform SHALL serve Dataset objects and outputs only through Presigned_URLs issued to authorized principals, and SHALL NOT expose customer data publicly.
5. THE Web_App SHALL display the retention period for each Dataset.
6. WHEN a Dataset deletion completes, THE Web_App SHALL display a confirmation, and THE API SHALL return HTTP 404 for every subsequent request for that Dataset.
7. IF a user requests deletion of a Dataset of another Organization, THEN THE API SHALL return HTTP 404 and delete nothing.
8. FOR ALL deleted Datasets, requests for the Dataset, the Profile, and the outputs SHALL return HTTP 404 (deletion completeness property).
9. FOR ALL Datasets and outputs whose retention period has expired, the stored object SHALL be absent after the next scheduled retention Job completes (retention property).

Phase 4A (continued): Commercial Records. R79 is numbered after R78 because IDs are stable; it belongs to Phase 4.

### Requirement 79: Commercial and Payment Records

**User Story:** As the Founder, I want quotations, payment schedules, invoice references, and payment statuses recorded against a Project, so that commercial status is traceable without the platform processing any payment.

**ID:** NP-R79 | **Phase:** 4 | **Scope:** MVP (minimal reference record); invoice generation Future | **Roles:** Founder, delegate of the Founder (A-06), Authorized_Approver, Client (read only, Client_Visible records) | **V1:** none (new) | **Depends:** R17, R18, R30, R36, R39, R42, R43, R45, R53, R54 | **Assumes:** A-05, A-06, A-13, A-34 | **Entities:** Commercial_Record, Project, Proposal_Version, Agreement, Project_Milestone, Maintenance_Engagement, Change_Request, Approval_Request, Organization, Audit_Log | **Failures:** create or change by a user who is neither the Founder nor a delegate, create or change of an amount by an Internal_Agent or AI component, issue without an Approved Approval_Request, Paid Recorded without an evidence reference, card data or bank credential in a field, link to a record of another Project, invalid status transition | **Validation:** type in {Quotation Reference, Milestone Payment Schedule Entry, Invoice Reference, Payment Status}, non-negative amount, ISO 4217 currency, due date, status per Appendix A.2, configured card number and bank credential detection patterns | **Security:** record keeping only, no payment processing, no card data or bank credentials stored, Internal_Only by default, Client responses limited to Client_Visible records

#### Acceptance Criteria

1. THE API SHALL store each Commercial_Record with a type of Quotation Reference, Milestone Payment Schedule Entry, Invoice Reference, or Payment Status, an amount, a currency, a due date, a status, the creating user, and the time.
2. THE API SHALL allow Commercial_Record statuses Draft, Issued, Paid Recorded, Overdue, and Void with the transitions defined in Appendix A.2, and IF an undefined transition is requested, THEN THE API SHALL return HTTP 409.
3. THE API SHALL link each Commercial_Record to exactly one Project, and optionally to one Proposal_Version, one Agreement under R39, one Project_Milestone under R45, one Maintenance_Engagement under R53, or one Change_Request under R54 of that Project.
4. IF a Commercial_Record link targets a record that belongs to another Project, THEN THE API SHALL reject the request with a field-level validation error.
5. THE API SHALL accept the creation or change of a Commercial_Record only from the Founder or a user to whom the Founder delegated the permission (A-06).
6. IF a user other than the Founder or a delegate creates or changes a Commercial_Record, THEN THE API SHALL return HTTP 403 and write an Audit_Log entry.
7. IF an Internal_Agent or an AI component of the Agent_Runtime requests the creation or change of a Commercial_Record amount, THEN THE API SHALL return HTTP 403, change no amount, and write an Audit_Log entry.
8. WHEN a user requests the transition of a Commercial_Record from Draft to Issued, THE API SHALL apply the transition only if an Approval_Request for issuing commercial quotations under R43 has status Approved and a content hash equal to the Commercial_Record content hash.
9. IF the guard of criterion 8 fails, THEN THE API SHALL reject the transition with a structured error and write an Audit_Log entry.
10. WHEN the Founder or a delegate sets a Commercial_Record to Paid Recorded, THE API SHALL require an evidence reference and store the recording user and the time as a manual record.
11. IF a Commercial_Record is set to Paid Recorded without an evidence reference, THEN THE API SHALL reject the request with a field-level validation error.
12. THE Platform SHALL provide no payment processing, and IF a Commercial_Record field matches a configured card number or bank credential detection pattern, THEN THE API SHALL reject the request with a field-level validation error and store no part of the value.
13. WHILE a Commercial_Record has status Issued and the current date is after the due date, THE API SHALL report the Commercial_Record status as Overdue.
14. THE API SHALL classify each Commercial_Record as Internal_Only unless the Founder or a delegate marks the Commercial_Record as Client_Visible.
15. THE API SHALL apply no behavior based on the reserved Organization `tier` attribute to Commercial_Records (A-05).
16. WHEN a Commercial_Record is created, changes status, changes amount, or changes visibility, THE API SHALL write an Audit_Log entry.
17. FOR ALL Commercial_Record amounts, the creating or last changing principal SHALL be a human user who is the Founder or a delegate of the Founder (human-authored amount property).
18. FOR ALL API responses to a Client, the response SHALL contain no Commercial_Record that is not Client_Visible (commercial record isolation property).

## Phase 5: NEUROPATH OPS and ENGINE

Phase 5 is internal only. OPS and ENGINE expose no customer-facing feature. Each agent beyond the first internal workflow (R67) is Optional and is enabled only on a documented operational need approved by the Founder. AWS queue and orchestration services (Amazon SQS, AWS Step Functions, Amazon EventBridge, AWS Lambda) are adopted only when Appendix C records a need; until then an in-process queue and worker behind the same interface is acceptable (A-27).

### Requirement 64: ENGINE Job Framework

**User Story:** As the Founder, I want every asynchronous unit of work to run through one controlled job framework with allowlisted job types, so that internal automation is bounded, retryable, and traceable.

**ID:** NP-R64 | **Phase:** 5 (interface available from the first phase that uses Jobs) | **Scope:** MVP | **Roles:** Founder, Administrator, Internal_Agent (requester only), API (system) | **V1:** 27.9, 27.10 | **Depends:** R3, R17, R18, R19, R27, R30, R42 | **Assumes:** A-08, A-27, A-29 | **Entities:** Job, Job type registration, dead-letter record, Notification, Audit_Log | **Failures:** unknown job type, parameters that fail the job type schema, duplicate delivery, transient failure, retries exhausted, CPU, memory, or time limit exceeded, cross-Organization data access attempt, operation outside the job type permission set | **Validation:** job type in the registry, Pydantic parameter schema per job type, dedupe key present, Job status per Appendix A.2 | **Security:** allowlisted operations only, no execution of model-generated code, per-job-type scoped permissions, Organization-scoped execution

#### Acceptance Criteria

1. THE ENGINE SHALL maintain a registry of job types in which each entry records a unique job type identifier, a Pydantic parameter schema, the handler module, the permission set, and the CPU, memory, and time limits.
2. IF a Job is submitted with a job type that is absent from the registry, THEN THE ENGINE SHALL reject the Job with a structured error and write an Audit_Log entry.
3. IF the parameters of a submitted Job fail validation against the job type parameter schema, THEN THE ENGINE SHALL reject the Job with a field-level validation error and create no Job record.
4. THE ENGINE SHALL execute only handler code that is registered for the job type and SHALL reject any Job whose parameters contain code, scripts, or expressions intended for execution.
5. THE ENGINE SHALL record each Job with a status of Queued, Running, Succeeded, Failed, or Cancelled and apply only the transitions defined in Appendix A.2.
6. WHEN a Job is submitted, THE ENGINE SHALL require a dedupe key, and WHEN a delivery arrives whose dedupe key matches an existing Job, THE ENGINE SHALL apply no further effect and return the existing Job identifier.
7. IF a Job fails with a transient infrastructure failure, THEN THE ENGINE SHALL retry the Job up to 3 times with backoff before setting the Job status to Failed.
8. IF a Job exceeds the CPU, memory, or time limit of the job type, THEN THE ENGINE SHALL terminate the Job and set the Job status to Failed with a reason that names the exceeded limit.
9. THE ENGINE SHALL execute each Job with access only to records of the Organization named in the Job and to the operations in the permission set of the job type.
10. IF a running Job requests a record of another Organization or an operation outside the job type permission set, THEN THE ENGINE SHALL deny the request, set the Job status to Failed, and write an Audit_Log entry.
11. WHEN a Job reaches Failed after exhausting the retries, THE ENGINE SHALL store a dead-letter record with the Job identifier, job type, parameters after redaction, error, and attempt count, and THE Founder_Control_Center SHALL display the dead-letter record to the Founder and Administrators.
12. WHEN a Job reaches Failed, THE Platform SHALL send a Notification to the Job owner through R27.
13. THE ENGINE SHALL expose job submission, status, and cancellation through an interface whose local implementation runs an in-process queue and worker, so that a queue technology recorded in Appendix C can replace the local implementation without changing callers.
14. THE ENGINE SHALL register retention enforcement, Approval_Request expiry, and Commercial_Record overdue computation as scheduled job types in the registry.
15. WHEN a Job completes, THE ENGINE SHALL record the Job duration and the estimated cost of the Job in usage_records under R42.
16. FOR ALL sequences of deliveries that share one dedupe key, the stored effects SHALL equal the effects of exactly one successful execution (exactly-once effect property).
17. FOR ALL executed Jobs, the executed handler SHALL be the handler registered for the job type in the registry (registry-only execution property).

### Requirement 65: Agent Architecture

**User Story:** As the Founder, I want each OPS agent defined in a registry with its own instructions, tools, and output schema, so that agent behavior is decomposed, inspectable, and limited to a documented operational need.

**ID:** NP-R65 | **Phase:** 5 | **Scope:** MVP for the agents used by R67; Optional for every other agent | **Roles:** Founder, Administrator (read only), Internal_Agent | **V1:** 37 | **Depends:** R17, R18, R30, R32, R64 | **Assumes:** A-27, A-28 | **Entities:** Agent registration, Agent_Task, Internal_Agent principal, Audit_Log | **Failures:** enable without a recorded operational need, enable by a non-Founder, tool call outside the tool list, output that fails the output schema, instruction injected through inbound content, Internal_Agent assigned an administrative role | **Validation:** unique agent id, non-empty purpose, instructions, tool list, output schema, model configuration, operational need record | **Security:** least privilege per agent, untrusted inbound content, minimum data, raw Dataset contents excluded by default, no Administrator or Founder role for agents

#### Acceptance Criteria

1. THE Agent_Runtime SHALL maintain an agent registry in which each entry records an agent id, a purpose, instructions, a tool list, an output schema, an enabled flag, a model configuration, and a reference to a documented operational need.
2. THE Agent_Runtime SHALL support registry entries for the potential agents Orchestrator, Business Intelligence, Lead Research, Marketing, Content, Outreach, Engineering Assistant, Data Assistant, and Quality & Security.
3. WHEN a request sets an agent enabled flag to true, THE API SHALL apply the change only if the request comes from the Founder and the registry entry references an operational need record that the Founder approved.
4. IF a request enables an agent without an approved operational need record or from a user other than the Founder, THEN THE API SHALL reject the request with a structured error and write an Audit_Log entry.
5. THE Agent_Runtime SHALL give each agent a separate, scoped prompt built from the instructions of that agent only.
6. IF an agent requests a tool that is absent from the agent tool list, THEN THE Agent_Runtime SHALL deny the call and write an Audit_Log entry with the agent id, the tool name, and the Agent_Task identifier.
7. THE Agent_Runtime SHALL validate every agent output against the output schema of the agent before the output is stored or passed to another agent.
8. IF an agent output fails output schema validation, THEN THE Agent_Runtime SHALL store no output for the Agent_Task and set the Agent_Task status to Failed with the validation error.
9. THE Agent_Runtime SHALL provide each agent only the fields named in the input definition of the Agent_Task and SHALL exclude raw Dataset contents from agent inputs unless the Founder enables Dataset access for that agent in the registry.
10. THE Agent_Runtime SHALL treat inquiry text, client messages, attachments, and fetched web content as untrusted data, and WHEN such content contains instructions, THE Agent_Runtime SHALL keep the agent instructions and tool list unchanged.
11. THE Orchestrator SHALL route work only by creating Agent_Tasks for other agents, and THE Orchestrator tool list SHALL contain only task creation and task status tools.
12. THE API SHALL run each agent as an Internal_Agent principal under R17 with the permission set of that agent, and IF a role assignment would give an agent the Administrator or Founder role, THEN THE API SHALL reject the assignment.
13. WHEN an agent registry entry is created or changed, THE API SHALL write an Audit_Log entry with the previous and new values.
14. FOR ALL Agent_Task executions, the set of tools available to the agent during the execution SHALL equal the tool list in the agent registry entry at the start of the execution (tool set property).
15. FOR ALL stored agent outputs, the output SHALL validate against the output schema of the producing agent (validated output property).

### Requirement 66: Agent Task Recording, Limits, and Cost Monitoring

**User Story:** As the Founder, I want every agent run recorded with its cost and bounded by token and daily cost limits, so that I can investigate any outcome and keep agent spend under control.

**ID:** NP-R66 | **Phase:** 5 | **Scope:** MVP | **Roles:** Founder, Administrator (read only), Internal_Agent | **V1:** 38, 42 (cost parts) | **Depends:** R27, R30, R42, R64, R65 | **Assumes:** A-08, A-30 | **Entities:** Agent_Task, usage_records, Notification, Audit_Log | **Failures:** transient model failure, retries exhausted, per-task token limit exceeded, per-day cost limit reached, missing cost data | **Validation:** Agent_Task status per Appendix A.2, non-negative tokens and cost, configured limit values | **Security:** redaction of secrets and personal data before storage, records Internal_Only

#### Acceptance Criteria

1. WHEN an Agent_Task is created, THE OPS SHALL queue the Agent_Task as a Job through R64 and record the Agent_Task with status Queued.
2. THE OPS SHALL record for each Agent_Task the task identifier, agent id, input, output, status, duration, model identifier, input and output token counts, estimated cost, error, and execution trace.
3. THE OPS SHALL allow Agent_Task statuses Queued, Running, Succeeded, Failed, Awaiting Approval, and Cancelled with the transitions defined in Appendix A.2.
4. THE OPS SHALL redact secrets and personal data from stored Agent_Task inputs, outputs, and traces according to a documented redaction policy before the record is written.
5. IF an Agent_Task fails with a transient failure, THEN THE OPS SHALL retry the Agent_Task up to 3 times with backoff before setting the status to Failed.
6. IF an Agent_Task reaches the configured per-task token limit, THEN THE OPS SHALL stop the Agent_Task and set the status to Failed with a reason that names the limit.
7. WHEN the recorded agent cost for the current day reaches the configured per-day agent cost limit (A-08), THE OPS SHALL start no new Agent_Task for the rest of the day and send a Notification to the Founder.
8. IF an Agent_Task is submitted while the per-day agent cost limit is reached, THEN THE OPS SHALL reject the Agent_Task with a structured error that names the limit.
9. WHEN an Agent_Task completes, THE OPS SHALL write the token counts, model identifier, and estimated cost of the Agent_Task to usage_records under R42.
10. IF the model provider returns no token or cost data for an Agent_Task, THEN THE OPS SHALL record the cost as unknown and include the Agent_Task in a missing cost count shown to the Founder.
11. THE API SHALL provide admin endpoints for agents, agent tasks, and approvals under `/api/v1/admin`, restricted to the roles that Appendix A.3 permits.
12. THE OPS SHALL run at most one Agent_Task in status Running at a time and SHALL check the per-day agent cost limit before each Agent_Task starts (A-30).
13. FOR ALL days, the total recorded agent cost SHALL be no greater than the configured per-day agent cost limit plus the cost of at most one Agent_Task that was running when the limit was reached (daily cost bound property).

### Requirement 67: First Internal Workflow: Inquiry Processing Assistance

**User Story:** As the Founder, I want each new Project_Inquiry prepared by an internal workflow up to the point of human review, so that reviewers start from a summary, draft questions, and a discipline suggestion without any automated decision.

**ID:** NP-R67 | **Phase:** 5 | **Scope:** MVP (the first and only MVP OPS workflow) | **Roles:** Founder, Authorized_Reviewer, Internal_Agent (Orchestrator and the agents of the workflow steps) | **V1:** 39 (reshaped) | **Depends:** R14, R21, R24, R27, R30, R32, R33, R64, R65, R66 | **Assumes:** A-01, A-11, A-28 | **Entities:** Project_Inquiry, Project, Agent_Task, Job, Inquiry_Question (draft), Notification, Audit_Log | **Failures:** step failure, step output that fails its schema, workflow attempt to change Project status, workflow attempt to contact the client, inquiry without AI processing consent | **Validation:** step order, output schema per step, discipline labels from the R32 label list | **Security:** outputs Internal_Only and advisory, no client contact, no qualification, rejection, or pricing by the workflow

#### Acceptance Criteria

1. WHEN a Project_Inquiry is stored with the AI-assisted processing consent flag set, THE OPS SHALL create one inquiry processing workflow run for the Project_Inquiry through the ENGINE.
2. IF a Project_Inquiry is stored without the AI-assisted processing consent flag, THEN THE OPS SHALL create no workflow run and record the reason on the Project as Internal_Only.
3. THE Orchestrator SHALL run the workflow steps requirement summary, draft clarification questions, discipline suggestion, and quality review, in that order, each as an Agent_Task.
4. THE OPS SHALL produce the requirement summary through the R32 analysis capability and the draft clarification questions as Inquiry_Question drafts under R33 that require human approval before sending.
5. THE OPS SHALL produce the discipline suggestion only with labels from the R32 label list, each with a stated justification.
6. THE OPS SHALL store the status, start time, end time, and duration of each workflow step.
7. IF a workflow step fails, THEN THE OPS SHALL halt the workflow, record the failing step and error, run no later step, and send a Notification to the Founder.
8. THE OPS SHALL classify every workflow output as Internal_Only and label every workflow output as advisory and AI-generated.
9. WHEN the quality review step completes, THE OPS SHALL send a Notification to the Founder and the assigned Authorized_Reviewer that the outputs are ready for review.
10. THE OPS SHALL grant the workflow agents no permission to change Project status, qualify or reject a Project, create a price or Commercial_Record, or send any Communication to the client.
11. IF a workflow agent requests a Project status change, a qualification, a rejection, a price, or a client contact, THEN THE API SHALL deny the request with HTTP 403 and write an Audit_Log entry.
12. WHEN the same Project_Inquiry triggers the workflow more than once, THE OPS SHALL use the Project_Inquiry identifier as the dedupe key and run one workflow.
13. FOR ALL workflow runs, the Project status before the run SHALL equal the Project status after the run, apart from changes made by human users (status preservation property).

### Requirement 68: OPS Approvals for Sensitive Actions

**User Story:** As the Founder, I want every Sensitive_Action proposed by an agent held for a named human decision on the exact content, so that no agent acts externally or commits NEUROPATH commercially.

**ID:** NP-R68 | **Phase:** 5 | **Scope:** MVP | **Roles:** Founder, Authorized_Approver, Internal_Agent (requester only) | **V1:** 40 | **Depends:** R17, R22, R30, R43, R65, R66, R79 | **Assumes:** A-06, A-08 | **Entities:** Approval_Request, Agent_Task, Commercial_Record, Communication, Audit_Log, Notification | **Failures:** Sensitive_Action without an Approved request, execution with a hash mismatch, decision by an Internal_Agent or non-approver, expired or invalidated request, agent creation of a quotation, price, or Commercial_Record amount | **Validation:** Approval_Request fields and status per R43 and Appendix A.2 | **Security:** content hash binding, decisions by humans only, append-only audit of decisions and external communications

#### Acceptance Criteria

1. WHEN an agent proposes a Sensitive_Action, THE OPS SHALL create an Approval_Request under R43 with the action type, target, exact content or parameters, content hash, requesting agent, and rationale, and set the Agent_Task status to Awaiting Approval.
2. WHILE an Approval_Request created by an agent has status Pending, THE OPS SHALL hold the proposed action unexecuted.
3. THE API SHALL accept a decision on an agent-originated Approval_Request only from the Founder or an Authorized_Approver.
4. WHEN an agent-originated Approval_Request is Approved, THE OPS SHALL execute the action only with content whose hash equals the approved content hash.
5. IF the content or parameters change after approval, THEN THE OPS SHALL set the Approval_Request to Invalidated under R43 and execute no action.
6. WHEN an agent-originated Approval_Request is Rejected, Expired, or Invalidated, THE OPS SHALL set the Agent_Task status to Cancelled and execute no action.
7. THE OPS SHALL grant no agent a permission to accept, sign, or confirm a commercial commitment, or to create or change a quotation, a price, or a Commercial_Record amount.
8. IF an agent requests the creation or change of a quotation, a price, or a Commercial_Record amount, THEN THE API SHALL return HTTP 403, change no record, and write an Audit_Log entry.
9. WHEN an approved external communication is performed, THE OPS SHALL record the communication in the Audit_Log with the Approval_Request reference.
10. IF a Sensitive_Action is attempted by or for an agent without an Approved Approval_Request with a matching content hash, THEN THE OPS SHALL block the action and write an Audit_Log entry.
11. WHEN an agent-originated Approval_Request is created, THE Platform SHALL send a Notification to the Founder.
12. FOR ALL agent-originated external actions that the OPS executes, an Approval_Request with status Approved and a content hash equal to the executed content hash SHALL exist (approved agent action property).

### Requirement 69: Ops Dashboard

**User Story:** As the Founder, I want one internal dashboard of agent activity, cost, and pending approvals, so that I can supervise OPS from stored records.

**ID:** NP-R69 | **Phase:** 5 | **Scope:** MVP | **Roles:** Founder, Administrator (read only for decisions and configuration), Authorized_Approver | **V1:** 41 | **Depends:** R17, R30, R43, R65, R66, R68 | **Assumes:** A-06, A-07 | **Entities:** Agent registration, Agent_Task, Approval_Request, usage_records, Audit_Log | **Failures:** access by a role other than Founder or Administrator, decision by a non-approver, rejection without a reason, configuration change by a non-Founder | **Validation:** filters by agent, status, and date range; non-empty rejection reason | **Security:** internal route only, server-side permission checks per Appendix A.3

#### Acceptance Criteria

1. THE Web_App SHALL provide an ops dashboard at `/admin/ops` that THE API serves only to the Founder and Administrators per Appendix A.3.
2. IF a principal other than the Founder or an Administrator requests `/admin/ops` or the ops dashboard endpoints, THEN THE API SHALL return HTTP 403 for authenticated principals and HTTP 401 for unauthenticated requests.
3. THE ops dashboard SHALL show an agent directory with name, purpose, enabled flag, last activity time, and the referenced operational need for each registered agent.
4. THE ops dashboard SHALL show the task queue, the running Agent_Tasks, and the Agent_Task history with filters by agent, status, and date range.
5. THE ops dashboard SHALL show token counts, model usage, estimated cost, and error counts computed from stored Agent_Task records.
6. THE ops dashboard SHALL show pending agent-originated Approval_Requests and accept approve or reject decisions only from the Founder or an Authorized_Approver.
7. IF a reject decision is submitted without a reason, THEN THE API SHALL reject the decision with a field-level validation error.
8. THE ops dashboard SHALL accept a change to an agent configuration only from the Founder, and WHEN the configuration changes, THE API SHALL write an Audit_Log entry with the previous and new values.
9. WHEN the Founder or an Administrator opens a failed Agent_Task, THE ops dashboard SHALL display the error, the redacted input, the redacted output, and the step timeline of the Agent_Task.
10. FOR ALL filter selections, each metric displayed on the ops dashboard SHALL equal the value computed from the stored records that match the filter (metric integrity property).

### Requirement 70: Lead Research and Outreach Limits

**User Story:** As the Founder, I want lead research and outreach restricted to lawful sources, drafts, and approved sends, so that NEUROPATH avoids legal and reputational harm.

**ID:** NP-R70 | **Phase:** 5 | **Scope:** Optional (enabled only on a documented operational need under R65) | **Roles:** Founder, Authorized_Approver, Internal_Agent (Lead Research, Outreach) | **V1:** 43.1, 43.2, 43.3, 43.5 | **Depends:** R22, R30, R43, R65, R68 | **Assumes:** A-11, A-28 | **Entities:** Lead, Lead_Source, Opt_Out_Entry, Agent_Task, Approval_Request, Audit_Log | **Failures:** source not on the allowed source list, Lead data item without a source, send without an Approved request, contact to an opted-out person | **Validation:** source on the Founder-approved source list, source reference per data item, normalized email checked against the opt-out list | **Security:** lawful sources only, drafts only, opt-out enforcement

#### Acceptance Criteria

1. THE Lead Research agent SHALL collect data only from sources on a source list that the Founder approved as permitted by applicable law, site terms, and access controls.
2. IF the Lead Research agent requests a source that is absent from the approved source list, THEN THE Agent_Runtime SHALL deny the request and write an Audit_Log entry.
3. THE API SHALL store a source reference for each Lead data item created by the Lead Research agent under R22.
4. IF a Lead data item from the Lead Research agent has no source reference, THEN THE API SHALL reject the data item with a field-level validation error.
5. THE Outreach agent SHALL produce outreach messages as drafts only.
6. WHEN an outreach draft is proposed for sending, THE OPS SHALL send the message only through an Approved Approval_Request under R68.
7. IF an outreach draft targets a person whose normalized email is on the opt-out list, THEN THE OPS SHALL reject the draft for sending with a structured error and create no Approval_Request.
8. FOR ALL persons whose normalized email is on the opt-out list, THE OPS SHALL record no outgoing outreach message (outreach opt-out property).

### Requirement 71: Content and Marketing Assistance

**User Story:** As the Founder, I want content and marketing drafts checked against verified records and published only after approval, so that NEUROPATH publishes only true and approved claims.

**ID:** NP-R71 | **Phase:** 5 | **Scope:** Optional (enabled only on a documented operational need under R65) | **Roles:** Founder, Authorized_Approver, Internal_Agent (Content, Marketing) | **V1:** 37.7, 43.4 | **Depends:** R11, R30, R43, R65, R68 | **Assumes:** A-17, A-28 | **Entities:** content_items, verified project records, Approval_Request, Audit_Log | **Failures:** claim without support in verified records, publish without an Approved request, undefined status transition | **Validation:** content_items status per Appendix A.2, claim list with a supporting record reference or an unsupported flag | **Security:** drafts only, truthful content under R11

#### Acceptance Criteria

1. THE Content agent and THE Marketing agent SHALL produce articles, LinkedIn posts, case-study drafts, and campaign plans as content_items with status Draft.
2. THE Content agent SHALL list each factual claim in a content_item with a reference to the verified project record under R11 that supports the claim.
3. IF a factual claim has no supporting verified project record, THEN THE Content agent SHALL flag the claim as unsupported in the content_item.
4. IF a content_item contains a claim flagged as unsupported, THEN THE API SHALL reject the transition of the content_item to Approved with a structured error that lists the unsupported claims.
5. THE API SHALL allow content_items statuses Draft, In Review, Approved, Scheduled, Published, and Rejected with the transitions defined in Appendix A.2.
6. WHEN a content_item is proposed for publishing, THE OPS SHALL publish the content_item only through an Approved Approval_Request under R68 whose content hash equals the content_item content hash.
7. WHEN a content_item changes status, THE API SHALL write an Audit_Log entry.
8. FOR ALL content_items with status Published, every factual claim SHALL reference a verified project record (published claim support property).

### Requirement 72: Engineering and Project Assistance

**User Story:** As a Project_Manager, I want the Engineering Assistant to draft plans, documentation reviews, and progress summaries from stored records, so that delivery staff save time while humans approve every client-visible output.

**ID:** NP-R72 | **Phase:** 5 | **Scope:** Optional (enabled only on a documented operational need under R65) | **Roles:** Founder, Project_Manager, Engineer, Internal_Agent (Engineering Assistant) | **V1:** 37.1 (Engineering agent) | **Depends:** R18, R30, R44, R45, R46, R47, R65, R66, R68 | **Assumes:** A-28 | **Entities:** Agent_Task, Project, Project_Milestone, Task, Communication, Deployment_Record, Approval_Request, Audit_Log | **Failures:** summary shown to a Client without human approval, request for production credentials or infrastructure access, infrastructure change without an Approved request, draft content not traceable to stored records | **Validation:** output schema per draft type, source record references | **Security:** no production credentials, no infrastructure access, Internal_Only drafts

#### Acceptance Criteria

1. THE Engineering Assistant SHALL produce implementation plan drafts, documentation review drafts, and project progress summary drafts with references to the stored records used.
2. THE Engineering Assistant SHALL read only records of the Project named in the Agent_Task.
3. THE OPS SHALL classify every Engineering Assistant draft as Internal_Only.
4. WHEN a project progress summary draft is proposed as a client update, THE API SHALL make the update Client_Visible only after human approval under R47.
5. THE Agent_Runtime SHALL give the Engineering Assistant no tool or permission that reads production credentials, secret values, or infrastructure control interfaces.
6. IF the Engineering Assistant requests production credentials, a secret value, or an infrastructure control operation, THEN THE Agent_Runtime SHALL deny the request and write an Audit_Log entry.
7. WHEN the Engineering Assistant proposes a change to production infrastructure, THE OPS SHALL handle the proposal as a Sensitive_Action under R68.
8. FOR ALL Engineering Assistant outputs that a Client can see, a human approval record under R47 SHALL exist for the output (approved client output property).

### Requirement 73: Full Founder Control Center

**User Story:** As the Founder, I want one internal console for the whole business, platform configuration, OPS, and audit, so that I can run NEUROPATH from stored records with every change traceable.

**ID:** NP-R73 | **Phase:** 5 | **Scope:** MVP (extends the Phase 2 dashboard of R28) | **Roles:** Founder, Administrator, Engineer, Project_Manager, Authorized_Approver | **V1:** 20, 42 | **Depends:** R17, R18, R28, R30, R42, R43, R56, R64, R66, R69, R79 | **Assumes:** A-04, A-07, A-08, A-36 | **Entities:** Organization, Project, Lead, Proposal_Version, Commercial_Record, Agent_Task, Approval_Request, Feature_Flag, configuration value, usage_records, Audit_Log | **Failures:** access outside the role section per Appendix A.3, configuration change without permission, deletion without an Approved request, request by a user of a suspended Organization, monitoring data unavailable | **Validation:** configuration value types and ranges, suspension reason required | **Security:** role separation per Appendix A.3, audit of every configuration change, deletion behind R43

#### Acceptance Criteria

1. THE Founder_Control_Center SHALL provide sections for inquiries, Prospective_Clients, Clients and Organizations, Project_Opportunities, Technical_Assessments, Proposals, Active_Engagements, Project_Milestones, team assignments, Deliverables, Support_Requests, Maintenance_Engagements, Commercial_Records, Labs, internal workflows, OPS agents, pending approvals, usage and infrastructure cost, Audit_Log, and system configuration.
2. THE API SHALL serve each Founder_Control_Center section only to the roles that Appendix A.3 grants for that section, with the Founder, Administrator, Engineer, and Project_Manager roles kept separate.
3. THE Founder_Control_Center dashboard SHALL show the counts of customers, inquiries, Active_Engagements, and processing Jobs, the agent activity, the pending approvals, and the recorded operational expenses, each computed from stored records.
4. WHERE the Data Engineering Playground is enabled, THE Founder_Control_Center dashboard SHALL show the pipeline success rate computed from stored Execution records.
5. THE Founder_Control_Center SHALL allow the Founder and Administrators permitted by Appendix A.3 to manage usage limits, Feature_Flags, upload limits, AI model configuration, and API configuration.
6. WHEN a configuration value is changed, THE API SHALL write one Audit_Log entry with the previous value, the new value, the actor, and the time.
7. WHEN the Founder or a permitted Administrator suspends an Organization with a reason, THE API SHALL set the Organization status to suspended and write an Audit_Log entry.
8. WHILE an Organization is suspended, THE API SHALL deny requests from users of that Organization with HTTP 403 and a structured error that states the Organization is suspended.
9. WHEN the Founder or a permitted Administrator reinstates a suspended Organization, THE API SHALL restore access for the Organization users and write an Audit_Log entry.
10. WHEN a staff member processes a deletion request for customer data, THE API SHALL delete the data only with an Approved Approval_Request under R43 whose content hash equals the hash of the deletion parameters; Client self-service Dataset deletion under R63.1 is exempt (A-36).
11. THE Founder_Control_Center SHALL display system health from monitoring data, and IF monitoring data cannot be retrieved, THEN THE Founder_Control_Center SHALL show an unavailable state with no health value.
12. THE Founder_Control_Center SHALL provide Audit_Log search by actor, action, resource, and time range.
13. THE API SHALL provide analytics endpoints overview, usage, and agents under `/api/v1/admin/analytics`, restricted to the roles that Appendix A.3 permits.
14. FOR ALL configuration changes, exactly one Audit_Log entry SHALL exist that records the previous and new values of the change (configuration audit property).

## Phase 6: Production Readiness

### Requirement 74: Security Hardening

**User Story:** As the Founder, I want a hardened platform with a recorded security review, so that customer data and client trust are protected before production use.

**ID:** NP-R74 | **Phase:** 6 | **Scope:** MVP | **Roles:** Founder, Administrator, Engineer | **V1:** 44 | **Depends:** R2, R3, R7, R17, R18, R19, R30, R32, R43, R65, R68 | **Assumes:** A-08, A-16, A-33 | **Entities:** S3 bucket, RDS instance, queue (if in use), IAM role, security review record, dependency scan result, Audit_Log | **Failures:** unencrypted connection, public bucket or object, public database endpoint, wildcard resource permission for data access, seeded sensitive value found in a log, missing security header, request from an origin outside the configured list, unresolved critical dependency finding | **Validation:** IAM policy checks, header checks, CORS origin list, log scan of test-suite output | **Security:** TLS in transit, encryption at rest, least privilege, tenant isolation, Internal_Only separation

#### Acceptance Criteria

1. THE Infrastructure SHALL encrypt all data in transit with TLS.
2. THE Infrastructure SHALL encrypt all data at rest in S3, RDS, and every queue in use.
3. THE Infrastructure SHALL keep every S3 bucket private with public access blocked.
4. THE Infrastructure SHALL place the RDS database in private subnets with no public endpoint.
5. THE Infrastructure SHALL grant each compute role only the permissions that the role uses, with every data access permission scoped to named resources and no wildcard resource.
6. THE API SHALL store the sensitive customer fields listed in `docs/SECURITY.md` in encrypted form.
7. THE API SHALL set the Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options, and frame protection headers on every response.
8. IF a cross-origin request comes from an origin outside the configured origin list, THEN THE API SHALL reject the request without CORS allow headers.
9. WHEN the test suite runs, THE Platform SHALL seed known sensitive values and scan every log produced by the test suite for those values.
10. IF the log scan finds a seeded sensitive value, THEN THE Platform SHALL fail the test run and report the log location of the value.
11. THE Platform SHALL record a security review in `docs/SECURITY.md` with the results of tenant isolation, Internal_Only separation, prompt-injection, tool-permission, and approval-enforcement tests.
12. THE Platform SHALL pass dependency vulnerability scanning with no unresolved critical finding before Phase 6 is reported complete.
13. FOR ALL logs produced by the test suite, no log SHALL contain a seeded sensitive value (log redaction property).

### Requirement 75: Reliability, Monitoring, and Recovery

**User Story:** As the Founder, I want the platform to be observable and recoverable, so that outages are short, failures are visible, and data is not lost.

**ID:** NP-R75 | **Phase:** 6 | **Scope:** MVP | **Roles:** Founder, Administrator, Engineer | **V1:** 45 | **Depends:** R2, R3, R7, R43, R64, R66, R73, R74 | **Assumes:** A-08, A-27, A-31 | **Entities:** RDS backup, S3 object version, restore test record, CloudWatch log, metric, alarm, health status, dead-letter record, Deployment_Record, Audit_Log | **Failures:** backup missing, restore to an unverified state, deleted customer object or version kept beyond the deletion window, health endpoint reporting a failed dependency as healthy, deployment without rollback steps, dead-letter record without an alarm | **Validation:** documented retention period, documented deletion window, documented RTO and RPO targets | **Security:** backups encrypted per R74, health endpoint discloses no secret values or internal addresses

#### Acceptance Criteria

1. THE Infrastructure SHALL enable automated RDS backups with the retention period documented in `docs/DEPLOYMENT.md`.
2. THE Infrastructure SHALL enable S3 versioning only on the buckets whose need is recorded in `docs/DEPLOYMENT.md`.
3. WHEN a customer object is deleted, THE Platform SHALL purge the object and every version of the object within the documented deletion window.
4. THE Platform SHALL document a restore procedure in `docs/DEPLOYMENT.md`.
5. WHEN the restore test runs, THE Platform SHALL restore data to a separate environment and verify the restored data against recorded checksums or record counts.
6. THE Platform SHALL emit structured logs, metrics, and alarms to CloudWatch for API errors, Job failures, agent failures, and cost thresholds.
7. WHERE a managed queue is in use, THE Infrastructure SHALL emit a queue depth metric and alarm to CloudWatch.
8. THE API SHALL expose a health endpoint that reports the status of each dependency as measured at the time of the request.
9. IF a dependency check fails or times out, THEN THE API health endpoint SHALL report that dependency as unavailable.
10. THE Platform SHALL record in `docs/DEPLOYMENT.md` the recovery time objective and recovery point objective set by the Founder (A-31).
11. THE Platform SHALL document a deployment process with rollback steps in `docs/DEPLOYMENT.md`.
12. WHEN a dead-letter record is created, THE Platform SHALL raise a CloudWatch alarm and create a dead-letter record visible in the Founder_Control_Center.
13. FOR ALL dependency states, the health endpoint SHALL report a dependency as healthy only when the check of that dependency succeeded in the same request (truthful health property).

### Requirement 76: Performance and Cost Optimization

**User Story:** As the Founder, I want measured performance and reviewed costs against targets I set, so that the platform meets its load needs without unjustified AWS spend.

**ID:** NP-R76 | **Phase:** 6 | **Scope:** MVP | **Roles:** Founder, Administrator, Engineer | **V1:** none (new) | **Depends:** R3, R7, R42, R66, R73, R75 | **Assumes:** A-08, A-27, A-32 | **Entities:** load test record, latency measurement, usage_records, AWS billing data, Appendix C service entry, billable deployment authorization, budget alarm | **Failures:** load test without Founder-set targets, missing p95 measurement for a main endpoint, AWS service in use without an Appendix C justification, billable deployment without written authorization, budget alarm not firing | **Validation:** Founder-set target values recorded before the load test, main endpoint list recorded | **Security:** load tests run against a non-production environment unless the Founder authorizes otherwise in writing

#### Acceptance Criteria

1. THE Platform SHALL record in `docs/DEPLOYMENT.md` the load test target values set by the Founder before Phase 6 acceptance (A-32).
2. WHEN the load test runs, THE Platform SHALL apply the documented load and record the result in `docs/IMPLEMENTATION_STATUS.md`.
3. WHEN the load test runs, THE Platform SHALL measure and record the p95 latency of each main API endpoint listed in `docs/DEPLOYMENT.md`.
4. THE Platform SHALL record a cost review per environment that compares recorded usage_records with AWS billing data for the same period.
5. THE Platform SHALL record in Appendix C a justification for each AWS service in use.
6. IF an AWS service in use has no Appendix C justification, THEN THE Infrastructure SHALL remove the service before Phase 6 acceptance.
7. THE Platform SHALL record the Founder written authorization for each billable deployment under R3.6.
8. THE Platform SHALL verify that each budget alarm defined under R7.4 fires at its threshold and record the verification result.

### Requirement 77: Test Coverage

**User Story:** As a developer, I want tests for each critical capability, so that no feature is claimed complete without evidence.

**ID:** NP-R77 | **Phase:** 6 | **Scope:** MVP (Data_Engine tests MVP-conditional per A-04) | **Roles:** Founder, Engineer | **V1:** 46 | **Depends:** R4, R5, R6, R8, R17, R18, R30, R55, R56, R57, R58, R59, R60, R61, R62, R63, R65, R68, R74, R75 | **Assumes:** A-04 | **Entities:** test suite, test result record, recorded model response, Feature_Flag | **Failures:** missing test category, test calling Bedrock in the default CI run, FOR ALL property without a property-based test, MVP flow test failing with Labs disabled, phase reported complete without recorded results | **Validation:** Appendix A.1, A.2, and A.3 conformance, migration up and down | **Security:** authorization, tenant isolation, Internal_Only visibility, prompt-injection, tool-permission, and approval-enforcement tests

#### Acceptance Criteria

1. THE Web_App test suite SHALL include component tests, form validation tests, navigation tests, responsive layout tests at 360 px, 768 px, and 1280 px, accessibility checks, and end-to-end tests for the MVP flows.
2. THE API test suite SHALL include unit, integration, authentication, and authorization tests, with the authorization tests checking conformance to the Appendix A.3 permission matrix.
3. THE API test suite SHALL include tenant isolation tests and Internal_Only visibility tests.
4. THE API test suite SHALL include status transition conformance tests against Appendix A.1 and Appendix A.2.
5. THE API test suite SHALL include database migration tests that apply every migration up and down.
6. WHERE the Data Engineering Playground is enabled, THE Data_Engine test suite SHALL include the tests defined by R56 to R63.
7. THE Agent_Runtime test suite SHALL include structured-output validation, hallucination checks against supplied facts, prompt-injection, tool-permission, and approval-enforcement tests.
8. THE Infrastructure test suite SHALL include deployment validation, IAM policy checks, storage access checks, backup checks, and monitoring checks.
9. THE Platform SHALL provide a property-based test for every FOR ALL property in this document.
10. THE Platform SHALL run model-dependent tests against recorded or stubbed model responses, and the default continuous integration run SHALL make no call to Amazon Bedrock.
11. WHILE all Labs are disabled, THE MVP project flow tests SHALL pass (R55.12).
12. WHEN a phase is reported complete, THE Platform SHALL have recorded the results of the tests relevant to that phase in `docs/IMPLEMENTATION_STATUS.md`.
13. FOR ALL properties stated with FOR ALL in this document, at least one property-based test SHALL reference the property by requirement ID and criterion number (property coverage property).

### Requirement 78: Phase Gating and MVP Acceptance

**User Story:** As the Founder, I want each phase reviewed against an explicit gate before the next begins, so that the app always works and scope stays controlled.

**ID:** NP-R78 | **Phase:** 6 | **Scope:** MVP (gates apply from Phase 0 onward) | **Roles:** Founder, Engineer | **V1:** 47 | **Depends:** R1 to R77, R79 | **Assumes:** A-04, A-08, A-31, A-32 | **Entities:** phase report, Founder review approval, go/no-go decision record, acceptance journey record, Audit_Log | **Failures:** phase started without Founder review approval, gate item failing, earlier feature broken, fabricated data, result, or success state, Playground shipped without a recorded go decision | **Validation:** phase report lists requirement IDs, test results, known issues, open assumptions, and next phase plan | **Security:** gate evidence comes from recorded test results and stored records only

#### Acceptance Criteria

1. WHEN a phase is completed, THE Platform SHALL provide a phase report listing the delivered requirement IDs, test results, known issues, open assumptions, and next phase plan.
2. WHEN work on a phase is requested, THE Platform SHALL require a recorded Founder review approval of the previous phase report before the phase starts.
3. WHEN a phase is completed, THE Platform SHALL build and run with all previously delivered features working.
4. THE Platform SHALL show only data, processing results, and success states that come from stored records or executed operations, in every phase.
5. WHEN the Phase 0 gate check runs, THE Platform SHALL confirm the repository structure, the passing CI pipeline, migrations that apply up and down, the required documentation set, and the absence of billable resources without a recorded Founder authorization.
6. WHEN the Phase 1 gate check runs, THE Platform SHALL confirm that all public pages render, that an inquiry form submission stores a Lead, a Project_Inquiry, and a Project, that the homepage meets the Lighthouse scores of at least 90 under R15, that the accessibility checks pass, and that no page shows the V1 tagline.
7. WHEN the Phase 2 gate check runs, THE Platform SHALL confirm invitation-based sign-in, passing Appendix A.3 matrix tests, passing tenant isolation property tests, the inquiry inbox, review, qualify, and reject actions, the Awaiting Information loop, notifications, Founder dashboard counts from stored records, and the Audit_Log.
8. WHEN the Phase 3 gate check runs, THE Platform SHALL confirm inquiry analysis, clarification, Technical_Assessment confirmation, validated architecture, Proposal versioning, human-approved pricing, approval-gated sending, client accept and decline, and Agreement records.
9. WHEN the Phase 4 gate check runs, THE Platform SHALL confirm the activation guard, Project_Milestones, Tasks, communication isolation, Deliverables, the quality gate, the handover gate, final acceptance, Support_Requests, Maintenance_Engagements, change requests, Commercial_Records, and a recorded Founder go or no-go decision for the Data Engineering Playground (A-04).
10. WHERE the Founder records a go decision for the Data Engineering Playground, THE Phase 4 gate check SHALL confirm that the tests for R56 to R63 pass.
11. WHEN the Phase 5 gate check runs, THE Platform SHALL confirm the ENGINE job type registry and idempotency, the R67 workflow completing without any Project status change, Approval_Requests blocking unapproved Sensitive_Actions, enforced cost limits, and the OPS dashboard.
12. WHEN the Phase 6 gate check runs, THE Platform SHALL confirm that R74, R75, R76, and R77 are met, that the restore test passed, and that the security review is recorded in `docs/SECURITY.md`.
13. WHEN the MVP acceptance check runs, THE Platform SHALL demonstrate this journey on one Project: a visitor submits an inquiry, the Founder reviews the inquiry and requests information, the client answers on the same inquiry, the inquiry is qualified, the Technical_Assessment is confirmed, the architecture is confirmed, a Proposal is drafted, priced by an Authorized_Approver, approved, and sent, the client accepts, the Agreement is In Effect, the Project is activated, Project_Milestones, Tasks, and updates are recorded, Deliverables are shared, testing passes the quality gate, the deployment is recorded and handover is complete, the client records final acceptance, the Project reaches Completed, and the client raises a Support_Request.
14. WHERE the Founder records a go decision for the Data Engineering Playground, THE MVP acceptance check SHALL include the Playground acceptance tests defined by R56 to R63.
15. WHEN the MVP acceptance check runs, THE Platform SHALL include the OPS acceptance checks of R67 and R68.
16. FOR ALL phases n greater than 0, the start record of phase n SHALL be later than the recorded Founder review approval of the phase n-1 report (phase order property).

## Appendix A: Status Models and Permission Matrix

This appendix is the status and permission source that R8, R17, R21, R24, and every requirement citing Appendix A refer to. R8.1 requires the API to hold each table below as machine-readable data, one source file per entity.

**Conventions used in this appendix**

- **System** means the API acting on a recorded event under the Platform principal. A System transition is never performed under an Internal_Agent or Agent_Runtime principal.
- **Authorized_Reviewer** means an internal user who holds the review permission for the action in A.3. **Authorized_Approver** means the Founder, or a user the Founder delegated under A-06.
- **Project Lead** means a current Project_Member with project role Project Lead (R44.4).
- **Client Owner** and **Client Member** are the Organization_Member roles of R25.5.
- **(inferred)** marks a row or cell that follows from requirement text where one detail (role, trigger, or status name) is not stated.
- **(proposed, Founder review)** marks a row that no requirement criterion states. The row is a proposal until the Founder confirms it.
- **Phase** is the first phase in which the transition is enabled. Under R8.6 and R24.4, a transition is enabled only when its target status and every entity its guard needs are delivered.
- Internal_Agent and Agent_Runtime are never an allowed role for a Project status transition (R21.8, R31.6, R67.10, R67.11).
- Every accepted transition writes an Audit_Log entry with prior status, new status, actor, time, and reason (R8.4, R24.13).

### A.1 Project Status Model

#### A.1.1 Project statuses

| Status | Stage | Client-facing label | Phase enabled | Terminal | Source |
|---|---|---|---|---|---|
| Draft | Inquiry | Draft, not yet sent | 2 | No | R24.3, R31.7 |
| Submitted | Inquiry | Received | 1 (creation only, R14.3); 2 (transitions, R24.3) | No | R14.3, R24.1, R24.3 |
| Under Review | Inquiry | Being reviewed | 2 | No | R24.3 |
| Awaiting Information | Inquiry | Waiting for your answers | 2 | No | R21.2, R24.3 |
| Qualified | Qualified project | Selected for technical assessment | 2 | No | R21.5, R24.3 |
| Assessment in Progress | Qualified project | Technical assessment underway | 2 | No | R29.1, R29.10 |
| Solution Designed | Qualified project | Solution designed | 3 | No | R29.10, R34.7 |
| Proposal Draft | Proposal stage | Preparing your proposal | 3 | No | Engagement Stage Definitions, R36 |
| Proposal Under Review | Proposal stage | Preparing your proposal | 3 | No | Engagement Stage Definitions, R40.8 |
| Proposal Sent | Proposal stage | Proposal sent | 3 | No | R40.8 |
| Awaiting Client Decision | Proposal stage | Proposal ready for your decision | 3 | No | R38.7, R40.8 |
| Accepted | Approved and accepted | Proposal accepted, agreement in preparation | 3 | No | R38.13, R44.1, A-35 |
| In Progress | Active engagement | Engineering underway | 4 | No | R44.1 |
| Testing | Active engagement | Testing | 4 | No | R44.1, R49.7 |
| Awaiting Client Acceptance | Active engagement | Preparing handover | 4 | No | R44.1, R49.8 |
| Delivered | Active engagement | Delivered, awaiting your acceptance | 4 | No | R44.1, R50.8, R51.3 |
| Completed | Closed | Completed | 4 | Yes | R44.1, R51.6 |
| On Hold | Paused | Paused | 2 | No | R24.3, R24.8 |
| Rejected | Closed | Not taken forward | 2 | Yes | R21.3, R24.3 |
| Cancelled | Closed | Cancelled | 2 | Yes | R24.3, R24.11 |

**Status order for R24.11 ("precedes Accepted").** Draft, Submitted, Under Review, Awaiting Information, Qualified, Assessment in Progress, Solution Designed, Proposal Draft, Proposal Under Review, Proposal Sent, Awaiting Client Decision, then Accepted, In Progress, Testing, Awaiting Client Acceptance, Delivered, Completed. A Project in On Hold takes the position of its stored prior status (inferred).

#### A.1.2 Project transitions

| # | From | To | Allowed roles | Guard | Source | Phase |
|---|---|---|---|---|---|---|
| T01 | (new record) | Submitted | System, on a Guest or Client inquiry submission | R14.3 validation, consent, honeypot, and rate limit pass; repeated submission token creates no second Project (R14.14, R41.10) | R14.3, R14.14, R24.1, R41.3, R41.6 | 1 |
| T02 | (new record) | Draft | System, on a signed-in Client saving Solution_Architect Lab output | User is signed in (R31.8) | R31.7, R31.8 | 3 |
| T03 | Draft | Submitted | Client Owner, Client Member of the owning Organization | R14.3 validation and consent pass on submission | R31.7, R14.3 (inferred: submit step for a saved draft) | 3 |
| T04 | Submitted | Under Review | Authorized_Reviewer (Founder, Administrator, Project_Manager, assigned Engineer) | None | (proposed, Founder review): no criterion states the trigger; R23 and R31.1 use the status | 2 |
| T05 | Under Review | Awaiting Information | Authorized_Reviewer | One or more Inquiry_Questions are set to Open in the same request (R21.2); from Phase 3, each question has a recorded approval (R33.2, R33.3) | R21.2, R33.2 | 2 |
| T06 | Awaiting Information | Under Review | System | A Client of the owning Organization answered the last Open Inquiry_Question of the Project | R24.7, R26.3, R33.5 | 2 |
| T07 | Under Review | Qualified | Authorized_Reviewer, human principal only | None stated | R21.5, R21.8 | 2 |
| T08 | Under Review | Rejected | Authorized_Reviewer, human principal only | Non-empty reason, stored with the decision | R21.3, R21.4, R21.8 | 2 |
| T09 | Awaiting Information | Rejected | Authorized_Reviewer, human principal only | Non-empty reason | R21.3, R21.4 (inferred: R21.3 does not limit the source status) | 2 |
| T10 | Submitted | Rejected | Authorized_Reviewer, human principal only | Non-empty reason | (proposed, Founder review): rejection without opening a review, for example spam | 2 |
| T11 | Qualified | Assessment in Progress | Engineer (assigned under R21.6), Founder | A Technical_Assessment is created in the same request; Project status is Qualified (R29.2) | R29.1, R29.2, R29.10 | 2 |
| T12 | Assessment in Progress | Solution Designed | Engineer (assigned), Founder (inferred roles) | A Confirmed Technical_Assessment_Version and a confirmed Solution_Architecture_Version exist | R34.7, R34.9, R29.10 | 3 |
| T13 | Solution Designed | Proposal Draft | System, when Engineer (assigned), Project_Manager, or Founder creates the first Proposal_Version in Draft | A Proposal_Version with status Draft exists; its architecture section references a confirmed Solution_Architecture_Version (R36.4) | R36.1, R36.4, R36.6 (inferred trigger) | 3 |
| T14 | Proposal Draft | Proposal Under Review | System, when a Proposal_Version of the Project moves from Draft to In Review | That Proposal_Version has status In Review | (proposed, Founder review): R36.2 names In Review but no criterion maps it to the Project status | 3 |
| T15 | Proposal Under Review | Proposal Draft | System, when the In Review Proposal_Version returns to Draft | No Proposal_Version of the Project is In Review or Approved | (proposed, Founder review) | 3 |
| T16 | Proposal Under Review | Proposal Sent | System, on a send executed by the Founder or a delegate (A-06) | Proposal_Version is Approved (R40.1, R40.2); an Approved Approval_Request for "issuing commercial quotations" and "sharing confidential information" has a content hash equal to the Proposal_Version hash (R40.3, R40.4); every price has an Authorized_Approver approval (R37.9) | R40.1 to R40.5, R40.8 | 3 |
| T17 | Proposal Sent | Awaiting Client Decision | System, in the same request as T16 | None | R40.8 | 3 |
| T18 | Awaiting Client Decision | Accepted | System | An Acceptance_Record exists for a Proposal_Version of the Project's Proposal, created by a Client Owner, a Client Member with the decision permission, or the Founder off-platform with an evidence reference (R38.5, R38.8, R38.9); no earlier accepted version exists (R38.11) | R38.13 | 3 (A-35) |
| T19 | Awaiting Client Decision | Proposal Draft | System, when a new Proposal_Version is created after a recorded Decline | A Decline is recorded on the Sent version (R38.6) | (proposed, Founder review): R38.6 records the decline and defines no Project status change | 3 |
| T20 | Accepted | In Progress | Founder, Project_Manager, Administrator (inferred roles, A-07) | The Project has an Agreement with status In Effect (R39.9, R44.2); on failure an Audit_Log entry is written (R44.3); on success Scope_Baseline version 1 is created (R54.1) | R39.9, R39.13, R44.2, R44.3 | 4 |
| T21 | In Progress | Testing | Project Lead, Founder | None | R49.7 | 4 |
| T22 | Testing | In Progress | Project Lead, Founder | None | (proposed, Founder review): rework after failed tests | 4 |
| T23 | Testing | Awaiting Client Acceptance | Project Lead, Project_Manager who is a current Project_Member, Founder (inferred roles: R49.8 says "a user") | No Defect with severity Blocker or Critical has a status other than Verified, Closed, or Won't Fix, and every acceptance criterion of every Project_Milestone is Met; on failure the error lists blocking Defects and unmet criteria (R49.9) | R49.8, R49.9, R49.11 | 4 |
| T24 | Awaiting Client Acceptance | Delivered | Project Lead, Project_Manager who is a current Project_Member, Founder (inferred roles: R50.8 says "a user") | Every mandatory Handover_Checklist item is Done; on failure the error lists open mandatory items (R50.9); on success the delivery reference and its content hash are computed (R51.2) | R50.8, R50.9, R50.12, R51.2 | 4 |
| T25 | Delivered | Completed | System | A final acceptance Acceptance_Record exists, created by a Client Owner, a Client Member with the decision permission, or the Founder off-platform with an evidence reference (R51.5, R51.9, R51.10) | R51.6, R51.13 | 4 |
| T26 | Delivered | In Progress | System | A final delivery rejection with a non-empty reason is recorded (R51.7, R51.8) | R51.7; choice of In Progress as the default target is (proposed, Founder review) | 4 |
| T27 | Delivered | Testing | System | Same as T26 | R51.7 permits this target; (proposed, Founder review): the Founder keeps exactly one of T26 or T27 | 4 |
| T28 | Any status except Completed, Rejected, Cancelled, On Hold | On Hold | Authorized_Reviewer (Founder, Administrator, Project_Manager) (inferred roles: R24.8 names none) | Non-empty reason; the reason and prior status are stored (R24.8, R24.9) | R24.8, R24.9 | 2 (from each status once that status is enabled) |
| T29 | On Hold | Stored prior status | Authorized_Reviewer | Target equals the stored prior status and is enabled in the current phase (R24.4); the entry guard of the prior status is not re-evaluated (proposed, Founder review) | R24.10 | 2 |
| T30 | Draft through Awaiting Client Decision, or On Hold whose stored prior status precedes Accepted | Cancelled | Client Owner, Client Member of the owning Organization | Current status (or stored prior status for On Hold) precedes Accepted; a request from Accepted or later is rejected (R24.12) | R24.11, R24.12 (On Hold case inferred) | 2 |
| T31 | Any status except Completed, Rejected, Cancelled | Cancelled | Founder | Non-empty reason | (proposed, Founder review): no requirement defines staff cancellation; R24.12 restricts only Client cancellation | 2 |
| T32 | Qualified, Assessment in Progress, Solution Designed | Rejected | Authorized_Reviewer, human principal only | Non-empty reason | (proposed, Founder review): R21.3 covers inquiry rejection only; declining after qualification is not stated | 2 (Solution Designed source from 3) |

**Events with no Project status change.** A Client Request Clarification keeps the Project in Awaiting Client Decision (R38.7). A Solution_Architect Job (R31.6, R31.14) and an R67 workflow run (R67.13) change no status. A new Proposal_Version sent while the Project is in Awaiting Client Decision follows T19, T14, T16, and T17 (proposed, Founder review).

**Notes on A.1**

- N1: Resolved by A-35. Accepted and T18 are enabled in Phase 3; activation to In Progress (T20) waits for Phase 4.
- N2: In the requirement text, Awaiting Client Acceptance is the handover-preparation status before Delivered, and the Client decides while the Project is Delivered (R51.3). The client-facing labels above follow that meaning. The Founder may want to rename the internal status.
- N3: R14.3 stores a Project in Submitted from Phase 1, before R24.3 enables the status set in Phase 2. T01 is therefore the only Project transition in Phase 1.

### A.2 Other Entity Status Tables

Each table lists the statuses and the transitions with From, To, allowed roles, guard, and source. "Staff (Assigned)" means a current Project_Member of the Project, plus the Founder and Administrators where R44.5 grants delivery writes. A transition not listed is rejected (R8.2), with HTTP 409 where the entity's requirement says so.

#### A.2.1 Lead

Statuses: New (proposed), Contacted (proposed), Converted (R25.4), Disqualified (proposed), Opted Out (proposed status name for the R22.8 opt-out), Merged (proposed status name for the R22.6 merge). R22.3 delegates the status set to this appendix and the text names none of these statuses except the conversion of R25.4.

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | New | System on inquiry storage; Lead Research Internal_Agent through its registered tool | A source is recorded for each data item (R22.2, R70.3, R70.4) | R22.1, R22.2, R70.3; status name (proposed, Founder review) |
| New | Contacted | Founder, Administrator, Project_Manager | Normalized email is not on the opt-out list (R22.9); external email only through the Founder-approved path (R27.11, A-09) | (proposed, Founder review) |
| New, Contacted | Converted | System, on Invitation acceptance | The Invitation bound to the Lead email is accepted (R25.4) | R25.4 |
| New, Contacted | Disqualified | Founder, Administrator, Project_Manager | Non-empty reason | (proposed, Founder review) |
| Any status except Merged | Opted Out | System, on an opt-out request | Normalized email is added to the opt-out list (R22.8) | R22.8; status name (proposed, Founder review) |
| Any status except Merged | Merged | Authorized_Reviewer approving the merge | Both Leads are flagged as possible duplicates (R22.5); every source and consent record is preserved (R22.6) | R22.5, R22.6; status name (proposed, Founder review) |

Opted Out and Merged have no outgoing transition (proposed, Founder review).

#### A.2.2 Inquiry_Question

Statuses: Draft (R33.1), Open, Answered, Withdrawn (R33.4).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Draft | Agent_Runtime or R67 workflow agent through its registered tool; Authorized_Reviewer adding a question manually | Linked to the Project_Inquiry | R33.1, R67.4 (Phase 3) |
| (new record) | Open | Authorized_Reviewer | The reviewer's own request counts as the approval (inferred) | R21.2 (Phase 2) |
| Draft | Open | Authorized_Reviewer | A recorded reviewer approval exists earlier than delivery (R33.2, R33.3, R33.10); for a Guest-submitted inquiry, the R25 Invitation is accepted or a Founder-approved email is used (R33.8) | R33.2, R33.3, R33.8 |
| Draft | Withdrawn | Authorized_Reviewer | None | (proposed, Founder review): discard a draft |
| Open | Answered | Client Owner, Client Member of the owning Organization | Non-empty answer within the configured maximum length; question belongs to the Client's Organization (R33.6) | R26.3, R33.5; triggers Project T06 |
| Open | Withdrawn | Authorized_Reviewer | None | R33.4, R33.9 (roles inferred) |

Answered and Withdrawn are terminal. (proposed, Founder review): when withdrawing the last Open question of a Project in Awaiting Information, the System also applies a move to Under Review, because R24.7 covers answers only.

#### A.2.3 Attachment

Statuses: pending scan (inferred name, R20.8), available, quarantined, rejected, deleted.

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (complete-upload) | pending scan | System | The object exists in storage (R20.3) | R20.3 |
| pending scan | rejected | System | Extension, inspected content type, or size check fails; the stored object is deleted (R20.7) | R20.4 to R20.7 (order of validation before scan inferred) |
| pending scan | available | System | Validation passed and the malware scan reported clean | R20.8 |
| pending scan | quarantined | System | Malware detected or scanner unavailable; an internal Notification is sent | R20.9, R27.5 |
| quarantined | pending scan | Founder, Administrator | The quarantine reason was "scanner unavailable" | (proposed, Founder review) |
| available, quarantined | deleted | Founder; Administrator by delegation | An Approved Approval_Request for deletion whose content hash equals the hash of the deletion parameters (R73.10) | R73.10 as revised by A-36 (staff-initiated deletion) |

A download Presigned_URL is issued only in status available (R20.12).

#### A.2.4 Invitation

Statuses: pending (inferred name), accepted, expired, revoked.

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | pending | Authorized_Reviewer; Client Owner for the Owner's own Organization only | Bound to a normalized email and one Organization; expiry set from the configured period (R25.3); a request naming another Organization returns HTTP 404 (R25.8) | R16.2, R25.1, R25.3, R25.7, R25.8 |
| pending | accepted | System, on registration | Not expired, not revoked, not used, and the registering email matches after normalization (R16.4, R25.9, R25.10) | R16.3, R25.4, R25.13 |
| pending | expired | System | Expiry time reached | R25.3, R25.9 |
| pending | revoked | Authorized_Reviewer; the issuing Client Owner | Not accepted | R25.11 |

accepted, expired, and revoked are terminal. The "rejected" event in R25.12 is a rejected registration attempt and is not an Invitation status (inferred).

#### A.2.5 Technical_Assessment_Version

Statuses: Unconfirmed (AI-generated, R34.4), Confirmed (R34.5). Content is immutable once stored; an edit stores a new version (R29.9, R29.13).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Unconfirmed | Agent_Runtime Job requested by an assigned Engineer or the Founder | A stored analysis exists (R34.1); labels are from the six service groups (R34.2); complexity has a justification (R34.3) | R34.1 to R34.4 (Phase 3) |
| (new record) | Confirmed | Assigned Engineer, Founder, saving a manual or edited version | R29.3 to R29.6 validation passes | R29.9, R34.5 (Phase 2 human versions treated as Confirmed: inferred) |
| Unconfirmed | Confirmed | Assigned Engineer, Founder | Confirming user and timestamp recorded; any other role receives HTTP 403 (R34.6) | R34.5, R34.6 |

#### A.2.6 Solution_Architecture_Version

Statuses: draft, confirmed (R35.8).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | draft | Agent_Runtime Job; assigned Engineer or Founder storing a change | Graph schema valid (R35.1, R35.2); non-empty rationale per stack item and decision (R35.3) | R35.1 to R35.4 |
| draft | confirmed | Assigned Engineer, Founder | None stated | R35.8 |

Client visibility is separate from status: Internal_Only until included in an Approved Proposal_Version (R35.9, R35.10).

#### A.2.7 Project_Requirements_Version

Status: Draft, marked AI-generated and Internal_Only (R32.13).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Draft | System, storing validated R32 Job output requested by an Authorized_Reviewer or Engineer | Output passed schema validation (R32.9, R32.10) | R32.13, R33.7 |

No requirement defines a transition out of Draft. A Confirmed status is (proposed, Founder review) if the Founder wants human sign-off on requirements.

#### A.2.8 Proposal_Version

Statuses: Draft, In Review, Approved, Sent, Superseded, Withdrawn (R36.2). Acceptance and decline are recorded as Acceptance_Records and decisions, not as version statuses (R38.5, R38.6).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Draft | Agent_Runtime on request, marked AI-generated; assigned Engineer, Project_Manager, or Founder for manual drafting (inferred) | Architecture section references a confirmed Solution_Architecture_Version, else HTTP 422 (R36.4); preliminary statement present (R36.7) | R36.4, R36.6, R36.7 |
| Draft | In Review | Assigned Engineer, Project_Manager, Founder | All R36.3 sections present | (proposed, Founder review) |
| In Review | Draft | Assigned Engineer, Project_Manager, Authorized_Approver | None | (proposed, Founder review) |
| In Review | Approved | Authorized_Approver | Every price was entered or approved by an Authorized_Approver (R37.1); on entry the content hash is stored and content is frozen (R36.9) | R36.9, R37.1, A-06 (approver role inferred from A-06) |
| Approved | Sent | Founder; delegate under A-06 | Status is Approved (R40.1, R40.2); a matching Approved Approval_Request exists, else HTTP 403 and an Audit_Log entry (R40.3, R40.4) | R40.1 to R40.5 |
| Sent | Superseded | System | Another version of the same Proposal is Sent (R40.7) or accepted (R38.12) | R38.12, R40.7 |
| Approved | Superseded | System | A later version of the same Proposal is Sent | (proposed, Founder review) |
| Draft, In Review, Approved | Withdrawn | Founder; delegate under A-06 | Non-empty reason | (proposed, Founder review): R36.2 names the status and no criterion sets it |
| Sent | Withdrawn | Founder; delegate under A-06 | No Acceptance_Record exists on the version; non-empty reason | (proposed, Founder review) |

A change to an Approved, Sent, Superseded, or Withdrawn version is rejected (R36.10). A Sent version that receives an Acceptance_Record stays Sent (inferred).

#### A.2.9 Approval_Request

Statuses: Pending, Approved, Rejected, Expired, Invalidated (R43.2).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Pending | Engineer, Project_Manager, Founder; Internal_Agent as requester only | Action type, target, exact content or parameters with content hash, requester, and rationale are present (R43.1) | R43.1, R68.1 |
| Pending | Approved | Authorized_Approver, human principal only | Any other principal receives HTTP 403 and an Audit_Log entry (R43.4) | R43.3, R43.4, R68.3 |
| Pending | Rejected | Authorized_Approver, human principal only | Non-empty reason (R43.9, R69.7) | R43.3, R43.9, R69.7 |
| Pending | Expired | System, through the scheduled job type of R64.14 | Configured expiry period reached (A-08) | R43.7, R64.14 |
| Approved | Invalidated | System | Content or parameters changed before execution | R43.6, R68.5 |
| Pending | Invalidated | System | Content or parameters changed while Pending | (proposed, Founder review) |

Rejected, Expired, and Invalidated are terminal. Execution of an Approved request is recorded in the Audit_Log (R68.9) and is not a status.

#### A.2.10 Agreement

Statuses: Draft, Pending Signature, In Effect, Expired, Terminated (R39.6). Only the Founder or an Administrator may create or change an Agreement (R39.3).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Draft | Founder, Administrator | An Acceptance_Record exists on a Proposal_Version of the Project, else HTTP 422 (R39.1, R39.2); end date not before effective date (R39.5) | R39.1 to R39.5 |
| Draft | Pending Signature | Founder, Administrator | None | (proposed, Founder review) |
| Pending Signature | In Effect | Founder, Administrator | The signed document is stored as an available Attachment (R39.7) | (proposed, Founder review) for the guard; R39.7 |
| In Effect | Expired | System | The end date has passed | (inferred from the optional end date of R39.4) |
| In Effect | Terminated | Founder, Administrator | Non-empty reason | (proposed, Founder review) |
| Draft, Pending Signature | Terminated | Founder, Administrator | Non-empty reason | (proposed, Founder review) |

Expired and Terminated are terminal.

#### A.2.11 Project_Milestone

Statuses: Planned, In Progress, Ready for Review, Accepted, Rejected (R45.2).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Planned | Staff (Assigned) | Name and dates present; due date not before planned start (R45.3) | R45.1, R45.3, R44.5 |
| Planned | In Progress | Staff (Assigned) | None | (proposed, Founder review) |
| In Progress | Ready for Review | Staff (Assigned) | None | (proposed, Founder review) |
| Ready for Review | Accepted | Client Owner; Client Member with the decision permission; Founder recording an off-platform acceptance with evidence (A-19) | Milestone is Client_Visible; an Acceptance_Record is created (R45.4) | R45.4, R45.6, A-19 |
| Ready for Review | Rejected | Client Owner; Client Member with the decision permission | Milestone is Client_Visible; non-empty reason stored in the Acceptance_Record (R45.5, R45.6) | R45.5, R45.6 |
| Rejected | In Progress | Staff (Assigned) | None | (proposed, Founder review): rework |
| Ready for Review | Accepted | Project_Manager who is a current Project_Member, Founder | Milestone is Internal_Only, so no Client can decide | (proposed, Founder review) |

Accepted is terminal.

#### A.2.12 Task

Statuses: To Do, In Progress, Blocked, Done, Cancelled (R46.2). R46.2 delegates the transitions to this appendix; every row below except the creation row is (proposed, Founder review). A Client create, edit, or status change returns HTTP 403 (R46.7).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | To Do | Staff (Assigned) | Assignee is a current Project_Member (R46.3) | R46.1, R46.3 |
| To Do | In Progress | Staff (Assigned) | None | (proposed, Founder review) |
| To Do, In Progress | Blocked | Staff (Assigned) | Non-empty reason (R46.4) | R46.4; row (proposed, Founder review) |
| Blocked | In Progress | Staff (Assigned) | None | (proposed, Founder review) |
| In Progress | Done | Staff (Assigned) | None | (proposed, Founder review) |
| To Do, In Progress, Blocked | Cancelled | Staff (Assigned) | None | (proposed, Founder review) |
| Done | In Progress | Staff (Assigned) | None | (proposed, Founder review): reopen |

#### A.2.13 Deliverable version

Statuses: draft (inferred name), Approved for Client (R48.6), Accepted, Rejected (inferred names for the R48.8 decisions). A revision creates a new version (R48.2).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | draft | Staff (Assigned) | File stored through R20 and available; a Source-Code Handover Reference holds a repository URL and commit or tag, with no embedded credentials (R48.3, R48.4, R48.5) | R48.2 to R48.5 |
| draft | Approved for Client | Holder of the Deliverable approval permission in A.3 | None beyond the creation guard | R48.6 |
| Approved for Client | Accepted | Client Owner; Client Member with the decision permission; Founder off-platform with evidence (A-19) | An Acceptance_Record is created | R48.8 |
| Approved for Client | Rejected | Client Owner; Client Member with the decision permission | Non-empty reason in the Acceptance_Record | R48.8 |

#### A.2.14 Defect

Statuses: Open, In Progress, Resolved, Verified, Closed, Won't Fix (R49.3). Severity: Blocker, Critical, Major, Minor (A-18). R49.3 delegates the transitions; rows without a guard from R49 are (proposed, Founder review).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Open | Staff (Assigned) | Severity in the A-18 set | R49.3 |
| Open | In Progress | Staff (Assigned) | None | (proposed, Founder review) |
| In Progress | Resolved | Staff (Assigned) | Non-empty resolution note (R49.4) | R49.4; row (proposed, Founder review) |
| Resolved | Verified | Staff (Assigned) | None | (proposed, Founder review) |
| Resolved | In Progress | Staff (Assigned) | None | (proposed, Founder review): verification failed |
| Verified | Closed | Staff (Assigned) | None | (proposed, Founder review) |
| Open, In Progress | Won't Fix | Staff (Assigned); Founder only for severity Blocker or Critical | Non-empty resolution note (R49.4); for Blocker or Critical, a recorded Founder approval, else rejection and an Audit_Log entry (R49.5) | R49.4, R49.5 |
| Closed, Won't Fix | Open | Staff (Assigned) | None | (proposed, Founder review): reopen |

#### A.2.15 Deployment_Record

Statuses: Planned, In Progress, Succeeded, Failed, Rolled Back (R50.2). An undefined transition returns HTTP 409. A Client write returns HTTP 403 (R50.10). Every field is checked against the configured secret detection patterns (R50.3).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Planned | Staff (Assigned), Project_Manager, Founder | Environment type in {dev, staging, production}; version or commit reference present; no secret pattern match | R50.1, R50.3 |
| Planned | In Progress | Staff (Assigned), Project_Manager, Founder | None | (proposed, Founder review) |
| In Progress | Succeeded | Staff (Assigned), Project_Manager, Founder | None | (proposed, Founder review) |
| In Progress | Failed | Staff (Assigned), Project_Manager, Founder | None | (proposed, Founder review) |
| Succeeded, Failed | Rolled Back | Staff (Assigned), Project_Manager, Founder | None | (proposed, Founder review) |

#### A.2.16 Handover_Checklist item

Statuses: Open, Done (R50.6). A Client write returns HTTP 403 (R50.10).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Open | Staff (Assigned), Project_Manager, Founder | No secret pattern match (R50.3) | R50.6 |
| Open | Done | Staff (Assigned), Project_Manager, Founder | For a mandatory item, an evidence Attachment or evidence note (R50.7) | R50.6, R50.7 |
| Done | Open | Staff (Assigned), Project_Manager, Founder | None | (proposed, Founder review) |

#### A.2.17 Support_Request

Statuses: New, Triaged, In Progress, Awaiting Client, Resolved, Closed (R52.4). R52.4 delegates the transitions; rows other than creation are (proposed, Founder review). An undefined transition returns HTTP 409.

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | New | Client Owner, Client Member of the owning Organization | Type in {bug, question, improvement, incident}; title and description present; Project of the Client's Organization (else HTTP 404) in In Progress, Testing, Awaiting Client Acceptance, Delivered, or Completed | R52.1 to R52.3 |
| New | Triaged | Staff (Assigned), Project_Manager, Founder | None | (proposed, Founder review) |
| Triaged | In Progress | Staff (Assigned), Project_Manager, Founder | None | (proposed, Founder review) |
| In Progress | Awaiting Client | Staff (Assigned), Project_Manager, Founder | None | (proposed, Founder review) |
| Awaiting Client | In Progress | System, on a Client comment; Staff (Assigned), Project_Manager, Founder | None | (proposed, Founder review) |
| In Progress | Resolved | Staff (Assigned), Project_Manager, Founder | None | (proposed, Founder review) |
| Resolved | Closed | Staff (Assigned), Project_Manager, Founder; Client Owner or Client Member of the owning Organization | None | (proposed, Founder review) |
| Resolved | In Progress | Client Owner or Client Member of the owning Organization; Staff (Assigned), Project_Manager, Founder | None | (proposed, Founder review): reopen |
| New, Triaged | Closed | Staff (Assigned), Project_Manager, Founder | Non-empty reason | (proposed, Founder review): duplicate or out of scope |

#### A.2.18 Maintenance_Engagement

Statuses: Proposed, Active, Suspended, Ended (R53.2). An undefined transition returns HTTP 409.

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Proposed | Founder, Administrator, Project_Manager | Exactly one originating Project of the same Organization; scope description present | R53.1 |
| Proposed | Active | Founder, Administrator, Project_Manager (inferred roles) | An Agreement under R39 with status In Effect; on failure an Audit_Log entry (R53.4) | R53.3, R53.4, R53.11 |
| Active | Suspended | Founder, Administrator, Project_Manager (inferred roles) | Non-empty reason (R53.5) | R53.5 |
| Suspended | Active | Founder, Administrator, Project_Manager (inferred roles) | An Agreement with status In Effect (R53.11 applies to every transition to Active) | R53.11 (inferred row) |
| Active, Suspended | Ended | Founder, Administrator, Project_Manager (inferred roles) | Non-empty reason (R53.5) | R53.5 |
| Proposed | Ended | Founder, Administrator, Project_Manager | Non-empty reason | (proposed, Founder review): abandoned before start |

#### A.2.19 Change_Request

Statuses: Submitted, Under Review, Approved, Rejected, Withdrawn, Implemented (R54.5). An undefined transition returns HTTP 409.

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Submitted | Client Owner, Client Member of the owning Organization; Project_Member of the Project | Project status in In Progress, Testing, Awaiting Client Acceptance, or Delivered; description, reason, and scope, timeline, and cost impact present; an Internal_Agent request returns HTTP 403 and an Audit_Log entry (R54.4) | R54.3, R54.4 |
| Submitted | Under Review | Project_Manager, Project Lead, Founder | None | (proposed, Founder review) |
| Under Review | Approved | Without timeline or cost impact: Founder or Project_Manager (R54.7). With timeline or cost impact: Founder or a delegated Authorized_Approver through R43 (R54.6) | An Acceptance_Record from a Client Owner or Client Member with the decision permission, or a Founder-recorded off-platform acceptance with evidence, exists for the Change_Request content hash (R54.8); with timeline or cost impact, an Approved Approval_Request with an equal content hash (R54.6) | R54.6, R54.7, R54.8 |
| Under Review | Rejected | Founder, Project_Manager; for timeline or cost impact, Founder or a delegated Authorized_Approver | Non-empty reason | (proposed, Founder review) |
| Submitted, Under Review | Withdrawn | The submitter; Founder | None | (proposed, Founder review) |
| Approved | Implemented | System, on an implementation request by the Project Lead, a Project_Manager who is a current Project_Member, or the Founder (inferred roles) | A new Scope_Baseline version referencing the Change_Request is created; earlier versions are unchanged (R54.9) | R54.9, R54.13 |

#### A.2.20 Commercial_Record

Statuses: Draft, Issued, Paid Recorded, Overdue, Void (R79.2). An undefined transition returns HTTP 409. No Internal_Agent or AI component holds any transition (R79.7, R68.7, R68.8).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Draft | Founder; delegate of the Founder (A-06) | Type in the R79.1 set; non-negative amount; ISO 4217 currency; due date; links only to records of the same Project (R79.3, R79.4); no card number or bank credential pattern match (R79.12) | R79.1 to R79.7, R79.12 |
| Draft | Issued | Founder; delegate | An Approval_Request for "issuing commercial quotations" with status Approved and a content hash equal to the Commercial_Record content hash; on failure an Audit_Log entry (R79.9) | R79.8, R79.9 |
| Issued | Overdue | System, through the scheduled job type of R64.14 | Current date is after the due date | R79.13, R64.14 (stored status rather than a computed report: inferred) |
| Issued, Overdue | Paid Recorded | Founder; delegate | Evidence reference present; recording user and time stored (R79.10, R79.11) | R79.10, R79.11 (Overdue source inferred) |
| Draft, Issued, Overdue | Void | Founder; delegate | Non-empty reason | (proposed, Founder review) |

#### A.2.21 Lab registration

Statuses: disabled, internal, client beta, available (R55.1).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| Any status | Any other status | Founder; Administrator delegated by the Founder | For the Data Engineering Playground in production, leaving disabled requires a recorded Founder go decision at the Phase 4 gate (R55.11, R78.9) | R55.1, R55.7, R55.11 |

R55 places no restriction on the order of Lab status changes, so every pair is allowed.

#### A.2.22 Dataset, Profile, Pipeline, Recommendation, and Execution

**Dataset.** Statuses: pending scan (inferred name), available, rejected, quarantined, deleted.

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (complete-upload) | pending scan | System | Object exists (R56.10); permission confirmation recorded (R56.8); Guest requests return HTTP 401 (R56.3) | R56.3, R56.8, R56.10 |
| pending scan | rejected | System | Extension, inspected content type, size, structure, or row count check fails; object deleted | R56.13, R56.14 |
| pending scan | quarantined | System | Malware detected or scanner unavailable | R56.15 |
| pending scan | available | System | Every check of R56.20 passed | R56.20 |
| available | deleted | Client Owner or Client Member of the owning Organization, Founder, Administrator | Dataset of the requester's Organization, else HTTP 404 (R63.7); no Approval_Request required (A-36) | R63.1, R63.6, R63.7 |
| available | deleted | System, through the retention job | Configured retention period expired | R63.2, R63.9 |

**Profiling Job.** Statuses: queued, running, completed, failed (R57.8). These map to the R64 Job statuses Queued, Running, Succeeded, and Failed (inferred). A failed profiling Job stores no partial Profile (R57.7).

**Pipeline version approval.** Each Pipeline version is unapproved or approved.

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| unapproved | approved | Client Owner, Client Member of the owning Organization; Founder, Administrator, Engineer, Project_Manager | Validation passes (R59.7, inferred as a guard); destructive Operations confirmed by name (R59.11) | R59.8, R59.11, R59.14 |
| approved | unapproved | System | The Pipeline is changed after approval; the change creates a new version and the approval is cleared | R59.6, R59.9, R59.14 |

**Recommendation.** A Recommendation is discarded with a reason when it names an Operation outside the allowlist or fails the parameter schema (R58.6). An accepted Recommendation joins a Pipeline only when a user approves it (R58.10).

**Execution.** Statuses: queued, running, completed, failed (status names inferred from the R57.8 set).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | queued | System, on an execute request by a user permitted to approve the Pipeline | The current Pipeline version is approved, else HTTP 409 and no Job (R59.10) | R59.10, R60.1 |
| queued | running | System | None | R60.6 (inferred) |
| running | completed | System | Every Operation succeeded | R60.3, R61.1 |
| running | failed | System | An Operation failed (R60.4), or the time or resource limit was exceeded (R60.8), or retries were exhausted (R60.10); a Notification is sent (R60.5) | R60.4, R60.5, R60.8, R60.10 |

#### A.2.23 Job

Statuses: Queued, Running, Succeeded, Failed, Cancelled (R64.5).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Queued | System (API feature endpoints); Founder, Administrator; Internal_Agent as requester only | Job type is in the registry, else rejection and an Audit_Log entry (R64.2); parameters pass the job type schema (R64.3); dedupe key present, and a matching key returns the existing Job (R64.6) | R64.2 to R64.6 |
| Queued | Running | System worker | None | R64.5 (inferred) |
| Running | Succeeded | System | Registered handler completed | R64.5, R64.17 |
| Running | Failed | System | Retries exhausted (R64.7); CPU, memory, or time limit exceeded (R64.8); cross-Organization or out-of-permission request (R64.10); a dead-letter record and a Notification follow (R64.11, R64.12) | R64.7 to R64.12 |
| Running | Queued | System | Transient infrastructure failure with fewer than 3 retries used | R64.7; modelling the retry as a status change is (proposed, Founder review), the alternative being an attempt counter while Running |
| Queued, Running | Cancelled | Job owner, Founder, Administrator | None | R64.13 (roles inferred) |

#### A.2.24 Agent_Task

Statuses: Queued, Running, Succeeded, Failed, Awaiting Approval, Cancelled (R66.3).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Queued | Orchestrator Internal_Agent through its task creation tool; System for the R67 workflow; Founder | Per-day agent cost limit not reached, else rejection naming the limit (R66.7, R66.8) | R65.11, R66.1, R66.8, R67.3 |
| Queued | Running | System | No other Agent_Task is Running; per-day cost limit checked before start (R66.12) | R66.12 |
| Running | Succeeded | System | Output validates against the agent output schema (R65.7) | R65.7, R65.15 |
| Running | Failed | System | Output schema failure (R65.8); per-task token limit reached (R66.6); retries exhausted (R66.5); workflow step failure (R67.7) | R65.8, R66.5, R66.6, R67.7 |
| Running | Awaiting Approval | System | The agent proposed a Sensitive_Action and an Approval_Request was created (R68.1) | R68.1, R68.2 |
| Awaiting Approval | Running | System | The Approval_Request is Approved and the content hash matches (R68.4) | R68.4 (intermediate status inferred) |
| Awaiting Approval | Cancelled | System | The Approval_Request is Rejected, Expired, or Invalidated | R68.6 |
| Queued | Cancelled | Founder | None | (proposed, Founder review) |
| Running | Queued | System | Transient failure with fewer than 3 retries used | R66.5; same modelling choice as the Job retry row (proposed, Founder review) |

#### A.2.25 content_items

Statuses: Draft, In Review, Approved, Scheduled, Published, Rejected (R71.5). Internal_Agents create Drafts only and hold no status transition.

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| (new record) | Draft | Content or Marketing Internal_Agent through its registered tool; Founder | Each factual claim lists a verified project record or is flagged unsupported (R71.2, R71.3) | R71.1 to R71.3 |
| Draft | In Review | Founder; delegated Authorized_Approver | None | (proposed, Founder review) |
| In Review | Approved | Authorized_Approver | No claim flagged unsupported, else an error listing the claims (R71.4) | R71.4 |
| In Review | Rejected | Authorized_Approver | Non-empty reason | (proposed, Founder review) |
| Rejected | Draft | Founder | None | (proposed, Founder review) |
| Approved | Scheduled | Founder; delegated Authorized_Approver | None | (proposed, Founder review) |
| Approved, Scheduled | Published | System (OPS) | An Approved Approval_Request under R68 with a content hash equal to the content_item hash (R71.6) | R71.6, R71.8 |

#### A.2.26 Organization

Statuses: active (inferred name), suspended (R73.7).

| From | To | Allowed roles | Guard | Source |
|---|---|---|---|---|
| active | suspended | Founder; Administrator permitted by the Founder | Non-empty reason | R73.7 |
| suspended | active | Founder; Administrator permitted by the Founder | None | R73.9 |

While suspended, requests from users of the Organization return HTTP 403 (R73.8).

### A.3 Permission Matrix

**Cell values**

- **Y**: granted.
- **N**: not granted.
- **Own org**: granted only for records of an Organization in which the user is an Organization_Member (R18.1, R18.2).
- **Assigned**: granted only on Projects where the user is a current Project_Member (R44.5, R44.6). "Assigned (Project Lead)" requires the project role Project Lead.
- **Delegated**: granted only to a named user to whom the Founder delegated the permission (A-06; "permitted Administrator" in R55.7, R73.5, R73.7, R73.9). The default is no delegation.
- **Configured**: for a Client Member, granted where the Founder enabled the permission for that Organization (R38.3, R51.3, A-07). For an Internal_Agent, granted only when the operation is in that agent's registered tool list and permission set (R17.7, R65.1, R65.12). For a Guest or Client on a Lab, granted within the Lab status and the configured Guest limit (R31.8, R55.3 to R55.6).
- **(A-07)**: a default the Founder must confirm.

**Rules applied to every row**

- The Founder holds every permission (R17.3). For Client decision rows, the Founder exercises the permission only by recording an off-platform decision with an evidence reference (A-19, R38.8, R51.9, R54.8).
- An Internal_Agent holds no approval, decision, status change, price, Commercial_Record amount, configuration, or role assignment permission (R17.7, R17.8, R21.8, R43.4, R54.4, R65, R67.10, R68.7, R79.7). Its "Configured" cells cover registered tool operations only.
- The Authorized_Approver is the Founder unless the Founder delegates (A-06), so every approval cell for other staff roles is Delegated.
- Writes to delivery records require a current Project_Member, the Founder, or an Administrator (R44.5, R44.10).

#### Public site

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| View public pages | Y | Y | Y | Y | Y | Y | Y | N | R9.7 |
| Submit a project inquiry or Engineering_Service_Request | Y | Own org | Own org | Y | Y (A-07) | Y (A-07) | Y (A-07) | N | R14.3, R41.3, R41.4 |
| Run Solution_Architect Lab analysis | Configured | Configured | Configured | Y | Y | Y | Y | N | R31.7 to R31.10, R55 |
| Save Lab output as an inquiry draft; submit the draft (T02, T03) | N | Own org | Own org | Y | N (A-07) | N (A-07) | N (A-07) | N | R31.8, R41.8 |
| Request opt-out for one's own email | Y | Y | Y | Y | Y | Y | Y | N | R22.8 |

#### Inquiries and leads

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| List and view Project_Inquiries | N | Own org | Own org | Y | Y | Assigned (A-07) | Y (A-07) | Configured | R21.1, R23.1, R26.2, R67.1 |
| View and edit Leads, sources, and consent records | N | N | N | Y | Y | N (A-07) | Y | Configured (Lead Research: create Lead data items with a source only) | R22, R70.3, R70.4 |
| Approve a Lead merge | N | N | N | Y | Y (A-07) | N (A-07) | Y (A-07) | N | R22.6 |
| Record an opt-out for a Lead | N | N | N | Y | Y | N | Y | N | R22.8 |
| Contact a Lead or send external email | N | N | N | Y | Delegated | N | Delegated | N (drafts only) | R22.9, R27.11, R70.5, R70.6, A-09 |

#### Invitations

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Invite a Prospective_Client into an Organization; edit the new Organization name | N | N | N | Y | Y | N (A-07) | Y | N | R16.2, R25.1, R25.2 |
| Invite a person to one's own Organization | N | Own org | N | Y | N | N | N | N | R25.7, R25.8 |
| Revoke an unaccepted Invitation | N | Own org (Invitations the Owner issued) | N | Y | Y | N (A-07) | Y | N | R25.11 |

#### Review and qualification

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Start review (T04) | N | N | N | Y | Y (A-07) | Assigned (A-07) | Y (A-07) | N | T04 (proposed) |
| Request information (T05) | N | N | N | Y | Y (A-07) | Assigned (A-07) | Y (A-07) | N | R21.2 |
| Qualify an inquiry (T07) | N | N | N | Y | Y (A-07) | N (A-07) | Y (A-07) | N | R21.5, R21.8 |
| Reject an inquiry or opportunity (T08 to T10, T32) | N | N | N | Y | Y (A-07) | N (A-07) | Y (A-07) | N | R21.3, R21.8 |
| Assign a technical reviewer | N | N | N | Y | Y | N | Y | N | R21.6 |
| Place On Hold and resume (T28, T29) | N | N | N | Y | Y (A-07) | N (A-07) | Y (A-07) | N | R24.8 to R24.10 |
| Cancel a Project before Accepted (T30) | N | Own org | Own org | Y | N | N | N | N | R24.11, R24.12 |
| Staff cancellation (T31) | N | N | N | Y | N | N | N | N | T31 (proposed) |
| Answer an Open Inquiry_Question | N | Own org | Own org | Y | N | N | N | N | R26.3, R33.5 |
| Request AI analysis and re-analysis | N | N | N | Y | N (A-07) | Assigned | Y (A-07) | Configured (R67 workflow) | R32.1, R33.7, R67.4 |
| Create draft Inquiry_Questions | N | N | N | Y | Y (A-07) | Assigned (A-07) | Y (A-07) | Configured | R33.1, R67.4 |
| Approve and send, or withdraw, an Inquiry_Question | N | N | N | Y | Y (A-07) | Assigned (A-07) | Y (A-07) | N | R33.2 to R33.4 |
| Invoke the Solution_Architect on a Project | N | N | N | Y | N (A-07) | Assigned | Y (A-07) | N | R31.1 to R31.3 |
| Publish part of a Solution_Architect_Draft to the Client | N | N | N | Y | N (A-07) | Assigned (A-07) | Y (A-07) | N | R31.4, R31.5 |
| View Internal_Only AI analysis and drafts | N | N | N | Y | Y | Assigned | Y | Configured | R31.4, R32.13 |

#### Assessments and architecture

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Start and edit a Technical_Assessment (T11); request an AI draft | N | N | N | Y | N | Assigned | N | N | R29.1, R29.9, R34.1 |
| Confirm a Technical_Assessment_Version | N | N | N | Y | N | Assigned | N | N | R34.5, R34.6 |
| Create and confirm a Solution_Architecture_Version | N | N | N | Y | N | Assigned | N | N | R35.4, R35.8 |
| Move a Project to Solution Designed (T12) | N | N | N | Y | N | Assigned | N (A-07) | N | R34.7 |
| View Technical_Assessments | N | N | N | Y | Y (A-07) | Assigned | Y (A-07) | N | R29.7, R29.8 |
| View a Solution_Architecture_Version | N | Own org (only when included in a Sent Proposal_Version) | Own org (same) | Y | Y (A-07) | Assigned | Y | N | R35.9, R35.10, R38.1 |
| Export a Solution_Architecture_Version as JSON | N | N | N | Y | N (A-07) | Assigned | Y (A-07) | N | R35.7 |

#### Proposals and pricing

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Create or edit a Draft Proposal_Version; request an AI draft | N | N | N | Y | N | Assigned | Y (A-07) | N | R36.6 |
| Submit a Proposal_Version for review; return it to Draft | N | N | N | Y | N | Assigned (A-07) | Y (A-07) | N | A.2.8 (proposed rows) |
| Approve a Proposal_Version | N | N | N | Y | Delegated | Delegated | Delegated | N | R36.9, A-06 |
| Enter or approve a price | N | N | N | Y | Delegated | Delegated | Delegated | N | R37.1 to R37.3, R68.7, R68.8 |
| Request and view an indicative AI Cost_Estimate | N | N | N | Y | N (A-07) | Assigned | Y (A-07) | N | R37.4 to R37.6 |
| Send a Proposal_Version | N | N | N | Y | Delegated | Delegated | Delegated | N | R40.1 to R40.5, A-06 |
| Withdraw a Proposal_Version | N | N | N | Y | Delegated | Delegated | Delegated | N | A.2.8 (proposed rows) |
| View Draft, In Review, or Approved Proposal_Versions | N | N | N | Y | Y (A-07) | Assigned | Y | N | R38.2 |
| View Sent Proposal_Versions | N | Own org | Own org | Y | Y (A-07) | Assigned | Y | N | R38.1 |
| Export a Proposal_Version (Approved or Sent for staff; Sent only for Clients) | N | Own org | Own org | Y | N (A-07) | Assigned | Y | N | R36.11, R40.9, R40.10 |

#### Approvals

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Create an Approval_Request | N | N | N | Y | N (A-07) | Y | Y | Configured (requester only) | R43.1, R68.1 |
| Decide an Approval_Request | N | N | N | Y | Delegated | Delegated | Delegated | N | R43.3, R43.4, R68.3, R69.6 |
| View pending Approval_Requests | N | N | N | Y | Y (read only) | Delegated | Delegated | N | R69.1, R69.6, R73.1 |

#### Agreements and commercial records

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Create or change an Agreement, attach the signed document, change Agreement status | N | N | N | Y | Y | N | N | N | R39.1 to R39.3, R39.6, R39.7 |
| View the full Agreement record and Internal_Only notes | N | N | N | Y | Y | N (A-07) | Y (A-07) | N | R39.10 |
| View Agreement status and the approved signed document | N | Own org | Own org | Y | Y | N (A-07) | Y (A-07) | N | R39.11 |
| Create or change a Commercial_Record, its amount, visibility, Paid Recorded, or Void | N | N | N | Y | Delegated | Delegated | Delegated | N | R79.5 to R79.7, R79.10, R79.14 |
| Issue a Commercial_Record (requires an Approved Approval_Request) | N | N | N | Y | Delegated | Delegated | Delegated | N | R79.8 |
| View Internal_Only Commercial_Records | N | N | N | Y | Y (A-07) | N (A-07) | N (A-07) | N | R73.1, R73.2 |
| View Client_Visible Commercial_Records | N | Own org | Own org | Y | Y (A-07) | N (A-07) | N (A-07) | N | R79.14, R79.18 |

#### Delivery: milestones, tasks, communication, deliverables, testing, deployment, handover

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Activate a Project (T20) | N | N | N | Y | Y (A-07) | N | Y (A-07) | N | R44.2 |
| Assign or unassign a Project_Member; change a project role | N | N | N | Y | N | N | Y | N | R44.4, R44.8 |
| View the project team (display name and project role) | N | Own org | Own org | Y | Y | Assigned | Y | N | R44.7 |
| Create and edit Project_Milestones; staff milestone status changes | N | N | N | Y | Y | Assigned | Assigned | N | R44.5, R45 |
| Create, edit, assign, and change the status of Tasks | N | N | N | Y | Y | Assigned | Assigned | N | R44.5, R46.3, R46.7 |
| View Client_Visible milestones and Tasks | N | Own org | Own org | Y | Y | Assigned | Y (A-07) | N | R45.9, R46.8 |
| Post a Communication | N | Own org (recorded Client_Visible) | Own org (recorded Client_Visible) | Y | Y | Assigned | Assigned | N | R44.5, R47.2, R47.3 |
| View Internal_Only Communications | N | N | N | Y | Y | Assigned | Y (A-07) | N | R47.4, R47.11 |
| Post a Client_Visible project update | N | N | N | Y | N | Assigned | Y | N | R47.6 |
| Approve an AI-drafted client update | N | N | N | Y | N | Assigned | Y | N | R47.7, R72.4 |
| Create a Deliverable version | N | N | N | Y | Y | Assigned | Assigned | N | R44.5, R48.2 |
| Mark a Deliverable version Approved for Client | N | N | N | Y | N (A-07) | N (A-07) | Assigned (A-07) | N | R48.6 |
| Download an Approved for Client Deliverable version | N | Own org | Own org | Y | Y | Assigned | Y | N | R48.7, R48.9 |
| Record test activities, acceptance criteria, and Defects | N | N | N | Y | Y | Assigned | Assigned | N | R44.5, R49.1 to R49.4 |
| Set a Blocker or Critical Defect to Won't Fix | N | N | N | Y | N | N | N | N | R49.5 |
| Submit testing feedback | N | Own org | Own org | Y | N | N | N | N | R49.6 |
| Move In Progress to Testing and back (T21, T22) | N | N | N | Y | N | Assigned (Project Lead) | Assigned (Project Lead) | N | R49.7 |
| Move Testing to Awaiting Client Acceptance, and to Delivered (T23, T24) | N | N | N | Y | N | Assigned (Project Lead) | Assigned | N | R49.8, R50.8 |
| Create and change Deployment_Records | N | N | N | Y | Y (A-07) | Assigned | Assigned | N | R50.1, R50.2, R50.10 |
| Mark a Deployment_Record Client_Visible | N | N | N | Y | N | Assigned | Y | N | R50.5 |
| Create and update Handover_Checklist items | N | N | N | Y | Y (A-07) | Assigned | Assigned | N | R50.6, R50.7, R50.10 |
| View Client_Visible Deployment_Records and Handover_Checklist items | N | Own org | Own org | Y | Y | Assigned | Y | N | R50 (Client read only) |

#### Acceptance decisions

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Accept, Decline, or Request Clarification on a Sent Proposal_Version | N | Own org | Configured (A-07) | Y (off-platform record only) | N | N | N | N | R38.3, R38.4 |
| Accept or reject a Client_Visible Project_Milestone | N | Own org | Configured (A-07) | Y (off-platform record only) | N | N | N | N | R45.4, R45.5 |
| Accept or reject a Deliverable version | N | Own org | Configured (A-07) | Y (off-platform record only) | N | N | N | N | R48.8 |
| Accept or reject the final delivery | N | Own org | Configured (A-07) | Y (off-platform record only) | N | N | N | N | R51.3, R51.4 |
| Accept a Change_Request | N | Own org | Configured (A-07) | Y (off-platform record only) | N | N | N | N | R54.8 |
| Record an off-platform acceptance with an evidence reference | N | N | N | Y | N | N | N | N | R38.8, R51.9, R54.8, A-19 |

#### Support and maintenance

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Submit a Support_Request; post a support comment | N | Own org | Own org | Y | N | N | N | N | R52.1, R52.6 |
| Change Support_Request status; post a staff support comment | N | N | N | Y | N (A-07) | Assigned | Y | N | R52.4, R52.5 |
| View Support_Requests | N | Own org | Own org | Y | Y | Assigned | Y | N | R52.9 |
| Create a Maintenance_Engagement; change its status | N | N | N | Y | Y | N | Y | N | R53.1 to R53.5 |
| Link a Support_Request to a Maintenance_Engagement | N | N | N | Y | N | Assigned | Y | N | R53.8 |
| Create maintenance tasks | N | N | N | Y | Y | Assigned | Assigned | N | R53.7, R46 |
| View Maintenance_Engagement status and Client_Visible scope | N | Own org | Own org | Y | Y | Assigned | Y | N | R53.9 |

#### Change requests

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Submit a Change_Request | N | Own org | Own org | Y | N | Assigned | Assigned | N | R54.3, R54.4 |
| Move a Change_Request to Under Review; reject it | N | N | N | Y | N | N | Y (A-07) | N | A.2.19 (proposed rows) |
| Approve a Change_Request without timeline or cost impact | N | N | N | Y | N | N | Y | N | R54.7 |
| Approve a Change_Request with timeline or cost impact | N | N | N | Y | Delegated | Delegated | Delegated | N | R54.6 |
| Withdraw one's own Change_Request | N | Own org | Own org | Y | N | Assigned | Assigned | N | A.2.19 (proposed row) |
| Mark a Change_Request Implemented | N | N | N | Y | N | Assigned (Project Lead) | Assigned | N | R54.9 |

#### Labs

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Change a Lab status | N | N | N | Y | Delegated | N | N | N | R55.7 |
| Configure the client beta Organizations of a Lab | N | N | N | Y | Delegated | N | N | N | R55.6, A-26 |
| Use a Lab in status internal | N | N | N | Y | Y | Y | Y | N | R55.5 |
| Use a Lab in status client beta | N | Configured | Configured | Y | Y | Y | Y | N | R55.6 |
| Use a Lab in status available | Configured (Solution_Architect only, within the Guest limit) | Y | Y | Y | Y | Y | Y | N | R31.8, R55, R56.3 |

#### Data Engineering Playground (only while the Lab is enabled)

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Upload a Dataset and confirm processing permission | N | Own org | Own org | Y | Y | Y (A-07) | Y (A-07) | N | R56.3, R56.8 |
| Request profiling and Recommendations | N | Own org | Own org | Y | Y | Y (A-07) | Y (A-07) | N | R57, R58 |
| Build, approve, and execute a Pipeline | N | Own org | Own org | Y | Y | Y (A-07) | Y (A-07) | N | R59.8, R60.1 |
| Download outputs | N | Own org | Own org | Y | Y | Y (A-07) | Y (A-07) | N | R61.3, R61.4 |
| Delete a Dataset | N | Own org | Own org | Y | Y | N | N | N | R63.1, R63.7 |
| Read raw Dataset contents as an agent | N | N | N | Y | N | N | N | Configured (Founder enables per agent) | R65.9 |

#### OPS and agents

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Approve an operational need record; enable an agent; change agent configuration | N | N | N | Y | N | N | N | N | R65.3, R65.4, R69.8 |
| View the agent registry, Agent_Tasks, `/admin/ops`, and dead-letter records | N | N | N | Y | Y | N | N | N | R64.11, R65, R69.1, R69.2 |
| Create an Agent_Task | N | N | N | Y | N | N | N | Configured (Orchestrator task creation tool) | R65.11, R66.1 |
| Cancel an Agent_Task | N | N | N | Y | N | N | N | N | A.2.24 (proposed row) |
| Submit or cancel a Job directly | N | N | N | Y | Y | N | N | Configured (requester only) | R64, R64.13 |
| Decide an agent-originated Approval_Request | N | N | N | Y | Delegated | Delegated | Delegated | N | R68.3, R69.6 |
| Approve the Lead Research source list | N | N | N | Y | N | N | N | N | R70.1 |
| Approve or reject a content_item | N | N | N | Y | Delegated | Delegated | Delegated | N | R71.4 |
| Request Engineering Assistant drafts | N | N | N | Y | N | Assigned | Assigned | N | R72 |
| Execute registered agent tool operations (agent-only permission; not applicable to human roles) | N | N | N | N/A | N | N | N | Configured | R17.7, R65.6, R65.14 |

#### Founder Control Center sections (view access; writes follow the rows above)

Guest, Client Owner, and Client Member are N for every section. Internal_Agent is N for every section.

| Section | Founder | Administrator | Engineer | Project_Manager | Source |
|---|---|---|---|---|---|
| Founder dashboard and analytics endpoints | Y | Y | N | N | R28.1, R73.3, R73.13 |
| Inquiries | Y | Y | Assigned (A-07) | Y (A-07) | R23.1, R73.1 |
| Prospective_Clients | Y | Y | N (A-07) | Y | R22, R73.1 |
| Clients and Organizations | Y | Y | N (A-07) | Y (A-07) | R73.1 |
| Project_Opportunities | Y | Y (A-07) | Assigned | Y | R73.1 |
| Technical_Assessments | Y | Y (A-07) | Assigned | Y (A-07) | R29.7, R73.1 |
| Proposals | Y | Y (A-07) | Assigned | Y | R73.1 |
| Active_Engagements, Project_Milestones, team assignments, Deliverables | Y | Y | Assigned | Y | R44.6, R73.1 |
| Support_Requests and Maintenance_Engagements | Y | Y | Assigned | Y | R73.1 |
| Commercial_Records | Y | Y (A-07) | N (A-07) | N (A-07) | R73.1, R79 |
| Labs | Y | Y | N (A-07) | N (A-07) | R55.7, R73.1 |
| Internal workflows and OPS agents | Y | Y (read only) | N | N | R65, R69.1, R73.1 |
| Pending approvals | Y | Y (read only) | Delegated | Delegated | R69.6, R73.1 |
| Usage and infrastructure cost | Y | Y | N | N | R42.8, R73.1 |
| Audit_Log | Y | Y | N | N | R30.6, R73.12 |
| System configuration | Y | Delegated (A-07) | N | N | R73.5 |

#### Configuration

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Change usage limits, Feature_Flags, upload limits, AI model configuration, API configuration, and A-08 values | N | N | N | Y | Delegated (A-07) | N | N | N | R73.5, R73.6, A-08 |
| Change agent configuration | N | N | N | Y | N | N | N | N | R69.8 |
| Configure which internal contact fields are Client_Visible | N | N | N | Y | N | N | N | N | R44.7 |
| Configure Client Member decision rights for an Organization | N | N (A-07) | N | Y | N | N | N | N | R38.3, R51.3, A-07 |

#### Audit log

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Search the Audit_Log | N | N | N | Y | Y | N | N | N | R30.6, R30.8, R73.12 |

No principal may update or delete an Audit_Log entry, because the API exposes no such operation (R6.9, R30.4).

#### User and role management

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Create a staff account; assign, change, or remove a staff role | N | N | N | Y | N | N | N | N | R16.5, R17.10 |
| Grant or revoke a per-user permission | N | N | N | Y | N | N | N | N | R17.11 |
| Register an Internal_Agent principal and its permission set | N | N | N | Y | N | N | N | N | R17.7, R17.8, R65.12 |
| Change an Organization_Member role between Owner and Member | N | Own org (A-07) | N | Y | N | N | N | N | R25.5 (proposed, Founder review) |

An Internal_Agent can never receive the Administrator role, the Founder role, or unrestricted administrative access (R17.8, R65.12).

#### Organization suspension

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Suspend or reinstate an Organization | N | N | N | Y | Delegated | N | N | N | R73.7, R73.9 |

#### Attachments

| Permission | Guest | Client Owner | Client Member | Founder | Administrator | Engineer | Project_Manager | Internal_Agent | Source |
|---|---|---|---|---|---|---|---|---|---|
| Upload an Attachment to an inquiry, Communication, Support_Request, or Deliverable | Y (inquiry only) | Own org | Own org | Y | Y | Assigned | Assigned | N | R20, R47.5, R48.5, R52.7 |
| Download an available Attachment | N | Own org | Own org | Y | Y | Assigned | Y (A-07) | N | R20.10, R20.11 |
| Request a re-scan of a quarantined Attachment | N | N | N | Y | Y | N | N | N | A.2.3 (proposed row) |
| Delete an Attachment or other customer data (requires an Approved Approval_Request) | N | N | N | Y | Delegated | N | N | N | R73.10 |
| Read extracted Attachment text as an agent | N | N | N | Y | N | N | N | Configured (only with the R14.10 AI-processing consent flag set) | R32.3, R32.4 |

#### Note: inferred cells and findings

The following cells and rows were inferred rather than read from a requirement criterion. Each needs Founder confirmation together with the (A-07) defaults.

1. Staff (Administrator, Engineer, Project_Manager) submitting a public inquiry: the public endpoint accepts any principal.
2. Engineer inquiry visibility "Assigned", based on R21.6 and R44.6. R44.6 only applies from Phase 4.
3. Administrator and Project_Manager split for review, qualification, rejection, On Hold, and question approval. R21 names all four internal roles as reviewers, and the matrix excludes the Engineer from qualify and reject decisions.
4. Roles for T04, T12, T20, T23, T24, and T28, where the criteria say "a user" or name no role.
5. Project_Manager holds "Assigned" for delivery writes because R44.5 limits writes to current Project_Members, while R47.6, R50.5, and R52 name the Project_Manager role without the assignment condition. The matrix grants Y on those three rows only.
6. Deliverable approval permission: Founder plus an assigned Project_Manager. R48.6 delegates the holder to this matrix.
7. Administrator writes on Deployment_Records and Handover_Checklist items. R44.5 lists "test records" but not deployment or handover records.
8. Staff access to Client Datasets (Y for Engineer and Project_Manager), based on "authorized NEUROPATH staff" in R61.3.
9. Guest Attachment upload on the inquiry, based on the Guest role in R20. R20.2 requires an Organization prefix, which a Guest inquiry receives only when the Project is stored (inferred).
10. Founder recording an answer to an Inquiry_Question, based on R17.3. No requirement describes this path.
11. Client Owner changing Organization_Member roles, and the setter of Client Member decision rights. No requirement names either actor.
12. Who may view Agreement records, Commercial_Records, and Technical_Assessments among Administrator, Engineer, and Project_Manager. R73.2 requires role separation and leaves the assignment to this matrix.

Findings recorded while deriving this appendix (requirement text is unchanged):

- F1: Accepted is enabled in Phase 4 (R44.1), while R38.13 and the Phase 3 gate (R78.8) expect client acceptance in Phase 3. See note N1 in A.1. Resolved by default A-35.
- F2: R63.1 lets a user delete a Dataset directly, while R73.10 requires an Approved Approval_Request for any deletion of customer data, and "deleting customer information" is a Sensitive_Action. The matrix grants Client self-deletion of Datasets under R63.1. The Founder should decide whether R73.10 applies to Client self-service deletion. Resolved by default A-36.
- F3: The glossary and R33.4 list Inquiry_Question statuses Open, Answered, and Withdrawn, while R33.1 creates draft questions. A.2.2 adds Draft. Resolved: glossary updated.
- F4: In Phase 2, R21.2 creates Open questions without a separate approval step, and from Phase 3, R33.2 requires an approval before sending. A.2.2 treats the reviewer's own Phase 2 request as the approval.
- F5: R22.3 delegates Lead statuses to this appendix, and no requirement names them. Every Lead status except Converted is proposed.
- F6: Resolved. Assumptions A-20 to A-37 are defined in the Founder Review Assumptions table.
- F7: "Awaiting Client Acceptance" is the handover-preparation status before Delivered. See note N2 in A.1. Recorded as A-37.

## Appendix B: Data Model Decisions

This appendix is the table list that R6.1 and R6.3 refer to. Every table decision below is marked "(decision, design phase may revise)" as a group: the design phase confirms or revises each row before R6.1 applies. Entity names follow the glossary and the **Entities** fields of the requirements. Where a requirement names an entity but no table, the row states how the entity is stored.

### B.1 Principles

All items in B.1 are (decision, design phase may revise) unless they quote a requirement.

1. **Database.** PostgreSQL on Amazon RDS in deployed environments and a local PostgreSQL container in development (R2.3, R3.3).
2. **Migrations.** Every schema change is an Alembic migration (R6.2). Each phase delivers the migrations for the tables listed for it in B.3 and creates no table of a later phase (R6.3). Every migration has a working downgrade, and applying then reverting a migration on an empty database leaves the schema equal to its starting state (R6.7, R77.5).
3. **Primary keys and timestamps.** Every table has a UUID primary key generated by the API, and `created_at` and `updated_at` columns of type `timestamptz` in UTC. Append-only tables have `created_at` only.
4. **Tenant ownership.** Every tenant-owned table has a non-null `organization_id` foreign key to `organizations` (R6.5). Every index used for tenant filtering or lookup leads with `organization_id`, for example `(organization_id, status)`, `(organization_id, project_id)`, and `(organization_id, created_at)` (R6.4). Unique constraints on tenant data include `organization_id` where the natural key is unique only within an Organization. Tenant-scoped repository methods take the Organization filter as a required argument (R6.6). Internal tables (owner "I" in B.2) have no `organization_id`, hold NEUROPATH-internal data, and are reachable only through repository methods restricted to internal roles under Appendix A.3.
5. **NEUROPATH internal organization.** NEUROPATH is itself an Organization (glossary). One `organizations` row of kind `internal` is seeded by migration in Phase 1.
6. **Guest inquiry ownership.** A Project_Inquiry and its Project submitted by a Guest are owned by the NEUROPATH internal organization until R25.4 links the Client Organization. On that link, the API changes `organization_id` on the Project_Inquiry, the Project, and their child rows in one transaction, copies any Attachment objects to the Client Organization prefix (R18.3), deletes the old objects, and writes Audit_Log entries. This keeps `organization_id` non-null (R6.5) and keeps Guest inquiries invisible to every Client until linking (R18.1).
7. **Foreign keys and unique constraints.** Every relationship has a foreign key and every natural key has a unique constraint (R6.4). Polymorphic "owner type plus owner id" columns are not used, because they cannot carry a foreign key. Where a row can belong to one of several parents, the table has one nullable foreign key column per parent and a CHECK constraint that exactly one is non-null.
8. **Append-only tables.** The API exposes no update or delete operation on `audit_logs`, `acceptance_records`, and `scope_baselines` (R6.9, R30.4, R38.14, R54.2), nor on `proposal_versions` after approval (R6.9, R36.9, R36.10), `consent_records`, and `delivery_references`. The database role used by the API holds INSERT and SELECT only on these tables, and a trigger rejects UPDATE and DELETE as a second control. The `proposal_versions` exception is defined in B.2 group E.
9. **Versions instead of in-place edits.** Changes to versioned content insert a new row with the next `version_number` and leave earlier rows unchanged: `technical_assessment_versions` (R29.9), `project_requirements_versions` (R32.13, R33.7), `solution_architecture_versions` (R35.4), `proposal_versions` (R36.10), `deliverable_versions` (R48.2), `communication_versions` (R47.8), `pipeline_versions` (R59.6), and `scope_baselines` (R54.9). Each version table has a unique constraint on `(parent_id, version_number)`.
10. **Visibility.** Tables whose rows may be shown to a Client carry a `client_visible boolean NOT NULL` column with default `false`, so Internal_Only is the default (R18.5, R46.1, R47.2, R50.5, R52.5, R79.14). Tables that are always Internal_Only carry no visibility column, and the API never serves them to Clients (R29.7, R31.4, R37.6). Visibility derived from status (Proposal_Version Sent, Deliverable version Approved for Client, Solution_Architecture_Version included in an Approved Proposal_Version) has no separate column (R35.9, R38.1, R48.6).
11. **Status columns.** Status columns are `text` columns. The API validates every status value and transition against the machine-readable Appendix A source files of R8.1. Each migration adds a CHECK constraint whose value list is generated from the same source file. PostgreSQL native ENUM types are not used, because removing an enum value has no clean downgrade (R6.7).
12. **Deletion.** Business records are not deleted through the API except where a requirement defines deletion. Stored objects of Attachments and Datasets, and the derived outputs and Profile of a Dataset, are hard-deleted (R20.7, R63.1, R75.3). The metadata row of a deleted Attachment or Dataset is kept with status `deleted`, so records that reference the object keep their metadata, and the API returns HTTP 404 for the object (R63.6, R63.8). Each deletion writes an Audit_Log entry (R30.2, R63.1). Deletion of other customer data follows B.5.
13. **Encryption.** RDS storage encryption covers every table (R74.2). The sensitive customer fields listed in `docs/SECURITY.md` are also encrypted at the application level (R74.6). Proposed candidates for that list: Lead name, email, and company; Invitation email; Project_Inquiry free-text fields; Agreement notes; and Commercial_Record evidence references. An encrypted field that the API must look up, such as a normalized email, also gets a keyed hash column used for equality lookups and unique constraints.
14. **Excluded data.** No column stores a password (R16.1), a secret value or plaintext credential (R50.3, R50.4), a card number, or a bank credential (R79.12). Session tokens live in cookies and Cognito, not in tables (R16.14). Invitation tokens are stored only as a hash.
15. **Configured values.** No retention period, size limit, upload limit, or expiry period is fixed in this appendix (A-08). Columns such as `expires_at` and `retention_expires_at` are computed from the configured value at the time of the write.

### B.2 Table Decisions

Column legend. **Owner**: T = tenant-owned (`organization_id` non-null); I = internal (no `organization_id`, internal roles only); U = user-scoped (filtered by recipient user); G = global principal. **Retention** codes are defined in B.5. `organization_id`, `id`, `created_at`, and `updated_at` are omitted from "Key columns" because B.1 adds them. Every row is (decision, design phase may revise).

#### Group A: Identity, tenancy, and access

| Candidate | Decision | Phase | Owner | Key columns | Relationships and FKs | Unique constraints | Important indexes | Retention | Sources |
|---|---|---|---|---|---|---|---|---|---|
| users | Create | 2 | G | cognito_sub, email, email_lookup_hash, display_name, platform_role (Client, Founder, Administrator, Engineer, Project_Manager), status | Membership through organization_members | cognito_sub; email_lookup_hash | platform_role | RET-BIZ | R16.1, R16.5, R16.11, R17.1 |
| organizations | Create | 1 (internal seed row and kind); status columns 5 | G | name, kind (internal, client), status (A.2.26), suspension_reason, tier (reserved, no behavior, A-05) | Parent of every tenant-owned table | Partial unique on kind where kind = internal | status | RET-BIZ | R6.5, R18, R25.2, R42.6, R73.7 to R73.9, A-05 |
| organization_members | Create | 2 | T | user_id, member_role (Owner, Member for client Organizations; Staff for the internal organization), can_decide (Client Member decision permission, A.3 note 11), joined_at, removed_at | users, organizations | (organization_id, user_id) | (user_id) | RET-BIZ | R16.11, R18.1, R25.4 to R25.7, R38.3, R51.3 |
| roles, permissions | Not created | n/a | n/a | n/a | n/a | n/a | n/a | n/a | R8.1, R17.2, R17.12 |
| user_permission_grants | Create | 3 | I | user_id, permission_key (validated against the Appendix A.3 keys), granted_by, granted_at, revoked_by, revoked_at, reason | users | Partial unique (user_id, permission_key) where revoked_at is null | (user_id) | RET-SYS | R17.11, R37.2, R79.5, A-06 |
| invitations | Create | 2 | T | email_lookup_hash, email (encrypted), token_hash, invited_by_user_id, lead_id, project_id, status (A.2.4), expires_at (configured period), accepted_at, accepted_user_id, revoked_at | organizations, users, leads, projects | token_hash; accepted_user_id where not null | (organization_id, status); (email_lookup_hash) | RET-BIZ | R16.2 to R16.4, R25.1 to R25.13 |

**roles and permissions justification.** The roles and the permission matrix are code-defined data held in the API, generated from Appendix A.3 as machine-readable files (R8.1). A role is stored as `users.platform_role` for internal and Client principals, as `organization_members.member_role` for Owner and Member, and as `project_members.project_role` for delivery roles. Internal_Agent permission sets come from `agent_registrations` (R17.7, R65.12). A database copy of the matrix would be a second source that can drift from the code, and the conformance test of R17.12 reads one source. The R17 entity Role_Assignment therefore has no table; role changes are recorded in `audit_logs` (R17.10). `user_permission_grants` is the only access table. It is created in Phase 3 because Founder delegation of pricing approval (A-06, R37.2) is the first MVP use. General per-user grants (R17.11) remain Optional and use the same table when the Founder enables them.

#### Group B: Leads and consent

| Candidate | Decision | Phase | Owner | Key columns | Relationships and FKs | Unique constraints | Important indexes | Retention | Sources |
|---|---|---|---|---|---|---|---|---|---|
| leads | Create | 1; status, duplicate, and merge columns 2 | I | name, email, company (encrypted), email_normalized_hash (R22.4), status (A.2.1), possible_duplicate, merged_into_lead_id, converted_user_id | leads (self, merge), users | None on email (duplicates are flagged, not blocked, R22.5) | (email_normalized_hash); (status) | RET-BIZ | R14.3, R22, R25.4, R28.2 |
| lead_sources | Create | 2; approved_source_id 5 (Optional) | I | lead_id, data_item, source_type (inquiry_form, engineering_service_request, lead_research, manual), source_reference, approved_source_id, obtained_at | leads, approved_sources | None | (lead_id) | RET-BIZ | R22.2, R22.6, R70.3, R70.4 |
| consent_records | Create (append-only) | 1 | I, with nullable organization_id | lead_id, user_id, organization_id, project_inquiry_id, consent_type (contact_and_processing, ai_processing, model_training), granted, wording_version, recorded_at | leads, users, organizations, project_inquiries | None | (lead_id); (organization_id, consent_type) | RET-APP | R14.10, R22.6, R22.7, R32.3, R63.3, R67.1 |
| opt_out_entries | Create | 2 | I | email_normalized_hash, requested_at, request_source, recorded_by | users | email_normalized_hash | (email_normalized_hash) | RET-APP | R22.8, R22.9, R22.11, R70.7 |

The Phase 2 migration backfills one `lead_sources` row per Phase 1 Lead with source_type `inquiry_form`. A consent change is a new `consent_records` row, so the consent history is never overwritten. Training consent (R63.3) uses `consent_type = model_training` with the Organization set.

#### Group C: Inquiry and early lifecycle

| Candidate | Decision | Phase | Owner | Key columns | Relationships and FKs | Unique constraints | Important indexes | Retention | Sources |
|---|---|---|---|---|---|---|---|---|---|
| project_inquiries (candidate "inquiries") | Create | 1; submitted_by_user_id 2 | T (internal organization until R25.4, B.1 item 6) | lead_id, submitted_by_user_id, submission_token, title, problem_description, desired_outcome, existing_systems, data_and_integrations, expected_users, constraints, budget_range, preferred_timeline, service_hint, entry_path (inquiry_form, engineering_service_request, solution_architect_lab) | leads, users | submission_token (R14.14, R41.10) | (organization_id, created_at); (lead_id) | RET-BIZ | R14, R23, R41.3, R41.4, R41.6 |
| projects | Create | 1; prior_status, status_reason, assigned_engineer_id 2 | T | project_inquiry_id, status (A.1), prior_status (R24.9), status_reason, assigned_engineer_id (R21.6) | project_inquiries, users | project_inquiry_id (R24.15) | (organization_id, status); (organization_id, created_at); (assigned_engineer_id) | RET-BIZ | R14.3, R21, R24, A-01 |
| inquiry_questions | Create | 2; approval columns 3 | T | project_id, project_inquiry_id, question_text, status (A.2.2), ai_generated, created_by, approved_by, approved_at, sent_at, answer_text, answered_by, answered_at, withdrawn_at | projects, project_inquiries, users | None | (organization_id, project_id, status) | RET-BIZ | R21.2, R24.7, R26.3, R26.4, R33 |
| inquiry_answers | Merge into inquiry_questions | 2 | n/a | answer_text, answered_by, answered_at on inquiry_questions | n/a | n/a | n/a | n/a | R26.3, R33.5 |
| attachments | Create (one generic table with one FK column per owner) | 2; owner FK columns added in the phase of each owner table | T | object_key, original_filename, declared_extension, detected_content_type, size_bytes, checksum, status (A.2.3), scan_result, scanned_at, uploaded_by, deleted_at; owner FKs project_inquiry_id, project_id (2), agreement_id, communication_id (3), deliverable_version_id, test_activity_id, handover_checklist_item_id, support_request_id, support_comment_id (4) | Each owner table; CHECK exactly one owner FK non-null | object_key | (organization_id, status); one index per owner FK | RET-OBJ | R18.3, R20, R23.3, R39.7, R47.5, R48.5, R49.1, R50.6, R50.7, R52.7 |
| inquiry_attachments | Merge into attachments (project_inquiry_id) | 2 | n/a | n/a | n/a | n/a | n/a | n/a | R20, A-03 |
| project_attachments | Merge into attachments (project_id and the delivery owner FKs) | 2 and 4 | n/a | n/a | n/a | n/a | n/a | n/a | R20, R47.5 |

**inquiry_answers justification.** Answered is a terminal Inquiry_Question status (A.2.2), so a question holds at most one answer. A separate table would add a join for a relationship that never has a second row. Revisit if the Founder allows several answers per question.

**attachments justification.** One table keeps the R20 rules (Presigned_URL scope, server-side type check, malware scan, quarantine, download audit) in one code path for every owner. One nullable FK column per owner, with a CHECK that exactly one is set, keeps database foreign keys (R6.4), which a polymorphic owner_type and owner_id pair cannot. Per-entity link tables would duplicate the same columns in about ten tables. Datasets are not stored in `attachments`, because their size, row, retention, and deletion rules differ (R56, R63).

#### Group D: Discovery

| Candidate | Decision | Phase | Owner | Key columns | Relationships and FKs | Unique constraints | Important indexes | Retention | Sources |
|---|---|---|---|---|---|---|---|---|---|
| project_assessments | Create as technical_assessments | 2 | T | project_id, created_by | projects, users | None (zero or more per Project) | (organization_id, project_id) | RET-BIZ | R29.1, R29.2 |
| technical_assessment_versions | Create (version table) | 2; ai_generated 3 | T | technical_assessment_id, version_number, feasibility, required_skills, resource_availability, risks, dependencies, missing_information, recommended_disciplines (six service groups), complexity, complexity_justification (CHECK non-empty), status (Unconfirmed, Confirmed; A.2.5), ai_generated, confirmed_by, confirmed_at, created_by | technical_assessments, users | (technical_assessment_id, version_number) | (organization_id, technical_assessment_id) | RET-BIZ | R29.3 to R29.13, R34 |
| requirement_records | Create as project_requirements_versions (version table) | 3 | T | project_id, version_number, content (JSONB, R32.7 sections validated by the Pydantic analysis schema), status (Draft; A.2.7), ai_generated, job_id, attachment_exclusions | projects, jobs | (project_id, version_number) | (organization_id, project_id) | RET-BIZ | R32.7, R32.13, R32.15, R33.7 |
| solution_architect_drafts | Create | 3 | T | project_id, job_id, content (JSONB), published_parts (JSONB list of part key, published_by, published_at) | projects, jobs | None | (organization_id, project_id) | RET-BIZ | R31.1, R31.4, R31.5 |
| solution_architectures | Create | 3 | T | project_id | projects | project_id | (organization_id, project_id) | RET-BIZ | R35 |
| solution_architecture_versions | Create (version table) | 3 | T | solution_architecture_id, version_number, graph (JSONB, B.4 schema), technology_stack (JSONB items with non-empty rationale), technical_decisions (JSONB: decision, alternatives, rationale), status (draft, confirmed; A.2.6), ai_generated, confirmed_by, confirmed_at, content_hash | solution_architectures, users | (solution_architecture_id, version_number) | (organization_id, solution_architecture_id) | RET-BIZ | R35.1 to R35.12, R34.7 |
| architecture_nodes, architecture_edges | Not created (graph stored as JSONB in solution_architecture_versions) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | R35.1, R35.2, R35.11, R35.12 |
| technical_decisions | Not created (JSONB in solution_architecture_versions) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | R35.3 |

**Graph storage justification.** A Solution_Architecture_Version is immutable and is always read, validated, rendered, and exported as one graph (R35.4, R35.5, R35.7). Storing the graph as one JSONB document validated by the Pydantic graph schema before insert makes the R35.12 integrity check a single in-memory check over the whole graph. It also makes the R35.11 round-trip property a property of one schema and one canonical serializer. Normalized node and edge tables would need a copy of every node and edge for each new version and would add joins that no query uses, since no requirement searches nodes across versions or Projects. Revisit trigger: a requirement that queries nodes, edges, or technical decisions across versions or Projects.

#### Group E: Proposal, agreement, and commercial

| Candidate | Decision | Phase | Owner | Key columns | Relationships and FKs | Unique constraints | Important indexes | Retention | Sources |
|---|---|---|---|---|---|---|---|---|---|
| proposals | Create | 3 | T | project_id | projects | project_id (R36.1) | (organization_id, project_id) | RET-BIZ | R36.1 |
| proposal_versions | Create (version table; immutable from Approved) | 3 | T | proposal_id, version_number, status (A.2.8), content (JSONB, R36.3 sections including milestones and deliverables), solution_architecture_version_id, ai_generated, content_hash, approved_by, approved_at, sent_at | proposals, solution_architecture_versions, users | (proposal_id, version_number); partial unique (proposal_id) where status = Sent (R40.12) | (organization_id, proposal_id, status) | RET-APP | R6.9, R36, R38.1, R38.12, R40 |
| proposal_deliverables | Not created (inside proposal_versions.content) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | R36.3, R36.9, R54.1 |
| price_entries | Create | 3 | T | proposal_version_id, category (service_fee, cloud_infrastructure, other), description, amount (numeric, CHECK >= 0), currency (ISO 4217), entered_by, approved_by, approved_at | proposal_versions, users | None | (organization_id, proposal_version_id) | RET-BIZ | R37.1 to R37.3, R37.8, R37.9 |
| cost_estimates | Create | 3 | T | project_id, proposal_version_id, cloud_cost_figures (JSONB), service_fee_figures (JSONB), assumptions (JSONB), grounded_input_refs (JSONB), status (indicative, approved), ai_generated, job_id, approved_by, approved_at | projects, proposal_versions, jobs, users | None | (organization_id, project_id) | RET-BIZ | R37.4 to R37.7 |
| approval_requests | Create | 3 | T (Organization of the target; internal organization for internal actions) | action_type, target_type, target_id, content (JSONB), content_hash, requester_type (user, agent), requester_user_id, requester_agent_id, rationale, status (A.2.9), expires_at (configured period), decided_by, decided_at, decision_reason | users, agent_registrations (5) | None | (status, expires_at); (organization_id, target_type, target_id) | RET-BIZ | R43, R40.3, R54.6, R68, R73.10, R79.8 |
| acceptance_records | Create (append-only) | 3; delivery subject FKs 4 | T | project_id, proposal_id (denormalized), subject FKs proposal_version_id (3), project_milestone_id, deliverable_version_id, delivery_reference_id, change_request_id (4) with CHECK exactly one, decision (accept, decline, reject), reason, content_hash, user_id, source (platform, off_platform), evidence_reference, recorded_by | projects, proposals, the subject tables, users | Partial unique (proposal_id) where decision = accept (R38.11, R38.17); partial unique (project_id) where subject is final delivery and decision = accept | (organization_id, project_id, created_at) | RET-APP | R38.5, R38.6, R38.8, R38.14, R38.16, R45.4, R45.5, R48.8, R51, R54.8 |
| agreements | Create | 3; maintenance_engagement_id 4 | T | project_id, maintenance_engagement_id (CHECK exactly one), accepted_proposal_version_id, parties (JSONB), effective_date, end_date (CHECK end_date >= effective_date), status (A.2.10), notes (Internal_Only, encrypted), signed_document_attachment_id, document_client_visible | projects, maintenance_engagements, proposal_versions, attachments | accepted_proposal_version_id where not null (one Agreement per accepted version) | (organization_id, project_id, status) | RET-BIZ | R39, R44.2, R53.3, A-13 |
| commercial_records | Create | 4 | T | project_id, proposal_version_id, agreement_id, project_milestone_id, maintenance_engagement_id, change_request_id, type (R79.1), amount (numeric, CHECK >= 0), currency (ISO 4217), due_date, status (A.2.20), client_visible, evidence_reference, content_hash, created_by, recorded_by | projects and each optional link table; same-Project check in the API (R79.4) | None | (organization_id, project_id, status); (status, due_date) | RET-BIZ | R79, R53.6, R64.14 |

**proposal_versions write rule.** The API exposes no generic update or delete operation on `proposal_versions`. After insert, the only writes are content edits while the status is Draft or In Review (implied by R36.10), status transitions through the R8 transition check, and setting `content_hash`, `approved_by`, and `approved_at` on Approved. From Approved onward, a trigger rejects any change to content columns (R36.9, R36.13). See the R6.9 note in the closing remarks of this appendix.

**proposal_deliverables justification.** Deliverables and milestones proposed in a Proposal_Version are part of the approved content that the content hash covers (R36.9). A separate table would need its own immutability control and hash coverage. Scope_Baseline version 1 copies them from the content (R54.1), and the delivered Deliverables of Phase 4 live in `deliverables`.

**Client decisions.** A decline (R38.6) is stored in `acceptance_records` with `decision = decline`, because the glossary defines an Acceptance_Record as the record of a Client decision on a Proposal_Version. The single-acceptance constraints of R38.11 and R38.17 apply to rows with `decision = accept`. A Request Clarification decision is a Client_Visible Communication (R38.7).

#### Group F: Project delivery and support

| Candidate | Decision | Phase | Owner | Key columns | Relationships and FKs | Unique constraints | Important indexes | Retention | Sources |
|---|---|---|---|---|---|---|---|---|---|
| projects (delivery) | No new table; Phase 4 enables statuses (R44.1) | 4 | T | n/a | n/a | n/a | n/a | RET-BIZ | R44.1 to R44.3 |
| project_members | Create | 4 | T | project_id, user_id, project_role (Project Lead, Engineer, Reviewer), assigned_by, assigned_at, unassigned_at | projects, users | Partial unique (project_id, user_id) where unassigned_at is null | (organization_id, project_id); (user_id) | RET-BIZ | R44.4 to R44.10 |
| project_milestones | Create | 4 | T | project_id, name, description, planned_start_date, due_date (CHECK due_date >= planned_start_date), expected_deliverables (JSONB), status (A.2.11), client_visible | projects | None | (organization_id, project_id, status); (organization_id, due_date) | RET-BIZ | R45 |
| milestone_acceptance_criteria | Create | 4 | T | project_milestone_id, description, status (Met, Not Met), updated_by | project_milestones, users | None | (organization_id, project_milestone_id) | RET-BIZ | R49.2, R49.8 |
| project_tasks | Create | 4 | T | project_id, project_milestone_id, maintenance_engagement_id (CHECK exactly one of the two), title, description, assignee_user_id, due_date, priority, status (A.2.12), blocked_reason, client_visible (default false) | projects, project_milestones, maintenance_engagements, users | None | (organization_id, project_id, status); (assignee_user_id, status); (organization_id, maintenance_engagement_id) | RET-BIZ | R45.7, R46, R53.7 |
| task_assignments | Not created (assignee column on project_tasks; history in audit_logs) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | R46.3, R46.5, R46.9 |
| maintenance_tasks | Merge into project_tasks (maintenance_engagement_id) | 4 | n/a | n/a | n/a | n/a | n/a | n/a | R53.7 |
| project_communications | Create as communications | 3; delivery use 4 | T | project_id, proposal_version_id (R38.7), author_user_id, kind (message, project_update, internal_note, test_feedback), body (sanitized), status_summary, client_visible (default false for staff; true for Client authors), ai_generated, approved_by, approved_at, current_version_number | projects, proposal_versions, users | None | (organization_id, project_id, created_at); (organization_id, project_id, client_visible) | RET-BIZ | R38.7, R41.7, R47, R49.6, R72.4 |
| project_updates | Merge into communications (kind = project_update) | 4 | n/a | n/a | n/a | n/a | n/a | n/a | R47.6, R47.7 |
| communication_versions (edit history) | Create (version table) | 4 | T | communication_id, version_number, body, edited_by, edited_at | communications, users | (communication_id, version_number) | (organization_id, communication_id) | RET-BIZ | R47.8 |
| deliverables | Create | 4 | T | project_id, project_milestone_id, type (R48.1), title | projects, project_milestones | None | (organization_id, project_id) | RET-BIZ | R48.1 |
| deliverable_versions | Create (version table) | 4 | T | deliverable_id, version_number, status (A.2.13), repository_url, commit_or_tag (credential check, R48.4), approved_for_client_by, approved_for_client_at, created_by; files through attachments.deliverable_version_id | deliverables, users | (deliverable_id, version_number) | (organization_id, deliverable_id, status) | RET-BIZ | R48.2 to R48.9 |
| test_activities | Create | 4 | T | project_id, project_milestone_id, type, scope, executed_by, executed_on, result (Pass, Fail, Blocked), client_visible; evidence through attachments.test_activity_id | projects, project_milestones, users | None | (organization_id, project_id) | RET-BIZ | R49.1, R49.10 |
| defects | Create | 4 | T | project_id, title, description, severity (A-18), status (A.2.14), resolution_note, wont_fix_approved_by, client_visible | projects, users | None | (organization_id, project_id, severity, status) | RET-BIZ | R49.3 to R49.5, R49.8 |
| deployment_records | Create | 4 | T | project_id, environment_name, environment_type (dev, staging, production), version_ref, status (A.2.15), notes, actor_user_id, client_visible | projects, users | None | (organization_id, project_id, created_at) | RET-BIZ | R50.1 to R50.5, R50.13 |
| handover_checklist_items | Create (the Handover_Checklist container is the set of items of one Project) | 4 | T | project_id, description, mandatory, status (Open, Done), evidence_note, completed_by, completed_at; evidence through attachments.handover_checklist_item_id | projects, users | None | (organization_id, project_id, mandatory, status) | RET-BIZ | R50.6 to R50.9, R50.12 |
| delivery_references | Create (append-only) | 4 | T | project_id, content (JSONB: Approved for Client Deliverable versions and Handover_Checklist item statuses), content_hash | projects | None | (organization_id, project_id, created_at) | RET-APP | R51.2, R51.5, R51.14 |
| change_requests | Create | 4 | T | project_id, description, reason, scope_impact, timeline_impact, cost_impact, content_hash, status (A.2.19), submitted_by, approval_request_id, decided_by | projects, approval_requests, users | None | (organization_id, project_id, status) | RET-BIZ | R54.3 to R54.8, R54.11 |
| scope_baselines | Create (append-only) | 4 | T | project_id, version_number, content (JSONB: scope, milestones, deliverables), source_proposal_version_id (version 1), change_request_id (versions above 1; CHECK exactly one of the two) | projects, proposal_versions, change_requests | (project_id, version_number); change_request_id where not null | (organization_id, project_id) | RET-APP | R54.1, R54.2, R54.9, R54.10, R54.12, R54.13 |
| support_requests | Create | 4 | T | project_id, maintenance_engagement_id, type (bug, question, improvement, incident), title, description, status (A.2.17), created_by, last_status_change_at | projects, maintenance_engagements, users | None | (organization_id, project_id, status) | RET-BIZ | R52.1 to R52.4, R52.9, R52.11, R53.8 |
| support_comments | Create | 4 | T | support_request_id, author_user_id, body (sanitized), client_visible (default false for staff; true for Client authors) | support_requests, users | None | (organization_id, support_request_id, created_at) | RET-BIZ | R52.5 to R52.7, R52.12 |
| maintenance_engagements | Create | 4 | T | originating_project_id, scope_description, client_visible_scope, status (A.2.18), status_reason, created_by | projects, users; Agreement through agreements.maintenance_engagement_id | None | (organization_id, originating_project_id, status) | RET-BIZ | R53, A-14 |

**communications in Phase 3.** R38.7 creates a Client_Visible Communication linked to a Proposal_Version and R41.7 creates an Internal_Only note, both in Phase 3, so `communications` is created in Phase 3 with no edit endpoint. Phase 4 adds `communication_versions` and the R47 thread behavior. The Phase 2 dashboard "recent Client_Visible updates" of R26.2 is computed from Project status changes and Notifications, because Phase 2 creates no Communication.

**task_assignments justification.** R46 needs the current assignee and an audited change history. The current assignee is a column on `project_tasks`, and R46.5 already requires an Audit_Log entry with previous and new assignee. Revisit trigger: a report of assignment history beyond Audit_Log search.

**maintenance_tasks justification.** R53.7 requires the same fields, statuses, and assignee rule as R46. Reusing `project_tasks` keeps one Task status table (A.2.12) and one assignee check. The assignee rule for a maintenance task checks current Project_Members of the originating Project.

#### Group G: Labs and Data Engineering Playground

The Data Engineering Playground tables are MVP-conditional (A-04). Their migration is delivered only after the Founder records a go decision at the Phase 4 gate (R55.11, R78.9), so that no unused table exists on a no-go decision.

| Candidate | Decision | Phase | Owner | Key columns | Relationships and FKs | Unique constraints | Important indexes | Retention | Sources |
|---|---|---|---|---|---|---|---|---|---|
| lab_registrations | Create (Lab module code declares id, name, and owned routes; the table holds the runtime status) | 4 | I | lab_key, name, status (disabled, internal, client beta, available; A.2.21), feature_flag_id, owned_route_prefixes | feature_flags | lab_key | (status) | RET-SYS | R55.1 to R55.7, R55.10 |
| feature_flags | Create | 3; feature_flag_organizations 4 | I | flag_key, enabled, description, updated_by; child table feature_flag_organizations (feature_flag_id, organization_id) for client beta | organizations (child table) | flag_key; (feature_flag_id, organization_id) | (flag_key) | RET-SYS | R31.10, R55.1, R55.6, R73.5 |
| datasets | Create (conditional) | 4 | T | project_id (same Organization, R56.11), object_key, original_filename, format (csv, xlsx, json), detected_content_type, size_bytes, row_count, checksum (R59.16), status (A.2.22), permission_confirmed_by, permission_confirmed_at, retention_expires_at (configured period), uploaded_by, deleted_by, deleted_at | projects, users | object_key | (organization_id, status); (status, retention_expires_at) | RET-CFG and RET-OBJ | R56, R63 |
| dataset_profiles | Create (conditional) | 4 | T | dataset_id, content (JSONB, R57.2 to R57.4), job_id | datasets, jobs | dataset_id (one current Profile; re-profiling replaces it, R57.11) | (organization_id, dataset_id) | Deleted with the Dataset (R63.1) | R57 |
| pipelines | Create (conditional) | 4 | T | dataset_id, name, created_by | datasets, users | None | (organization_id, dataset_id) | RET-CFG | R59.1 |
| pipeline_versions | Create (conditional, version table) | 4 | T | pipeline_id, version_number, operations (JSONB ordered list of Operation key, enabled, parameters), approved_by, approved_at, destructive_confirmations (JSONB) | pipelines, users | (pipeline_id, version_number) | (organization_id, pipeline_id) | RET-CFG | R59.6 to R59.11, R59.14 |
| recommendations | Create (conditional) | 4 | T | dataset_id, dataset_profile_id, job_id, operation_key, parameters (JSONB), affected_columns, reason, outcome (accepted, discarded, added_to_pipeline), discard_reason, ai_generated | datasets, dataset_profiles, jobs | None | (organization_id, dataset_id) | RET-CFG | R58 |
| pipeline_executions | Create (conditional) | 4 | T | pipeline_version_id, job_id, requested_by, status (A.2.22), started_at, ended_at, operation_results (JSONB per Operation: status, start, end, records processed, records affected, warnings, errors), log_lines (JSONB, redacted counts and names only), outputs (JSONB manifest of output object keys, quality report, transformation summary, configuration file, metadata, prepared-for-modeling dataset, fitted transform metadata) | pipeline_versions, jobs, users | job_id (R60.15) | (organization_id, pipeline_version_id, created_at) | RET-CFG and RET-OBJ | R60, R61, R62.5 |

Training consent for R63.3 is a `consent_records` row (Group B). Output objects listed in the `outputs` manifest are hard-deleted with the Dataset (R63.1).

#### Group H: ENGINE, OPS, usage, notifications, audit, and configuration

| Candidate | Decision | Phase | Owner | Key columns | Relationships and FKs | Unique constraints | Important indexes | Retention | Sources |
|---|---|---|---|---|---|---|---|---|---|
| jobs | Create | 2 (first long-running work: attachment malware scan, R19.7, R19.8); R64 columns completed by 5 | T | job_type (registry key), parameters (JSONB, validated), dedupe_key, status (A.2.23), attempt_count, available_at (backoff), lease_owner, lease_expires_at, requester_user_id, requester_agent_id, parent_job_id (workflow runs), result (JSONB), error, started_at, finished_at, duration_ms, estimated_cost | users, agent_registrations (5), jobs (self) | (job_type, dedupe_key) (R64.6) | (status, available_at); (organization_id, created_at); (parent_job_id) | RET-CFG | R19.7, R19.8, R64, R67.12 |
| Job type registry | Not created (code registry, R64.1) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | R64.1, R64.17 |
| job_dead_letters | Create | 5 | T | job_id, job_type, redacted_parameters (JSONB), error, attempt_count | jobs | job_id | (created_at) | RET-CFG | R64.11, R75.12 |
| agents | Create as agent_registrations | 5 | I | agent_key, purpose, instructions_ref (repository path and content hash), tool_list (JSONB), output_schema_ref, enabled, model_config (JSONB), dataset_access_enabled (R65.9), operational_need_record_id | operational_need_records | agent_key | (enabled) | RET-SYS | R17.7, R65, R69.3, R69.8 |
| operational_need_records | Create | 5 | I | title, description, requested_by, approved_by, approved_at, status (proposed, approved, withdrawn) | users | None | (status) | RET-SYS | R65.1, R65.3, R65.4 |
| agent_tasks | Create | 5 | T (internal organization unless the task concerns a Client Organization) | agent_registration_id, job_id, workflow_job_id, step_name, step_index, input (JSONB, redacted), output (JSONB, redacted), status (A.2.24), model_id, input_tokens, output_tokens, estimated_cost (null = unknown, R66.10), error, trace (JSONB, redacted), started_at, ended_at, duration_ms, approval_request_id | agent_registrations, jobs, approval_requests | None | (status); (agent_registration_id, created_at); (created_at) for the daily cost check | RET-CFG | R65, R66, R67.3, R67.6, R68.1 |
| R67 workflow run | Not created (a parent Job with dedupe key equal to the Project_Inquiry id, plus one agent_tasks row per step) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | R67.1, R67.3, R67.6, R67.12 |
| approval_requests | See Group E | 3 | n/a | n/a | n/a | n/a | n/a | n/a | R43, R68 |
| content_items | Create (Optional, only when the Content or Marketing agent is enabled) | 5 | I | item_type (article, linkedin_post, case_study_draft, campaign_plan), title, body, claims (JSONB: claim, verified_record_ref or unsupported flag), status (A.2.25), content_hash, created_by_agent_id, approval_request_id | agent_registrations, approval_requests | None | (status) | RET-SYS | R71, A-17 |
| approved_sources | Create (Optional, only when the Lead Research agent is enabled) | 5 | I | name, source_pattern, permitted_basis, approved_by, approved_at, revoked_at | users | source_pattern where revoked_at is null | (revoked_at) | RET-SYS | R70.1, R70.2 |
| usage_records | Create (AI_Usage_Record of R32 and R58 is merged here) | 3 | T | usage_type (upload, storage, job, ai_call, agent_task), job_id, agent_task_id, model_id, input_tokens, output_tokens, quantity, unit, estimated_cost (CHECK >= 0, null = unknown), recorded_at | jobs, agent_tasks (5) | None | (organization_id, recorded_at); (usage_type, recorded_at) | RET-CFG | R42, R64.15, R66.9, R76.4 |
| notifications | Create | 2 | U | recipient_user_id, organization_id (nullable context), event_type, resource_type, resource_id, title, body, read_at, email_status (not_requested, pending_approval, sent, failed) | users, organizations | None | (recipient_user_id, read_at, created_at) | RET-CFG | R27, R24.13 |
| notification_preferences | Create | 2 | U | user_id, event_type, email_opt_in | users | (user_id, event_type) | (user_id) | RET-SYS | R27.10, R27.14 |
| audit_logs | Create (append-only) | 1 (minimal use by R14.11; full R30.1 columns from the first migration); search indexes 2 | T where an Organization applies; nullable organization_id for Guest and system events | actor_type (user, agent, system), actor_id, action, resource_type, resource_id, organization_id, request_id, metadata (JSONB, redacted per R30.3, including previous and new values for status and configuration changes) | organizations | None | (organization_id, created_at); (actor_type, actor_id, created_at); (resource_type, resource_id); (action, created_at) | RET-AUD | R8.4, R14.11, R30, R73.6, R73.12 |
| system_configurations | Create | 5 | I | config_key, value (JSONB), value_type, valid_range, updated_by | users | config_key | (config_key) | RET-SYS | R73.5, R73.6, R73.14, A-08 |

**audit_logs in Phase 1.** R14.11 requires an Audit_Log entry for each stored Project_Inquiry in Phase 1, while R30 is a Phase 2 requirement. The Phase 1 migration therefore creates `audit_logs` with the full R30.1 column set and the append-only controls of B.1 item 8, and Phase 1 writes only inquiry entries. Phase 2 adds the search indexes, the R30.6 search, and the remaining event types. Creating the full column set in Phase 1 avoids a later migration that changes an append-only table.

**jobs before Phase 5.** R19.7 and R19.8 (Phase 2) require HTTP 202 and a job status endpoint, and R64 states the interface is available from the first phase that uses Jobs. `jobs` is created in Phase 2 for the attachment scan and gains its R64 controls by Phase 5. Scheduled job types (R64.14) that span Organizations submit one Job per Organization, so each Job names a single Organization (R64.9).

**system_configurations before Phase 5.** Until Phase 5, configured values (A-08 limits, invitation expiry, rate limits, maximum field lengths) live in versioned configuration files and environment variables documented under R3.1. Phase 5 moves the Founder-editable values into `system_configurations` so that R73.5 and R73.6 can change and audit them at runtime.

**Not stored in tables.** Rate-limit counters for R14.7 and R19.5 are held in process memory while the API runs as one instance; revisit when the API runs more than one replica. Guest Solution_Architect Lab results are not stored before sign-in (R31.8). Verified project records for R71 come from repository content files (A-17). Security reviews, load test results, restore test records, and billable deployment authorizations are documents (R74.11, R75.5, R76.1 to R76.7).

### B.3 Tables by Phase

Each phase's migration creates only the tables listed for that phase (R6.3). Column additions to earlier tables are listed after "Adds". (decision, design phase may revise)

| Phase | New tables | Adds to earlier tables |
|---|---|---|
| 0 | None. The Alembic baseline revision with an empty schema, used by the R78.5 up-and-down check. | n/a |
| 1 | organizations (internal organization seed row), leads, consent_records, project_inquiries, projects, audit_logs | n/a |
| 2 | users, organization_members, invitations, lead_sources, opt_out_entries, inquiry_questions, attachments, notifications, notification_preferences, technical_assessments, technical_assessment_versions, jobs | leads (status, possible_duplicate, merged_into_lead_id, converted_user_id); projects (prior_status, status_reason, assigned_engineer_id); project_inquiries (submitted_by_user_id); audit_logs (search indexes) |
| 3 | user_permission_grants, feature_flags, solution_architect_drafts, project_requirements_versions, solution_architectures, solution_architecture_versions, proposals, proposal_versions, price_entries, cost_estimates, approval_requests, acceptance_records, agreements, communications, usage_records | inquiry_questions (approved_by, approved_at, ai_generated); technical_assessment_versions (ai_generated); attachments (agreement_id, communication_id) |
| 4 (4A) | project_members, project_milestones, milestone_acceptance_criteria, project_tasks, communication_versions, deliverables, deliverable_versions, test_activities, defects, deployment_records, handover_checklist_items, delivery_references, change_requests, scope_baselines, support_requests, support_comments, maintenance_engagements, commercial_records, lab_registrations, feature_flag_organizations | attachments (deliverable_version_id, test_activity_id, handover_checklist_item_id, support_request_id, support_comment_id); acceptance_records (project_milestone_id, deliverable_version_id, delivery_reference_id, change_request_id); agreements (maintenance_engagement_id) |
| 4 (4B, only after a go decision, A-04) | datasets, dataset_profiles, pipelines, pipeline_versions, recommendations, pipeline_executions | n/a |
| 5 | job_dead_letters, operational_need_records, agent_registrations, agent_tasks, system_configurations. Optional: content_items (R71), approved_sources (R70) | organizations (status, suspension_reason); jobs (requester_agent_id FK); approval_requests (requester_agent_id FK); usage_records (agent_task_id); lead_sources (approved_source_id, Optional) |
| 6 | None | Hardening only (R74.6 field encryption changes, if any) |

Phase 1 notes: R14.12 notifies internal users through the notification interface, and in Phase 1 that interface has only its local implementation, because `notifications` is created in Phase 2 (R27). R14.3 stores the Project in status Submitted and T01 is the only Project transition in Phase 1 (A.1 note N3).

### B.4 Allowed Architecture Node and Edge Types

R35.2 refers to this list. The whole section is (decision, design phase may revise).

**Graph document.** A `solution_architecture_versions.graph` value has the fields `schema_version`, `nodes`, and `edges`. Each node has `id`, `type`, `label`, and the optional fields `description`, `technology`, and `parent_id`. Each edge has `id`, `source`, `target`, `type`, and an optional `label`. The canonical serializer writes keys in a fixed order and keeps list order, so serializing and parsing return an equal graph (R35.11).

**Node types**

| Type | Meaning |
|---|---|
| actor | A human user group or role that uses the system |
| client_app | A desktop or mobile client application |
| web_frontend | A browser-based user interface |
| api_service | A service that exposes an API |
| worker | A background processor or job runner |
| database | A relational, document, or other database |
| object_storage | A file or object store |
| queue | A message queue or stream |
| cache | An in-memory cache |
| identity_provider | An authentication or identity service |
| ai_model | A hosted or self-managed AI model or model endpoint |
| external_system | A third-party or existing client system outside the proposed solution |
| analytics | A reporting, BI, or analytics component |
| monitoring | A logging, metrics, or alerting component |
| network_boundary | A grouping node for a network, account, or trust boundary. Other nodes reference it through `parent_id`; it is not an edge endpoint |

**Edge types**

| Type | Meaning |
|---|---|
| calls | Synchronous request from source to target |
| reads | Source reads data from target |
| writes | Source writes data to target |
| publishes | Source sends messages or events to target |
| subscribes | Source receives messages or events from target |
| authenticates | Source authenticates through target |
| deploys_to | Source is deployed into target |

**Validation rules (R35.2, R35.12).** Node ids are unique. Edge ids are unique. Every edge `source` and `target` references an existing node id that is not a `network_boundary`. Every `parent_id` references an existing `network_boundary` node, and containment has no cycle. Self-loop edges are rejected. Each violation is reported by name in the HTTP 422 error.

### B.5 Retention and Deletion

No retention period is fixed in this document. Every period below is a value the Founder sets in configuration before the phase that uses it is accepted (A-08). (decision, design phase may revise)

| Code | Data class | Tables | Rule | Sources |
|---|---|---|---|---|
| RET-AUD | Audit trail | audit_logs | Retained. The API exposes no update or delete operation. Entries contain no raw customer content (R30.3), so they remain after customer data is deleted. Any purge would need a new requirement. | R6.9, R30.3, R30.4, R30.10 |
| RET-APP | Append-only business records | acceptance_records, scope_baselines, proposal_versions (from Approved), consent_records, opt_out_entries, delivery_references | Retained for the life of the owning Organization. Not deleted through any API operation. Opt-out entries are kept so that R22.9 and R70.7 keep working. Customer deletion under R73.10 is an open conflict, see the closing remarks. | R6.9, R22.8, R38.14, R54.2 |
| RET-BIZ | Business records | Every other T and I business table in groups A to F | Retained for the life of the owning Organization. Deleted only through a customer data deletion request executed with an Approved Approval_Request whose content hash equals the hash of the deletion parameters, with an Audit_Log entry. | R30.2, R73.10, R43 |
| RET-OBJ | Stored objects | attachments, datasets, and output objects in pipeline_executions.outputs | Objects are hard-deleted. The metadata row is kept with status deleted, the API returns HTTP 404 for the object, and every object version is purged within the documented deletion window. Rejected uploads are deleted at rejection. | R20.7, R56.14, R63.1, R63.6, R75.3 |
| RET-CFG | Data with a configured retention period | datasets, dataset_profiles, pipelines, pipeline_versions, recommendations, pipeline_executions, jobs, job_dead_letters, agent_tasks, usage_records, notifications | Deleted by the scheduled retention Job of R64.14 when the configured period expires. Dataset retention follows R63.2 and R63.9. For the other tables the period is a Founder-configured value; until a value is set, rows are retained. | R63.2, R63.9, R64.14, A-08 |
| RET-SYS | Internal configuration and registries | user_permission_grants, lab_registrations, feature_flags, agent_registrations, operational_need_records, approved_sources, content_items, system_configurations, notification_preferences | Retained. Changes are recorded in audit_logs with previous and new values. Revocation sets an end timestamp instead of deleting. | R17.11, R55.7, R65.13, R73.6 |

**Dataset self-deletion.** R63.1 lets a Client delete a Dataset directly. The object, derived outputs, and Profile are removed, the Dataset row moves to status deleted, and an Audit_Log entry is written. Under the default A-36, Client self-service deletion needs no Approval_Request. If the Founder changes A-36, the R63.1 path creates an Approval_Request and deletes only after approval.

**Backups.** RDS automated backups and S3 object versions follow R75.1 to R75.3. The backup retention period is documented in `docs/DEPLOYMENT.md`. Deleted customer objects and their versions are purged within the documented deletion window (R75.3).

#### Closing remarks for Appendix B

- R6.9 says Proposal_Version is stored in a table with no update operation exposed by the API, while R36.10 implies Draft and In Review versions can change and R36.2 defines status transitions. Group E reads R6.9 as "no generic update or delete, and no content change from Approved". The Founder should confirm this reading. Resolved: R6.9 now states this exception.
- R73.10 allows deletion of customer data with an approved request, while R6.9, R38.14, and R54.2 make Acceptance_Records, Proposal_Versions, and Scope_Baselines append-only. No requirement states which wins. Proposed rule for design review: R73.10 deletion does not remove rows of append-only tables, and those rows keep only identifiers and hashes after the related customer content is deleted.
- R38.17 literally says at most one Proposal_Version has an Acceptance_Record. Group E stores declines in the same table and applies R38.17 to accept decisions. The alternative is a separate table for declines. Resolved: R38.17 now applies to accept decisions.

## Appendix C: Infrastructure Service Necessity

This appendix is the service register that R7.5, R64.13, R75.7, R76.5, and R76.6 refer to. It reviews the stack of R2 for services that a small founding team does not need yet. Every row is (decision, design phase may revise) and every adoption is subject to these rules:

- No billable AWS resource is created until the Founder has authorized the specific deployment in writing (R3.6, R76.7). This appendix authorizes nothing.
- In each deployed environment, the AWS budget alarm is created before any other resource (R7.4).
- A service that is not listed in R2 is provisioned only after its justification is recorded in `docs/ARCHITECTURE.md` (R7.5). Rows marked "not in R2" below need that record.
- Before Phase 6 acceptance, every AWS service in use has a row here with status Required or an adopted Conditional row, and any other service is removed (R76.5, R76.6).
- "First deployed phase" means the first phase whose deployment the Founder authorizes. If the public site is deployed at the end of Phase 1, that is Phase 1.

**Status values.** Required: needed by a requirement in the stated phase. Conditional: adopted only when the stated trigger occurs. Deferred: not used in MVP; reconsider on the trigger. Not adopted: not planned.

### C.1 Service Register

| Service | Purpose | Needed by requirement(s) | First phase needed | Status | Local development substitute (R3) | Trigger to adopt |
|---|---|---|---|---|---|---|
| AWS Budgets | Budget alarm per environment | R7.4, R76.8 | First deployed phase, before any other resource | Required (not in R2) | None needed | n/a |
| Next.js hosting | Serve Web_App (public site, Client_Workspace, Founder_Control_Center) | R2.1, R9 to R15 | First deployed phase | Required; hosting option is a Founder decision | `next dev` and `next start` | n/a |
| Amazon ECS on Fargate | Run the API container and the in-process worker; proposed also for the Next.js container | R2.5, R64.13 | First deployed phase | Required | Docker Compose with the API, worker, and PostgreSQL | n/a |
| Application Load Balancer | TLS termination and routing to Fargate tasks | R74.1 | First deployed phase | Required with ECS (not in R2) | Direct local ports | n/a |
| Amazon ECR | Store container images for Fargate | R2.5 | First deployed phase | Required with ECS (not in R2) | Local Docker images | n/a |
| AWS Certificate Manager | TLS certificates for the load balancer | R74.1 | First deployed phase with a domain | Required (not in R2) | Plain HTTP on localhost | n/a |
| DNS (Amazon Route 53 or the registrar's DNS) | Domain records | R15.1 (canonical URLs) | First deployed phase with a domain | Conditional on the domain choice (A-16) (not in R2) | localhost | Domain chosen (A-16); Route 53 only if the Founder prefers AWS-managed DNS |
| Amazon RDS for PostgreSQL | Relational data | R2.3, R6, R74.4, R75.1 | First deployed phase | Required; single small instance, Multi-AZ Deferred until R75.10 targets require it | PostgreSQL container | n/a |
| Amazon VPC with private subnets | Place RDS without a public endpoint | R74.4 | First deployed phase (no hourly charge for the VPC itself) | Required | Docker network | n/a |
| NAT gateway | Outbound internet access from private subnets | R74.4 | Phase 6 at the latest | Conditional (not in R2) | n/a | Fargate tasks move to private subnets and need outbound access that VPC endpoints do not cover. A NAT gateway has an hourly charge plus a per-GB charge; compare with a free S3 gateway endpoint and per-hour interface endpoints (ECR, Secrets Manager, CloudWatch Logs, Bedrock) before choosing |
| Amazon S3 | Private object storage for Attachments, Deliverable files, Datasets, and outputs | R2.3, R18.3, R20, R56, R61, R75.2 | 2 | Required | Local filesystem storage adapter behind the storage interface | n/a |
| Amazon Cognito | Authentication, verification, password recovery, lockout | R16, R2.5 | 2 | Required | Local auth adapter that issues development tokens, enabled only in the local environment | n/a |
| AWS Secrets Manager | Secrets in deployed environments | R3.2 | First deployed phase | Required | Environment variables | n/a |
| Amazon CloudWatch | Logs, metrics, alarms, dead-letter alarm | R75.6, R75.12, R2.5 | First deployed phase | Required | Structured logs to stdout | n/a |
| AWS KMS | Encryption at rest | R20.1, R74.2, R74.6 | First deployed phase | Required with AWS managed keys (default service encryption). Customer managed keys Deferred | None | One customer managed key becomes Conditional if R74.6 field encryption uses KMS envelope encryption; the alternative is a data key held in Secrets Manager |
| Malware scanning service | Scan Attachments and Datasets before availability | R20.8, R20.9, R56.15 | 2 | Required; product not chosen (A-16) (not in R2) | A local scanner container, or a stub that reports "scanner unavailable" so files stay quarantined. The stub never reports a clean result (R3.4) | n/a |
| Transactional email provider | Founder-approved external email and user email opt-in | R27.10, R27.11, R27.13, R40.6 | 2 at the earliest | Conditional; provider not chosen (A-16, A-09) (not in R2) | Local outbox that writes messages to a file or log | The first Founder-approved external email, the first user email opt-in, or Cognito verification volume above the Cognito default email sender quota |
| Amazon Bedrock | Model calls for analysis, drafting, Recommendations, and OPS agents | R2.4, R32, R34 to R37, R58, R65 | 3 (when AI analysis goes live) | Required from Phase 3 | Recorded or stubbed model responses; the default CI run makes no Bedrock call (R77.10) | n/a |
| Strands Agents | Agent library inside Agent_Runtime; not an AWS service and not billed | R2.4, R32, R65 | 3 (Solution_Architect), 5 (OPS agents) | Required (library) | Same library with stubbed model responses | n/a |
| Amazon SQS | Managed job queue | R64.13, R75.7 | n/a | Conditional (A-27) | In-process queue and worker over the `jobs` table | See the queue decision record in C.3 |
| AWS Lambda | Short-running job handlers | R2.5 | n/a | Conditional; not required for MVP | Same handler code in the in-process worker | A specific job type is shown to cost less on Lambda than on the always-on worker, or needs isolation that the worker cannot give |
| AWS Step Functions | Durable multi-step orchestration | R2.5 | n/a | Deferred | Parent Job plus Agent_Task steps (R67) | R67 or a later workflow needs durable multi-step state, waits, or compensation beyond what R64 retries and the `jobs` table provide |
| Amazon EventBridge (including EventBridge Scheduler) | Event routing and schedules | R2.5, R64.14 | n/a | Deferred | In-process scheduler in the worker for R64.14 scheduled job types | More than one consumer needs the same event, or scheduled jobs must run while no worker task is running |
| Amazon CloudFront | CDN for static assets | R15.9 | n/a | Deferred (not in R2) | n/a | The R15.9 Lighthouse target or measured latency is not met without a CDN, or Amplify Hosting is chosen (which includes one) |
| AWS WAF | Web request filtering | R14.7, R74 | n/a | Deferred (not in R2) | n/a | Abuse that the R14.7 and R19.5 application rate limits do not contain, or a Phase 6 security review finding |
| Amazon ElastiCache | Shared cache or rate-limit store | none | n/a | Not adopted (not in R2) | n/a | The API runs more than one replica and rate-limit counters must be shared; first try PostgreSQL for the counters |
| Infrastructure as code tool | Define Infrastructure as code | R2.6, A-10 | 0 (decision), first deployed phase (use) | Required; CDK or Terraform is a Founder decision recorded once in Phase 0 (A-10) | `cdk synth` or `terraform plan` without deployment | n/a |

**Next.js hosting options.** (a) Run Web_App as a second container on the same ECS on Fargate cluster behind the same load balancer. This uses services already in R2, one deployment pipeline, and one IaC stack. (b) AWS Amplify Hosting, which manages builds, the CDN, and TLS, but adds a service that is not in R2 and needs an R7.5 justification. (c) A hosting platform outside AWS, which also needs a Founder decision on vendor and data location. Recommendation: option (a), because it adds no service and keeps one deployment path for a small team. The choice is a Founder decision.

**IaC tool note.** Both options create a small amount of billable state before the first stack: CDK bootstraps an S3 bucket, an ECR repository, and IAM roles, and Terraform needs a remote state backend such as an S3 bucket. That bootstrap is a billable deployment under R3.6 and comes after the budget alarm of R7.4.

### C.2 Removed or Deferred to Avoid Premature Complexity

- Amazon SQS, AWS Step Functions, Amazon EventBridge, and AWS Lambda: replaced in MVP by one in-process worker over the PostgreSQL `jobs` table behind the R64.13 interface (A-27).
- Separate worker service: the worker runs in the API task definition until job volume or isolation needs a separate Fargate service.
- Multi-AZ RDS, read replicas, and RDS Proxy: deferred until the R75.10 recovery targets or load test results of R76 require them.
- NAT gateway: deferred until Fargate tasks move to private subnets; VPC endpoints are compared first.
- Customer managed KMS keys: deferred unless R74.6 field encryption uses KMS.
- CloudFront and AWS WAF: deferred until a measured need.
- ElastiCache and any other cache: not adopted.
- Separate environments beyond local, one non-production environment, and production: not planned. Each deployed environment needs its own Founder authorization and budget alarm.
- Content management system: not adopted; content comes from repository files (A-17).
- Native mobile hosting, multi-region deployment, and e-signature or payment services: out of scope.

### C.3 Queue Technology Decision Record

R64.13 requires that a queue technology recorded in this appendix can replace the local implementation without changing callers.

| Field | Value |
|---|---|
| ID | QDR-01 |
| Context | ENGINE runs Jobs for attachment scans (Phase 2), AI analysis (Phase 3), Playground profiling and execution (Phase 4), scheduled job types (R64.14), and OPS Agent_Tasks (Phase 5). R64 requires dedupe keys, up to 3 retries with backoff, dead-letter records, and limits per job type. R60.9 and R64.16 require an exactly-once effect under duplicate delivery. |
| Current decision | In-process queue and worker behind the R64.13 interface. The `jobs` table is the queue: a worker claims a Queued Job with a row lock that skips locked rows, holds a lease (`lease_owner`, `lease_expires_at`), and a Job whose lease expires returns to Queued. Jobs survive process restarts because they are rows in PostgreSQL. Dedupe uses the unique constraint on `(job_type, dedupe_key)`. |
| Status | Pending Founder confirmation (A-27). |
| Options considered | (1) In-process worker over the PostgreSQL `jobs` table: no added service or cost, transactional with the business write, and limited by database load. (2) Amazon SQS with the `jobs` table as the record of state: managed durability and scaling, a dead-letter queue, a queue depth metric (R75.7), and one more service, IAM policy, and failure mode. (3) Step Functions or EventBridge: orchestration and fan-out features that no MVP requirement needs. |
| Consequences | No queue depth alarm under R75.7 while no managed queue is in use; the R75.12 dead-letter alarm is raised from `job_dead_letters` through CloudWatch metrics instead. Worker throughput is bounded by one database. |
| Revisit triggers | Adopt option (2) when any of these occurs: Job claiming adds database load that the R76 load test shows as a bottleneck; more than one worker service must scale independently of the API; a job type must run in Lambda; or the Founder sets R75.10 recovery targets that the database-backed queue cannot meet. Record the change here and in `docs/ARCHITECTURE.md` before provisioning (R7.5). |

## Appendix D: V1 to V2 Mapping

This appendix maps every requirement of the archived V1 document (`docs/archive/REQUIREMENTS_V1.md`, V1 R1 to R47) to this document. The V2 IDs come from the **V1** field of each V2 metadata block, read in reverse.

**Disposition values.** Retained: same scope and purpose, with editorial rewording only. Modified: same subject, with changed scope, roles, or content. Moved: the V1 content is kept, and its delivery phase changed (earlier or later). Split: the V1 content is distributed across two or more V2 requirements. Merged: the V1 content is combined into a V2 requirement that also covers other V1 content. Removed: no V2 counterpart.

V1 phases were: 0 Foundation, 1 Public website, 2 Auth and customer dashboard, 3 Data Engineering Playground, 4 AI Solution Architect, 5 NEUROPATH OPS, 6 Production readiness.

### D.1 V1 Requirement Dispositions

| V1 ID | V1 title | Disposition | V2 IDs | Note |
|---|---|---|---|---|
| 1 | Monorepo Structure | Retained | R1 | Phase 0 in both. |
| 2 | Technology Stack and Architecture Decisions | Retained | R2 | Phase 0 in both. Appendix C reviews which R2 services are needed for MVP. |
| 3 | Local Development and External Service Fallbacks | Retained | R3 | R3.6 now requires authorization of the specific deployment. |
| 4 | Design System | Retained | R4 | Same tokens and constraints. |
| 5 | Documentation Set | Modified | R5 | Adds R5.6: this file is the single canonical requirements source. |
| 6 | Database Baseline | Modified | R6 | Renamed Data Model Governance. Tables are created only by the phase that needs them (Appendix B.3), and R6.9 adds append-only tables. |
| 7 | Continuous Verification and Cost Control | Retained | R7 | R7.4 now requires the budget alarm before any other resource. |
| 8 | Global Navigation and Layout | Modified | R9 | Labs link removed from primary navigation and How We Work added (R9.1). "Start a Project" replaces Get Started (R9.2). |
| 9 | Homepage | Modified | R10 | The V1 tagline "Engineering Intelligence. Enabling Growth." and the Labs-first hero ("Explore Our Labs") are removed and replaced by the new identity "Technology. Engineered to Solve." R10.11 forbids the V1 tagline. |
| 10 | Truthful Content | Modified | R11 | Adds R11.6 for the Why NEUROPATH section. |
| 11 | Services Pages | Modified | R12 | Six V1 service categories replaced by six capability groups. The call to action is "Start a Project" and the service is only an optional hint (R12.11). |
| 12 | Additional Public Pages | Modified | R13 | Page set is Solutions, Projects, How We Work, About, Insights. The V1 Labs page is removed, and the Labs are described on the Solutions page as optional supporting capabilities (R13.2). |
| 13 | Contact and Consultation Form | Split | R14, R22, R27 | Contact form becomes the Project Inquiry Form (R14). Lead storage moves to R22, and the V1 13.10 notification moves to R27. |
| 14 | SEO, Performance, and Accessibility of the Public Website | Retained | R15 | Phase 1 in both. |
| 15 | Registration, Sign-In, and Account Recovery | Modified | R16 | Client accounts are created by invitation after inquiry review (A-02, R25). Staff accounts added. |
| 16 | Roles and Authorization | Modified | R17 | Registered_Customer and Premium_Customer become Client (A-05). Engineer and Project_Manager roles added. Permission matrix in Appendix A.3. |
| 17 | Tenant Isolation | Modified | R18 | Adds Internal_Only visibility property (R18.8). |
| 18 | Customer Dashboard Overview and Notifications | Split | R26, R27 | Dashboard becomes the project-focused Client_Workspace (R26). Notifications move to R27. |
| 19 | Project Management for Customers | Split | R8, R24, R38 | Status contract (R8, extends V1 19.2 and 19.3), Project record and early statuses (R24), client proposal decision (R38, from V1 19.4). The V1 status list is replaced by Appendix A.1. |
| 20 | Basic Administration in Phase 2 | Split | R28, R30, R73 | Founder dashboard (R28, Phase 2), audit logging (R30, from V1 20.6), full Founder Control Center (R73, Phase 5). |
| 21 | Rate Limiting, Validation, and Structured Errors | Retained | R19 | Renamed API Conventions; adds an OpenAPI drift check (R19.9). |
| 22 | Pricing and Monetization Posture | Modified | R42 | Moved from V1 Phase 2 to V2 Phase 3 as usage and cost tracking. The V1 SaaS tiers (Free, Starter, Professional, Enterprise) are removed from MVP and deferred to Future (Scope Register, A-05). Billing is Out-of-scope. |
| 23 | Dataset Upload | Split | R56, R20 | Dataset upload (R56) moves from V1 Phase 3 to V2 Phase 4, MVP-conditional (A-04). The secure upload criteria V1 23.7 to 23.11 also form inquiry and project Attachments in V2 Phase 2 (R20). |
| 24 | Data Profiling | Moved | R57 | V1 Phase 3 to V2 Phase 4, MVP-conditional (A-04). |
| 25 | AI Recommendations for Data Operations | Moved | R58 | V1 Phase 3 to V2 Phase 4, MVP-conditional (A-04). |
| 26 | Pipeline Builder | Moved | R59 | V1 Phase 3 to V2 Phase 4, MVP-conditional (A-04). |
| 27 | Pipeline Execution and Logs | Split | R60, R64 | Execution (R60) to V2 Phase 4, MVP-conditional. The V1 27.9 and 27.10 queue rules become the ENGINE Job Framework (R64, Phase 5 interface, used from the first phase with Jobs). |
| 28 | Outputs, Downloads, and Completion Dashboard | Moved | R61 | V1 Phase 3 to V2 Phase 4, MVP-conditional (A-04). |
| 29 | Machine Learning Preparation | Moved | R62 | V1 Phase 3 to V2 Phase 4, MVP-conditional (A-04). |
| 30 | Dataset Lifecycle, Retention, and Privacy | Moved | R63 | V1 Phase 3 to V2 Phase 4, MVP-conditional (A-04). Self-service deletion clarified by A-36. |
| 31 | Solution Intake | Split | R31, R32, R33 | V1 Phase 4 to V2 Phase 3. The Solution_Architect becomes a supporting tool inside discovery (R31), with analysis (R32) and clarification (R33). |
| 32 | Requirement Analysis and Classification | Split | R32, R34 | V1 Phase 4 to V2 Phase 3. Classification uses the six service groups (R34). |
| 33 | Solution Design Output | Split | R36, R37 | V1 Phase 4 to V2 Phase 3. Proposal drafting (R36) and human-approved pricing and cost estimates (R37). |
| 34 | Architecture Diagram | Moved | R35 | V1 Phase 4 to V2 Phase 3 (earlier). |
| 35 | Proposal Generation and Consultation Request | Split | R31, R36, R40, R41 | V1 Phase 4 to V2 Phase 3. Guest limit (R31), versioned proposals (R36), sending and export (R40), consultation request (R41). |
| 36 | Engineering Service Request Lab | Merged | R41 | V1 Phase 4 to V2 Phase 3, merged with the V1 35 consultation options. |
| 37 | Agent Architecture | Split | R65, R71, R72 | Stays in Phase 5 and is internal only. R65 is MVP only for the agents used by R67 (A-28). V1 37.7 goes to R71 and the V1 Engineering agent to R72, both Optional. |
| 38 | Task Execution and Recording | Split | R66, R42 | Agent task recording and limits (R66, Phase 5). The V1 38.6 cost limit is partly in R42 (Phase 3). |
| 39 | Project Inquiry Workflow | Modified | R67 | Reshaped as the only MVP OPS workflow (A-28): inquiry processing assistance under human review, Phase 5. |
| 40 | Approvals for Sensitive Actions | Split | R43, R68 | General Approval_Requests move earlier to V2 Phase 3 for commercial actions (R43). OPS approvals stay in Phase 5 (R68). |
| 41 | Ops Dashboard | Retained | R69 | Phase 5 in both, internal only. |
| 42 | Full Administration | Split | R28, R30, R66, R73 | Founder dashboard metrics start in Phase 2 (R28), audit search in R30, agent cost parts in R66, full control center in R73 (Phase 5). |
| 43 | Lead Research and Outreach Limits | Split | R22, R70, R71 | Lead source and opt-out (R22, Phase 2, MVP). Lead Research and Outreach agents (R70) and content publishing (R71) are Optional in Phase 5. |
| 44 | Security Hardening | Split | R74, R30 | Phase 6 hardening (R74). The V1 44.5 log rule is also applied in the Phase 2 audit baseline (R30). |
| 45 | Reliability, Monitoring, and Recovery | Retained | R75 | Phase 6 in both. RTO and RPO values are set by the Founder (A-31). |
| 46 | Test Coverage | Retained | R77 | Adds R77.9: a property-based test for every FOR ALL property. |
| 47 | Phase Gating and MVP Acceptance | Modified | R78 | MVP acceptance journey rewritten around inquiry, proposal, delivery, and acceptance, with a go/no-go decision for MVP-conditional items. |

No V1 requirement is Removed in full. Removed V1 content inside Modified rows: the V1 tagline and Labs-first homepage (V1 9, replaced by the new identity under R10), the Labs navigation emphasis (V1 8, V1 12), the SaaS tiers (V1 22, deferred to Future), and the Premium_Customer role (V1 16, A-05).

**Phase moves summary.**

- V1 Phase 3 Data Engineering Playground (V1 23 to 30) moves to V2 Phase 4 as MVP-conditional (R56 to R63, A-04). Secure upload rules also appear earlier, in V2 Phase 2 (R20).
- V1 Phase 4 AI Solution Architect (V1 31 to 36) moves to V2 Phase 3 as a supporting tool inside discovery and proposal (R31 to R37, R40, R41).
- V1 Phase 5 OPS (V1 37 to 43) stays in V2 Phase 5 and is internal only (R65 to R72). Approvals (R43) and lead consent and opt-out (R22) move earlier, to Phases 3 and 2.
- V1 Phase 2 pricing posture (V1 22) moves to V2 Phase 3 (R42). V1 Phase 2 administration (V1 20) is split between V2 Phase 2 (R28, R30) and V2 Phase 5 (R73).

### D.2 New in V2 (no V1 source)

V2 requirements whose V1 field is "none (new)" or "new":

| V2 ID | Purpose |
|---|---|
| R8 | One authoritative status and transition contract for all status-bearing entities (V1 field: "new (extends 19.2, 19.3)"). |
| R39 | Agreement records with status, parties, dates, and a signed-document reference (A-13). |
| R44 | Project activation after an Agreement is in effect, and team assignment through Project_Member records. |
| R45 | Project milestones with acceptance criteria and client milestone decisions. |
| R46 | Tasks within milestones, with assignees and statuses. |
| R47 | Project communication threads with Client_Visible and Internal_Only messages. |
| R48 | Deliverables with versions, approval for client, and client decisions. |
| R49 | Testing and quality assurance records, test activities, and Defects. |
| R50 | Deployment records and the Handover_Checklist, without secret values. |
| R51 | Final delivery acceptance against the delivery reference. |
| R52 | Client support requests for active or completed Projects. |
| R53 | Maintenance engagements with their own scope and Agreement (A-14). |
| R54 | Change requests and versioned scope baselines. |
| R55 | Labs module framework: Labs as optional, independently enabled modules. |
| R76 | Performance and cost optimization review. |
| R79 | Commercial and payment records, record-keeping only, no payment processing. |

V2 requirements whose metadata block has no V1 field (treated as new):

| V2 ID | Purpose |
|---|---|
| R21 | Human review, questioning, qualification, and rejection of inquiries. |
| R23 | Founder inquiry inbox for internal staff. |
| R25 | Client invitation and Organization onboarding. |
| R29 | Internal technical assessment records in Phase 2. |

### D.3 Summary Counts

| Category | Count | Basis |
|---|---|---|
| V1 Retained | 10 | V1 1, 2, 3, 4, 7, 14, 21, 41, 45, 46 |
| V1 Modified | 13 | V1 5, 6, 8, 9, 10, 11, 12, 15, 16, 17, 22, 39, 47 |
| V1 Moved | 7 | V1 24, 25, 26, 28, 29, 30, 34 |
| V1 Split | 16 | V1 13, 18, 19, 20, 23, 27, 31, 32, 33, 35, 37, 38, 40, 42, 43, 44 |
| V1 Merged | 1 | V1 36 |
| V1 Removed | 0 | No V1 requirement lacks a V2 counterpart |
| V1 total | 47 | |
| New in V2 | 20 | 16 with V1 field "none (new)" or "new", and 4 with no V1 field (R21, R23, R25, R29) |

The remaining 59 V2 requirements trace to at least one V1 requirement. Several V1 phase changes also occur inside Split rows (V1 23, 27, 31, 32, 33, 35, 40, 42, 43); the Moved count includes only rows whose whole content moved.

## Appendix E: Self-Review

Each answer is Yes, Partially, or No, with the requirements that support the answer and the remaining gap. "Partially" is used where the remaining gap is a Founder decision or a Founder-set value.

| # | Question | Answer | Supporting IDs | Remaining gap |
|---|---|---|---|---|
| 1 | Does the document present NEUROPATH as a custom technology solutions and engineering company? | Yes | Introduction, R9.1, R9.6, R10.1 to R10.11, R12.1, R12.8, R13.5 | None. The V1 tagline is forbidden (R10.11), and Labs are kept out of the Hero (R10.9). |
| 2 | Can a client bring a problem without knowing the technology? | Yes | R10.6, R12.11, R14, R41 (Engineering_Service_Request needs no Lab or technology), R33 | The consent wording of R14 needs legal review by the Founder before launch (A-11). |
| 3 | Can NEUROPATH analyze, scope, design, propose, build, test, deploy, and hand over? | Yes | Analyze: R21, R29, R32, R34. Scope: R32, R36, R54.1. Design: R35. Propose: R36, R37, R40. Build: R44 to R47. Test: R49. Deploy and hand over: R50, R51 | Test activity types and coverage per Project are not fixed (A-24). |
| 4 | Can clients track their projects? | Yes | R24, R26, R27, R45, R47, R48, R51, R52 | None. |
| 5 | Can the Founder manage leads, proposals, clients, projects, and deliverables? | Yes | Leads: R22, R23. Proposals: R36 to R40, R43. Clients: R25, R73. Projects: R24, R28, R44 to R46. Deliverables: R48. Control center: R73 | Default permissions for Engineer and Project_Manager need confirmation (A-07, Appendix A.3 note items 1 to 12). |
| 6 | Are the Data Playground and the AI Solution Architect supporting tools? | Yes | Introduction ("Clients are never required to use a Lab"), R10.9, R13.2, R31 (Solution_Architect inside discovery, drafts only), R55, R56 to R63 (MVP-conditional, A-04) | The Founder decides at the Phase 4 gate whether the Data Playground ships (A-04). |
| 7 | Is OPS internal? | Yes | Glossary (OPS), R65, R67, R69, Scope Register (Customer-facing OPS Out-of-scope), A-28 | None. |
| 8 | Is the platform suitable for a small founding team? | Yes | Delivery Phases table, A-27, A-28, A-30, R67 (one MVP OPS workflow), R70 to R72 (Optional), Appendix C.2 | None beyond the Founder-set values of F.5. |
| 9 | Is the MVP realistic and financially responsible? | Partially | R3.6 (no billable resource without written authorization of the specific deployment), R7.4 (budget alarm before any other resource), A-27 (in-process queue instead of managed queue services), Appendix C (service necessity register, C.2 deferrals), R42, R66, R76 | Founder must set AI cost limits and other values (A-08), choose the Next.js hosting option and IaC tool (Appendix C.1, A-10), and confirm QDR-01 (Appendix C.3). Data Playground scope is a Phase 4 go/no-go (A-04). |
| 10 | Are security and confidentiality protected? | Partially | R16, R17, R18 (isolation and Internal_Only properties), R20 (quarantine property), R30, R43, R68, R74, R75, R79.12 | Founder must record the sensitive fields and seeded values for the log scan (A-33), approve the secret and card detection patterns (A-34), choose the malware scanning product (A-16), and decide the R73.10 versus append-only conflict (Appendix B closing remarks). |
| 11 | Are all requirements testable? | Yes | Every acceptance criterion is written in an EARS pattern with a named system and an observable response. Invariants, round trips, idempotence, and isolation are stated as FOR ALL properties, and R77.9 requires a property-based test for every FOR ALL property. Counts are in Appendix F.1 | Criteria that depend on Founder-set values (A-08, A-29, A-31, A-32) become testable when the values are set. |
| 12 | Does the roadmap receive and manage real inquiries before advanced automation? | Yes | Phase 1 (R14, inquiry form) and Phase 2 (R21 to R30, review and CRM) come before Phase 5 OPS and ENGINE automation (R64 to R73). R78 gates each phase on Founder review | None. |
| 13 | Is the commercial workflow complete? | Partially | Discovery: R14, R21, R31 to R33. Scope definition: R32, R36, R54.1. Quotation: R37, R40, R79. Agreement: R39. Milestones: R45. Payment records: R79. Change requests: R54. Delivery acceptance: R45, R48, R51. Maintenance: R52, R53 | Records only: no e-signature (A-13), no invoice generation or payment processing (Scope Register, R79.12). No support response time is defined (A-12). Founder confirms A-35 (Accepted in Phase 3) and A-37 (status naming). |

## Appendix F: Completeness Report

All values in this appendix were computed by searching this file after Appendices D and E were added. No value is estimated.

### F.1 Counts

**Requirements.** 79 headings match `^### Requirement`.

| Phase | Requirements | IDs | Numbered acceptance criteria | FOR ALL properties |
|---|---|---|---|---|
| 0 Foundation | 8 | R1 to R8 | 54 | 1 |
| 1 Public Company Website | 7 | R9 to R15 | 66 | 1 |
| 2 Client Acquisition and Founder CRM | 15 | R16 to R30 | 173 | 17 |
| 3 Solution Discovery and Proposal | 13 | R31 to R43 | 157 | 18 |
| 4 Project Delivery and Engineering Labs | 21 | R44 to R63, R79 | 260 | 38 |
| 5 NEUROPATH OPS and ENGINE | 10 | R64 to R73 | 118 | 12 |
| 6 Production Readiness | 5 | R74 to R78 | 63 | 4 |
| Total | 79 | | 891 | 91 |

Phase is the section in which the requirement appears. Some requirements span phases in their metadata: R4, R5, R6 (every phase), R8 (enforced from Phase 2), R39 (Phase 3 records, Phase 4 activation guard), R43 (reused in Phase 5), R64 (interface available from the first phase that uses Jobs).

**Numbered acceptance criteria.** 891 lines match `^\d+\. ` between `## Requirements` and `## Appendix A`. The highest criterion number of each requirement also sums to 891, so criterion numbering has no gaps inside any requirement.

**FOR ALL properties.** 91 acceptance criteria start with `FOR ALL`. One more criterion, R77.9, contains the words "FOR ALL" because it requires a property-based test for every FOR ALL property; it is not counted as a property.

**Scope class (leading class in the Scope metadata field).**

| Scope class | Count | IDs |
|---|---|---|
| MVP | 68 | R1 to R55, R64 to R69, R73 to R79 |
| MVP-conditional | 8 | R56 to R63 (A-04) |
| Optional | 3 | R70, R71, R72 |
| Future | 0 | Future items are listed in the Scope Register only |
| Total | 79 | |

Six MVP requirements carry a mixed qualifier: R17 (per-user grants Optional), R42 (billing Out-of-scope), R55 (Data Engineering Playground MVP-conditional), R65 (Optional for agents other than those of R67), R77 (Data_Engine tests MVP-conditional per A-04), and R79 (invoice generation Future).

### F.2 ID Continuity

The requirement IDs found are R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66, R67, R68, R69, R70, R71, R72, R73, R74, R75, R76, R77, R78, R79.

- Missing IDs in R1 to R79: none.
- Duplicate IDs: none.
- Order: R79 appears in Phase 4 after R63 and before R64, as stated in "How to Read This Document". Every other ID appears in ascending order.
- Every metadata block carries the matching NP-Rnn ID.

### F.3 Reference Check

| Reference type | Occurrences | Unresolved |
|---|---|---|
| Requirement references `Rn` and `Rn.m` | 2,405, of which 1,387 name a criterion `Rn.m` | None. Every `Rn` is between R1 and R79, and every `Rn.m` names an existing criterion number. |
| Assumption references `A-nn` | 451 | None. A-01 to A-37 are all defined in the Founder Review Assumptions table. |
| Appendix references (`Appendix X`, `Appendix X.n`, and section numbers such as A.2.14, B.3, C.3) | Appendix A to F and sections A.1, A.1.1, A.1.2, A.2, A.2.1 to A.2.26, A.3, B.1 to B.5, C.1 to C.3, D.1 to D.3, E, F.1 | None. Every referenced section exists as a heading. |
| Transition references `Tnn` | T1 to T32 referenced | None. T01 to T32 are defined in A.1.2. |
| Decision record `QDR-01` | Referenced in Appendix C.3 | None. |

**Stale text.** None remaining. The QDR-01 Status row was corrected after this report was first computed.

### F.4 Scope Register Coverage

The Scope Register has 54 rows: 33 MVP, 1 MVP-conditional, 5 Optional, 7 Future, and 8 Out-of-scope.

- Every requirement and criterion ID named in the register exists (R1 to R79 ranges, R17.11, R21.8, R27.10, R55.10, R56.4, R58.7, R63.3, R64.4, R68.7).
- Every assumption named in the register exists (A-04, A-05, A-13, A-15).
- Every requirement R1 to R79 is named by at least one MVP, MVP-conditional, or Optional row.
- Rows with "none" or "beyond R79" are Future or Out-of-scope items that have, by design, no requirement: maintenance reporting dashboards, client-facing analytics, invoice generation and billing integration, payment processing and billing, customer-facing OPS, and native mobile apps. Managed queue and orchestration services map to Appendix C.

### F.5 Open Items Requiring Founder Decisions

- **Defaults the Founder may change (marked "(Founder decision, default)"):** A-35 (Accepted and T18 enabled in Phase 3), A-36 (Client self-service Dataset deletion without an Approval_Request), A-37 (Awaiting Client Acceptance as the handover-preparation status).
- **Values or choices the Founder must set:** A-08 (all configured limits and periods), A-10 (CDK or Terraform), A-11 (legal review of consent wording), A-16 (domain, email provider, malware scanner), A-29 (job CPU, memory, time limits, and retry backoff), A-31 (RTO and RPO), A-32 (load test targets and main endpoints), A-33 (sensitive fields and seeded log-scan values), A-34 (secret, card number, and bank credential detection patterns).
- **Appendix A.3 inferred cells:** 12 items in "Note: inferred cells and findings" need confirmation together with the A-07 defaults. Findings F4 (Phase 2 question approval) and F5 (proposed Lead statuses) are open; F1, F2, F3, F6, and F7 are resolved or recorded as assumptions.
- **Proposed entries:** 78 appendix entries are marked "(proposed, Founder review)": 77 in Appendix A.1 and A.2, and 1 in Appendix A.3. One further occurrence is the explanation in "How to Read This Document". 8 entries are marked "(decision, design phase may revise)".
- **Appendix B conflict:** R73.10 deletion of customer data versus the append-only tables of R6.9, R38.14, and R54.2. A proposed rule (keep identifiers and hashes, remove customer content) awaits design review and Founder confirmation.
- **Appendix C:** the Next.js hosting option (recommended option (a), a second container on ECS on Fargate), and confirmation of QDR-01 (in-process queue over the `jobs` table).
- **Phase 4 gate:** go or no-go for the Data Engineering Playground (A-04).

### F.6 Status Statement

This document is a requirements specification. Nothing described in it is implemented. No AWS resources are deployed, and no billable resource creation is authorized by this document (R3.6).
