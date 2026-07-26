"use client";

import { useMutation } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { useMoodStore, type MoodVector } from "@/stores/mood-store";

interface MoodCheckinResponse {
  valence: number;
  arousal: number;
  label: string;
  emotionScores: Record<string, number>;
}

/** Submits a manual or text-derived mood signal to the Mood Agent (via backend). */
export function useMoodDetection() {
  const setCurrent = useMoodStore((s) => s.setCurrent);
  const pushHistory = useMoodStore((s) => s.pushHistory);

  return useMutation({
    mutationFn: (payload: { text?: string; moodTap?: string }) =>
      apiClient.post<MoodCheckinResponse>("/mood/checkin", payload),
    onSuccess: (data) => {
      const mood: MoodVector = {
        valence: data.valence,
        arousal: data.arousal,
        label: data.label,
        emotionScores: data.emotionScores,
      };
      setCurrent(mood);
      pushHistory({ timestamp: new Date().toISOString(), mood });
    },
  });
}
