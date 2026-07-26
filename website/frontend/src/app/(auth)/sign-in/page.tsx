"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { GlassCard } from "@/components/shared/glass-card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { signInSchema, type SignInInput } from "@/schemas/auth";
import { authClient } from "@/lib/auth-client";
import { useState } from "react";

export default function SignInPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignInInput>({ resolver: zodResolver(signInSchema) });

  const onSubmit = async (data: SignInInput) => {
    setError(null);
    const { error: authError } = await authClient.signIn.email(data);
    if (authError) {
      setError(authError.message ?? "Couldn't sign you in. Check your details and try again.");
      return;
    }
    router.push("/dashboard");
  };

  return (
    <GlassCard strong>
      <h1 className="mb-1 font-[var(--font-display)] text-2xl font-medium">Welcome back</h1>
      <p className="mb-6 text-sm text-[var(--color-mist-500)]">VibeAI remembers where you left off.</p>
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
        <div>
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="you@example.com" {...register("email")} />
          {errors.email && <p className="mt-1 text-xs text-[var(--color-aurora-magenta)]">{errors.email.message}</p>}
        </div>
        <div>
          <Label htmlFor="password">Password</Label>
          <Input id="password" type="password" placeholder="••••••••" {...register("password")} />
          {errors.password && (
            <p className="mt-1 text-xs text-[var(--color-aurora-magenta)]">{errors.password.message}</p>
          )}
        </div>
        {error && <p className="text-xs text-[var(--color-aurora-magenta)]">{error}</p>}
        <Button type="submit" disabled={isSubmitting} className="mt-2 w-full">
          {isSubmitting ? "Signing in…" : "Sign in"}
        </Button>
      </form>
      <p className="mt-6 text-center text-sm text-[var(--color-mist-500)]">
        New here? <Link href="/sign-up" className="text-[var(--color-aurora-cyan)]">Create an account</Link>
      </p>
    </GlassCard>
  );
}
