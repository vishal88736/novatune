export interface MoodVector {
  valence: number;
  arousal: number;
  label: string;
  emotionScores?: Record<string, number>;
}
