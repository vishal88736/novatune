"use client";

import { motion } from "framer-motion";
import { VibeOrb } from "@/components/magic/vibe-orb";

const AGENT_LABELS: Record<string, string> = {
  conversation_agent: "Thinking",
  mood_agent: "Reading your mood",
  recommendation_agent: "Finding tracks",
  sequencing_agent: "Building your arc",
  explainability_agent: "Writing the why",
  discovery_agent: "Digging for hidden gems",
};

export function AgentThinkingIndicator({ agent }: { agent: string | null }) {
  if (!agent) return null;
  return (
    <motion.div
      initial={{ opacity: 0, y: 4 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex items-center gap-3"
    >
      <VibeOrb size={28} energy={0.7} listening />
      <span className="text-xs text-[var(--color-mist-500)]">
        {AGENT_LABELS[agent] ?? "Working"}…
      </span>
    </motion.div>
  );
}
