import { renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { useCallbackUrl } from "./use-callback-url";

/**
 * `useSearchParams` is mocked so each case can pin down the query string.
 * The hook only ever returns a same-origin path — anything else would turn
 * the login form into an open redirect.
 */
const mocks = vi.hoisted(() => ({ search: "" }));

vi.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams(mocks.search),
}));

function setSearch(value: string) {
  mocks.search = value;
}

describe("useCallbackUrl", () => {
  it("falls back to the dashboard when no callback is present", () => {
    setSearch("");
    const { result } = renderHook(() => useCallbackUrl());
    expect(result.current).toBe("/dashboard");
  });

  it("keeps a same-origin path", () => {
    setSearch("callbackURL=%2Fchat");
    const { result } = renderHook(() => useCallbackUrl());
    expect(result.current).toBe("/chat");
  });

  it("rejects an absolute URL", () => {
    setSearch("callbackURL=https%3A%2F%2Fevil.com");
    const { result } = renderHook(() => useCallbackUrl());
    expect(result.current).toBe("/dashboard");
  });

  it("rejects a protocol-relative URL", () => {
    setSearch("callbackURL=%2F%2Fevil.com");
    const { result } = renderHook(() => useCallbackUrl());
    expect(result.current).toBe("/dashboard");
  });

  it("rejects a javascript: URL", () => {
    setSearch("callbackURL=javascript%3Aalert(1)");
    const { result } = renderHook(() => useCallbackUrl());
    expect(result.current).toBe("/dashboard");
  });
});
