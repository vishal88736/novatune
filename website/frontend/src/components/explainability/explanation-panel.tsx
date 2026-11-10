import { SurfaceCard } from "@/components/shared/surface-card";
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
    <SurfaceCard strong>
      <CardHeader>
        <CardTitle>Why "{trackTitle}"?</CardTitle>
      </CardHeader>
      <p className="mb-5 text-sm leading-relaxed text-[var(--color-ink-soft)]">{narrative}</p>
      <div className="flex flex-col gap-2">
        {signals.map((s) => (
          <div key={s.label} className="flex items-center gap-3">
            <span className="w-32 shrink-0 text-xs text-[var(--color-ink-muted)]">{s.label}</span>
            <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-[var(--color-canvas-soft)]">
              <div
                className="h-full rounded-full bg-[var(--color-grape)]"
                style={{ width: `${Math.round(s.weight * 100)}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </SurfaceCard>
  );
}
