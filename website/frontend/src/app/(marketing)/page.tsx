import Link from "next/link";
import { Brain, Radio, Sparkles, Fingerprint, Compass, LineChart } from "lucide-react";
import { AuroraBackground } from "@/components/shared/aurora-background";
import { VibeOrb } from "@/components/magic/vibe-orb";
import { GlassCard } from "@/components/shared/glass-card";
import { Marquee } from "@/components/magic/marquee";
import { AnimatedCounter } from "@/components/magic/animated-counter";
import { Button } from "@/components/ui/button";

const AGENTS = [
  { icon: Brain, name: "Conversation Agent", desc: "Talks with you like a companion, not a chatbot." },
  { icon: Sparkles, name: "Mood Agent", desc: "Reads emotional texture from what you say and how you listen." },
  { icon: Fingerprint, name: "Taste Profiling Agent", desc: "Builds a living model of your musical identity." },
  { icon: Radio, name: "Sequencing Agent", desc: "Arranges tracks into an emotional arc, not a shuffle." },
  { icon: Compass, name: "Discovery Agent", desc: "Surfaces artists the algorithm usually buries." },
  { icon: LineChart, name: "Analytics Agent", desc: "Shows you the emotional shape of your year." },
];

const MOODS = [
  "3am and wired", "post-breakup numb", "sunday morning slow",
  "pre-interview nerves", "nostalgic for a place", "finally exhaling",
  "angry and need to move", "quietly content",
];

export default function HomePage() {
  return (
    <main className="relative overflow-hidden">
      {/* Hero */}
      <section className="relative flex min-h-[92dvh] flex-col items-center justify-center px-6 text-center">
        <AuroraBackground />
        <div className="relative z-10 flex flex-col items-center">
          <VibeOrb size={96} energy={0.5} className="mb-8" />
          <p className="mb-4 font-[var(--font-mono)] text-xs uppercase tracking-[0.3em] text-[var(--color-mist-500)]">
            Not a playlist app
          </p>
          <h1 className="max-w-3xl font-[var(--font-display)] text-5xl font-medium leading-[1.05] tracking-tight text-[var(--color-mist-100)] sm:text-6xl">
            The AI that understands <span className="text-gradient-aurora">your vibe.</span>
          </h1>
          <p className="mt-6 max-w-xl text-base leading-relaxed text-[var(--color-mist-300)]">
            VibeAI is an emotionally intelligent music companion — part personal DJ, part music
            therapist, part memory. Tell it how you feel. It listens, understands, and
            orchestrates the exact experience you need, one honest conversation at a time.
          </p>
          <div className="mt-10 flex items-center gap-4">
            <Link href="/sign-up">
              <Button size="lg">Start a conversation</Button>
            </Link>
            <Link href="/how-it-works">
              <Button size="lg" variant="secondary">See how it thinks</Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Mood marquee — sets tone: this understands specific, real emotional states */}
      <section className="border-y border-white/5 py-6">
        <Marquee items={MOODS} />
      </section>

      {/* Agent constellation */}
      <section className="mx-auto max-w-6xl px-6 py-28">
        <div className="mb-14 text-center">
          <p className="mb-3 font-[var(--font-mono)] text-xs uppercase tracking-[0.3em] text-[var(--color-aurora-cyan)]">
            Under the hood
          </p>
          <h2 className="font-[var(--font-display)] text-3xl font-medium text-[var(--color-mist-100)]">
            Eleven agents. One companion.
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-sm text-[var(--color-mist-500)]">
            Every recommendation you get has been through a real reasoning process —
            not a similarity score. You can always ask VibeAI why.
          </p>
        </div>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {AGENTS.map(({ icon: Icon, name, desc }) => (
            <GlassCard key={name} className="transition-transform hover:-translate-y-1">
              <Icon size={22} className="mb-4 text-[var(--color-aurora-cyan)]" />
              <h3 className="mb-1.5 font-[var(--font-display)] text-base font-medium">{name}</h3>
              <p className="text-sm text-[var(--color-mist-500)]">{desc}</p>
            </GlassCard>
          ))}
        </div>
      </section>

      {/* Proof strip */}
      <section className="mx-auto max-w-4xl px-6 pb-28">
        <GlassCard strong className="grid grid-cols-1 gap-8 py-10 text-center sm:grid-cols-3">
          <div>
            <p className="font-[var(--font-display)] text-3xl text-gradient-aurora">
              <AnimatedCounter value={27} />
            </p>
            <p className="mt-1 text-xs text-[var(--color-mist-500)]">Emotion classes read per check-in</p>
          </div>
          <div>
            <p className="font-[var(--font-display)] text-3xl text-gradient-aurora">
              <AnimatedCounter value={11} />
            </p>
            <p className="mt-1 text-xs text-[var(--color-mist-500)]">Specialized agents working per request</p>
          </div>
          <div>
            <p className="font-[var(--font-display)] text-3xl text-gradient-aurora">
              <AnimatedCounter value={0} suffix="%" />
            </p>
            <p className="mt-1 text-xs text-[var(--color-mist-500)]">Chance it just shuffles your library</p>
          </div>
        </GlassCard>
      </section>
    </main>
  );
}
