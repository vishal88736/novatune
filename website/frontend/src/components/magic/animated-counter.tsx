"use client";

import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import { useEffect, useState } from "react";

export function AnimatedCounter({ value, suffix = "" }: { value: number; suffix?: string }) {
  const count = useMotionValue(0);
  const rounded = useTransform(count, (v) => Math.round(v).toLocaleString());
  const [display, setDisplay] = useState("0");

  useEffect(() => {
    setDisplay(rounded.get());
    const unsubscribe = rounded.on("change", (v) => setDisplay(v));
    const controls = animate(count, value, { duration: 1.4, ease: [0.22, 1, 0.36, 1] });
    return () => {
      unsubscribe();
      controls.stop();
    };
  }, [value, count, rounded]);

  return (
    <motion.span>
      {display}
      {suffix}
    </motion.span>
  );
}
