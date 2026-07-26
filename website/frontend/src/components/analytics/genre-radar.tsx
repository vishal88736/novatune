"use client";

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts";

export function GenreRadar({ data }: { data: { genre: string; affinity: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <RadarChart data={data}>
        <PolarGrid stroke="rgba(255,255,255,0.08)" />
        <PolarAngleAxis dataKey="genre" tick={{ fill: "#8b899e", fontSize: 11 }} />
        <Radar dataKey="affinity" stroke="#38e1c6" fill="#7c5cfc" fillOpacity={0.35} />
      </RadarChart>
    </ResponsiveContainer>
  );
}
