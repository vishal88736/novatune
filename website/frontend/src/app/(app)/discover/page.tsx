"use client";

import { DiscoveryGrid } from "@/components/recommendation/discovery-grid";
import { usePlayerStore } from "@/stores/player-store";

const HIDDEN_GEMS = [
  { id: "g1", youtubeVideoId: "abc123", title: "Undertow", artist: "Field Runner", durationSeconds: 214, thumbnailUrl: "https://i.ytimg.com/vi/abc123/hqdefault.jpg" },
  { id: "g2", youtubeVideoId: "def456", title: "Paper Boats", artist: "Nova Kestrel", durationSeconds: 187, thumbnailUrl: "https://i.ytimg.com/vi/def456/hqdefault.jpg" },
];

export default function DiscoverPage() {
  const setQueue = usePlayerStore((s) => s.setQueue);

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="font-[var(--font-display)] text-3xl font-medium">Discover</h1>
        <p className="mt-1 text-sm text-[var(--color-mist-500)]">
          The Discovery Agent deliberately surfaces artists the popularity algorithm buries.
        </p>
      </div>
      <DiscoveryGrid tracks={HIDDEN_GEMS} onPlay={() => setQueue(HIDDEN_GEMS)} />
    </div>
  );
}
