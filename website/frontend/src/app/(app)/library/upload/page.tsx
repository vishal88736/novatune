"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { UploadCloud } from "lucide-react";
import { SurfaceCard } from "@/components/shared/surface-card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/lib/api-client";

export default function UploadPlaylistPage() {
  const [file, setFile] = useState<File | null>(null);

  const { mutate, isPending, data } = useMutation({
    mutationFn: async () => {
      const form = new FormData();
      if (file) form.append("file", file);
      form.append("source", "upload_csv");
      return apiClient.post<{ id: string; status: string }>("/playlists/upload", form);
    },
  });

  return (
    <div className="mx-auto flex max-w-xl flex-col gap-6">
      <div>
        <h1 className="font-[var(--font-display)] text-3xl font-bold">Upload a playlist</h1>
        <p className="mt-1 text-sm text-[var(--color-ink-muted)]">
          CSV export, Spotify export, or a share URL — the Playlist Upload Analysis Agent
          handles the parsing.
        </p>
      </div>

      <SurfaceCard strong>
        <label
          htmlFor="playlist-file"
          className="flex cursor-pointer flex-col items-center gap-3 rounded-xl border border-dashed border-[var(--color-line-strong)] py-12 text-center"
        >
          <UploadCloud size={26} className="text-[var(--color-grape)]" />
          <span className="text-sm text-[var(--color-ink-soft)]">
            {file ? file.name : "Click to choose a file, or drag it here"}
          </span>
          <input
            id="playlist-file"
            type="file"
            accept=".csv,.json"
            className="hidden"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
        </label>
        <Button onClick={() => mutate()} disabled={!file || isPending} className="mt-6 w-full">
          {isPending ? "Analyzing…" : "Analyze playlist"}
        </Button>
        {data && (
          <p className="mt-3 text-center text-xs text-[var(--color-grape)]">
            Queued for analysis — status: {data.status}
          </p>
        )}
      </SurfaceCard>
    </div>
  );
}
