import { cn } from "@/lib/utils";

/**
 * The wordmark: a grape "record" mark beside the product name, with the
 * AI half picked out in the brand colour.
 */
export function Logo({ className }: { className?: string }) {
  return (
    <span className={cn("inline-flex items-center gap-2.5", className)}>
      <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-[var(--color-grape)] shadow-[var(--shadow-grape)]">
        <svg viewBox="0 0 32 32" className="h-4 w-4" fill="none" aria-hidden="true">
          <circle cx="16" cy="16" r="9" stroke="white" strokeWidth="2.5" />
          <circle cx="16" cy="16" r="2.75" fill="white" />
        </svg>
      </span>
      <span className="font-[var(--font-display)] text-xl font-extrabold tracking-tight text-[var(--color-ink)]">
        Vibe<span className="italic text-[var(--color-grape)]">AI</span>
      </span>
    </span>
  );
}
