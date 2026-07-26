"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { GlassCard } from "@/components/shared/glass-card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { signUpSchema, type SignUpInput } from "@/schemas/auth";
import { authClient } from "@/lib/auth-client";

export default function SignUpPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignUpInput>({ resolver: zodResolver(signUpSchema) });

  const onSubmit = async (data: SignUpInput) => {
    setError(null);
    const { error: authError } = await authClient.signUp.email({
      name: data.name,
      email: data.email,
      password: data.password,
    });
    if (authError) {
      setError(authError.message ?? "Couldn't create your account. Try again.");
      return;
    }
    router.push("/dashboard");
  };

  return (
    <GlassCard strong>
      <h1 className="mb-1 font-[var(--font-display)] text-2xl font-medium">Meet your companion</h1>
      <p className="mb-6 text-sm text-[var(--color-mist-500)]">Takes 30 seconds. No playlists required.</p>
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
        <div>
          <Label htmlFor="name">Name</Label>
          <Input id="name" placeholder="Your name" {...register("name")} />
          {errors.name && <p className="mt-1 text-xs text-[var(--color-aurora-magenta)]">{errors.name.message}</p>}
        </div>
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
        <div>
          <Label htmlFor="confirmPassword">Confirm password</Label>
          <Input id="confirmPassword" type="password" placeholder="••••••••" {...register("confirmPassword")} />
          {errors.confirmPassword && (
            <p className="mt-1 text-xs text-[var(--color-aurora-magenta)]">{errors.confirmPassword.message}</p>
          )}
        </div>
        {error && <p className="text-xs text-[var(--color-aurora-magenta)]">{error}</p>}
        <Button type="submit" disabled={isSubmitting} className="mt-2 w-full">
          {isSubmitting ? "Creating account…" : "Create account"}
        </Button>
      </form>
      <p className="mt-6 text-center text-sm text-[var(--color-mist-500)]">
        Already have an account? <Link href="/sign-in" className="text-[var(--color-aurora-cyan)]">Sign in</Link>
      </p>
    </GlassCard>
  );
}
