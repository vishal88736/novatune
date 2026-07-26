import Link from "next/link";
import { Logo } from "@/components/shared/logo";
import { Button } from "@/components/ui/button";

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative min-h-dvh">
      <header className="sticky top-0 z-50 border-b border-white/5 bg-[var(--color-void-950)]/70 backdrop-blur-xl">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link href="/">
            <Logo />
          </Link>
          <nav className="hidden items-center gap-8 text-sm text-[var(--color-mist-300)] md:flex">
            <Link href="/how-it-works" className="hover:text-white">How it works</Link>
          </nav>
          <div className="flex items-center gap-3">
            <Link href="/sign-in">
              <Button variant="ghost" size="sm">Sign in</Button>
            </Link>
            <Link href="/sign-up">
              <Button size="sm">Get started</Button>
            </Link>
          </div>
        </div>
      </header>
      {children}
      <footer className="border-t border-white/5 px-6 py-10 text-center text-xs text-[var(--color-mist-500)]">
        VibeAI — an AI companion, not a playlist app.
      </footer>
    </div>
  );
}
