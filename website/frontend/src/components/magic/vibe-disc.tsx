import { cn } from "@/lib/utils";

/**
 * The signature gradient disc. A purple → pink → orange ring with a
 * clean hole punched through the middle, used as the hero's focal
 * object. Optional chips float on the ring in the reference's style.
 */
export function VibeDisc({
  className,
  children,
}: {
  className?: string;
  children?: React.ReactNode;
}) {
  return (
    <div className={cn("relative aspect-square rounded-full", className)}>
      <div className="disc absolute inset-0 rounded-full" />
      <div className="absolute inset-[17%] rounded-full bg-[var(--color-canvas)]" />
      {children}
    </div>
  );
}

/**
 * A yellow squircle chip that holds a single icon — the reference uses
 * these to punctuate the disc.
 */
export function DiscChip({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return <div className={cn("chip absolute grid place-items-center", className)}>{children}</div>;
}
