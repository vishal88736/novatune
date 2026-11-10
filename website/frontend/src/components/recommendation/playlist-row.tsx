"use client";

import { TrackCard } from "./track-card";
import type { QueueTrack } from "@/stores/player-store";

export function PlaylistRow({
  title,
  tracks,
  onPlayTrack,
}: {
  title: string;
  tracks: QueueTrack[];
  onPlayTrack: (index: number) => void;
}) {
  return (
    <section className="flex flex-col gap-3">
      <h3 className="font-[var(--font-display)] text-base font-bold text-[var(--color-ink)]">{title}</h3>
      <div className="flex flex-col gap-2">
        {tracks.map((t, i) => (
          <TrackCard key={t.id} track={t} onPlay={() => onPlayTrack(i)} />
        ))}
      </div>
    </section>
  );
}
