import { create } from "zustand";

interface UIState {
  commandPaletteOpen: boolean;
  sidebarCollapsed: boolean;
  activeModal: string | null;
  toggleCommandPalette: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  openModal: (id: string) => void;
  closeModal: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  commandPaletteOpen: false,
  sidebarCollapsed: false,
  activeModal: null,
  toggleCommandPalette: () => set((s) => ({ commandPaletteOpen: !s.commandPaletteOpen })),
  setSidebarCollapsed: (sidebarCollapsed) => set({ sidebarCollapsed }),
  openModal: (activeModal) => set({ activeModal }),
  closeModal: () => set({ activeModal: null }),
}));
