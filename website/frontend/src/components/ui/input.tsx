import * as React from "react";
import { cn } from "@/lib/utils";

export const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        "flex h-11 w-full rounded-xl border border-[var(--color-line)] bg-[var(--color-canvas-soft)] px-4 text-sm text-[var(--color-ink)] placeholder:text-[var(--color-ink-muted)] outline-none transition-colors focus:border-[var(--color-grape)]/60",
        className,
      )}
      {...props}
    />
  ),
);
Input.displayName = "Input";
