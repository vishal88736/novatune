"use client";

import { SurfaceCard } from "@/components/shared/surface-card";
import { MoodWheel } from "./mood-wheel";
import { useMoodDetection } from "@/hooks/use-mood-detection";
import { EmotionBadge } from "./emotion-badge";
import { useMoodStore } from "@/stores/mood-store";

export function MoodCheckinCard() {
  const { mutate, isPending } = useMoodDetection();
  const current = useMoodStore((s) => s.current);

  return (
    <SurfaceCard strong className="flex flex-col items-center gap-6 py-8">
      <MoodWheel onSelect={(label) => mutate({ moodTap: label })} />
      {isPending && <p className="text-xs text-[var(--color-ink-muted)]">Reading your vibe…</p>}
      {current && !isPending && <EmotionBadge mood={current} />}
    </SurfaceCard>
  );
}
