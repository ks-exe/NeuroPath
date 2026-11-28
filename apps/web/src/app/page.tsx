import { MAIN_CONTENT_ID } from "@/components/skip-link";
import Link from "next/link";
import { Card, Heading, MonoLabel, Section, buttonVariants, cn } from "@neuropath/ui";
import {
  getConfirmedWhyStatements,
  getServiceGroups,
  getSolutionsCapabilities,
  getVerifiedProjects,
} from "@content";
import { SectionHeader } from "@/components/section-header";
import { journeySteps } from "@/lib/journey";
import { startProjectCta, TAGLINE } from "@/lib/navigation";
import { pageMetadata } from "@/lib/site";

export const metadata = pageMetadata({
  title: "Technology. Engineered to Solve.",
  description:
    "Bring us your problem. We'll engineer the solution. NEUROPATH is a Technology Solutions & Engineering Company.",
  path: "/",
});

const SERVICES_HREF = "/services";
const SOLUTIONS_HREF = "/solutions";

const container = "mx-auto max-w-6xl px-4 md:px-6";
const bodyText = "font-body text-base text-muted-foreground";
const textLink =
  "rounded font-body text-sm font-medium text-foreground underline underline-offset-4 transition-colors duration-200 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background";

/** Problem types a client may bring, worded as listed in R10.6. */
const problemTypes: readonly string[] = [
  "A manual process",
  "An AI application need",
  "Workflow automation",
  "System integration",
  "A data pipeline or analytics need",
  "Cloud infrastructure",
  "Custom software",
  "Modernization",
  "An idea, without knowing the technology",
];

/**
 * Industries and business use cases.
 * COPY FOR FOUNDER REVIEW: the spec does not list industries or use cases.
 * These are generic descriptions of problem types and make no claim about
 * past customers, sectors served, or results.
 */
const useCases: readonly { title: string; description: string }[] = [
  {
    title: "Operations",
    description: "Repetitive tasks, approvals, and hand-offs that could run with less manual effort.",
  },
  {
    title: "Data and reporting",
    description: "Information spread across files and systems that needs to be collected, cleaned, and analysed.",
  },
  {
    title: "Customer-facing services",
    description: "Portals, applications, and assistants that serve customers or partners.",
  },
  {
    title: "Internal tools",
    description: "Software built around the way a team actually works.",
  },
  {
    title: "Legacy systems",
    description: "Existing systems that need to be integrated, moved to the cloud, or modernized.",
  },
];

/** Playground and Solution Architect appear only as supporting capabilities (R10.9). */
const supportingCapabilityIds = new Set(["data-engineering-playground", "ai-solution-architect"]);

