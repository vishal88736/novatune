import { AuroraBackground } from "@/components/shared/aurora-background";
import { Logo } from "@/components/shared/logo";
import Link from "next/link";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative flex min-h-dvh items-center justify-center overflow-hidden px-6">
      <AuroraBackground className="opacity-45" />
      {/* Keeps the middle of the page quiet so the card stays the focus */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_center,var(--color-canvas)_0%,transparent_62%)]" />
      <div className="relative z-10 w-full max-w-sm">
        <Link href="/" className="mb-8 flex justify-center">
          <Logo />
        </Link>
        {children}
      </div>
    </div>
  );
}
