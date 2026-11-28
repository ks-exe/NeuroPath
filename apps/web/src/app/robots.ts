import type { MetadataRoute } from "next";
import { absoluteUrl } from "@/lib/site";

/** Robots file: all public pages may be crawled; the API proxy may not (R15.2). */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", allow: "/", disallow: "/api/" },
    sitemap: absoluteUrl("/sitemap.xml"),
  };
}
