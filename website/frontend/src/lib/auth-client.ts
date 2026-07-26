import { createAuthClient } from "better-auth/react";

/**
 * Better Auth client — talks to the Next.js route handler at
 * /api/auth/[...all], which in turn issues/verifies the session cookie
 * that website/backend validates on every API request.
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000",
});

export const { signIn, signUp, signOut, useSession } = authClient;
