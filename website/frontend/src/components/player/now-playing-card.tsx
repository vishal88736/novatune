"use client";

import Image from "next/image";
import { GlassCard } from "@/components/shared/glass-card";
import { usePlayerStore } from "@/stores/player-store";

export function NowPlayingCard() {
  const track = usePlayerStore((s) => s.queue[s.currentIndex]);

  if (!track) {
    return (
      <GlassCard className="flex h-40 items-center justify-center text-sm text-[var(--color-mist-500)]">
        Nothing queued yet — tell VibeAI how you're feeling to start.
      </GlassCard>
    );
  }

  return (
    <GlassCard strong className="flex gap-4">
      <Image
        src={track.thumbnailUrl}
        alt={track.title}
        width={88}
        height={88}
        className="rounded-xl object-cover"
      />
      <div className="flex flex-col justify-center">
        <p className="font-[var(--font-display)] text-base font-medium">{track.title}</p>
        <p className="text-sm text-[var(--color-mist-500)]">{track.artist}</p>
        {track.reasonSummary && (
          <p className="mt-2 text-xs text-[var(--color-aurora-cyan)]">{track.reasonSummary}</p>
        )}
      </div>
    </GlassCard>
  );
}
