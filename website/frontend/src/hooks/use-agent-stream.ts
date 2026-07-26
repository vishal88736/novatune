"use client";

import { useCallback, useRef } from "react";
import { useChatStore } from "@/stores/chat-store";

/**
 * Opens an SSE connection to /api/stream (which proxies to
 * website/backend -> ai-engine orchestrator streaming channel) and pipes
 * tokens + agent-status events into the chat store as they arrive.
 */
export function useAgentStream() {
  const controllerRef = useRef<AbortController | null>(null);
  const { appendMessage, updateStreamingMessage, finalizeMessage, setThinking } = useChatStore();

  const send = useCallback(
    async (sessionId: string, message: string) => {
      controllerRef.current?.abort();
      const controller = new AbortController();
      controllerRef.current = controller;

      const assistantId = crypto.randomUUID();
      appendMessage({
        id: assistantId,
        role: "assistant",
        content: "",
        isStreaming: true,
        createdAt: new Date().toISOString(),
      });
      setThinking(true, "conversation_agent");

      const res = await fetch("/api/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId, message }),
        signal: controller.signal,
      });

      if (!res.body) {
        setThinking(false);
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      // eslint-disable-next-line no-constant-condition
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        for (const line of chunk.split("\n\n")) {
          if (!line.startsWith("data:")) continue;
          const payload = line.replace(/^data:\s*/, "");
          try {
            const event = JSON.parse(payload) as
              | { type: "token"; content: string }
              | { type: "agent"; name: string }
              | { type: "done" };

            if (event.type === "agent") setThinking(true, event.name);
            if (event.type === "token") updateStreamingMessage(assistantId, event.content);
            if (event.type === "done") {
              finalizeMessage(assistantId);
              setThinking(false);
            }
          } catch {
            // ignore malformed keepalive frames
          }
        }
      }
    },
    [appendMessage, updateStreamingMessage, finalizeMessage, setThinking],
  );

  return { send };
}
