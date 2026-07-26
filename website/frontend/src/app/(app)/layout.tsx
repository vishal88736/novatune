import Link from "next/link";
import {
  LayoutDashboard, MessageCircle, Compass, Library, LineChart, Settings, Waypoints,
} from "lucide-react";
import { Logo } from "@/components/shared/logo";
import { PlayerDock } from "@/components/player/player-dock";
import { PageTransition } from "@/components/shared/page-transition";

const NAV = [
  { href: "/dashboard", label: "Today's Vibe", icon: LayoutDashboard },
  { href: "/chat", label: "Conversation", icon: MessageCircle },
  { href: "/discover", label: "Discover", icon: Compass },
  { href: "/library", label: "Library", icon: Library },
  { href: "/journey", label: "Journey", icon: Waypoints },
  { href: "/analytics", label: "Analytics", icon: LineChart },
  { href: "/settings", label: "Settings", icon: Settings },
];

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-dvh bg-[var(--color-void-950)]">
      <aside className="sticky top-0 hidden h-dvh w-60 shrink-0 flex-col border-r border-white/5 p-5 md:flex">
        <Link href="/dashboard" className="mb-8 px-2">
          <Logo />
        </Link>
        <nav className="flex flex-1 flex-col gap-1">
          {NAV.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-[var(--color-mist-300)] transition-colors hover:bg-white/5 hover:text-white"
            >
              <Icon size={17} />
              {label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="min-w-0 flex-1 pb-28">
        <PageTransition>
          <div className="mx-auto max-w-6xl px-6 py-10">{children}</div>
        </PageTransition>
      </main>
      <PlayerDock />
    </div>
  );
}
