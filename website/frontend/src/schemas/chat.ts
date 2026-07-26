import { z } from "zod";

export const chatMessageSchema = z.object({
  message: z.string().min(1, "Say something first").max(2000),
});
export type ChatMessageInput = z.infer<typeof chatMessageSchema>;
