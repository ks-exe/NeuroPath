import { Heading, MonoLabel, Section } from "@neuropath/ui";

export default function HomePage() {
  return (
    <main>
      <Section>
        <MonoLabel>Neuropath</MonoLabel>
        <Heading level={1} size="xl" className="mt-2">
          NEUROPATH
        </Heading>
        <p className="mt-2 text-muted-foreground">Technology. Engineered to Solve.</p>
      </Section>
    </main>
  );
}
