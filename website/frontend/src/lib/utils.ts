import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Merge Tailwind class lists safely, resolving conflicting utilities. */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/** Format seconds as m:ss, used across player/track surfaces. */
export function formatDuration(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = Math.floor(totalSeconds % 60);
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
}

/** Map a GoEmotions-derived valence/arousal pair to a human label. */
export function moodLabelFromValenceArousal(valence: number, arousal: number): string {
  if (valence >= 0.3 && arousal >= 0.3) return "Euphoric";
  if (valence >= 0.3 && arousal < 0.3) return "Content";
  if (valence < -0.3 && arousal >= 0.3) return "Anxious";
  if (valence < -0.3 && arousal < 0.3) return "Melancholic";
  return "Neutral";
}
