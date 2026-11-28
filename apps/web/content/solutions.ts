import type { SolutionsCapability } from "./types";

/**
 * Optional supporting capabilities on the Solutions page (R13.2).
 *
 * Availability follows the delivery plan: the AI Solution Architect (R31) and
 * the Engineering Service Request (R41) are Phase 3; the Data Engineering
 * Playground (R56 to R63) depends on the Founder's go decision (A-04).
 * Change a status to "available" only when the capability is live.
 */
export const solutionsCapabilities: readonly SolutionsCapability[] = [
  {
    id: "data-engineering-playground",
    name: "Data Engineering Playground",
    availability: "conditional",
    availabilityNote: "Not available. Offered only if NEUROPATH decides to launch it.",
  },
  {
    id: "ai-solution-architect",
    name: "AI Solution Architect",
    availability: "planned",
    availabilityNote: "Not yet available. Planned for a later release.",
  },
  {
    id: "engineering-service-request",
    name: "Engineering Service Request",
    availability: "planned",
    availabilityNote:
      "Not yet available. Planned for a later release. Use Start a Project to describe your problem today.",
  },
];
