"use client";

import React from "react";

interface MoodScoreBadgeProps {
  score: number | null | undefined;
}

export default function MoodScoreBadge({ score }: MoodScoreBadgeProps) {
  if (score == null || score === undefined) return null;

  const s = Math.round(Number(score));
  if (s < 0 || s > 10) return null;

  const [bg, text] =
    s >= 8
      ? ["bg-emerald-100", "text-emerald-800"]
      : s >= 4
        ? ["bg-slate-100", "text-slate-700"]
        : ["bg-amber-100", "text-amber-800"];

  return (
    <span
      title="AI 情绪指数 (0-10)"
      className={`inline-flex items-center justify-center min-w-[1.75rem] px-1.5 py-0.5 text-[10px] font-medium tabular-nums rounded ${bg} ${text}`}
    >
      {s}/10
    </span>
  );
}
