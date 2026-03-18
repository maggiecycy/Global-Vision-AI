"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

export interface SentimentDataPoint {
  date: string;
  score: number;
  count?: number;
}

interface SentimentChartProps {
  data: SentimentDataPoint[];
  height?: number;
}

export default function SentimentChart({ data, height = 260 }: SentimentChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e4e4e7" />
        <XAxis dataKey="date" stroke="#71717a" fontSize={11} tickLine={false} />
        <YAxis
          domain={[0, 10]}
          stroke="#71717a"
          fontSize={11}
          tickLine={false}
          label={{ value: "情绪分值", angle: -90, position: "insideLeft", fontSize: 11 }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "#18181b",
            border: "none",
            borderRadius: "8px",
            color: "#fafafa",
          }}
          // Recharts 的 Tooltip value 可能为 undefined，避免严格注解导致构建失败
          formatter={(value) => [typeof value === "number" ? value.toFixed(1) : String(value ?? ""), "情绪分值"]}
          labelFormatter={(label) => `日期: ${label}`}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="score"
          name="情绪分值"
          stroke="#3b82f6"
          strokeWidth={2}
          dot={{ fill: "#3b82f6", r: 3 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
