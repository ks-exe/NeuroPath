# Website content source

Plain TypeScript data modules for the public pages (R11, R12, R13). Pages read
them through the loaders in `index.ts` (import from `@content`). Loaders return
only entries you have approved, so nothing appears on the site until you set
its flag.

| File | What it holds | Flag that makes an entry visible |
| --- | --- | --- |
| `services.ts` | Service groups A to F and their detail lists | Always shown. Wording is fixed by R12.1 to R12.7. |
| `projects.ts` | Selected projects and case studies | `verification: "verified"` |
| `why.ts` | Why NEUROPATH statements about the working method | `confirmed: true` |
| `about.ts` | About page statements | `confirmed: true` |
| `insights.ts` | Insights articles | `published: true` (also set `publishedAt`) |
| `solutions.ts` | Optional supporting capabilities | Always shown with their `availability` status |

## Rules

- Add only true claims. No invented customers, client names, outcomes,
  metrics, prices, testimonials, certifications, or SLAs (R11.2).
- A project needs `title`, `description`, `technologies`, and `verification`.
  Set `verification: "verified"` only after you have checked the project is
  real and every claim in it is accurate. Anything else is hidden (R11.5).
- The drafts in `why.ts` and `about.ts` ship with `confirmed: false`. Edit the
  wording if needed, then set `confirmed: true` to publish them.
- While no project is verified, the Projects section says case studies are
  being prepared. While no article is published, Insights says articles are
  forthcoming. The `sample-unverified` project in `projects.ts` is a format
  example and is never displayed; delete it when you add a real project.
- In `solutions.ts`, change `availability` to `"available"` only when the
  capability is live, and update `availabilityNote` to match.

## Adding an entry

```ts
// projects.ts
{
  id: "short-kebab-id",
  title: "Project title",
  description: "What was built and why, in plain language.",
  technologies: ["Python", "AWS Lambda"],
  verification: "verified",
},
```

```ts
// insights.ts
{
  slug: "article-slug",
  title: "Article title",
  summary: "One or two sentences.",
  publishedAt: "2025-01-31",
  published: true,
},
```

Run `python scripts/dev.py web lint`, `web typecheck`, and `web test` after
editing.
