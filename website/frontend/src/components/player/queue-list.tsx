"use client";

import Image from "next/image";
import { usePlayerStore } from "@/stores/player-store";
import { cn, formatDuration } from "@/lib/utils";

export function QueueList() {
  const { queue, currentIndex } = usePlayerStore();

  return (
    <ul className="flex flex-col gap-1">
      {queue.map((track, i) => (
        <li
          key={track.id}
          className={cn(
            "flex items-center gap-3 rounded-xl px-3 py-2 transition-colors",
            i === currentIndex ? "bg-[var(--color-grape-wash)]" : "hover:bg-[var(--color-canvas-soft)]",
          )}
        >
          <Image src={track.thumbnailUrl} alt={track.title} width={36} height={36} className="rounded-md" />
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm text-[var(--color-ink)]">{track.title}</p>
            <p className="truncate text-xs text-[var(--color-ink-muted)]">{track.artist}</p>
          </div>
          <span className="text-xs text-[var(--color-ink-muted)]">{formatDuration(track.durationSeconds)}</span>
        </li>
      ))}
    </ul>
  );
}
