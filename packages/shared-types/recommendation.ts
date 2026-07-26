import type { Track } from "./track";

export interface RecommendationBatch {
  tracks: Track[];
  arcLabel: string;
  generatedForMood: string;
}
