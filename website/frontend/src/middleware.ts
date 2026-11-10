import { NextResponse, type NextRequest } from "next/server";
import { SESSION_COOKIE_NAME } from "@/lib/auth-options";

/**
 * Guards the authenticated shell.
 *
 * The check is deliberately cheap — it only looks for the presence of the
 * session cookie. The cookie is signed, so a request that gets past here
 * is still verified properly by website/backend, which calls Better Auth's
 * session-verification endpoint on every request. This middleware exists
 * so an unauthenticated visitor is sent to the sign-in screen instead of
 * landing on an app shell that cannot load any of its data.
 */
export function middleware(request: NextRequest) {
  if (request.cookies.get(SESSION_COOKIE_NAME)) {
    return NextResponse.next();
  }

  const url = new URL("/sign-in", request.url);
  if (request.nextUrl.pathname !== "/sign-in") {
    url.searchParams.set("callbackURL", `${request.nextUrl.pathname}${request.nextUrl.search}`);
  }
  return NextResponse.redirect(url);
}

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/chat/:path*",
    "/discover/:path*",
    "/library/:path*",
    "/journey/:path*",
    "/analytics/:path*",
    "/settings/:path*",
  ],
};
