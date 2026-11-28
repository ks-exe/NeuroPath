"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useId, useRef, useState } from "react";
import { Menu, X } from "lucide-react";
import { buttonVariants, cn } from "@neuropath/ui";
import { isCurrentPath, primaryNav, signInLink, startProjectCta } from "@/lib/navigation";

const focusRing =
  "rounded focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background";

const navLinkClass = (current: boolean) =>
  cn(
    "font-body text-sm transition-colors duration-200 hover:text-foreground",
    current ? "font-medium text-foreground" : "text-muted-foreground",
    focusRing,
  );

export interface SiteHeaderProps {
  /** Server-provided flag; the Sign In link renders only when true (R9.3). */
  authEnabled: boolean;
}

export function SiteHeader({ authEnabled }: SiteHeaderProps) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const menuId = useId();
  const toggleRef = useRef<HTMLButtonElement>(null);

  // Close the menu after navigation.
  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  // Close on Escape and return focus to the toggle.
  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setOpen(false);
        toggleRef.current?.focus();
      }
    };
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [open]);

  const close = () => setOpen(false);

  return (
    <header className="border-b border-border bg-background">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-4 md:px-6">
        <Link href="/" className={cn("font-heading text-lg font-semibold text-foreground", focusRing)}>
          NEUROPATH
        </Link>

        <nav aria-label="Primary" className="hidden md:block">
          <ul className="flex items-center gap-5">
            {primaryNav.map((item) => {
              const current = isCurrentPath(pathname, item.href);
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    aria-current={current ? "page" : undefined}
                    className={navLinkClass(current)}
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        <div className="hidden items-center gap-4 md:flex">
          {authEnabled ? (
            <Link
              href={signInLink.href}
              aria-current={isCurrentPath(pathname, signInLink.href) ? "page" : undefined}
              className={navLinkClass(isCurrentPath(pathname, signInLink.href))}
            >
              {signInLink.label}
            </Link>
          ) : null}
          <Link href={startProjectCta.href} className={buttonVariants({ variant: "primary", size: "md" })}>
            {startProjectCta.label}
          </Link>
        </div>

        <button
          ref={toggleRef}
          type="button"
          className={cn("inline-flex h-10 w-10 items-center justify-center text-foreground md:hidden", focusRing)}
          aria-expanded={open}
          aria-controls={menuId}
          aria-label={open ? "Close menu" : "Open menu"}
          onClick={() => setOpen((value) => !value)}
        >
          {open ? <X aria-hidden="true" className="h-5 w-5" /> : <Menu aria-hidden="true" className="h-5 w-5" />}
        </button>
      </div>

      <div id={menuId} hidden={!open} className="border-t border-border bg-background md:hidden">
        <nav aria-label="Primary mobile" className="mx-auto max-w-6xl px-4 py-4">
          <ul className="flex flex-col gap-3">
            {primaryNav.map((item) => {
              const current = isCurrentPath(pathname, item.href);
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    aria-current={current ? "page" : undefined}
                    className={navLinkClass(current)}
                    onClick={close}
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}
            {authEnabled ? (
              <li>
                <Link
                  href={signInLink.href}
                  aria-current={isCurrentPath(pathname, signInLink.href) ? "page" : undefined}
                  className={navLinkClass(isCurrentPath(pathname, signInLink.href))}
                  onClick={close}
                >
                  {signInLink.label}
                </Link>
              </li>
            ) : null}
          </ul>
          <Link
            href={startProjectCta.href}
            className={cn(buttonVariants({ variant: "primary", size: "md" }), "mt-4 w-full")}
            onClick={close}
          >
            {startProjectCta.label}
          </Link>
        </nav>
      </div>
    </header>
  );
}
