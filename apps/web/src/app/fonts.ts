import { IBM_Plex_Mono, Manrope, Playfair_Display } from "next/font/google";

// CSS variable names match fontVariables in @neuropath/design-tokens (R4.3).
export const headingFont = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-heading",
  display: "swap",
});

export const bodyFont = Manrope({
  subsets: ["latin"],
  variable: "--font-body",
  display: "swap",
});

export const monoFont = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono",
  display: "swap",
});
