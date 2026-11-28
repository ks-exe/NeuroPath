import { fireEvent, render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { isCurrentPath, primaryNav, signInLink, startProjectCta, TAGLINE } from "@/lib/navigation";

const nav = vi.hoisted(() => ({ pathname: "/" as string | null }));

vi.mock("next/navigation", () => ({
  usePathname: () => nav.pathname,
}));

function getToggle() {
  return screen.getByRole("button", { name: /menu/i });
}

function getMobileMenu() {
  const toggle = getToggle();
  const id = toggle.getAttribute("aria-controls");
  expect(id).toBeTruthy();
  const menu = document.getElementById(id as string);
  expect(menu).not.toBeNull();
  return menu as HTMLElement;
}

beforeEach(() => {
  nav.pathname = "/";
});

describe("isCurrentPath", () => {
  it("matches exact paths", () => {
    expect(isCurrentPath("/services", "/services")).toBe(true);
    expect(isCurrentPath("/services", "/solutions")).toBe(false);
    expect(isCurrentPath("/", "/")).toBe(true);
  });

  it("ignores a trailing slash", () => {
    expect(isCurrentPath("/services/", "/services")).toBe(true);
    expect(isCurrentPath("/", "/services")).toBe(false);
  });

  it("returns false for a null pathname", () => {
    expect(isCurrentPath(null, "/")).toBe(false);
  });
});

describe("SiteHeader menu toggle (R9.4)", () => {
  it("is a mobile-only toggle while the desktop nav shows from md (768 px)", () => {
    render(<SiteHeader authEnabled={false} />);
    expect(getToggle()).toHaveClass("md:hidden");
    const desktopNav = screen.getByRole("navigation", { name: "Primary" });
    expect(desktopNav).toHaveClass("hidden", "md:block");
  });

  it("opens and closes the menu and reflects state in aria-expanded", () => {
    render(<SiteHeader authEnabled={false} />);
    const toggle = getToggle();
    const menu = getMobileMenu();

    expect(toggle).toHaveAttribute("aria-expanded", "false");
    expect(menu).toHaveAttribute("hidden");

    fireEvent.click(toggle);
    expect(toggle).toHaveAttribute("aria-expanded", "true");
    expect(menu).not.toHaveAttribute("hidden");

    fireEvent.click(toggle);
    expect(toggle).toHaveAttribute("aria-expanded", "false");
    expect(menu).toHaveAttribute("hidden");
  });

  it("closes on Escape and returns focus to the toggle", () => {
    render(<SiteHeader authEnabled={false} />);
    const toggle = getToggle();
    fireEvent.click(toggle);
    const menu = getMobileMenu();
    within(menu).getByRole("link", { name: "Services" }).focus();

    fireEvent.keyDown(document, { key: "Escape" });

    expect(toggle).toHaveAttribute("aria-expanded", "false");
    expect(menu).toHaveAttribute("hidden");
    expect(toggle).toHaveFocus();
  });

  it("closes when a menu link is clicked", () => {
    render(<SiteHeader authEnabled={false} />);
    const toggle = getToggle();
    fireEvent.click(toggle);
    const menu = getMobileMenu();

    // jsdom cannot navigate; stop the anchor's default action after React handles the click.
    const preventNavigation = (event: Event) => event.preventDefault();
    document.addEventListener("click", preventNavigation);
    try {
      fireEvent.click(within(menu).getByRole("link", { name: "About" }));
    } finally {
      document.removeEventListener("click", preventNavigation);
    }

    expect(toggle).toHaveAttribute("aria-expanded", "false");
    expect(menu).toHaveAttribute("hidden");
  });
});

describe("SiteHeader aria-current (R9.5)", () => {
  it("marks only the link matching the current path", () => {
    nav.pathname = "/projects";
    render(<SiteHeader authEnabled={false} />);
    const desktopNav = screen.getByRole("navigation", { name: "Primary" });

    for (const item of primaryNav) {
      const link = within(desktopNav).getByRole("link", { name: item.label });
      if (item.href === "/projects") {
        expect(link).toHaveAttribute("aria-current", "page");
      } else {
        expect(link).not.toHaveAttribute("aria-current");
      }
    }
    const current = document.querySelectorAll('[aria-current="page"]');
    // One in the desktop nav, one in the mobile menu.
    expect(current).toHaveLength(2);
    current.forEach((el) => expect(el).toHaveAttribute("href", "/projects"));
  });

  it("marks nothing for an unknown path", () => {
    nav.pathname = "/does-not-exist";
    render(<SiteHeader authEnabled={true} />);
    expect(document.querySelectorAll("[aria-current]")).toHaveLength(0);
  });
});

describe("SiteHeader Sign In flag (R9.3)", () => {
  it("omits Sign In when auth is disabled", () => {
    render(<SiteHeader authEnabled={false} />);
    expect(screen.queryAllByRole("link", { name: signInLink.label, hidden: true })).toHaveLength(0);
    expect(screen.getAllByRole("link", { name: startProjectCta.label, hidden: true }).length).toBeGreaterThan(0);
  });

  it("shows Sign In when auth is enabled", () => {
    render(<SiteHeader authEnabled={true} />);
    const links = screen.getAllByRole("link", { name: signInLink.label, hidden: true });
    expect(links.length).toBeGreaterThan(0);
    links.forEach((link) => expect(link).toHaveAttribute("href", signInLink.href));
  });
});

describe("SiteFooter", () => {
  it("lists every primary destination and the tagline", () => {
    render(<SiteFooter />);
    const footerNav = screen.getByRole("navigation", { name: "Footer" });
    for (const item of [...primaryNav, startProjectCta]) {
      expect(within(footerNav).getByRole("link", { name: item.label })).toHaveAttribute("href", item.href);
    }
    expect(screen.getByText(TAGLINE)).toBeInTheDocument();
  });
});
