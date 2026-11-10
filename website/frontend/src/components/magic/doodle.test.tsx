import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Doodle, DoodleRing } from "./doodle";
import { VibeDisc } from "./vibe-disc";
import { Logo } from "@/components/shared/logo";

describe("Doodle", () => {
  it("draws a single dashed curve", () => {
    const { container } = render(<Doodle />);
    expect(container.querySelectorAll("path.doodle")).toHaveLength(1);
  });

  it("adds a solid marker only when an end is requested", () => {
    const withMarker = render(<Doodle end="arrow" />);
    expect(withMarker.container.querySelectorAll("path")).toHaveLength(2);

    const without = render(<Doodle end="none" />);
    expect(without.container.querySelectorAll("path")).toHaveLength(1);
  });
});

describe("DoodleRing", () => {
  it("draws an elliptical ring", () => {
    const { container } = render(<DoodleRing />);
    expect(container.querySelector("ellipse.doodle-ring")).not.toBeNull();
  });
});

describe("VibeDisc", () => {
  it("renders the gradient disc with a hole punched through it", () => {
    const { container } = render(<VibeDisc />);
    expect(container.querySelector(".disc")).not.toBeNull();
    expect(container.querySelectorAll(".rounded-full").length).toBeGreaterThanOrEqual(2);
  });
});

describe("Logo", () => {
  it("renders the wordmark", () => {
    render(<Logo />);
    expect(screen.getByText("AI")).toBeTruthy();
  });
});
