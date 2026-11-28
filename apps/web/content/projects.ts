import type { Project } from "./types";

/**
 * Selected projects and case studies (R11.1, R11.4).
 *
 * Add an entry only for a real project, and set `verification: "verified"`
 * only after the Founder has confirmed it. Unverified entries are never shown
 * (R11.5). The sample below is a typed placeholder that the loader filters out;
 * it describes no real customer or outcome.
 */
export const projects: readonly Project[] = [
  {
    id: "sample-unverified",
    title: "Sample entry (not displayed)",
    description: "Format example only. Replace with a real project before verifying.",
    technologies: [],
    verification: "unverified",
  },
];
