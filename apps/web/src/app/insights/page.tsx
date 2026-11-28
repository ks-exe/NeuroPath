import { MAIN_CONTENT_ID } from "@/components/skip-link";
import { Card, Heading, MonoLabel, Section, cn } from "@neuropath/ui";
import { getPublishedArticles } from "@content";
import { pageMetadata } from "@/lib/site";
import { bodyText, container } from "@/lib/styles";

// COPY FOR FOUNDER REVIEW: description text is not given by the spec.
export const metadata = pageMetadata({
  title: "Insights",
  description: "Articles from NEUROPATH.",
  path: "/insights",
});

const dateFormat = new Intl.DateTimeFormat("en", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" });

/** Lists published articles only; states that articles are forthcoming otherwise (R13.6). */
export default function InsightsPage() {
  const articles = getPublishedArticles();

  return (
    <main id={MAIN_CONTENT_ID} tabIndex={-1} className="focus:outline-none">
      <Section aria-labelledby="insights-heading">
        <div className={container}>
          <MonoLabel>Insights</MonoLabel>
          <Heading id="insights-heading" level={1} size="xl" className="mt-4 max-w-4xl">
            Insights
          </Heading>
          {articles.length === 0 ? (
            <p className={cn(bodyText, "mt-6")}>Articles are forthcoming.</p>
          ) : (
            <ul className="mt-8 grid gap-4 md:grid-cols-2">
              {articles.map((article) => (
                <li key={article.slug}>
                  <Card className="h-full">
                    <Heading level={2} size="sm">
                      {article.title}
                    </Heading>
                    {article.publishedAt ? (
                      <p className="mt-1 font-mono text-xs text-muted-foreground">
                        <time dateTime={article.publishedAt}>{dateFormat.format(new Date(article.publishedAt))}</time>
                      </p>
                    ) : null}
                    <p className="mt-2 font-body text-sm text-muted-foreground">{article.summary}</p>
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
