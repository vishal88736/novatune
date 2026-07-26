import { GlassCard } from "@/components/shared/glass-card";

const STEPS = [
  { title: "You share a vibe", body: "Type, talk, or tap the mood wheel. No forced categories — say it how you'd say it to a friend." },
  { title: "The Mood Agent listens", body: "A GoEmotions-based model reads 27 emotional dimensions, not just 'happy or sad'." },
  { title: "Your taste meets the moment", body: "The Taste Profiling Agent blends your long-term identity with what you need right now." },
  { title: "An arc gets built", body: "The Sequencing Agent doesn't shuffle — it composes a journey with a beginning, a peak, and a landing." },
  { title: "You get the why", body: "The Explainability Agent tells you, in plain language, why each track is here." },
];

export default function HowItWorksPage() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-24">
      <h1 className="mb-4 font-[var(--font-display)] text-4xl font-medium">How VibeAI thinks</h1>
      <p className="mb-14 text-[var(--color-mist-400)]">
        Five steps happen behind every recommendation. None of them are a similarity score.
      </p>
      <ol className="flex flex-col gap-4">
        {STEPS.map((step, i) => (
          <GlassCard key={step.title} className="flex gap-5">
            <span className="font-[var(--font-mono)] text-sm text-[var(--color-aurora-cyan)]">
              {String(i + 1).padStart(2, "0")}
            </span>
            <div>
              <h3 className="mb-1 font-[var(--font-display)] text-base font-medium">{step.title}</h3>
              <p className="text-sm text-[var(--color-mist-500)]">{step.body}</p>
            </div>
          </GlassCard>
        ))}
      </ol>
    </main>
  );
}
