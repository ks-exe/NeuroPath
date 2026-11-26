import * as React from "react";
import { cn } from "./cn";

export type SectionProps = React.HTMLAttributes<HTMLElement>;

export function Section({ className, children, ...props }: SectionProps) {
  return (
    <section className={cn("py-16 md:py-24", className)} {...props}>
      <div className="mx-auto w-full max-w-6xl px-4 md:px-8">{children}</div>
    </section>
  );
}
