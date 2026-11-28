/** Single source of truth for site navigation, used by the header and footer (R9). */
export interface NavItem {
  readonly label: string;
  readonly href: string;
}

export const primaryNav: readonly NavItem[] = [
  { label: "Home", href: "/" },
  { label: "Services", href: "/services" },
  { label: "Solutions", href: "/solutions" },
  { label: "Projects", href: "/projects" },
  { label: "How We Work", href: "/how-we-work" },
  { label: "About", href: "/about" },
  { label: "Insights", href: "/insights" },
  { label: "Contact", href: "/contact" },
];

/** Header call to action; links to the project inquiry form (R9.2). */
export const startProjectCta: NavItem = { label: "Start a Project", href: "/start-a-project" };

/** Shown only when `features.authEnabled` is true (R9.3). */
export const signInLink: NavItem = { label: "Sign In", href: "/sign-in" };

export const TAGLINE = "Technology. Engineered to Solve.";

/** True when `href` is the current page (R9.5). A trailing slash is ignored. */
export function isCurrentPath(pathname: string | null, href: string): boolean {
  if (!pathname) return false;
  const normalized = pathname.length > 1 ? pathname.replace(/\/+$/, "") : pathname;
  return normalized === href;
}
