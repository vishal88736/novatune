"use client";

import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts";

export function MoodTimeline({ data }: { data: { date: string; valence: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={220}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="valenceGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#8b3dd8" stopOpacity={0.45} />
            <stop offset="100%" stopColor="#8b3dd8" stopOpacity={0} />
          </linearGradient>
        </defs>
        <XAxis
          dataKey="date"
          tick={{ fill: "#7d7499", fontSize: 11 }}
          axisLine={false}
          tickLine={false}
        />
        <YAxis hide domain={[-1, 1]} />
        <Tooltip
          contentStyle={{
            background: "#ffffff",
            border: "1px solid #ece4f5",
            borderRadius: 12,
            boxShadow: "0 18px 40px -24px rgb(88 46 140 / 0.35)",
            fontSize: 12,
          }}
        />
        <Area type="monotone" dataKey="valence" stroke="#8b3dd8" fill="url(#valenceGradient)" strokeWidth={2} />
      </AreaChart>
    </ResponsiveContainer>
  );
}
