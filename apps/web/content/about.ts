import type { Statement } from "./types";

/**
 * About page statements (R13.5).
 *
 * The draft below uses the company description required by R13.5. It stays
 * `confirmed: false` until the Founder confirms the wording; only confirmed
 * statements are displayed. Do not add history, team size, clients, or
 * credentials unless the Founder has confirmed them.
 */
export const aboutStatements: readonly Statement[] = [
  {
    id: "company-description",
    text: "NEUROPATH is a Technology Solutions & Engineering Company.",
    confirmed: false,
  },
];
