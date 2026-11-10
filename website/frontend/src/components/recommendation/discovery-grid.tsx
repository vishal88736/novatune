"use client";

import Image from "next/image";
import { SurfaceCard } from "@/components/shared/surface-card";
import { Badge } from "@/components/ui/badge";
import type { QueueTrack } from "@/stores/player-store";

export function DiscoveryGrid({ tracks, onPlay }: { tracks: QueueTrack[]; onPlay: (i: number) => void }) {
  return (
    <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
      {tracks.map((track, i) => (
        <SurfaceCard
          key={track.id}
          className="cursor-pointer !p-3 transition-transform hover:-translate-y-1"
          onClick={() => onPlay(i)}
        >
          <Image
            src={track.thumbnailUrl}
            alt={track.title}
            width={200}
            height={200}
            className="mb-3 aspect-square w-full rounded-lg object-cover"
          />
          <Badge className="mb-2 border-[var(--color-sun)]/40 bg-[var(--color-sun-wash)] text-[var(--color-sun-deep)]">
            Hidden gem
          </Badge>
          <p className="truncate text-sm font-medium">{track.title}</p>
          <p className="truncate text-xs text-[var(--color-ink-muted)]">{track.artist}</p>
        </SurfaceCard>
      ))}
    </div>
  );
}
