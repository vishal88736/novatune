"use client";

import Image from "next/image";
import { Pause, Play, SkipBack, SkipForward, Volume2 } from "lucide-react";
import { usePlayerStore } from "@/stores/player-store";
import { formatDuration, cn } from "@/lib/utils";

/**
 * Persistent bottom playback dock, present across the entire authenticated
 * shell. Reads/writes usePlayerStore; actual YouTube transport is driven by
 * useYoutubePlayer at the layout level.
 */
export function PlayerDock() {
  const { queue, currentIndex, isPlaying, progressSeconds, toggle, next, previous } =
    usePlayerStore();
  const track = queue[currentIndex];

  if (!track) return null;

  const progressPct = Math.min(100, (progressSeconds / Math.max(track.durationSeconds, 1)) * 100);

  return (
    <div className="fixed inset-x-0 bottom-0 z-40 border-t border-[var(--color-line)] bg-[var(--color-surface)]/90 backdrop-blur-2xl">
      <div className="h-1 w-full bg-[var(--color-canvas-soft)]">
        <div
          className="h-full bg-[var(--color-grape)] transition-[width] duration-300"
          style={{ width: `${progressPct}%` }}
        />
      </div>
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-3">
        <div className="flex min-w-0 items-center gap-3">
          <Image
            src={track.thumbnailUrl}
            alt={track.title}
            width={44}
            height={44}
            className="rounded-xl object-cover"
          />
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold text-[var(--color-ink)]">{track.title}</p>
            <p className="truncate text-xs text-[var(--color-ink-muted)]">{track.artist}</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button onClick={previous} aria-label="Previous track" className="text-[var(--color-ink-soft)] hover:text-[var(--color-grape)]">
            <SkipBack size={18} />
          </button>
          <button
            onClick={toggle}
            aria-label={isPlaying ? "Pause" : "Play"}
            className={cn(
              "flex h-10 w-10 items-center justify-center rounded-full bg-[var(--color-grape)] text-white shadow-[var(--shadow-grape)]",
            )}
          >
            {isPlaying ? <Pause size={18} /> : <Play size={18} className="ml-0.5" />}
          </button>
          <button onClick={next} aria-label="Next track" className="text-[var(--color-ink-soft)] hover:text-[var(--color-grape)]">
            <SkipForward size={18} />
          </button>
        </div>

        <div className="hidden items-center gap-2 text-xs text-[var(--color-ink-muted)] sm:flex">
          <span>{formatDuration(progressSeconds)}</span>
          <span>/</span>
          <span>{formatDuration(track.durationSeconds)}</span>
          <Volume2 size={16} className="ml-3" />
        </div>
      </div>
    </div>
  );
}
