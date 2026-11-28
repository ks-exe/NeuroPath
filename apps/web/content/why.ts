import type { Statement } from "./types";

/**
 * Why NEUROPATH statements about the working method (R11.6).
 *
 * The drafts below paraphrase working-method rules stated in the requirements
 * (R12.8, R13.4). They stay `confirmed: false` until the Founder confirms the
 * wording in this file; only confirmed statements are displayed.
 */
export const whyStatements: readonly Statement[] = [
  {
    id: "feasibility-assessment",
    text: "Each project is assessed for feasibility, required skills, resources, risk, and scope before NEUROPATH accepts it.",
    confirmed: false,
  },
  {
    id: "engineer-review",
    text: "AI-drafted material is reviewed by a NEUROPATH engineer before it reaches a client.",
    confirmed: false,
  },
  {
    id: "problem-first",
    text: "Clients can describe a problem without choosing a technology first.",
    confirmed: false,
  },
];
