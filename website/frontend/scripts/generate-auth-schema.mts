/**
 * Generates the SQL for Better Auth's own tables (user, session, account,
 * verification).
 *
 * Better Auth owns these tables; website/backend owns the domain tables.
 * The generated SQL is checked into website/backend/alembic/versions so the
 * whole schema is created by `alembic upgrade head` like everything else.
 *
 * Run from website/frontend:
 *   node --experimental-strip-types scripts/generate-auth-schema.mts
 */
import { createRequire } from "node:module";
import { getMigrations } from "better-auth/db";
import { PostgresDialect } from "kysely";

// Next.js loads .env.local for the app, but this script runs under plain
// Node, so the environment has to be loaded explicitly — and before the
// auth options are imported, since they read it at module scope.
try {
  process.loadEnvFile(".env.local");
} catch {
  // no .env.local — rely on the ambient environment
}

const { authOptions } = await import("../src/lib/auth-options.ts");

// pg ships CommonJS, so it cannot be named-imported from an ES module.
const require = createRequire(import.meta.url);
const { Pool } = require("pg");

const database = {
  // Better Auth reads the dialect type from `database.type` when a dialect
  // is supplied — without it the schema is generated with SQLite types.
  type: "postgres" as const,
  dialect: new PostgresDialect({
    pool: new Pool({ connectionString: process.env.DATABASE_URL }),
  }),
};

const migrations = await getMigrations({ ...authOptions, database });
const sql = await migrations.compileMigrations();

process.stdout.write(sql);
