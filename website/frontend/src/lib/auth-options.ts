import type { BetterAuthOptions } from "better-auth";

/**
 * Cookie prefix Better Auth uses. Kept as a constant so the route guard
 * (src/middleware.ts) can look for the session cookie without pulling
 * Better Auth's runtime into the Edge bundle.
 */
export const AUTH_COOKIE_PREFIX = "better-auth";

export const SESSION_COOKIE_NAME = `${AUTH_COOKIE_PREFIX}.session_token`;

/**
 * Better Auth configuration, kept separate from the database wiring so it
 * can be shared with the schema generator (scripts/generate-auth-schema.mts)
 * without pulling in `pg`.
 */
export const authOptions = {
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL,
  emailAndPassword: { enabled: true },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID ?? "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? "",
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID ?? "",
      clientSecret: process.env.GITHUB_CLIENT_SECRET ?? "",
    },
  },
  session: {
    cookieCache: { enabled: true, maxAge: 5 * 60 },
  },
  advanced: {
    cookiePrefix: AUTH_COOKIE_PREFIX,
    /**
     * The domain tables key on UUIDs (see website/backend/app/db/models/user.py),
     * and website/backend parses the session's user id straight into a UUID.
     * Better Auth's default id generator returns an opaque string, so it is
     * overridden here to keep both sides in agreement.
     */
    generateId: () => crypto.randomUUID(),
  },
} satisfies BetterAuthOptions;
