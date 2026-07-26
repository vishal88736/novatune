"use client";

import { useState } from "react";
import { Mic } from "lucide-react";
import { VibeOrb } from "@/components/magic/vibe-orb";

export function VoiceOrbButton({ onTranscript }: { onTranscript: (text: string) => void }) {
  const [listening, setListening] = useState(false);

  const handleClick = async () => {
    // Full implementation records via MediaRecorder and posts to
    // /api/backend/voice/transcribe (Groq Whisper). Wiring left to the
    // media-capture module.
    setListening((v) => !v);
    if (listening) onTranscript("");
  };

  return (
    <button
      onClick={handleClick}
      aria-label="Voice input"
      className="relative flex h-11 w-11 items-center justify-center rounded-full glass"
    >
      {listening ? <VibeOrb size={28} listening energy={0.8} /> : <Mic size={18} className="text-[var(--color-mist-300)]" />}
    </button>
  );
}
