"use client";

import { useEffect, useRef } from "react";
import { useChatStore } from "@/stores/chat-store";
import { useAgentStream } from "@/hooks/use-agent-stream";
import { ChatBubble } from "@/components/chat/chat-bubble";
import { ChatInput } from "@/components/chat/chat-input";
import { AgentThinkingIndicator } from "@/components/chat/agent-thinking-indicator";
import { VibeOrb } from "@/components/magic/vibe-orb";

export default function ChatPage() {
  const { sessionId, setSessionId, messages, appendMessage, isThinking, activeAgent } = useChatStore();
  const { send } = useAgentStream();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!sessionId) setSessionId(crypto.randomUUID());
  }, [sessionId, setSessionId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  const handleSend = (text: string) => {
    appendMessage({
      id: crypto.randomUUID(),
      role: "user",
      content: text,
      createdAt: new Date().toISOString(),
    });
    if (sessionId) send(sessionId, text);
  };

  return (
    <div className="flex h-[calc(100dvh-8rem)] flex-col">
      <div className="mb-6 flex items-center gap-3">
        <VibeOrb size={32} energy={0.4} />
        <div>
          <h1 className="font-[var(--font-display)] text-xl font-medium">Conversation</h1>
          <p className="text-xs text-[var(--color-mist-500)]">Talk to VibeAI like you would a friend who gets music.</p>
        </div>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto pr-2">
        {messages.length === 0 && (
          <p className="mt-10 text-center text-sm text-[var(--color-mist-500)]">
            Try: "I can't stop thinking about someone I used to love" or "I need energy for a workout."
          </p>
        )}
        {messages.map((m) => (
          <ChatBubble key={m.id} message={m} />
        ))}
        {isThinking && <AgentThinkingIndicator agent={activeAgent} />}
        <div ref={bottomRef} />
      </div>

      <div className="mt-4">
        <ChatInput onSubmit={handleSend} />
      </div>
    </div>
  );
}
