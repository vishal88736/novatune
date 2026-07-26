import { toNextJsHandler } from "better-auth/next-js";
import { auth } from "@/lib/auth-server";

/**
 * Better Auth's catch-all route handler. Owns sign-up, sign-in, OAuth
 * callbacks, session issuance/verification, and sign-out. website/backend
 * verifies the resulting session cookie on every API request (see
 * website/backend/app/core/security.py).
 */
export const { GET, POST } = toNextJsHandler(auth);
