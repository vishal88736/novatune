"use client";

import Image from "next/image";
import { SurfaceCard } from "@/components/shared/surface-card";
import { usePlayerStore } from "@/stores/player-store";

export function NowPlayingCard() {
  const track = usePlayerStore((s) => s.queue[s.currentIndex]);

  if (!track) {
    return (
      <SurfaceCard className="flex h-40 items-center justify-center text-sm text-[var(--color-ink-muted)]">
        Nothing queued yet — tell VibeAI how you're feeling to start.
      </SurfaceCard>
    );
  }

  return (
    <SurfaceCard strong className="flex gap-4">
      <Image
        src={track.thumbnailUrl}
        alt={track.title}
        width={88}
        height={88}
        className="rounded-xl object-cover"
      />
      <div className="flex flex-col justify-center">
        <p className="font-[var(--font-display)] text-base font-bold">{track.title}</p>
        <p className="text-sm text-[var(--color-ink-muted)]">{track.artist}</p>
        {track.reasonSummary && (
          <p className="mt-2 text-xs text-[var(--color-grape)]">{track.reasonSummary}</p>
        )}
      </div>
    </SurfaceCard>
  );
}
