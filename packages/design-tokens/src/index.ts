/**
 * NEUROPATH design tokens: "Editorial Brutalism x Engineering Journal" (R4).
 * Single source of truth for color, type, radius and motion.
 * No gradients, no glassmorphism (R4.4): flat colors only.
 */

/** Brand palette (R4.2). */
export const colors = {
  primary: "#762B3B",
  background: "#F4F0E9",
  dark: "#171515",
  secondary: "#D9D0C6",
  accent: "#A76C58",
} as const;

export type ColorToken = keyof typeof colors;

/** CSS variable names exposed for next/font (R4.3). */
export const fontVariables = {
  heading: "--font-heading",
  body: "--font-body",
  mono: "--font-mono",
} as const;

/** Font families (R4.3). Loaded in the web app via next/font. */
export const fonts = {
  heading: "Playfair Display",
  body: "Manrope",
  mono: "IBM Plex Mono",
} as const;

/** Maximum border radius for cards in px (R4.4). */
export const MAX_CARD_RADIUS_PX = 4;

export const radius = {
  none: "0px",
  sm: "2px",
  DEFAULT: `${MAX_CARD_RADIUS_PX}px`,
  card: `${MAX_CARD_RADIUS_PX}px`,
} as const;

/** Maximum motion duration in ms (R4.5). */
export const MAX_MOTION_MS = 300;

export const motion = {
  instant: 0,
  fast: 100,
  base: 200,
  slow: MAX_MOTION_MS,
} as const;

/** Convert "#RRGGBB" to "R G B" channels for `rgb(var(--x) / <alpha-value>)`. */
export function hexToRgbChannels(hex: string): string {
  const m = /^#([0-9a-f]{6})$/i.exec(hex);
  if (!m || !m[1]) {
    throw new Error(`Invalid hex color: ${hex}`);
  }
  const n = parseInt(m[1], 16);
  return `${(n >> 16) & 255} ${(n >> 8) & 255} ${n & 255}`;
}
