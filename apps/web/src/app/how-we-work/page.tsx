import { MAIN_CONTENT_ID } from "@/components/skip-link";
import Link from "next/link";
import { Heading, MonoLabel, Section, buttonVariants, cn } from "@neuropath/ui";
import { journeySteps } from "@/lib/journey";
import { startProjectCta } from "@/lib/navigation";
import { pageMetadata } from "@/lib/site";
import { bodyText, container } from "@/lib/styles";

// COPY FOR FOUNDER REVIEW: description text is not given by the spec.
export const metadata = pageMetadata({
  title: "How We Work",
  description:
    "The NEUROPATH engagement journey from Discovery to Maintenance: what you provide and what we deliver at each step.",
  path: "/how-we-work",
});

export default function HowWeWorkPage() {
  return (
    <main id={MAIN_CONTENT_ID} tabIndex={-1} className="focus:outline-none">
      <Section aria-labelledby="how-we-work-heading" className="border-b border-border">
        <div className={container}>
          <MonoLabel>How We Work</MonoLabel>
          <Heading id="how-we-work-heading" level={1} size="xl" className="mt-4 max-w-4xl">
            From problem to running system
          </Heading>
          {/* Required statement (R13.4). */}
          <p className={cn(bodyText, "mt-4 max-w-3xl text-lg")}>
            AI-drafted material is reviewed by a NEUROPATH engineer before it reaches a client.
          </p>
        </div>
      </Section>

      {/* Journey steps, Discovery to Maintenance (R13.4) */}
      <Section aria-label="Engagement journey">
        <div className={container}>
          <ol className="space-y-4">
            {journeySteps.map((step, index) => (
              <li key={step.name} className="rounded-card border border-border bg-card p-6">
                <MonoLabel>{String(index + 1).padStart(2, "0")}</MonoLabel>
                <Heading level={2} size="md" className="mt-2">
                  {step.name}
                </Heading>
                <dl className="mt-4 grid gap-4 md:grid-cols-2">
                  <div>
                    <dt className="font-body text-sm font-medium text-card-foreground">What you provide</dt>
                    <dd className="mt-1 font-body text-sm text-muted-foreground">{step.clientProvides}</dd>
                  </div>
                  <div>
                    <dt className="font-body text-sm font-medium text-card-foreground">What NEUROPATH delivers</dt>
                    <dd className="mt-1 font-body text-sm text-muted-foreground">{step.neuropathDelivers}</dd>
                  </div>
                </dl>
              </li>
            ))}
          </ol>
        </div>
      </Section>

      <Section aria-labelledby="how-we-work-cta-heading" className="border-t border-border bg-secondary">
        <div className={container}>
          <Heading id="how-we-work-cta-heading" level={2} size="lg">
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
