import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-full text-sm font-semibold transition-all duration-200 disabled:pointer-events-none disabled:opacity-40 focus-visible:outline-none",
  {
    variants: {
      variant: {
        primary:
          "bg-[var(--color-grape)] text-white shadow-[var(--shadow-grape)] hover:bg-[var(--color-grape-deep)] active:scale-[0.98]",
        secondary:
          "surface text-[var(--color-ink)] hover:border-[var(--color-line-strong)] hover:bg-[var(--color-canvas-soft)]",
        ghost:
          "text-[var(--color-ink-soft)] hover:text-[var(--color-ink)] hover:bg-[var(--color-canvas-soft)]",
        outline:
          "border border-[var(--color-line-strong)] text-[var(--color-ink)] hover:bg-[var(--color-canvas-soft)]",
        accent:
          "bg-[var(--color-sun)] text-[var(--color-ink)] shadow-[0_12px_28px_-12px_rgb(223_167_36/0.9)] hover:bg-[var(--color-sun-deep)] active:scale-[0.98]",
      },
      size: {
        sm: "h-9 px-5 text-xs",
        md: "h-11 px-6",
        lg: "h-14 px-8 text-base",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: { variant: "primary", size: "md" },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button ref={ref} className={cn(buttonVariants({ variant, size }), className)} {...props} />
  ),
);
Button.displayName = "Button";
