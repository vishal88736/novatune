"use client";

import { GlassCard } from "@/components/shared/glass-card";
import { MoodTimeline } from "@/components/analytics/mood-timeline";

const SAMPLE_TIMELINE = [
  { date: "Mon", valence: 0.2 }, { date: "Tue", valence: -0.3 }, { date: "Wed", valence: -0.1 },
  { date: "Thu", valence: 0.4 }, { date: "Fri", valence: 0.6 }, { date: "Sat", valence: 0.5 }, { date: "Sun", valence: 0.1 },
];

const MILESTONES = [
  { date: "Wed", label: "Rough week acknowledged", detail: "You told VibeAI you were overwhelmed — it slowed the tempo down for three days." },
  { date: "Fri", label: "Turning point", detail: "First high-energy request in 9 days. VibeAI leaned into it." },
];

export default function JourneyPage() {
  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="font-[var(--font-display)] text-3xl font-medium">Emotional Journey</h1>
        <p className="mt-1 text-sm text-[var(--color-mist-500)]">
          The Memory Agent's long-term view of how you've been feeling.
        </p>
      </div>

      <GlassCard strong>
        <MoodTimeline data={SAMPLE_TIMELINE} />
      </GlassCard>

      <div className="flex flex-col gap-3">
        {MILESTONES.map((m) => (
          <GlassCard key={m.label} className="flex gap-4">
            <span className="font-[var(--font-mono)] text-xs text-[var(--color-aurora-cyan)]">{m.date}</span>
            <div>
              <p className="text-sm font-medium">{m.label}</p>
              <p className="text-xs text-[var(--color-mist-500)]">{m.detail}</p>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
