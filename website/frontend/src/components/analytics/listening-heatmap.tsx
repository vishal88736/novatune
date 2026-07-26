import { cn } from "@/lib/utils";

export function ListeningHeatmap({ data }: { data: number[][] }) {
  return (
    <div className="grid grid-cols-24 gap-1">
      {data.flat().map((v, i) => (
        <div
          key={i}
          className={cn("aspect-square rounded-sm")}
          style={{ background: `color-mix(in oklab, var(--color-aurora-cyan) ${Math.round(v * 100)}%, var(--color-void-800))` }}
        />
      ))}
    </div>
  );
}
