import type { Metadata } from "next";
import { getServiceGroups } from "@content";

export const SITE_NAME = "NEUROPATH";
export const SITE_LOCALE = "en";
const DEFAULT_SITE_URL = "http://localhost:3000";

/**
 * Public origin of the site, read server-side from SITE_URL (not a secret).
 * Used for metadataBase, canonical URLs, the sitemap and robots (R15.1, R15.2).
 * Pages are statically rendered, so the value must be set at build time.
 */
export function getSiteUrl(env: Record<string, string | undefined> = process.env): URL {
  const raw = env.SITE_URL?.trim() || DEFAULT_SITE_URL;
  const url = new URL(raw);
  if (url.protocol !== "http:" && url.protocol !== "https:") {
    throw new Error("SITE_URL must use http or https");
  }
  return new URL(url.origin);
}

/** Absolute URL for a site path such as "/services". */
export function absoluteUrl(path: string): string {
  return new URL(path, getSiteUrl()).toString();
}

/** Static public routes. The 404 page and the /api/ proxy are not public pages. */
export const STATIC_PUBLIC_PATHS: readonly string[] = [
  "/",
  "/services",
  "/solutions",
  "/projects",
  "/how-we-work",
  "/about",
  "/insights",
  "/contact",
  "/start-a-project",
];

/** Every public page path, including one per service group. Used by the sitemap. */
export function publicPaths(): string[] {
  return [...STATIC_PUBLIC_PATHS, ...getServiceGroups().map((group) => `/services/${group.slug}`)];
}

interface PageMetadataInput {
  /** Page title without the site suffix; the root layout template appends it. */
  title: string;
  description: string;
  /** Route path, starting with "/". */
  path: string;
}

/** Unique title, description, canonical URL and Open Graph data for one page (R15.1). */
export function pageMetadata({ title, description, path }: PageMetadataInput): Metadata {
  return {
    title,
    description,
    alternates: { canonical: path },
    openGraph: {
      // Page-level openGraph replaces the layout's, so the defaults are repeated here.
      title: `${title} | ${SITE_NAME}`,
      description,
      url: path,
      siteName: SITE_NAME,
      type: "website",
      locale: SITE_LOCALE,
    },
  };
}
