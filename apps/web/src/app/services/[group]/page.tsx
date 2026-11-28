import { MAIN_CONTENT_ID } from "@/components/skip-link";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Card, Heading, MonoLabel, Section, buttonVariants, cn } from "@neuropath/ui";
import { getServiceGroupBySlug, getServiceGroups, SERVICES_FEASIBILITY_STATEMENT } from "@content";
import { SectionHeader } from "@/components/section-header";
import { startProjectCta } from "@/lib/navigation";
import { pageMetadata } from "@/lib/site";

interface PageProps {
  params: Promise<{ group: string }>;
}

const container = "mx-auto max-w-6xl px-4 md:px-6";
const bodyText = "font-body text-base text-muted-foreground";
const textLink =
  "rounded font-body text-sm font-medium text-foreground underline underline-offset-4 transition-colors duration-200 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background";

export const dynamicParams = false;

export function generateStaticParams(): { group: string }[] {
  return getServiceGroups().map((group) => ({ group: group.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { group: slug } = await params;
  const group = getServiceGroupBySlug(slug);
  if (!group) return {};
  return pageMetadata({
    title: group.name,
    description: `${group.name}: ${group.details.slice(0, 4).join(", ")}, and more.`,
    path: `/services/${group.slug}`,
  });
}

export default async function ServiceGroupPage({ params }: PageProps) {
  const { group: slug } = await params;
  const group = getServiceGroupBySlug(slug);
  if (!group) notFound();

  // R12.10 sub-blocks: rendered only when the Founder has supplied content.
  const subBlocks = [
    { id: "engagements", label: "Typical Engagements", title: "Typical engagements", items: group.engagements },
    { id: "deliverables", label: "Deliverables", title: "Deliverables", items: group.deliverables },
    { id: "technologies", label: "Technologies", title: "Technologies", items: group.technologies },
  ].filter((block) => block.items.length > 0);

  // R12.11: the group is only an optional hint the visitor may change or clear.
  const startHref = `${startProjectCta.href}?serviceHint=${encodeURIComponent(group.id)}`;

  return (
    <main id={MAIN_CONTENT_ID} tabIndex={-1} className="focus:outline-none">
      <Section aria-labelledby="service-heading" className="border-b border-border">
        <div className={container}>
          <p>
            <Link href="/services" className={textLink}>
              All services
            </Link>
          </p>
          <MonoLabel className="mt-6 block">Service group {group.id}</MonoLabel>
          <Heading id="service-heading" level={1} size="xl" className="mt-4 max-w-4xl">
            {group.name}
          </Heading>
          {/* R12.8 */}
          <p className={cn(bodyText, "mt-4 max-w-3xl text-lg")}>{SERVICES_FEASIBILITY_STATEMENT}</p>
        </div>
      </Section>

      {/* R12.2 to R12.7 */}
      <Section aria-labelledby="service-scope-heading">
        <div className={container}>
          <SectionHeader id="service-scope-heading" label="Scope" title="What this covers" />
          <ul className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {group.details.map((detail) => (
              <li key={detail} className="rounded-card border border-border bg-card p-4 font-body text-card-foreground">
                {detail}
              </li>
            ))}
          </ul>
          {/* R12.9: groups B and E only */}
          {group.complianceNote ? (
            <p className={cn(bodyText, "mt-6 max-w-3xl text-sm")}>{group.complianceNote}</p>
          ) : null}
        </div>
      </Section>

      {subBlocks.map((block) => {
        const headingId = `service-${block.id}-heading`;
        return (
          <Section key={block.id} aria-labelledby={headingId} className="border-t border-border">
            <div className={container}>
              <SectionHeader id={headingId} label={block.label} title={block.title} />
              <Card className="mt-8">
                <ul className="space-y-2 font-body text-sm text-card-foreground">
                  {block.items.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </Card>
            </div>
          </Section>
        );
      })}

      {/* R12.11 */}
      <Section aria-labelledby="service-cta-heading" className="border-t border-border bg-secondary">
        <div className={container}>
          <Heading id="service-cta-heading" level={2} size="lg" className="max-w-3xl">
            Have a problem in this area?
          </Heading>
          <p className={cn(bodyText, "mt-4 max-w-3xl")}>
            Describe it in your own words. You can change or clear the selected service on the form.
          </p>
          <Link href={startHref} className={cn(buttonVariants({ variant: "primary", size: "lg" }), "mt-8")}>
            {startProjectCta.label}
          </Link>
        </div>
      </Section>
    </main>
  );
}
