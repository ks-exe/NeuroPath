import { MAIN_CONTENT_ID } from "@/components/skip-link";
import { Heading, MonoLabel, Section, cn } from "@neuropath/ui";
import { getServiceGroups } from "@content";
import { InquiryForm } from "@/components/inquiry-form";
import { parseServiceHint } from "@/lib/inquiry";
import { pageMetadata } from "@/lib/site";
import { bodyText, container } from "@/lib/styles";

export const metadata = pageMetadata({
  title: "Start a Project",
  description:
    "Describe the problem you want to solve. No technology choice is needed; NEUROPATH reviews each inquiry and responds.",
  path: "/start-a-project",
});

interface PageProps {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}

export default async function StartAProjectPage({ searchParams }: PageProps) {
  const params = await searchParams;
  // R12.11: only group ids A to F are accepted; anything else is ignored.
  const initialServiceHint = parseServiceHint(params.serviceHint);
  const serviceOptions = getServiceGroups().map((group) => ({ id: group.id, name: group.name }));

  return (
    <main id={MAIN_CONTENT_ID} tabIndex={-1} className="focus:outline-none">
      <Section aria-labelledby="start-heading">
        <div className={cn(container, "max-w-3xl")}>
          <MonoLabel>Start a Project</MonoLabel>
          <Heading id="start-heading" level={1} size="xl" className="mt-4">
            Tell us about your problem
          </Heading>
          <p className={cn(bodyText, "mt-4 text-lg")}>
            Describe what you want to solve. You do not need to know which technology fits. We review every
            inquiry and respond.
          </p>
          <div className="mt-10">
            <InquiryForm initialServiceHint={initialServiceHint} serviceOptions={serviceOptions} />
          </div>
        </div>
      </Section>
    </main>
  );
}
