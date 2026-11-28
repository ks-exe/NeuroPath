/** Id of the single <main> landmark on every page; target of the skip link (R15.6). */
export const MAIN_CONTENT_ID = "main-content";

/** First focusable element on every page; visible only while focused. */
export function SkipLink() {
  return (
    <a
      href={`#${MAIN_CONTENT_ID}`}
      className="sr-only rounded bg-primary px-4 py-2 font-body text-sm font-medium text-primary-foreground focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
    >
      Skip to main content
    </a>
  );
}
