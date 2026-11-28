import { MAIN_CONTENT_ID } from "@/components/skip-link";
import type { Metadata } from "next";
import Link from "next/link";
import { Heading, MonoLabel, Section, buttonVariants, cn } from "@neuropath/ui";
import { startProjectCta } from "@/lib/navigation";
import { bodyText, container } from "@/lib/styles";

// Not a public page: excluded from the sitemap and from indexing.
export const metadata: Metadata = {
  title: "Page not found",
  description: "The page you requested does not exist.",
  robots: { index: false, follow: true },
};

/** Styled 404 page with navigation (R13.7). Header and footer come from the root layout. */
export default function NotFound() {
  return (
    <main id={MAIN_CONTENT_ID} tabIndex={-1} className="focus:outline-none">
      <Section aria-labelledby="not-found-heading">
        <div className={container}>
          <MonoLabel>404</MonoLabel>
          <Heading id="not-found-heading" level={1} size="xl" className="mt-4 max-w-4xl">
            Page not found
          </Heading>
          {/* COPY FOR FOUNDER REVIEW */}
          <p className={cn(bodyText, "mt-4 max-w-3xl")}>
            The page you are looking for does not exist or has moved.
          </p>
          <nav aria-label="Not found" className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link href="/" className={buttonVariants({ variant: "outline", size: "lg" })}>
              Back to Home
            </Link>
            <Link href={startProjectCta.href} className={buttonVariants({ variant: "primary", size: "lg" })}>
              {startProjectCta.label}
            </Link>
          </nav>
        </div>
      </Section>
    </main>
  );
}
