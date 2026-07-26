import { z } from "zod";

export const playlistUploadSchema = z.object({
  source: z.enum(["upload_csv", "upload_url", "spotify_export", "manual"]),
  url: z.string().url().optional(),
  file: z.instanceof(File).optional(),
});
export type PlaylistUploadInput = z.infer<typeof playlistUploadSchema>;
