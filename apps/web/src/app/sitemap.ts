import type { MetadataRoute } from "next";
import { absoluteUrl, publicPaths } from "@/lib/site";

/** Sitemap of every public page with absolute URLs (R15.2). */
export default function sitemap(): MetadataRoute.Sitemap {
  return publicPaths().map((path) => ({ url: absoluteUrl(path) }));
}
