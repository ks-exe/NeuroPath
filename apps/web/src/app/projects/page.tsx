import { MAIN_CONTENT_ID } from "@/components/skip-link";
import { Card, Heading, MonoLabel, Section, cn } from "@neuropath/ui";
import { getVerifiedProjects } from "@content";
import { pageMetadata } from "@/lib/site";
import { bodyText, container } from "@/lib/styles";

// COPY FOR FOUNDER REVIEW: description text is not given by the spec.
export const metadata = pageMetadata({
  title: "Projects",
  description: "Selected projects and case studies from NEUROPATH.",
  path: "/projects",
});

/** Lists verified projects only (R13.3 applying R11.1, R11.3, R11.5). */
export default function ProjectsPage() {
  const projects = getVerifiedProjects();

  return (
    <main id={MAIN_CONTENT_ID} tabIndex={-1} className="focus:outline-none">
      <Section aria-labelledby="projects-heading">
        <div className={container}>
          <MonoLabel>Projects</MonoLabel>
          <Heading id="projects-heading" level={1} size="xl" className="mt-4 max-w-4xl">
            Selected projects and case studies
          </Heading>
          {projects.length === 0 ? (
            <p className={cn(bodyText, "mt-6")}>Case studies are being prepared.</p>
          ) : (
            <ul className="mt-8 grid gap-4 md:grid-cols-2">
              {projects.map((project) => (
                <li key={project.id}>
                  <Card className="h-full">
                    <Heading level={2} size="sm">
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
    </main>
  );
}
