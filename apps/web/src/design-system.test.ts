// @vitest-environment node
import { ESLint } from "eslint";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { colors, hexToRgbChannels, MAX_CARD_RADIUS_PX, MAX_MOTION_MS, motion, radius } from "@neuropath/design-tokens";
import preset from "@neuropath/design-tokens/tailwind-preset";

const extend = (preset.theme?.extend ?? {}) as Record<string, Record<string, string>>;

describe("design tokens (R4.2)", () => {
  it("defines the five brand colors", () => {
    expect(colors).toEqual({
      primary: "#762B3B",
      background: "#F4F0E9",
      dark: "#171515",
      secondary: "#D9D0C6",
      accent: "#A76C58",
    });
  });

  it("converts hex to rgb channels", () => {
    expect(hexToRgbChannels("#762B3B")).toBe("118 43 59");
    expect(() => hexToRgbChannels("red")).toThrow();
  });
});

describe("radius cap (R4.4)", () => {
  it("keeps every token and preset borderRadius at or below 4 px", () => {
    expect(MAX_CARD_RADIUS_PX).toBe(4);
    const values = [...Object.values(radius), ...Object.values(extend.borderRadius ?? {})];
    expect(values.length).toBeGreaterThan(0);
    for (const v of values) {
      expect(v).toMatch(/^\d+px$/);
      expect(parseFloat(v)).toBeLessThanOrEqual(4);
    }
  });
});

describe("motion cap (R4.5)", () => {
  it("keeps every token and preset transitionDuration at or below 300 ms", () => {
    expect(MAX_MOTION_MS).toBe(300);
    for (const v of Object.values(motion)) expect(v).toBeLessThanOrEqual(300);
    const durations = Object.values(extend.transitionDuration ?? {});
    expect(durations.length).toBeGreaterThan(0);
    for (const v of durations) {
      expect(v).toMatch(/^\d+ms$/);
      expect(parseFloat(v)).toBeLessThanOrEqual(300);
    }
  });
});

describe("lint rule: no gradients or glassmorphism (R4.4)", () => {
  const eslint = new ESLint({ cwd: fileURLToPath(new URL("..", import.meta.url)) });
  const lint = async (code: string) => {
    const [result] = await eslint.lintText(code, { filePath: "src/components/sample.tsx" });
    return (result?.messages ?? []).filter((m) => m.ruleId === "no-restricted-syntax");
  };

  it("rejects bg-gradient-* and backdrop-blur classes", async () => {
    const bad = [
      'export const A = () => <div className="bg-gradient-to-r from-red-500" />;\n',
      'export const B = () => <div className="p-4 backdrop-blur-md" />;\n',
      "export const c = `flex ${'x'} backdrop-blur`;\n",
    ];
    for (const code of bad) expect(await lint(code)).toHaveLength(1);
  }, 60_000);

  it("accepts flat classes", async () => {
    expect(await lint('export const A = () => <div className="bg-primary rounded p-4" />;\n')).toHaveLength(0);
  }, 60_000);
});
