import { cn } from "@/lib/utils";

export function Logo({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "font-[var(--font-display)] text-xl font-semibold tracking-tight text-[var(--color-mist-100)]",
        className,
      )}
    >
      Vibe<span className="text-gradient-aurora">AI</span>
    </span>
  );
}
