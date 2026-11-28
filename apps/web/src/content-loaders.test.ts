// @vitest-environment node
import { describe, expect, it } from "vitest";
import {
  getConfirmedAboutStatements,
  getConfirmedWhyStatements,
  getPublishedArticles,
  getServiceGroup,
  getServiceGroups,
  getSolutionsCapabilities,
  getVerifiedProjects,
  type Article,
  type Project,
  type Statement,
} from "@content";

// The "being prepared" / "forthcoming" UI states are rendered by pages (task 11).
// These tests cover the data side: loaders return empty arrays with no placeholders.

const project = (id: string, verification: Project["verification"]): Project => ({
  id,
  title: id,
  description: "d",
  technologies: [],
  verification,
});

const statement = (id: string, confirmed: boolean): Statement => ({ id, text: id, confirmed });

const article = (slug: string, published: boolean): Article => ({
  slug,
  title: slug,
  summary: "s",
  published,
});

describe("getVerifiedProjects (R11.2, R11.3, R11.5)", () => {
  it("returns only verified projects from a mixed source", () => {
    const source = [project("a", "verified"), project("b", "unverified"), project("c", "verified")];
    expect(getVerifiedProjects(source).map((p) => p.id)).toEqual(["a", "c"]);
  });

  it("returns an empty list when nothing is verified", () => {
    expect(getVerifiedProjects([project("x", "unverified")])).toEqual([]);
    expect(getVerifiedProjects([])).toEqual([]);
  });

  it("never returns the shipped unverified sample", () => {
    expect(getVerifiedProjects()).toEqual([]);
  });
});

describe("getPublishedArticles (R13.6)", () => {
  it("returns only published articles from a mixed source", () => {
    const source = [article("a", true), article("b", false)];
    expect(getPublishedArticles(source).map((a) => a.slug)).toEqual(["a"]);
  });

  it("returns an empty list for the shipped data", () => {
    expect(getPublishedArticles()).toEqual([]);
  });
});

describe("confirmed-only statements (R11.2)", () => {
  const mixed = [statement("yes", true), statement("no", false)];

  it("filters Why and About statements to confirmed ones", () => {
    expect(getConfirmedWhyStatements(mixed).map((s) => s.id)).toEqual(["yes"]);
    expect(getConfirmedAboutStatements(mixed).map((s) => s.id)).toEqual(["yes"]);
  });

  it("does not return shipped drafts", () => {
    expect(getConfirmedWhyStatements().every((s) => s.confirmed)).toBe(true);
    expect(getConfirmedAboutStatements().every((s) => s.confirmed)).toBe(true);
    expect(getConfirmedWhyStatements()).toEqual([]);
    expect(getConfirmedAboutStatements()).toEqual([]);
  });
});

describe("service groups", () => {
  it("returns six groups A to F in order, each with details", () => {
    const groups = getServiceGroups();
    expect(groups.map((g) => g.id)).toEqual(["A", "B", "C", "D", "E", "F"]);
    for (const group of groups) {
      expect(group.details.length).toBeGreaterThan(0);
    }
  });

  it("looks up a single group by id", () => {
    expect(getServiceGroup("B")?.id).toBe("B");
  });
});

describe("solutions capabilities", () => {
  it("each has an allowed availability status", () => {
    const allowed = ["available", "planned", "conditional"];
    const capabilities = getSolutionsCapabilities();
    expect(capabilities.length).toBeGreaterThan(0);
    for (const capability of capabilities) {
      expect(allowed).toContain(capability.availability);
    }
  });
});
