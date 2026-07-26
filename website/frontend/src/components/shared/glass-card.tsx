import { cn } from "@/lib/utils";
import * as React from "react";

export function GlassCard({
  className,
  strong = false,
  ...props
}: React.HTMLAttributes<HTMLDivElement> & { strong?: boolean }) {
  return <div className={cn(strong ? "glass-strong" : "glass", "p-6", className)} {...props} />;
}
