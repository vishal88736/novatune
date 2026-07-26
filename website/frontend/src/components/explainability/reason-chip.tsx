import { Sparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export function ReasonChip({ reason }: { reason: string }) {
  return (
    <Badge className="gap-1.5 border-[var(--color-aurora-violet)]/30 bg-[var(--color-aurora-violet)]/10 text-[var(--color-mist-100)]">
      <Sparkles size={11} className="text-[var(--color-aurora-violet)]" />
      {reason}
    </Badge>
  );
}
