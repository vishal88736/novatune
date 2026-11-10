import { cn } from "@/lib/utils";

/**
 * The hand-drawn dashed curves that tie the hero together. Two shapes are
 * used across the layout: a long S-curve that sweeps up toward the nav,
 * and a shorter hook that drops toward the feature block. Each can end in
 * a solid arrowhead, a heart, or a plain taper.
 */
export type DoodleEnd = "arrow" | "heart" | "none";

const ARROW = "M0 0 L-9 -5.5 L-6 0 Z";
const HEART =
  "M0 5.2 C-7.5 -0.8 -6.4 -7.2 -2.4 -7.2 C-0.7 -7.2 0 -5.6 0 -4.6 C0 -5.6 0.7 -7.2 2.4 -7.2 C6.4 -7.2 7.5 -0.8 0 5.2 Z";

/**
 * Each curve is drawn in a 320x140 viewBox. `end` is the point the marker
 * is anchored to, and `rotate` orients the marker along the tangent there.
 */
const PATHS = {
  sweep: {
    d: "M6 132 C 78 132 62 34 148 34 C 236 34 214 112 286 12",
    end: { x: 286, y: 12, rotate: 18 },
  },
  hook: {
    d: "M312 14 C 250 14 262 96 176 96 C 96 96 112 26 40 30",
    end: { x: 40, y: 30, rotate: -160 },
  },
} as const;

export function Doodle({
  variant = "sweep",
  end = "arrow",
  className,
}: {
  variant?: keyof typeof PATHS;
  end?: DoodleEnd;
  className?: string;
}) {
  const path = PATHS[variant];
  const marker = end === "arrow" ? ARROW : end === "heart" ? HEART : null;

  return (
    <svg
      viewBox="0 0 320 140"
      fill="none"
      aria-hidden="true"
      className={cn("overflow-visible", className)}
    >
      <path d={path.d} className="doodle" />
      {marker ? (
        <g transform={`translate(${path.end.x} ${path.end.y}) rotate(${path.end.rotate})`}>
          <path d={marker} fill="currentColor" />
        </g>
      ) : null}
    </svg>
  );
}

/**
 * The loose elliptical ring the reference draws around a highlighted word.
 * Sized to hug the text it wraps.
 */
export function DoodleRing({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 240 84"
      fill="none"
      aria-hidden="true"
      preserveAspectRatio="none"
      className={cn("overflow-visible", className)}
    >
      <ellipse cx="120" cy="42" rx="114" ry="34" className="doodle-ring" />
    </svg>
  );
}
