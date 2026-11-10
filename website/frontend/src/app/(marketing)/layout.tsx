import Link from "next/link";
import { Logo } from "@/components/shared/logo";
import { Button } from "@/components/ui/button";

const NAV = [
  { href: "/#agents", label: "Agents" },
  { href: "/how-it-works", label: "How it works" },
  { href: "/#proof", label: "Proof" },
];

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative min-h-dvh bg-[var(--color-canvas)]">
      <header className="sticky top-0 z-50 border-b border-[var(--color-line)] bg-[var(--color-canvas)]/85 backdrop-blur-xl">
        <div className="mx-auto grid max-w-6xl grid-cols-[1fr_auto_1fr] items-center gap-6 px-6 py-4">
          <Link href="/" className="justify-self-start">
            <Logo />
          </Link>

          <nav className="hidden items-center gap-9 md:flex">
            {NAV.map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                className="text-[11px] font-semibold uppercase tracking-[0.2em] text-[var(--color-ink)] transition-colors hover:text-[var(--color-grape)]"
              >
                {label}
              </Link>
            ))}
          </nav>

          <div className="flex items-center justify-self-end gap-4">
            <Link
              href="/sign-in"
              className="text-[11px] font-semibold uppercase tracking-[0.2em] text-[var(--color-ink)] transition-colors hover:text-[var(--color-grape)]"
            >
              Login
            </Link>
            <Link href="/sign-up">
              <Button size="sm" className="uppercase tracking-[0.12em]">
                Join now
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {children}

      <footer className="border-t border-[var(--color-line)] bg-[var(--color-canvas-soft)] px-6 py-10 text-center text-xs text-[var(--color-ink-muted)]">
        VibeAI — an AI companion, not a playlist app.
      </footer>
    </div>
  );
}
