import { create } from "zustand";

export type ChatRole = "user" | "assistant" | "agent-status";

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  agentName?: string;
  isStreaming?: boolean;
  createdAt: string;
}

interface ChatState {
  sessionId: string | null;
  messages: ChatMessage[];
  isThinking: boolean;
  activeAgent: string | null;
  setSessionId: (id: string) => void;
  appendMessage: (message: ChatMessage) => void;
  updateStreamingMessage: (id: string, chunk: string) => void;
  finalizeMessage: (id: string) => void;
  setThinking: (thinking: boolean, agent?: string | null) => void;
  reset: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  sessionId: null,
  messages: [],
  isThinking: false,
  activeAgent: null,
  setSessionId: (sessionId) => set({ sessionId }),
  appendMessage: (message) => set((s) => ({ messages: [...s.messages, message] })),
  updateStreamingMessage: (id, chunk) =>
    set((s) => ({
      messages: s.messages.map((m) => (m.id === id ? { ...m, content: m.content + chunk } : m)),
    })),
  finalizeMessage: (id) =>
    set((s) => ({
      messages: s.messages.map((m) => (m.id === id ? { ...m, isStreaming: false } : m)),
    })),
  setThinking: (isThinking, agent = null) => set({ isThinking, activeAgent: agent }),
  reset: () => set({ sessionId: null, messages: [], isThinking: false, activeAgent: null }),
}));
