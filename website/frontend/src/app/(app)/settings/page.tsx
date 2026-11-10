"use client";

import { SurfaceCard } from "@/components/shared/surface-card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useSession, signOut } from "@/lib/auth-client";

export default function SettingsPage() {
  const { data: session } = useSession();

  return (
    <div className="mx-auto flex max-w-xl flex-col gap-6">
      <h1 className="font-[var(--font-display)] text-3xl font-bold">Settings</h1>

      <SurfaceCard strong>
        <h3 className="mb-4 font-[var(--font-display)] text-base font-bold">Profile</h3>
        <div className="flex flex-col gap-4">
          <div>
            <Label htmlFor="name">Name</Label>
            <Input id="name" defaultValue={session?.user?.name ?? ""} />
          </div>
          <div>
            <Label htmlFor="email">Email</Label>
            <Input id="email" defaultValue={session?.user?.email ?? ""} disabled />
          </div>
        </div>
      </SurfaceCard>

      <SurfaceCard>
        <h3 className="mb-2 font-[var(--font-display)] text-base font-bold">Session</h3>
        <p className="mb-4 text-sm text-[var(--color-ink-muted)]">Sign out of VibeAI on this device.</p>
        <Button variant="outline" onClick={() => signOut()}>Sign out</Button>
      </SurfaceCard>
    </div>
  );
}
