import Link from "next/link";
import { UploadCloud } from "lucide-react";
import { GlassCard } from "@/components/shared/glass-card";
import { Button } from "@/components/ui/button";

export default function LibraryPage() {
  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-[var(--font-display)] text-3xl font-medium">Library</h1>
          <p className="mt-1 text-sm text-[var(--color-mist-500)]">Your uploaded playlists and taste profile.</p>
        </div>
        <Link href="/library/upload">
          <Button size="sm" variant="secondary">
            <UploadCloud size={16} /> Upload playlist
          </Button>
        </Link>
      </div>

      <GlassCard className="flex flex-col items-center justify-center gap-3 py-16 text-center">
        <UploadCloud size={28} className="text-[var(--color-mist-500)]" />
        <p className="text-sm text-[var(--color-mist-500)]">
          No playlists uploaded yet. Upload one and the Playlist Upload Analysis Agent
          will break down its genre and mood DNA in seconds.
        </p>
        <Link href="/library/upload">
          <Button size="sm" className="mt-2">Upload your first playlist</Button>
        </Link>
      </GlassCard>
    </div>
  );
}
