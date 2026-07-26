import { Badge } from "@/components/ui/badge";
import type { MoodVector } from "@/stores/mood-store";

export function EmotionBadge({ mood }: { mood: MoodVector }) {
  return (
    <Badge className="border-[var(--color-aurora-cyan)]/30 bg-[var(--color-aurora-cyan)]/10 text-[var(--color-aurora-cyan)]">
      Currently reading: {mood.label}
    </Badge>
  );
}
