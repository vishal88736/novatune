"use client";

import { GlassCard } from "@/components/shared/glass-card";
import { GenreRadar } from "@/components/analytics/genre-radar";
import { ListeningHeatmap } from "@/components/analytics/listening-heatmap";

const GENRE_DATA = [
  { genre: "Indie Folk", affinity: 80 }, { genre: "Lo-fi", affinity: 65 }, { genre: "Synthwave", affinity: 55 },
  { genre: "Jazz", affinity: 40 }, { genre: "Alt Rock", affinity: 70 }, { genre: "Ambient", affinity: 60 },
];

const HEATMAP = Array.from({ length: 7 }, () => Array.from({ length: 24 }, () => Math.random()));

export default function AnalyticsPage() {
  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="font-[var(--font-display)] text-3xl font-medium">Analytics</h1>
        <p className="mt-1 text-sm text-[var(--color-mist-500)]">The Analytics Agent's read on your listening patterns.</p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <GlassCard strong>
          <h3 className="mb-4 font-[var(--font-display)] text-base font-medium">Genre affinity</h3>
          <GenreRadar data={GENRE_DATA} />
        </GlassCard>
        <GlassCard strong>
          <h3 className="mb-4 font-[var(--font-display)] text-base font-medium">Listening heatmap</h3>
          <ListeningHeatmap data={HEATMAP} />
        </GlassCard>
      </div>
    </div>
  );
}
