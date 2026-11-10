"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

const MOODS = [
  { label: "Motivated", angle: -135, color: "var(--color-sun)" },
  { label: "Euphoric", angle: -90, color: "var(--color-sun)" },
  { label: "Content", angle: -45, color: "var(--color-grape)" },
  { label: "Calm", angle: 0, color: "var(--color-grape)" },
  { label: "Melancholic", angle: 45, color: "var(--color-grape)" },
  { label: "Anxious", angle: 90, color: "var(--color-coral)" },
  { label: "Angry", angle: 135, color: "var(--color-coral)" },
  { label: "Nostalgic", angle: 180, color: "var(--color-grape)" },
];

/**
 * Radial mood-tap input — an alternative, faster path to a mood signal than
 * typing a full sentence to the Conversation Agent. Selecting a segment
 * posts directly to the Mood Agent via useMoodDetection.
 */
export function MoodWheel({ onSelect }: { onSelect: (label: string) => void }) {
  return (
    <div className="relative mx-auto h-80 w-80">
      <div className="absolute inset-0 rounded-full surface" />

      {MOODS.map((mood) => (
        <motion.button
          key={mood.label}
          onClick={() => onSelect(mood.label)}
          whileHover={{ scale: 1.08 }}
          whileTap={{ scale: 0.95 }}
          className={cn(
            "absolute left-1/2 top-1/2 flex h-16 w-16 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full px-1 text-center text-[10px] font-semibold leading-tight text-white shadow-lg",
          )}
          style={{
            transform: `rotate(${mood.angle}deg) translate(112px) rotate(${-mood.angle}deg) translate(-50%, -50%)`,
            background: `color-mix(in oklab, ${mood.color} 78%, var(--color-canvas-soft))`,
          }}
        >
          {mood.label}
        </motion.button>
      ))}

      {/* Hub keeps the prompt clear of the surrounding segments */}
      <div className="absolute left-1/2 top-1/2 grid h-28 w-28 -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full bg-[var(--color-surface)] text-center shadow-[var(--shadow-soft)]">
        <p className="px-2 text-[11px] font-medium leading-snug text-[var(--color-ink-muted)]">
          How&apos;s your vibe?
        </p>
      </div>
    </div>
  );
}
