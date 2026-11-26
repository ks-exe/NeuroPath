import * as React from "react";
import { cn } from "./cn";

export type MonoLabelProps = React.HTMLAttributes<HTMLSpanElement>;

export function MonoLabel({ className, ...props }: MonoLabelProps) {
  return <span className={cn("font-mono text-xs uppercase tracking-widest text-muted-foreground", className)} {...props} />;
}
