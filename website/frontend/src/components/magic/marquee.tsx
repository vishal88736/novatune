"use client";

import { cn } from "@/lib/utils";

export function Marquee({
  items,
  className,
  reverse = false,
}: {
  items: string[];
  className?: string;
  reverse?: boolean;
}) {
  return (
    <div className={cn("relative overflow-hidden", className)}>
      <div
        className={cn(
          "flex w-max gap-8 whitespace-nowrap",
          reverse ? "animate-[marquee-reverse_28s_linear_infinite]" : "animate-[marquee_28s_linear_infinite]",
        )}
      >
        {[...items, ...items].map((item, i) => (
          <span key={i} className="text-sm text-[var(--color-ink-muted)]">
            {item}
          </span>
        ))}
      </div>
      <style jsx>{`
        @keyframes marquee {
          from { transform: translateX(0); }
          to { transform: translateX(-50%); }
        }
        @keyframes marquee-reverse {
          from { transform: translateX(-50%); }
          to { transform: translateX(0); }
        }
      `}</style>
    </div>
  );
}
