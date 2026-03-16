"use client";

import React from "react";
import { TagCloud } from "react-tagcloud";

export interface TagItem {
  value: string;
  count: number;
}

interface KeywordCloudProps {
  tags: TagItem[];
  minSize?: number;
  maxSize?: number;
}

export default function KeywordCloud({
  tags,
  minSize = 14,
  maxSize = 36,
}: KeywordCloudProps) {
  if (!tags.length) {
    return (
      <div className="flex items-center justify-center h-48 text-zinc-400 text-sm">
        暂无关键词数据
      </div>
    );
  }
  return (
    <div className="w-full h-48 flex items-center justify-center">
      <TagCloud
        minSize={minSize}
        maxSize={maxSize}
        tags={tags}
        shuffle={false}
        colorOptions={{
          hue: "blue",
          luminosity: "light",
          format: "rgb",
          alpha: 0.9,
        }}
      />
    </div>
  );
}
