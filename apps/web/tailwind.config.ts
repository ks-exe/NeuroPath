import type { Config } from "tailwindcss";
import tailwindcssAnimate from "tailwindcss-animate";
import designTokensPreset from "@neuropath/design-tokens/tailwind-preset";

// Palette, fonts, radius and motion come from packages/design-tokens (R4).
const config: Config = {
  darkMode: ["class"],
  presets: [designTokensPreset as Config],
  content: ["./src/**/*.{ts,tsx}", "../../packages/ui/src/**/*.{ts,tsx}"],
  plugins: [tailwindcssAnimate],
};

export default config;
