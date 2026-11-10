import { betterAuth } from "better-auth";
import { Pool } from "pg";
import { authOptions } from "./auth-options";

/**
 * Server-side Better Auth instance. Uses the same Postgres database as
 * website/backend (Neon in production), with Better Auth's own tables scoped
 * to the `auth` schema so they never collide with the domain tables in
 * `public` that website/backend owns.
 */
export const auth = betterAuth({
  ...authOptions,
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
    // Sends unqualified table names to the `auth` schema first, so
    // Better Auth's "user"/"session"/"account"/"verification" tables
    // resolve there.
    options: "-c search_path=auth,public",
  }),
});
