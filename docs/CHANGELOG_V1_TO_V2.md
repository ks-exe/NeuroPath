# Changelog: V1 to V2 Requirements

The full requirement-by-requirement mapping (V1 R1 to R47, with dispositions Retained, Modified, Moved, Split, Merged, Removed) is in **Appendix D** of the canonical requirements file: [`.kiro/specs/neuropath-platform/requirements.md`](../.kiro/specs/neuropath-platform/requirements.md). This page summarizes the main changes only.

## Summary

- **Company model.** V2 describes NEUROPATH as a technology solutions and engineering company: clients bring problems and NEUROPATH engineers solutions. V2 adds inquiry intake, a Founder CRM, solution discovery, proposals and project delivery.
- **Phase order.** V1 phases were 0 Foundation, 1 Public website, 2 Auth and customer dashboard, 3 Data Engineering Playground, 4 AI Solution Architect, 5 OPS, 6 Production readiness. V2 phases are 0 Foundation, 1 Public Company Website, 2 Client Acquisition and Founder CRM, 3 Solution Discovery and Proposal, 4 Project Delivery and Engineering Labs, 5 OPS and ENGINE, 6 Production Readiness.
- **Data Engineering Playground.** Moved from V1 Phase 3 to V2 Phase 4 as a Lab, and made MVP-conditional on a Founder decision at the Phase 4 gate (A-04).
- **AI Solution Architect.** Moved into the Phase 3 discovery workflow as a drafting tool. Its output stays a draft until a human approves it.
- **Roles.** V1 Registered_Customer and Premium_Customer map to the single role Client (A-05).
- **Documentation.** `.kiro/specs/neuropath-platform/requirements.md` is the single canonical requirements source; `docs/REQUIREMENTS_V2.md` only points to it (R5.6).
- **Data model.** Tables are created only in the phase that needs them (R6, Appendix B).
- **New governance.** V2 adds a status transition contract (R8, Appendix A), the Labs module framework (R55), and phase gating with Founder approval (R78).
- **Scope classes.** Each requirement is classed as MVP, MVP-conditional, Optional, Future or Out-of-scope in the Scope Register.

The V1 document is archived at [`docs/archive/REQUIREMENTS_V1.md`](archive/REQUIREMENTS_V1.md).
