import { Sparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export function ReasonChip({ reason }: { reason: string }) {
  return (
    <Badge className="gap-1.5 border-[var(--color-grape)]/30 bg-[var(--color-grape)]/10 text-[var(--color-ink)]">
      <Sparkles size={11} className="text-[var(--color-grape)]" />
      {reason}
    </Badge>
  );
}
