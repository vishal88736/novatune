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
    <div className={cn("surface-strong flex items-center gap-3.5 p-4", className)}>
      <div className="grid h-12 w-12 shrink-0 place-items-center rounded-full bg-[var(--color-grape)] text-white shadow-[var(--shadow-grape)]">
        <Disc3 size={22} strokeWidth={1.75} />
      </div>

      <div className="min-w-0 flex-1">
        <p className="truncate font-[var(--font-display)] text-sm font-bold text-[var(--color-ink)]">
          {title}
        </p>
        <p className="truncate text-xs text-[var(--color-ink-muted)]">{artist}</p>
      </div>

      <span className="hidden shrink-0 font-[var(--font-mono)] text-[11px] text-[var(--color-ink-muted)] sm:inline">
        {elapsed}
      </span>
      <div className="hidden h-1.5 w-16 shrink-0 overflow-hidden rounded-full bg-[var(--color-canvas-deep)] sm:block">
        <div className="h-full rounded-full bg-[var(--color-grape)]" style={{ width: `${progress}%` }} />
      </div>
      <button
        type="button"
        aria-label="Pause"
        className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-[var(--color-grape)] text-white shadow-[var(--shadow-grape)] transition-transform hover:scale-105"
      >
        <Pause size={16} fill="currentColor" />
      </button>
    </div>
  );
}
