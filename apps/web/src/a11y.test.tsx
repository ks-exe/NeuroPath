import type { ReactElement } from "react";
import { cleanup, render } from "@testing-library/react";
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
import { MAIN_CONTENT_ID, SkipLink } from "@/components/skip-link";

vi.mock("next/navigation", () => ({
  usePathname: () => "/",
  notFound: () => {
    throw new Error("notFound");
  },
}));

vi.mock("@/components/inquiry-form", () => ({
  InquiryForm: () => <form aria-label="Project inquiry" />,
}));

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
    { name: "start-a-project", element: await StartAProjectPage({ searchParams: Promise.resolve({}) }) },
  ];
  for (const group of getServiceGroups()) {
    pages.push({
      name: `services/${group.slug}`,
      element: await ServiceGroupPage({ params: Promise.resolve({ group: group.slug }) }),
    });
  }
  return pages;
}

/** Renders a page inside the same chrome as the root layout. */
function renderWithLayout(page: ReactElement) {
  return render(
    <>
      <SkipLink />
      <SiteHeader authEnabled={false} />
      <div>{page}</div>
      <SiteFooter />
    </>,
  );
}

const FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])';

function accessibleName(el: Element): string {
  const labelledBy = el.getAttribute("aria-labelledby");
  const fromIds = labelledBy
    ? labelledBy
        .split(" ")
        .map((id) => document.getElementById(id)?.textContent ?? "")
        .join(" ")
    : "";
  return (el.getAttribute("aria-label") ?? fromIds ?? "").trim() || (el.textContent ?? "").trim();
}

describe("Keyboard and text alternatives on every public page (R15.4, R15.6)", () => {
  it("puts the skip link first and targets the single main landmark", async () => {
    for (const { name, element } of await allPages()) {
      const { container } = renderWithLayout(element);
      const first = container.querySelector(FOCUSABLE);
      expect(first?.textContent, name).toBe("Skip to main content");
      expect(first?.getAttribute("href"), name).toBe(`#${MAIN_CONTENT_ID}`);

      const mains = container.querySelectorAll("main");
      expect(mains, name).toHaveLength(1);
      expect(mains[0]?.id, name).toBe(MAIN_CONTENT_ID);
      expect(mains[0]?.getAttribute("tabindex"), name).toBe("-1");
      cleanup();
    }
  });

  it("gives every image alt text and every button and link an accessible name", async () => {
    for (const { name, element } of await allPages()) {
      const { container } = renderWithLayout(element);
      for (const img of Array.from(container.querySelectorAll("img"))) {
        expect(img.hasAttribute("alt"), `${name}: img without alt`).toBe(true);
      }
      for (const svg of Array.from(container.querySelectorAll("svg"))) {
        const decorative = svg.getAttribute("aria-hidden") === "true";
        const labelled = Boolean(svg.getAttribute("aria-label")) || svg.getAttribute("role") === "img";
        expect(decorative || labelled, `${name}: svg without aria-hidden or label`).toBe(true);
      }
      for (const control of Array.from(container.querySelectorAll("button, a[href]"))) {
        expect(accessibleName(control), `${name}: ${control.outerHTML.slice(0, 80)}`).not.toBe("");
      }
      cleanup();
    }
  });
});
