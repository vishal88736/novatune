import { Badge } from "@/components/ui/badge";
import type { MoodVector } from "@/stores/mood-store";

export function EmotionBadge({ mood }: { mood: MoodVector }) {
  return (
    <Badge className="border-[var(--color-grape)]/30 bg-[var(--color-grape)]/10 text-[var(--color-grape)]">
      Currently reading: {mood.label}
    </Badge>
  );
}