export default function HomePage() {
  const serviceGroups = getServiceGroups();
  const projects = getVerifiedProjects();
  const whyStatements = getConfirmedWhyStatements();
  const supportingCapabilities = getSolutionsCapabilities().filter((c) => supportingCapabilityIds.has(c.id));

  return (
    <main id={MAIN_CONTENT_ID} tabIndex={-1} className="focus:outline-none">
      {/* Hero (R10.2, R10.3, R10.4, R10.5) */}
      <Section aria-labelledby="hero-heading" className="border-b border-border">
        <div className={container}>
          <MonoLabel>NEUROPATH</MonoLabel>
          <Heading id="hero-heading" level={1} size="xl" className="mt-4 max-w-4xl">
            Bring us your problem. We&apos;ll engineer the solution.
          </Heading>
          <p className={cn(bodyText, "mt-4 text-lg")}>{TAGLINE}</p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link href={startProjectCta.href} className={buttonVariants({ variant: "primary", size: "lg" })}>
              {startProjectCta.label}
            </Link>
            <Link href={SERVICES_HREF} className={buttonVariants({ variant: "outline", size: "lg" })}>
              Explore Our Capabilities
            </Link>
          </div>
        </div>
      </Section>

      {/* What We Solve (R10.6) */}
      <Section aria-labelledby="what-we-solve-heading">
        <div className={container}>
          <SectionHeader id="what-we-solve-heading" label="What We Solve" title="You don't need to know the technology" />
          <p className={cn(bodyText, "mt-4 max-w-3xl")}>
            You can come to us with any of the following, even if you don&apos;t know which technology fits.
          </p>
          <ul className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {problemTypes.map((item) => (
              <li key={item} className="rounded-card border border-border bg-card p-4 font-body text-card-foreground">
                {item}
              </li>
            ))}
          </ul>
        </div>
      </Section>

      {/* Engineering Capabilities (R10.7, R10.9) */}
      <Section aria-labelledby="capabilities-heading" className="border-t border-border">
        <div className={container}>
          <SectionHeader id="capabilities-heading" label="Engineering Capabilities" title="What we engineer" />
          <ul className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {serviceGroups.map((group) => (
              <li key={group.id}>
                <Card className="h-full">
                  <MonoLabel>{group.id}</MonoLabel>
                  <Heading level={3} size="sm" className="mt-2">
                    {group.name}
                  </Heading>
                  <ul className="mt-4 space-y-1 font-body text-sm text-muted-foreground">
                    {group.details.map((detail) => (
                      <li key={detail}>{detail}</li>
                    ))}
                  </ul>
                </Card>
              </li>
            ))}
          </ul>
          <p className="mt-6">
            <Link href={SERVICES_HREF} className={textLink}>
              See all services
            </Link>
          </p>

          {supportingCapabilities.length > 0 ? (
            <div className="mt-12">
              <Heading level={3} size="sm">
                Supporting capabilities
              </Heading>
              <ul className="mt-4 grid gap-4 md:grid-cols-2">
                {supportingCapabilities.map((capability) => (
                  <li key={capability.id} className="rounded-card border border-border p-4">
                    <p className="font-body font-medium text-foreground">{capability.name}</p>
                    <p className="mt-1 font-body text-sm text-muted-foreground">{capability.availabilityNote}</p>
                  </li>
                ))}
              </ul>
              <p className="mt-4">
                <Link href={SOLUTIONS_HREF} className={textLink}>
                  About our solutions
                </Link>
              </p>
            </div>
          ) : null}
        </div>
      </Section>

      {/* Industries and Business Use Cases */}
      <Section aria-labelledby="use-cases-heading" className="border-t border-border">
        <div className={container}>
          <SectionHeader id="use-cases-heading" label="Industries and Business Use Cases" title="Where problems come from" />
          <ul className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {useCases.map((useCase) => (
              <li key={useCase.title}>
                <Card className="h-full">
                  <Heading level={3} size="sm">
                    {useCase.title}
                  </Heading>
                  <p className="mt-2 font-body text-sm text-muted-foreground">{useCase.description}</p>
                </Card>
              </li>
            ))}
          </ul>
        </div>
      </Section>

      {/* Selected Projects and Case Studies (R11.1, R11.3, R11.4, R11.5) */}
      <Section aria-labelledby="projects-heading" className="border-t border-border">
        <div className={container}>
          <SectionHeader id="projects-heading" label="Selected Projects and Case Studies" title="Selected projects" />
          {projects.length === 0 ? (
            <p className={cn(bodyText, "mt-6")}>Case studies are being prepared.</p>
          ) : (
            <ul className="mt-8 grid gap-4 md:grid-cols-2">
              {projects.map((project) => (
                <li key={project.id}>
                  <Card className="h-full">
                    <Heading level={3} size="sm">
                      {project.title}
                    </Heading>
                    <p className="mt-2 font-body text-sm text-muted-foreground">{project.description}</p>
                    {project.technologies.length > 0 ? (
                      <ul className="mt-4 flex flex-wrap gap-2" aria-label="Technologies">
                        {project.technologies.map((tech) => (
                          <li key={tech} className="rounded border border-border px-2 py-1 font-mono text-xs text-foreground">
                            {tech}
                          </li>
                        ))}
                      </ul>
                    ) : null}
                  </Card>
                </li>
              ))}
            </ul>
          )}
        </div>
      </Section>

      {/* How We Work (R10.8) */}
      <Section aria-labelledby="how-we-work-heading" className="border-t border-border">
        <div className={container}>
          <SectionHeader id="how-we-work-heading" label="How We Work" title="From problem to running system" />
          <ol className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
            {journeySteps.map((step, index) => (
              <li key={step.name} className="rounded-card border border-border bg-card p-4">
                <MonoLabel>{String(index + 1).padStart(2, "0")}</MonoLabel>
                <p className="mt-2 font-body font-medium text-card-foreground">{step.name}</p>
              </li>
            ))}
          </ol>
          <p className="mt-6">
            <Link href="/how-we-work" className={textLink}>
              How we work in detail
            </Link>
          </p>
        </div>
      </Section>

      {/* Why NEUROPATH (R11.6): only Founder-confirmed statements. */}
      <Section aria-labelledby="why-heading" className="border-t border-border">
        <div className={container}>
          <SectionHeader id="why-heading" label="Why NEUROPATH" title="Why NEUROPATH" />
          {whyStatements.length === 0 ? (
            <p className={cn(bodyText, "mt-6")}>This section is being prepared.</p>
          ) : (
            <ul className="mt-8 grid gap-4 md:grid-cols-2">
              {whyStatements.map((statement) => (
                <li key={statement.id} className="rounded-card border border-border p-4 font-body text-foreground">
                  {statement.text}
                </li>
              ))}
            </ul>
          )}
        </div>
      </Section>

      {/* Final Project Inquiry CTA (R10.10) */}
      <Section aria-labelledby="final-cta-heading" className="border-t border-border bg-secondary">
        <div className={container}>
          <Heading id="final-cta-heading" level={2} size="lg" className="max-w-3xl">
            Have a problem to solve?
          </Heading>
          <p className={cn(bodyText, "mt-4 max-w-3xl")}>
            Describe it in your own words. You don&apos;t need to know the technology.
          </p>
          <Link href={startProjectCta.href} className={cn(buttonVariants({ variant: "primary", size: "lg" }), "mt-8")}>
            {startProjectCta.label}
          </Link>
        </div>
      </Section>
    </main>
  );
}
