"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

export interface LanguageDataPoint {
  name: string;
  value: number;
}

const COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#ec4899", "#8b5cf6"];

interface LanguagePieChartProps {
  data: LanguageDataPoint[];
  height?: number;
}

export default function LanguagePieChart({ data, height = 260 }: LanguagePieChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={90}
          paddingAngle={2}
          dataKey="value"
          nameKey="name"
        >
          {data.map((_, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: "#18181b",
            border: "none",
            borderRadius: "8px",
            color: "#fafafa",
          }}
          // Recharts 的类型在不同版本下对 formatter 的 value 可能含 undefined；避免严格注解导致构建失败
          formatter={(value) => [value ?? 0, "数量"]}
        />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
