import { cn } from "@/lib/utils";

/**
 * The ambient wash behind the page: soft out-of-focus colour blooms over
 * the cream canvas. Pure CSS (see globals.css `.canvas-wash`) — no canvas
 * element, cheap to render.
 */
export function AuroraBackground({ className }: { className?: string }) {
  return (
    <div
      className={cn("canvas-wash pointer-events-none absolute inset-0 overflow-hidden", className)}
    />
  );
}
