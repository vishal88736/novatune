import { cn } from "@/lib/utils";
import * as React from "react";

export function SurfaceCard({
  className,
  strong = false,
  ...props
}: React.HTMLAttributes<HTMLDivElement> & { strong?: boolean }) {
  return (
    <div className={cn(strong ? "surface-strong" : "surface", "p-6", className)} {...props} />
  );
}
