import plugin from "tailwindcss/plugin";
import type { Config } from "tailwindcss";
import { colors, fontVariables, hexToRgbChannels, motion, radius } from "./index";

const rgb = (name: string) => `rgb(var(--${name}) / <alpha-value>)`;

/**
 * Shared Tailwind preset. Emits the CSS variables from the tokens, so the
 * palette is defined in one place (R4.1). Semantic names follow shadcn/ui.
 */
const preset: Partial<Config> = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: rgb("brand-primary"),
          background: rgb("brand-background"),
          dark: rgb("brand-dark"),
          secondary: rgb("brand-secondary"),
          accent: rgb("brand-accent"),
        },
        border: rgb("border"),
        input: rgb("input"),
        ring: rgb("ring"),
        background: rgb("background"),
        foreground: rgb("foreground"),
        primary: { DEFAULT: rgb("primary"), foreground: rgb("primary-foreground") },
        secondary: { DEFAULT: rgb("secondary"), foreground: rgb("secondary-foreground") },
        accent: { DEFAULT: rgb("accent"), foreground: rgb("accent-foreground") },
        muted: { DEFAULT: rgb("muted"), foreground: rgb("muted-foreground") },
        card: { DEFAULT: rgb("card"), foreground: rgb("card-foreground") },
      },
      fontFamily: {
        heading: [`var(${fontVariables.heading})`, "Georgia", "serif"],
        body: [`var(${fontVariables.body})`, "system-ui", "sans-serif"],
        mono: [`var(${fontVariables.mono})`, "ui-monospace", "monospace"],
        sans: [`var(${fontVariables.body})`, "system-ui", "sans-serif"],
        serif: [`var(${fontVariables.heading})`, "Georgia", "serif"],
      },
      // Every radius is capped at the 4 px card maximum (R4.4).
      borderRadius: {
        none: radius.none,
        sm: radius.sm,
        DEFAULT: radius.DEFAULT,
        md: radius.DEFAULT,
        lg: radius.DEFAULT,
        xl: radius.DEFAULT,
        "2xl": radius.DEFAULT,
        "3xl": radius.DEFAULT,
        card: radius.card,
      },
      // Transitions are capped at 300 ms (R4.5).
      transitionDuration: {
        DEFAULT: `${motion.base}ms`,
        0: "0ms",
        75: "75ms",
        100: `${motion.fast}ms`,
        150: "150ms",
        200: `${motion.base}ms`,
        300: `${motion.slow}ms`,
      },
    },
  },
  plugins: [
    plugin(({ addBase }) => {
      const c = colors;
      const vars: Record<string, string> = {
        "--brand-primary": hexToRgbChannels(c.primary),
        "--brand-background": hexToRgbChannels(c.background),
        "--brand-dark": hexToRgbChannels(c.dark),
        "--brand-secondary": hexToRgbChannels(c.secondary),
        "--brand-accent": hexToRgbChannels(c.accent),
        "--background": hexToRgbChannels(c.background),
        "--foreground": hexToRgbChannels(c.dark),
        "--card": hexToRgbChannels(c.background),
        "--card-foreground": hexToRgbChannels(c.dark),
        "--primary": hexToRgbChannels(c.primary),
        "--primary-foreground": hexToRgbChannels(c.background),
        "--secondary": hexToRgbChannels(c.secondary),
        "--secondary-foreground": hexToRgbChannels(c.dark),
        "--accent": hexToRgbChannels(c.accent),
        "--accent-foreground": hexToRgbChannels(c.dark),
        "--muted": hexToRgbChannels(c.secondary),
        "--muted-foreground": "75 71 71",
        "--border": hexToRgbChannels(c.secondary),
        // Form control borders need 3:1 against the background (WCAG 1.4.11, R15.5).
        "--input": hexToRgbChannels(c.accent),
        "--ring": hexToRgbChannels(c.primary),
        "--radius": radius.DEFAULT,
      };
      addBase({
        ":root": vars,
        body: {
          fontFamily: `var(${fontVariables.body}), system-ui, sans-serif`,
        },
        "h1, h2, h3, h4, h5, h6": {
          fontFamily: `var(${fontVariables.heading}), Georgia, serif`,
        },
        "code, kbd, pre, samp": {
          fontFamily: `var(${fontVariables.mono}), ui-monospace, monospace`,
        },
        // Disable non-essential animation for reduced-motion users (R4.6).
        "@media (prefers-reduced-motion: reduce)": {
          "*, *::before, *::after": {
            animationDuration: "0.01ms !important",
            animationIterationCount: "1 !important",
            transitionDuration: "0.01ms !important",
            scrollBehavior: "auto !important",
          },
        },
      });
    }),
  ],
};

export default preset;
