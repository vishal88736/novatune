import { cn } from "@/lib/utils";
import type { ChatMessage } from "@/stores/chat-store";
import { VibeOrb } from "@/components/magic/vibe-orb";

export function ChatBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div className={cn("flex items-end gap-3", isUser && "flex-row-reverse")}>
      {!isUser && <VibeOrb size={28} energy={0.3} />}
      <div
        className={cn(
          "max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed",
          isUser
            ? "bg-[var(--color-grape)] text-white shadow-[var(--shadow-grape)]"
            : "surface text-[var(--color-ink)]",
        )}
      >
        {message.content || (message.isStreaming ? "…" : "")}
      </div>
    </div>
  );
}
