export interface Track {
  id: string;
  youtubeVideoId: string;
  title: string;
  artist: string;
  durationSeconds: number;
  thumbnailUrl: string;
  reasonSummary?: string;
}
