"use client";

import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts";

export function MoodTimeline({ data }: { data: { date: string; valence: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={220}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="valenceGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#7c5cfc" stopOpacity={0.5} />
            <stop offset="100%" stopColor="#7c5cfc" stopOpacity={0} />
          </linearGradient>
        </defs>
        <XAxis dataKey="date" tick={{ fill: "#8b899e", fontSize: 11 }} axisLine={false} tickLine={false} />
        <YAxis hide domain={[-1, 1]} />
        <Tooltip contentStyle={{ background: "#101219", border: "1px solid rgba(255,255,255,0.1)" }} />
        <Area type="monotone" dataKey="valence" stroke="#7c5cfc" fill="url(#valenceGradient)" strokeWidth={2} />
      </AreaChart>
    </ResponsiveContainer>
  );
}
