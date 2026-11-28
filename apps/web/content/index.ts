import { aboutStatements } from "./about";
import { articles } from "./insights";
import { projects } from "./projects";
import { serviceGroups } from "./services";
import { solutionsCapabilities } from "./solutions";
import type {
  Article,
  Project,
  ServiceGroup,
  ServiceGroupId,
  SolutionsCapability,
  Statement,
} from "./types";
import { whyStatements } from "./why";

export type * from "./types";
export { DATA_COLLECTION_COMPLIANCE_NOTE } from "./services";

/** All six service groups, in order A to F (R12.1). */
export function getServiceGroups(): readonly ServiceGroup[] {
  return serviceGroups;
}

export function getServiceGroup(id: ServiceGroupId): ServiceGroup | undefined {
  return serviceGroups.find((group) => group.id === id);
}

/** Lookup by URL slug, used by the service detail pages (R12.1). */
export function getServiceGroupBySlug(slug: string): ServiceGroup | undefined {
  return serviceGroups.find((group) => group.slug === slug);
}

/**
 * Feasibility statement shown on the Services page and each detail page
 * (R12.8).
 */
export const SERVICES_FEASIBILITY_STATEMENT =
  "Each service group is a capability. Each project is assessed for feasibility, required skills, resources, risk, and scope before NEUROPATH accepts it.";

/** Only projects whose verification flag is "verified" (R11.1, R11.5). */
export function getVerifiedProjects(source: readonly Project[] = projects): Project[] {
  return source.filter((project) => project.verification === "verified");
}

function confirmedOnly(source: readonly Statement[]): Statement[] {
  return source.filter((statement) => statement.confirmed === true);
}

/** Only Founder-confirmed Why NEUROPATH statements (R11.6). */
export function getConfirmedWhyStatements(
  source: readonly Statement[] = whyStatements,
): Statement[] {
  return confirmedOnly(source);
}

/** Only Founder-confirmed About statements (R13.5). */
export function getConfirmedAboutStatements(
  source: readonly Statement[] = aboutStatements,
): Statement[] {
  return confirmedOnly(source);
}

/** Only published articles (R13.6). */
export function getPublishedArticles(source: readonly Article[] = articles): Article[] {
  return source.filter((article) => article.published === true);
}

/** Optional supporting capabilities with availability status (R13.2). */
export function getSolutionsCapabilities(): readonly SolutionsCapability[] {
  return solutionsCapabilities;
}
