import { MAIN_CONTENT_ID } from "@/components/skip-link";
import { Heading, MonoLabel, Section, cn } from "@neuropath/ui";
import { getConfirmedAboutStatements } from "@content";
import { pageMetadata } from "@/lib/site";
import { bodyText, container } from "@/lib/styles";

export const metadata = pageMetadata({
  title: "About",
  description: "NEUROPATH is a Technology Solutions & Engineering Company.",
  path: "/about",
});

/**
 * Shows the company description required by R13.5 and Founder-confirmed
 * statements only. No history, team, figures or clients are written here.
 */
export default function AboutPage() {
  const statements = getConfirmedAboutStatements();

  return (
    <main id={MAIN_CONTENT_ID} tabIndex={-1} className="focus:outline-none">
      <Section aria-labelledby="about-heading">
        <div className={container}>
          <MonoLabel>About</MonoLabel>
          <Heading id="about-heading" level={1} size="xl" className="mt-4 max-w-4xl">
            About NEUROPATH
          </Heading>
          <p className={cn(bodyText, "mt-4 max-w-3xl text-lg")}>
            NEUROPATH is a Technology Solutions &amp; Engineering Company.
          </p>
          {statements.length === 0 ? (
            // COPY FOR FOUNDER REVIEW: neutral placeholder until About statements are confirmed.
            <p className={cn(bodyText, "mt-6")}>More about NEUROPATH is being prepared.</p>
          ) : (
            <ul className="mt-8 max-w-3xl space-y-4">
              {statements.map((statement) => (
                <li key={statement.id} className="font-body text-base text-foreground">
                  {statement.text}
                </li>
              ))}
            </ul>
          )}
        </div>
      </Section>
    </main>
  );
}
