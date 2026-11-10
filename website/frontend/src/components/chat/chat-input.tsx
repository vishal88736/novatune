"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Send } from "lucide-react";
import { chatMessageSchema, type ChatMessageInput } from "@/schemas/chat";
import { VoiceOrbButton } from "./voice-orb-button";

export function ChatInput({ onSubmit }: { onSubmit: (text: string) => void }) {
  const { register, handleSubmit, reset } = useForm<ChatMessageInput>({
    resolver: zodResolver(chatMessageSchema),
  });

  const submit = handleSubmit(({ message }) => {
    onSubmit(message);
    reset();
  });

  return (
    <form onSubmit={submit} className="flex items-center gap-2 surface-strong p-2">
      <VoiceOrbButton onTranscript={(t) => t && onSubmit(t)} />
      <input
        {...register("message")}
        placeholder="Tell VibeAI how you're feeling…"
        className="flex-1 bg-transparent px-2 text-sm text-[var(--color-ink)] placeholder:text-[var(--color-ink-muted)] outline-none"
      />
      <button
        type="submit"
        aria-label="Send"
        className="flex h-10 w-10 items-center justify-center rounded-full bg-[var(--color-grape)] text-white shadow-[var(--shadow-grape)] transition-transform hover:scale-105"
      >
        <Send size={16} />
      </button>
    </form>
  );
}
