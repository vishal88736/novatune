import { Disc3, Pause } from "lucide-react";
import { cn } from "@/lib/utils";

/**
 * The floating now-playing card used in the marketing hero. Unlike the
 * real PlayerDock (which is wired to playback state) this one is purely
 * presentational — it shows what the product feels like to use.
 */
export function PlayerPreview({
  title = "Cluster One",
  artist = "Pink Floyd",
  elapsed = "01:25",
  progress = 32,
  className,
}: {
  title?: string;
  artist?: string;
  elapsed?: string;
  progress?: number;
  className?: string;
}) {
  return (
    <div className={cn("surface-strong flex items-center gap-4 p-5", className)}>
      <div className="grid h-14 w-14 shrink-0 place-items-center rounded-full bg-[var(--color-grape)] text-white shadow-[var(--shadow-grape)]">
        <Disc3 size={26} strokeWidth={1.75} />
      </div>

      <div className="min-w-0 flex-1">
        <p className="truncate font-[var(--font-display)] text-base font-semibold text-[var(--color-ink)]">
          {title}
        </p>
        <p className="truncate text-sm text-[var(--color-ink-muted)]">{artist}</p>
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden items-center gap-3 sm:flex">
          <span className="font-[var(--font-mono)] text-xs text-[var(--color-ink-muted)]">{elapsed}</span>
          <div className="h-1.5 w-24 overflow-hidden rounded-full bg-[var(--color-canvas-deep)]">
            <div
              className="h-full rounded-full bg-[var(--color-grape)]"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
        <button
          type="button"
          aria-label="Pause"
          className="grid h-11 w-11 place-items-center rounded-full bg-[var(--color-grape)] text-white shadow-[var(--shadow-grape)] transition-transform hover:scale-105"
        >
          <Pause size={18} fill="currentColor" />
        </button>
      </div>
    </div>
  );
}
