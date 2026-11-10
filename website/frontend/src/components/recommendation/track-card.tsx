"use client";

import Image from "next/image";
import { Play } from "lucide-react";
import { SurfaceCard } from "@/components/shared/surface-card";
import { formatDuration } from "@/lib/utils";
import type { QueueTrack } from "@/stores/player-store";

export function TrackCard({ track, onPlay }: { track: QueueTrack; onPlay: () => void }) {
  return (
    <SurfaceCard className="group flex items-center gap-4 !p-3 transition-colors hover:bg-[var(--color-grape-wash)]">
      <div className="relative shrink-0">
        <Image src={track.thumbnailUrl} alt={track.title} width={56} height={56} className="rounded-lg object-cover" />
        <button
          onClick={onPlay}
          aria-label={`Play ${track.title}`}
          className="absolute inset-0 flex items-center justify-center rounded-lg bg-black/50 opacity-0 transition-opacity group-hover:opacity-100"
        >
          <Play size={18} className="text-white" />
        </button>
      </div>
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium text-[var(--color-ink)]">{track.title}</p>
        <p className="truncate text-xs text-[var(--color-ink-muted)]">{track.artist}</p>
        {track.reasonSummary && (
          <p className="mt-1 truncate text-[11px] text-[var(--color-grape)]">{track.reasonSummary}</p>
        )}
      </div>
      <span className="shrink-0 text-xs text-[var(--color-ink-muted)]">{formatDuration(track.durationSeconds)}</span>
    </SurfaceCard>
  );
}
