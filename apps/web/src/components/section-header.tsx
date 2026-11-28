import { Heading, MonoLabel } from "@neuropath/ui";

/** Mono label above an h2, shared by marketing pages. */
export function SectionHeader({ id, label, title }: { id: string; label: string; title: string }) {
  return (
    <div className="max-w-3xl">
      <MonoLabel>{label}</MonoLabel>
      <Heading id={id} level={2} size="lg" className="mt-2">
        {title}
      </Heading>
    </div>
  );
}
