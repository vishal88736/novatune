"use client";

import { cn } from "@/lib/utils";

/**
 * The signature visual element of VibeAI: a slow-drifting three-color
 * aurora mesh behind a fixed grain/vignette. Pure CSS (see globals.css
 * `.aurora-field`) — no canvas, cheap to render, respects
 * prefers-reduced-motion automatically.
 */
export function AuroraBackground({ className }: { className?: string }) {
  return (
    <div className={cn("pointer-events-none absolute inset-0 overflow-hidden", className)}>
      <div className="aurora-field absolute inset-[-10%] opacity-60" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_0%,var(--color-void-950)_75%)]" />
    </div>
  );
}
