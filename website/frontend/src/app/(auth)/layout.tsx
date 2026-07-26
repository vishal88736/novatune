import { AuroraBackground } from "@/components/shared/aurora-background";
import { Logo } from "@/components/shared/logo";
import Link from "next/link";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative flex min-h-dvh items-center justify-center px-6">
      <AuroraBackground />
      <div className="relative z-10 w-full max-w-sm">
        <Link href="/" className="mb-8 flex justify-center">
          <Logo />
        </Link>
        {children}
      </div>
    </div>
  );
}
