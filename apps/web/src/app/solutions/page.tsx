import { MAIN_CONTENT_ID } from "@/components/skip-link";
import Link from "next/link";
import { Card, Heading, MonoLabel, Section, buttonVariants, cn } from "@neuropath/ui";
import { getServiceGroups, getSolutionsCapabilities, type AvailabilityStatus } from "@content";
import { SectionHeader } from "@/components/section-header";
import { startProjectCta } from "@/lib/navigation";
import { pageMetadata } from "@/lib/site";
import { bodyText, container, textLink } from "@/lib/styles";

// COPY FOR FOUNDER REVIEW: title, description and intro text are not given by the spec.
export const metadata = pageMetadata({
  title: "Solutions",
  description:
    "Problem-oriented solution areas, and optional supporting capabilities with their current availability.",
  path: "/solutions",
});

/** Plain labels for each availability status (R13.2). */
const availabilityLabel: Record<AvailabilityStatus, string> = {
  available: "Available",
  planned: "Planned",
  conditional: "Not yet confirmed",
};

export default function SolutionsPage() {
  const groups = getServiceGroups();
  const capabilities = getSolutionsCapabilities();

  return (
    <main id={MAIN_CONTENT_ID} tabIndex={-1} className="focus:outline-none">
      <Section aria-labelledby="solutions-heading" className="border-b border-border">
        <div className={container}>
          <MonoLabel>Solutions</MonoLabel>
          <Heading id="solutions-heading" level={1} size="xl" className="mt-4 max-w-4xl">
            Solutions start with the problem
          </Heading>
          {/* COPY FOR FOUNDER REVIEW */}
          <p className={cn(bodyText, "mt-4 max-w-3xl text-lg")}>
            Describe the problem you want to solve. We work out which engineering areas apply.
          </p>
        </div>
      </Section>

      {/* Problem-oriented solution areas (R13.2) */}
      <Section aria-labelledby="areas-heading">
        <div className={container}>
          <SectionHeader id="areas-heading" label="Solution Areas" title="Problems we engineer for" />
          <ul className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {groups.map((group) => (
              <li key={group.id}>
                <Card className="h-full">
                  <Heading level={3} size="sm">
                    {group.name}
                  </Heading>
                  <ul className="mt-4 space-y-1 font-body text-sm text-muted-foreground">
                    {group.details.map((detail) => (
                      <li key={detail}>{detail}</li>
                    ))}
                  </ul>
                  <p className="mt-4">
                    <Link href={`/services/${group.slug}`} className={textLink}>
                      More about {group.name}
                    </Link>
                  </p>
                </Card>
              </li>
            ))}
          </ul>
        </div>
      </Section>

      {/* Optional supporting capabilities with availability status (R13.2) */}
      <Section aria-labelledby="supporting-heading" className="border-t border-border">
        <div className={container}>
          <SectionHeader id="supporting-heading" label="Supporting Capabilities" title="Optional supporting capabilities" />
          {/* COPY FOR FOUNDER REVIEW */}
          <p className={cn(bodyText, "mt-4 max-w-3xl")}>
            These capabilities are optional. You do not need them to start a project.
          </p>
          <ul className="mt-8 grid gap-4 md:grid-cols-3">
            {capabilities.map((capability) => (
              <li key={capability.id}>
                <Card className="h-full">
                  <Heading level={3} size="sm">
                    {capability.name}
                  </Heading>
                  <p className="mt-2">
                    <span className="rounded border border-border px-2 py-1 font-mono text-xs text-foreground">
                      Status: {availabilityLabel[capability.availability]}
                    </span>
                  </p>
                  <p className="mt-4 font-body text-sm text-muted-foreground">{capability.availabilityNote}</p>
                </Card>
              </li>
            ))}
          </ul>
        </div>
      </Section>

      <Section aria-labelledby="solutions-cta-heading" className="border-t border-border bg-secondary">
        <div className={container}>
          <Heading id="solutions-cta-heading" level={2} size="lg">
            Have a problem to solve?
          </Heading>
          <Link href={startProjectCta.href} className={cn(buttonVariants({ variant: "primary", size: "lg" }), "mt-8")}>
            {startProjectCta.label}
          </Link>
        </div>
      </Section>
    </main>
  );
}
