/**
 * Types for the structured content source (R11, R12, R13).
 *
 * Every entry that could carry a factual claim has a flag set by the Founder:
 * projects carry `verification`, statements carry `confirmed`, articles carry
 * `published`. Loaders in `./index.ts` return only flagged entries.
 */

export type ServiceGroupId = "A" | "B" | "C" | "D" | "E" | "F";

export interface ServiceGroup {
  id: ServiceGroupId;
  /** URL-safe slug for the detail section or page (R12.1). */
  slug: string;
  name: string;
  /** Detail items listed by R12.2 to R12.7. */
  details: readonly string[];
  /**
   * Typical engagements, deliverables, and technologies (R12.10).
   * The spec does not supply this content; lists stay empty until the
   * Founder provides wording, and empty lists are not rendered.
   */
  engagements: readonly string[];
  deliverables: readonly string[];
  technologies: readonly string[];
  /**
   * Lawful data collection statement, required for groups B and E when
   * content describes scraping or automated data collection (R12.9).
   */
  complianceNote?: string;
}

export type VerificationStatus = "verified" | "unverified";

export interface Project {
  id: string;
  title: string;
  description: string;
  technologies: readonly string[];
  /** Only "verified" entries are displayed (R11.1, R11.5). */
  verification: VerificationStatus;
}

export interface Statement {
  id: string;
  text: string;
  /** Only Founder-confirmed statements are displayed (R11.6, R13.5). */
  confirmed: boolean;
}

export interface Article {
  slug: string;
  title: string;
  summary: string;
  /** ISO 8601 date, set when the article is published. */
  publishedAt?: string;
  /** Only published articles are listed (R13.6). */
  published: boolean;
}

/**
 * Availability of an optional supporting capability on the Solutions page
 * (R13.2).
 * - `available`: usable now.
 * - `planned`: scheduled for a later delivery phase.
 * - `conditional`: depends on a pending Founder decision.
 */
export type AvailabilityStatus = "available" | "planned" | "conditional";

export interface SolutionsCapability {
  id: "data-engineering-playground" | "ai-solution-architect" | "engineering-service-request";
  name: string;
  availability: AvailabilityStatus;
  /** Plain-language note explaining the availability status. */
  availabilityNote: string;
}
