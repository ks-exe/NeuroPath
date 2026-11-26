import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "./cn";

const headingVariants = cva("font-heading font-semibold text-foreground", {
  variants: {
    size: {
      xl: "text-4xl md:text-5xl",
      lg: "text-3xl md:text-4xl",
      md: "text-2xl",
      sm: "text-xl",
    },
  },
  defaultVariants: { size: "lg" },
});

export interface HeadingProps
  extends React.HTMLAttributes<HTMLHeadingElement>,
    VariantProps<typeof headingVariants> {
  /** Semantic level; independent from visual size. */
  level?: 1 | 2 | 3 | 4;
}

export function Heading({ level = 2, size, className, ...props }: HeadingProps) {
  const Tag = `h${level}` as const;
  return <Tag className={cn(headingVariants({ size }), className)} {...props} />;
}
