"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

/**
 * The "vibe orb" — a pulsing aurora sphere used as the Conversation Agent's
 * avatar and the voice-input affordance. Its pulse speed maps to
 * `energy` (0-1), giving a lightweight visual signal that VibeAI is a living
 * companion, not a static chat window.
 */
export function VibeOrb({
  energy = 0.4,
  listening = false,
  size = 56,
  className,
}: {
  energy?: number;
  listening?: boolean;
  size?: number;
  className?: string;
}) {
  const duration = 2.6 - energy * 1.4;
  return (
    <motion.div
      className={cn("relative rounded-full", className)}
      style={{ width: size, height: size }}
    >
      <motion.div
        className="absolute inset-0 rounded-full bg-gradient-to-br from-[var(--color-grape)] via-[var(--color-grape-soft)] to-[var(--color-coral)]"
        animate={{ scale: listening ? [1, 1.15, 1] : [1, 1.05, 1] }}
        transition={{ duration, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute inset-0 rounded-full blur-md bg-gradient-to-br from-[var(--color-grape)] via-[var(--color-grape-soft)] to-[var(--color-coral)] opacity-70"
        animate={{ scale: listening ? [1.1, 1.4, 1.1] : [1, 1.1, 1] }}
        transition={{ duration: duration * 1.2, repeat: Infinity, ease: "easeInOut" }}
      />
    </motion.div>
  );
}
