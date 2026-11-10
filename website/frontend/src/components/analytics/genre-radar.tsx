"use client";

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts";

export function GenreRadar({ data }: { data: { genre: string; affinity: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <RadarChart data={data}>
        <PolarGrid stroke="rgba(36, 28, 59, 0.12)" />
        <PolarAngleAxis dataKey="genre" tick={{ fill: "#7d7499", fontSize: 11 }} />
        <Radar dataKey="affinity" stroke="#8b3dd8" fill="#8b3dd8" fillOpacity={0.28} />
      </RadarChart>
    </ResponsiveContainer>
  );
}
