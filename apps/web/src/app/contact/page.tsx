import { MAIN_CONTENT_ID } from "@/components/skip-link";
import Link from "next/link";
import { Heading, MonoLabel, Section, buttonVariants, cn } from "@neuropath/ui";
import { startProjectCta } from "@/lib/navigation";
import { pageMetadata } from "@/lib/site";
import { bodyText, container } from "@/lib/styles";

// COPY FOR FOUNDER REVIEW: R13 does not define a Contact page. This page only
// points to the inquiry form. Real contact details (address, phone, email)
// need Founder input and must not be added until confirmed.
export const metadata = pageMetadata({
  title: "Contact",
  description: "Contact NEUROPATH through the project inquiry form.",
  path: "/contact",
});

export default function ContactPage() {
  return (
    <main id={MAIN_CONTENT_ID} tabIndex={-1} className="focus:outline-none">
      <Section aria-labelledby="contact-heading">
        <div className={container}>
          <MonoLabel>Contact</MonoLabel>
          <Heading id="contact-heading" level={1} size="xl" className="mt-4 max-w-4xl">
            Contact
          </Heading>
          <p className={cn(bodyText, "mt-4 max-w-3xl text-lg")}>
            To tell us about a problem or a project, use the project inquiry form.
          </p>
          <Link href={startProjectCta.href} className={cn(buttonVariants({ variant: "primary", size: "lg" }), "mt-8")}>
            {startProjectCta.label}
          </Link>
        </div>
      </Section>
    </main>
  );
}
