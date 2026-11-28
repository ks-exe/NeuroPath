import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import type { ReactElement } from "react";
import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { getServiceGroups } from "@content";
import AboutPage from "@/app/about/page";
import ContactPage from "@/app/contact/page";
import HowWeWorkPage from "@/app/how-we-work/page";
import InsightsPage from "@/app/insights/page";
import NotFound from "@/app/not-found";
import HomePage from "@/app/page";
import ProjectsPage from "@/app/projects/page";
import ServiceGroupPage from "@/app/services/[group]/page";
import ServicesPage from "@/app/services/page";
import SolutionsPage from "@/app/solutions/page";
import StartAProjectPage from "@/app/start-a-project/page";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";

vi.mock("next/navigation", () => ({
  usePathname: () => "/does-not-exist",
  notFound: () => {
    throw new Error("notFound");
  },
}));

// The real form calls the API on mount; the page content is what is under test here.
vi.mock("@/components/inquiry-form", () => ({
  InquiryForm: () => <form aria-label="Project inquiry" />,
}));

const V1_TAGLINE = "Engineering Intelligence. Enabling Growth.";

afterEach(cleanup);

async function allPages(): Promise<{ name: string; element: ReactElement }[]> {
  const pages: { name: string; element: ReactElement }[] = [
    { name: "home", element: <HomePage /> },
    { name: "services", element: <ServicesPage /> },
    { name: "solutions", element: <SolutionsPage /> },
    { name: "projects", element: <ProjectsPage /> },
    { name: "how-we-work", element: <HowWeWorkPage /> },
    { name: "about", element: <AboutPage /> },
    { name: "insights", element: <InsightsPage /> },
    { name: "contact", element: <ContactPage /> },
    { name: "not-found", element: <NotFound /> },
    {
      name: "start-a-project",
      element: await StartAProjectPage({ searchParams: Promise.resolve({}) }),
    },
  ];
  for (const group of getServiceGroups()) {
    pages.push({
      name: `services/${group.slug}`,
      element: await ServiceGroupPage({ params: Promise.resolve({ group: group.slug }) }),
    });
  }
  return pages;
}

describe("HomePage section order (R10.1)", () => {
  it("renders the sections in the required order", () => {
    const { container } = render(<HomePage />);
    const ids = Array.from(container.querySelectorAll("section[aria-labelledby]")).map((section) =>
      section.getAttribute("aria-labelledby"),
    );
    expect(ids).toEqual([
      "hero-heading",
      "what-we-solve-heading",
      "capabilities-heading",
      "use-cases-heading",
      "projects-heading",
      "how-we-work-heading",
      "why-heading",
      "final-cta-heading",
    ]);
    for (const id of ids) {
      expect(document.getElementById(id as string)).not.toBeNull();
    }
  });
});

describe("Page content rules", () => {
  it("no page contains the V1 tagline and each page has exactly one h1 (R10.11)", async () => {
    for (const { name, element } of await allPages()) {
      const { container, unmount } = render(element);
      expect(container.textContent ?? "", name).not.toContain(V1_TAGLINE);
      expect(container.querySelectorAll("h1"), name).toHaveLength(1);
      unmount();
    }
  });

  it("no source or content file contains the V1 tagline (R10.11)", () => {
    // jsdom replaces the global URL, so resolve from __dirname (provided by vite-node).
    const webRoot = resolve(__dirname, "..");
    const thisFile = "pages-content.test.tsx";
    const files: string[] = [];
    const walk = (dir: string) => {
      for (const entry of readdirSync(dir)) {
        const full = join(dir, entry);
        if (statSync(full).isDirectory()) walk(full);
        else if (/\.tsx?$/.test(entry) && entry !== thisFile) files.push(full);
      }
    };
    walk(join(webRoot, "src"));
    walk(join(webRoot, "content"));

    expect(files.length).toBeGreaterThan(0);
    const offenders = files.filter((file) => readFileSync(file, "utf8").includes(V1_TAGLINE));
    expect(offenders).toEqual([]);
  });
});

describe("Not-found page (R13.7)", () => {
  it("renders a styled 404 with navigation inside the site chrome", () => {
    render(
      <>
        <SiteHeader authEnabled={false} />
        <NotFound />
        <SiteFooter />
      </>,
    );
    expect(screen.getByRole("heading", { level: 1, name: "Page not found" })).toBeInTheDocument();
    expect(screen.getByText("404")).toBeInTheDocument();
    const notFoundNav = screen.getByRole("navigation", { name: "Not found" });
    expect(within(notFoundNav).getByRole("link", { name: "Back to Home" })).toHaveAttribute("href", "/");
    expect(screen.getByRole("navigation", { name: "Primary" })).toBeInTheDocument();
  });
});
