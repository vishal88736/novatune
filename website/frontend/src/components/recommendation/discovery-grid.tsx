"use client";

import Image from "next/image";
import { GlassCard } from "@/components/shared/glass-card";
import { Badge } from "@/components/ui/badge";
import type { QueueTrack } from "@/stores/player-store";

export function DiscoveryGrid({ tracks, onPlay }: { tracks: QueueTrack[]; onPlay: (i: number) => void }) {
  return (
    <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
      {tracks.map((track, i) => (
        <GlassCard
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
          <Badge className="mb-2 border-[var(--color-aurora-amber)]/30 bg-[var(--color-aurora-amber)]/10 text-[var(--color-aurora-amber)]">
            Hidden gem
          </Badge>
          <p className="truncate text-sm font-medium">{track.title}</p>
          <p className="truncate text-xs text-[var(--color-mist-500)]">{track.artist}</p>
        </GlassCard>
      ))}
    </div>
  );
}
