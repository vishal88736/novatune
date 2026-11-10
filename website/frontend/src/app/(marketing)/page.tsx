import Link from "next/link";
import {
  Brain, Radio, Sparkles, Fingerprint, Compass, LineChart, Mail, Play, Zap, Disc3,
} from "lucide-react";
import { AuroraBackground } from "@/components/shared/aurora-background";
import { VibeDisc, DiscChip } from "@/components/magic/vibe-disc";
import { Doodle, DoodleRing } from "@/components/magic/doodle";
import { PlayerPreview } from "@/components/magic/player-preview";
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
      {/* Hero — a single cream canvas card with the reference's two-column split */}
      <section className="px-4 py-6 sm:px-6">
        <div className="relative mx-auto max-w-6xl overflow-hidden rounded-[2.5rem] border border-[var(--color-line)] bg-[var(--color-surface)] shadow-[var(--shadow-lift)]">
          <AuroraBackground className="opacity-70" />

          <div className="relative grid grid-cols-1 items-center gap-12 px-8 py-16 sm:px-12 lg:grid-cols-[1.05fr_0.95fr] lg:py-20">
            {/* Left column */}
            <div className="relative">
              <Doodle
                variant="sweep"
                end="heart"
                className="pointer-events-none absolute -top-28 right-0 hidden h-36 w-80 text-[var(--color-grape)] lg:block"
              />

              <p className="eyebrow mb-6">Stay in tune</p>

              <h1 className="relative font-[var(--font-display)] text-[3.25rem] font-extrabold leading-[0.95] tracking-[-0.03em] text-[var(--color-ink)] sm:text-6xl lg:text-7xl">
                Keep the{" "}
                <span className="relative inline-block text-[var(--color-grape)]">
                  <DoodleRing className="pointer-events-none absolute -inset-x-6 -inset-y-3 h-[calc(100%+1.5rem)] w-[calc(100%+3rem)] text-[var(--color-sun)]" />
                  spirit
                </span>{" "}
                up
              </h1>

              <p className="mt-7 max-w-md text-lg text-[var(--color-ink-soft)]">
                Find the tracks that match how you actually feel — not just what you last played.
              </p>

              {/* Email-style capture pill, as in the reference */}
              <form className="mt-9 flex w-full max-w-lg items-center gap-3 rounded-full border border-[var(--color-line)] bg-[var(--color-surface)] p-2 pl-3 shadow-[var(--shadow-soft)]">
                <span className="chip h-11 w-11 shrink-0">
                  <Mail size={18} />
                </span>
                <div className="min-w-0 flex-1 px-1">
                  <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-[var(--color-ink-muted)]">
                    Your mail address
                  </p>
                  <p className="truncate text-sm font-medium text-[var(--color-ink)]">
                    hello@vibeai.fm
                  </p>
                </div>
                <Button type="submit" size="md" className="shrink-0">
                  Get started
                </Button>
              </form>

              <div className="mt-6">
                <Link href="/sign-in">
                  <Button variant="ghost" size="sm" className="px-2">
                    Already using VibeAI? Sign in
                  </Button>
                </Link>
              </div>

              {/* Lower-left feature block, as in the reference */}
              <div className="relative mt-14 flex items-center gap-5">
                <div className="grid h-24 w-24 shrink-0 place-items-center rounded-full bg-[var(--color-grape-wash)] shadow-[var(--shadow-soft)]">
                  <div className="grid h-16 w-16 place-items-center rounded-full bg-[var(--color-grape)] text-white">
                    <Disc3 size={28} strokeWidth={1.75} />
                  </div>
                </div>
                <div>
                  <p className="eyebrow mb-1.5">Featured</p>
                  <p className="font-[var(--font-display)] text-2xl font-extrabold leading-tight tracking-tight text-[var(--color-ink)]">
                    New releases
                    <br />
                    for you
                  </p>
                  <p className="mt-1 text-sm text-[var(--color-ink-muted)]">Top-rated albums</p>
                </div>
                <Button size="icon" className="hidden h-14 w-14 rounded-2xl lg:inline-flex">
                  <Play size={20} fill="currentColor" className="ml-0.5" />
                </Button>
                <Doodle
                  variant="hook"
                  end="arrow"
                  className="pointer-events-none absolute -top-16 left-6 hidden h-20 w-48 text-[var(--color-grape)] lg:block"
                />
              </div>
            </div>

            {/* Right column — the gradient disc */}
            <div className="relative mx-auto w-full max-w-[440px] lg:mx-0">
              <VibeDisc className="w-full">
                <DiscChip className="left-[1%] top-[14%] h-16 w-16">
                  <Sparkles size={24} />
                </DiscChip>
                <DiscChip className="right-[1%] top-[36%] h-14 w-14">
                  <Radio size={22} />
                </DiscChip>
              </VibeDisc>

              {/* Lightning accents over the disc */}
              <Zap className="absolute left-[18%] top-[-3%] h-14 w-14 rotate-[18deg] fill-[var(--color-sun)] text-[var(--color-sun-deep)]" />
              <Zap className="absolute bottom-[16%] right-[0%] h-11 w-11 rotate-[12deg] fill-[var(--color-sun)] text-[var(--color-sun-deep)]" />

              <PlayerPreview className="absolute -bottom-12 left-0 z-10 w-[calc(100%-1.5rem)] max-w-[24rem] lg:-bottom-14 lg:left-[-4rem]" />
            </div>
          </div>
        </div>
      </section>

      {/* Mood marquee — sets tone: this understands specific, real emotional states */}
      <section className="border-y border-[var(--color-line)] bg-[var(--color-canvas-soft)] py-6">
        <Marquee items={MOODS} />
      </section>

      {/* Agent constellation */}
      <section id="agents" className="mx-auto max-w-6xl scroll-mt-24 px-6 py-24">
        <div className="mb-14 text-center">
          <p className="eyebrow mb-3">Under the hood</p>
          <h2 className="font-[var(--font-display)] text-4xl font-extrabold tracking-[-0.02em] text-[var(--color-ink)] sm:text-5xl">
            Eleven agents. One companion.
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-sm text-[var(--color-ink-muted)]">
            Every recommendation you get has been through a real reasoning process —
            not a similarity score. You can always ask VibeAI why.
          </p>
        </div>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {AGENTS.map(({ icon: Icon, name, desc }) => (
            <div
              key={name}
              className="surface p-6 transition-transform hover:-translate-y-1 hover:shadow-[var(--shadow-lift)]"
            >
              <span className="chip mb-4 h-11 w-11">
                <Icon size={20} />
              </span>
              <h3 className="mb-1.5 font-[var(--font-display)] text-base font-bold text-[var(--color-ink)]">
                {name}
              </h3>
              <p className="text-sm text-[var(--color-ink-muted)]">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Proof strip */}
      <section id="proof" className="mx-auto max-w-4xl scroll-mt-24 px-6 pb-24">
        <div className="surface-strong grid grid-cols-1 gap-8 py-12 text-center sm:grid-cols-3">
          <div>
            <p className="font-[var(--font-display)] text-4xl font-extrabold text-gradient-brand">
              <AnimatedCounter value={27} />
            </p>
            <p className="mt-1.5 text-xs text-[var(--color-ink-muted)]">
              Emotion classes read per check-in
            </p>
          </div>
          <div>
            <p className="font-[var(--font-display)] text-4xl font-extrabold text-gradient-brand">
              <AnimatedCounter value={11} />
            </p>
            <p className="mt-1.5 text-xs text-[var(--color-ink-muted)]">
              Specialized agents working per request
            </p>
          </div>
          <div>
            <p className="font-[var(--font-display)] text-4xl font-extrabold text-gradient-brand">
              <AnimatedCounter value={0} suffix="%" />
            </p>
            <p className="mt-1.5 text-xs text-[var(--color-ink-muted)]">
              Chance it just shuffles your library
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
