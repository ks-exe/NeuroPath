import type { Metadata } from "next";
import type { ReactNode } from "react";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { SkipLink } from "@/components/skip-link";
import { features } from "@/lib/features";
import { getSiteUrl, SITE_LOCALE, SITE_NAME } from "@/lib/site";
import { bodyFont, headingFont, monoFont } from "./fonts";
import "./globals.css";

const defaultDescription = "Technology. Engineered to Solve.";

// Defaults for every page; each page sets its own title, description and canonical URL (R15.1).
export const metadata: Metadata = {
  metadataBase: getSiteUrl(),
  title: { default: SITE_NAME, template: `%s | ${SITE_NAME}` },
  description: defaultDescription,
  openGraph: {
    siteName: SITE_NAME,
    type: "website",
    locale: SITE_LOCALE,
    title: SITE_NAME,
    description: defaultDescription,
  },
  twitter: { card: "summary" },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={`${headingFont.variable} ${bodyFont.variable} ${monoFont.variable}`}>
      <body className="flex min-h-screen flex-col bg-background text-foreground">
        <SkipLink />
        <SiteHeader authEnabled={features.authEnabled} />
        <div className="flex-1">{children}</div>
        <SiteFooter />
      </body>
    </html>
  );
}
