// @vitest-environment node
import { describe, expect, it } from "vitest";
import preset from "@neuropath/design-tokens/tailwind-preset";

/**
 * WCAG 2.2 AA contrast audit of the color pairings used in apps/web and packages/ui (R15.5).
 * Values come from the CSS variables the shared preset emits, so a token change re-runs the audit.
 */

type PluginWithHandler = { handler: (api: { addBase: (base: Record<string, Record<string, string>>) => void }) => void };

function readRootVars(): Record<string, string> {
  let root: Record<string, string> = {};
  for (const p of (preset.plugins ?? []) as unknown as PluginWithHandler[]) {
    p.handler({
      addBase: (base) => {
        if (base[":root"]) root = base[":root"];
      },
    });
  }
  return root;
}

const vars = readRootVars();

function channels(name: string): [number, number, number] {
  const value = vars[`--${name}`];
  if (!value) throw new Error(`Missing CSS variable --${name}`);
  const [r, g, b] = value.split(" ").map(Number);
  return [r ?? 0, g ?? 0, b ?? 0];
}

function luminance([r, g, b]: [number, number, number]): number {
  const lin = (c: number) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
}

function contrast(fg: string, bg: string): number {
  const a = luminance(channels(fg));
  const b = luminance(channels(bg));
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}

const TEXT = 4.5;
const NON_TEXT = 3;

// [foreground, background, threshold, where it is used]
const pairings: [string, string, number, string][] = [
  ["foreground", "background", TEXT, "body text, headings, labels, links"],
  ["muted-foreground", "background", TEXT, "body copy, hints, mono labels, nav links"],
  ["card-foreground", "card", TEXT, "card content"],
  ["foreground", "secondary", TEXT, "text on bg-secondary sections"],
  ["muted-foreground", "secondary", TEXT, "muted text on bg-secondary sections and confirmation panel"],
  ["secondary-foreground", "secondary", TEXT, "secondary button"],
  ["primary-foreground", "primary", TEXT, "primary button, skip link"],
  ["primary-foreground", "brand-dark", TEXT, "primary and secondary button hover"],
  ["foreground", "muted", TEXT, "muted surfaces"],
  ["primary", "background", TEXT, "link hover text"],
  ["primary", "secondary", TEXT, "link hover text on bg-secondary sections"],
  ["input", "background", NON_TEXT, "input, select, textarea and outline button borders"],
  ["ring", "background", NON_TEXT, "focus indicator on the page background"],
  ["ring", "secondary", NON_TEXT, "focus indicator on bg-secondary sections"],
  ["primary", "background", NON_TEXT, "checkbox accent color and primary button boundary"],
];

describe("WCAG 2.2 AA contrast of token pairings (R15.5)", () => {
  it.each(pairings)("%s on %s meets %d:1 (%s)", (fg, bg, threshold) => {
    const ratio = contrast(fg, bg);
    expect(ratio, `${fg} on ${bg} is ${ratio.toFixed(2)}:1`).toBeGreaterThanOrEqual(threshold);
  });

  it("reports the computed ratios", () => {
    const report = pairings.map(([fg, bg, t]) => `${fg} on ${bg}: ${contrast(fg, bg).toFixed(2)}:1 (min ${t})`);
    console.info(report.join("\n"));
    expect(report).toHaveLength(pairings.length);
  });
});
