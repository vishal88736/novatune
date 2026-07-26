import { create } from "zustand";

export interface QueueTrack {
  id: string;
  youtubeVideoId: string;
  title: string;
  artist: string;
  durationSeconds: number;
  thumbnailUrl: string;
  reasonSummary?: string;
}

interface PlayerState {
  queue: QueueTrack[];
  currentIndex: number;
  isPlaying: boolean;
  progressSeconds: number;
  volume: number;
  setQueue: (queue: QueueTrack[]) => void;
  play: () => void;
  pause: () => void;
  toggle: () => void;
  next: () => void;
  previous: () => void;
  setProgress: (seconds: number) => void;
  setVolume: (v: number) => void;
  currentTrack: () => QueueTrack | undefined;
}

export const usePlayerStore = create<PlayerState>((set, get) => ({
  queue: [],
  currentIndex: 0,
  isPlaying: false,
  progressSeconds: 0,
  volume: 0.8,
  setQueue: (queue) => set({ queue, currentIndex: 0, progressSeconds: 0 }),
  play: () => set({ isPlaying: true }),
  pause: () => set({ isPlaying: false }),
  toggle: () => set((s) => ({ isPlaying: !s.isPlaying })),
  next: () =>
    set((s) => ({
      currentIndex: Math.min(s.currentIndex + 1, Math.max(s.queue.length - 1, 0)),
      progressSeconds: 0,
    })),
  previous: () =>
    set((s) => ({ currentIndex: Math.max(s.currentIndex - 1, 0), progressSeconds: 0 })),
  setProgress: (progressSeconds) => set({ progressSeconds }),
  setVolume: (volume) => set({ volume }),
  currentTrack: () => get().queue[get().currentIndex],
}));
