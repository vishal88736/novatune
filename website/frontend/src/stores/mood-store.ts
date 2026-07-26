import { create } from "zustand";

export interface MoodVector {
  valence: number; // -1 (negative) .. 1 (positive)
  arousal: number; // -1 (calm) .. 1 (energetic)
  label: string;
  emotionScores?: Record<string, number>;
}

interface MoodState {
  current: MoodVector | null;
  history: { timestamp: string; mood: MoodVector }[];
  setCurrent: (mood: MoodVector) => void;
  pushHistory: (entry: { timestamp: string; mood: MoodVector }) => void;
}

export const useMoodStore = create<MoodState>((set) => ({
  current: null,
  history: [],
  setCurrent: (current) => set({ current }),
  pushHistory: (entry) => set((s) => ({ history: [...s.history, entry] })),
}));
