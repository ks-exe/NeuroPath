import type { Metadata } from "next";
import { describe, expect, it } from "vitest";
import { getServiceGroups } from "@content";
import { metadata as aboutMeta } from "@/app/about/page";
import { metadata as contactMeta } from "@/app/contact/page";
import { metadata as howWeWorkMeta } from "@/app/how-we-work/page";
import { metadata as insightsMeta } from "@/app/insights/page";
import { metadata as notFoundMeta } from "@/app/not-found";
import { metadata as homeMeta } from "@/app/page";
import { metadata as projectsMeta } from "@/app/projects/page";
import robots from "@/app/robots";
import { generateMetadata as serviceGroupMeta } from "@/app/services/[group]/page";
import { metadata as servicesMeta } from "@/app/services/page";
import sitemap from "@/app/sitemap";
import { metadata as solutionsMeta } from "@/app/solutions/page";
import { metadata as startMeta } from "@/app/start-a-project/page";
import { getSiteUrl, publicPaths } from "@/lib/site";

// R15.1, R15.2
async function allPageMetadata(): Promise<Metadata[]> {
  const groups = await Promise.all(
    getServiceGroups().map((group) => serviceGroupMeta({ params: Promise.resolve({ group: group.slug }) })),
  );
  return [
    homeMeta,
    servicesMeta,
    solutionsMeta,
    projectsMeta,
    howWeWorkMeta,
    aboutMeta,
    insightsMeta,
    contactMeta,
    startMeta,
    ...groups,
  ];
}

describe("page metadata", () => {
  it("gives every public page a unique title, description, canonical URL and Open Graph data", async () => {
    const pages = await allPageMetadata();
    const titles = pages.map((m) => m.title);
    const descriptions = pages.map((m) => m.description);
    const canonicals = pages.map((m) => m.alternates?.canonical);

    for (const m of pages) {
      expect(typeof m.title).toBe("string");
      expect(m.description).toBeTruthy();
      expect(m.openGraph?.title).toBeTruthy();
      expect(m.openGraph?.description).toBe(m.description);
      expect(m.openGraph?.url).toBe(m.alternates?.canonical);
    }
    expect(new Set(titles).size).toBe(pages.length);
    expect(new Set(descriptions).size).toBe(pages.length);
    expect([...canonicals].sort()).toEqual([...publicPaths()].sort());
  });

  it("marks the 404 page as not indexable", () => {
    expect(notFoundMeta.robots).toMatchObject({ index: false });
  });
});

describe("sitemap and robots", () => {
  it("lists each public route once with an absolute URL", () => {
    const urls = sitemap().map((entry) => entry.url);
    expect(new Set(urls).size).toBe(urls.length);
    expect(urls).toHaveLength(publicPaths().length);
    const origin = getSiteUrl().origin;
    for (const url of urls) expect(url.startsWith(`${origin}/`)).toBe(true);
    for (const group of getServiceGroups()) expect(urls).toContain(`${origin}/services/${group.slug}`);
    expect(urls.some((url) => url.includes("not-found"))).toBe(false);
  });

  it("references the sitemap and disallows the API proxy", () => {
    const file = robots();
    expect(file.sitemap).toBe(`${getSiteUrl().origin}/sitemap.xml`);
    expect(file.rules).toMatchObject({ userAgent: "*", allow: "/", disallow: "/api/" });
  });

  it("rejects a SITE_URL that is not http or https", () => {
    expect(getSiteUrl({}).origin).toBe("http://localhost:3000");
    expect(getSiteUrl({ SITE_URL: "https://example.test/path" }).origin).toBe("https://example.test");
    expect(() => getSiteUrl({ SITE_URL: "ftp://example.test" })).toThrow();
  });
});
