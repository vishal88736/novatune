import { NextRequest } from "next/server";

/**
 * Proxies the browser's SSE connection to website/backend's streaming chat
 * endpoint, which in turn streams from ai-engine's orchestrator. Kept as a
 * thin passthrough so the browser never talks to internal services directly.
 */
export async function POST(req: NextRequest) {
  const { sessionId, message } = await req.json();
  const backendUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

  const upstream = await fetch(`${backendUrl}/api/v1/chat/message`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      cookie: req.headers.get("cookie") ?? "",
    },
    body: JSON.stringify({ session_id: sessionId, message }),
  });

  return new Response(upstream.body, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
