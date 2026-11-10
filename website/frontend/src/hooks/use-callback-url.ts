"use client";

import { useSearchParams } from "next/navigation";

/**
 * Where to send the user after a successful sign-in or sign-up.
 *
 * The route guard in src/middleware.ts puts the originally requested page
 * in `callbackURL` so a deep link survives the detour through sign-in.
 * Only same-origin relative paths are honoured — an absolute URL here
 * would turn the login form into an open redirect.
 */
export function useCallbackUrl(fallback = "/dashboard"): string {
  const searchParams = useSearchParams();
  const callback = searchParams.get("callbackURL");

  if (!callback) return fallback;
  if (!callback.startsWith("/") || callback.startsWith("//")) return fallback;

  return callback;
}
