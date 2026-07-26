import { GlassCard } from "@/components/shared/glass-card";
import { CardHeader, CardTitle } from "@/components/ui/card";

export function ExplanationPanel({
  trackTitle,
  narrative,
  signals,
}: {
  trackTitle: string;
  narrative: string;
  signals: { label: string; weight: number }[];
}) {
  return (
    <GlassCard strong>
      <CardHeader>
        <CardTitle>Why "{trackTitle}"?</CardTitle>
      </CardHeader>
      <p className="mb-5 text-sm leading-relaxed text-[var(--color-mist-300)]">{narrative}</p>
      <div className="flex flex-col gap-2">
        {signals.map((s) => (
          <div key={s.label} className="flex items-center gap-3">
            <span className="w-32 shrink-0 text-xs text-[var(--color-mist-500)]">{s.label}</span>
            <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/5">
              <div
                className="h-full rounded-full bg-gradient-to-r from-[var(--color-aurora-violet)] to-[var(--color-aurora-cyan)]"
                style={{ width: `${Math.round(s.weight * 100)}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
}
