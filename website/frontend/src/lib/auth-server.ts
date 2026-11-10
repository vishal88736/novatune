import { betterAuth } from "better-auth";
import { Pool } from "pg";

/**
 * Server-side Better Auth instance. Uses the same Postgres database as
 * website/backend (Neon in production), with tables scoped to the `auth`
 * schema to avoid collision with domain tables owned by the FastAPI app.
 */
export const auth = betterAuth({
  database: new Pool({ connectionString: process.env.DATABASE_URL }),
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
    /**
     * The domain tables key on UUIDs (see website/backend/app/db/models/user.py),
     * and website/backend parses the session's user id straight into a UUID.
     * Better Auth's default id generator returns an opaque string, so it is
     * overridden here to keep both sides in agreement.
     */
    generateId: () => crypto.randomUUID(),
  },
});
