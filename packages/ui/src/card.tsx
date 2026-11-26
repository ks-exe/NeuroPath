import * as React from "react";
import { cn } from "./cn";

export type CardProps = React.HTMLAttributes<HTMLDivElement>;

/** Flat surface: 1 px border, card radius (max 4 px), no shadow, gradient or blur. */
export function Card({ className, ...props }: CardProps) {
  return <div className={cn("rounded-card border border-border bg-card p-6 text-card-foreground", className)} {...props} />;
}
