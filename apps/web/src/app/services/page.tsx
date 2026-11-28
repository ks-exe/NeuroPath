import { MAIN_CONTENT_ID } from "@/components/skip-link";
import Link from "next/link";
import { Card, Heading, MonoLabel, Section, buttonVariants, cn } from "@neuropath/ui";
import { getServiceGroups, SERVICES_FEASIBILITY_STATEMENT } from "@content";
import { startProjectCta } from "@/lib/navigation";
import { pageMetadata } from "@/lib/site";

export const metadata = pageMetadata({
  title: "Services",
  description:
    "Six engineering service groups: AI & ML, data, cloud and DevOps, custom software, automation and integration, and technical consulting.",
  path: "/services",
});

const container = "mx-auto max-w-6xl px-4 md:px-6";
const bodyText = "font-body text-base text-muted-foreground";
const textLink =
  "rounded font-body text-sm font-medium text-foreground underline underline-offset-4 transition-colors duration-200 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background";

export default function ServicesPage() {
  const groups = getServiceGroups();

  return (
    <main id={MAIN_CONTENT_ID} tabIndex={-1} className="focus:outline-none">
      <Section aria-labelledby="services-heading" className="border-b border-border">
        <div className={container}>
          <MonoLabel>Services</MonoLabel>
          <Heading id="services-heading" level={1} size="xl" className="mt-4 max-w-4xl">
            What we engineer
          </Heading>
          {/* R12.8 */}
          <p className={cn(bodyText, "mt-4 max-w-3xl text-lg")}>{SERVICES_FEASIBILITY_STATEMENT}</p>
          <nav aria-label="Service groups" className="mt-8">
            <ul className="flex flex-wrap gap-3">
              {groups.map((group) => (
                <li key={group.id}>
                  <a href={`#${group.slug}`} className={textLink}>
                    {group.id}. {group.name}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </Section>

      {/* Six service groups (R12.1 to R12.7, R12.9) */}
      {groups.map((group) => {
        const headingId = `${group.slug}-heading`;
        return (
          <Section key={group.id} id={group.slug} aria-labelledby={headingId} className="scroll-mt-20 border-t border-border">
            <div className={container}>
              <MonoLabel>{group.id}</MonoLabel>
              <Heading id={headingId} level={2} size="lg" className="mt-2">
                {group.name}
              </Heading>
              <Card className="mt-6">
                <ul className="grid gap-2 font-body text-sm text-card-foreground sm:grid-cols-2 lg:grid-cols-3">
                  {group.details.map((detail) => (
                    <li key={detail}>{detail}</li>
                  ))}
                </ul>
              </Card>
              {group.complianceNote ? (
                <p className={cn(bodyText, "mt-4 max-w-3xl text-sm")}>{group.complianceNote}</p>
              ) : null}
              <p className="mt-6">
                <Link href={`/services/${group.slug}`} className={textLink}>
                  {group.name} in detail
                </Link>
              </p>
            </div>
          </Section>
        );
      })}

      <Section aria-labelledby="services-cta-heading" className="border-t border-border bg-secondary">
        <div className={container}>
          <Heading id="services-cta-heading" level={2} size="lg" className="max-w-3xl">
            Not sure which group fits?
          </Heading>
          <p className={cn(bodyText, "mt-4 max-w-3xl")}>
            Describe the problem in your own words. You don&apos;t need to know the technology.
          </p>
          <Link href={startProjectCta.href} className={cn(buttonVariants({ variant: "primary", size: "lg" }), "mt-8")}>
            {startProjectCta.label}
          </Link>
        </div>
      </Section>
    </main>
  );
}
