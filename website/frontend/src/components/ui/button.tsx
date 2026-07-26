import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-full text-sm font-medium transition-all duration-200 disabled:pointer-events-none disabled:opacity-40 focus-visible:outline-none",
  {
    variants: {
      variant: {
        primary:
          "bg-gradient-to-r from-[var(--color-aurora-violet)] to-[var(--color-aurora-magenta)] text-white shadow-[0_0_24px_-4px_var(--color-aurora-violet)] hover:brightness-110 active:brightness-95",
        secondary: "glass text-[var(--color-mist-100)] hover:bg-white/10",
        ghost: "text-[var(--color-mist-300)] hover:text-[var(--color-mist-100)] hover:bg-white/5",
        outline: "border border-white/15 text-[var(--color-mist-100)] hover:border-white/30",
      },
      size: {
        sm: "h-9 px-4 text-xs",
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
