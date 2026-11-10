"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

const MOODS = [
  { label: "Euphoric", angle: -60, color: "var(--color-sun)" },
  { label: "Content", angle: -20, color: "var(--color-grape)" },
  { label: "Calm", angle: 20, color: "var(--color-grape)" },
  { label: "Melancholic", angle: 60, color: "var(--color-grape)" },
  { label: "Anxious", angle: 100, color: "var(--color-coral)" },
  { label: "Angry", angle: 140, color: "var(--color-coral)" },
  { label: "Nostalgic", angle: 180, color: "var(--color-grape)" },
  { label: "Motivated", angle: -100, color: "var(--color-sun)" },
];

/**
 * Radial mood-tap input — an alternative, faster path to a mood signal than
 * typing a full sentence to the Conversation Agent. Selecting a segment
 * posts directly to the Mood Agent via useMoodDetection.
 */
export function MoodWheel({ onSelect }: { onSelect: (label: string) => void }) {
  return (
    <div className="relative mx-auto h-72 w-72">
      <div className="absolute inset-0 rounded-full surface" />
      {MOODS.map((mood) => (
        <motion.button
          key={mood.label}
          onClick={() => onSelect(mood.label)}
          whileHover={{ scale: 1.08 }}
          whileTap={{ scale: 0.95 }}
          className={cn(
            "absolute left-1/2 top-1/2 flex h-16 w-16 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full text-center text-[11px] font-medium text-white shadow-lg",
          )}
          style={{
            transform: `rotate(${mood.angle}deg) translate(110px) rotate(${-mood.angle}deg) translate(-50%, -50%)`,
            background: `color-mix(in oklab, ${mood.color} 70%, var(--color-canvas-soft))`,
          }}
        >
          {mood.label}
        </motion.button>
      ))}
      <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-xs text-[var(--color-ink-muted)]">
        How's your vibe?
      </div>
    </div>
  );
}
