import Link from "next/link";
import { cn } from "@neuropath/ui";
import { primaryNav, startProjectCta, TAGLINE } from "@/lib/navigation";

const linkClass = cn(
  "rounded font-body text-sm text-muted-foreground transition-colors duration-200 hover:text-foreground",
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background",
);

/** Footer with every navigation destination and the tagline (R9.6). */
export function SiteFooter() {
  return (
    <footer className="border-t border-border bg-background">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-10 md:flex-row md:items-start md:justify-between md:px-6">
        <div>
          <p className="font-heading text-lg font-semibold text-foreground">NEUROPATH</p>
          <p className="mt-1 font-body text-sm text-muted-foreground">{TAGLINE}</p>
        </div>
        <nav aria-label="Footer">
          <ul className="grid grid-cols-2 gap-x-8 gap-y-2 sm:grid-cols-3">
            {[...primaryNav, startProjectCta].map((item) => (
              <li key={item.href}>
                <Link href={item.href} className={linkClass}>
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </footer>
  );
}
