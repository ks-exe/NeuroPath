import * as React from "react";
import { cn } from "./cn";

export interface TextareaFieldProps extends Omit<React.TextareaHTMLAttributes<HTMLTextAreaElement>, "id"> {
  /** Visible label text (always rendered). */
  label: string;
  /** Used for the textarea id and the hint/error element ids. */
  id: string;
  hint?: string;
  error?: string;
  ref?: React.Ref<HTMLTextAreaElement>;
}

/** Multi-line counterpart of `Field`, with the same label, hint, and error pattern. */
export function TextareaField({
  label,
  id,
  hint,
  error,
  className,
  required,
  ref,
  rows = 4,
  "aria-describedby": describedBy,
  ...props
}: TextareaFieldProps) {
  const hintId = hint ? `${id}-hint` : undefined;
  const errorId = `${id}-error`;
  const ids = [describedBy, hintId, error ? errorId : undefined].filter(Boolean).join(" ") || undefined;

  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={id} className="text-sm font-medium text-foreground">
        {label}
        {required ? <span aria-hidden="true"> *</span> : null}
      </label>
      {hint ? (
        <p id={hintId} className="text-sm text-muted-foreground">
          {hint}
        </p>
      ) : null}
      <textarea
        ref={ref}
        id={id}
        rows={rows}
        required={required}
        aria-invalid={error ? true : undefined}
        aria-describedby={ids}
        className={cn(
          "rounded border border-input bg-background px-3 py-2 text-sm text-foreground transition-colors duration-200 placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50",
          error && "border-2 border-foreground",
          className,
        )}
        {...props}
      />
      {/* Always mounted so assistive tech announces text when it appears. */}
      <p id={errorId} role="alert" className={cn("text-sm font-medium text-foreground", !error && "-mt-1.5")}>
        {error ? <span className="font-mono">Error: </span> : null}
        {error}
      </p>
    </div>
  );
}
