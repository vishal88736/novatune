"use client";

import { MoodCheckinCard } from "@/components/mood/mood-checkin-card";
import { NowPlayingCard } from "@/components/player/now-playing-card";
import { PlaylistRow } from "@/components/recommendation/playlist-row";
import { usePlayerStore } from "@/stores/player-store";

// Placeholder data — replaced at runtime by /recommendations (Recommendation +
// Sequencing Agents). Shapes mirror packages/shared-types.
const SAMPLE_QUEUE = [
  { id: "1", youtubeVideoId: "dQw4w9WgXcQ", title: "Golden Hour", artist: "Kacey Musgraves", durationSeconds: 199, thumbnailUrl: "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg", reasonSummary: "Matches your calm-but-hopeful mood" },
];

export default function DashboardPage() {
  const setQueue = usePlayerStore((s) => s.setQueue);

  return (
    <div className="flex flex-col gap-10">
      <div>
        <h1 className="font-[var(--font-display)] text-3xl font-bold">Today's Vibe</h1>
        <p className="mt-1 text-sm text-[var(--color-ink-muted)]">
          Check in, and VibeAI will build the next hour around how you actually feel.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_1.2fr]">
        <MoodCheckinCard />
        <NowPlayingCard />
      </div>

      <PlaylistRow
        title="Built for right now"
        tracks={SAMPLE_QUEUE}
        onPlayTrack={() => setQueue(SAMPLE_QUEUE)}
      />
    </div>
  );
}
