"use client";

import React, { useState, useEffect } from "react";
import { apiGet, apiRequest } from "@/lib/api";

const DEFAULT_LIMIT_PER_SOURCE = 3;

interface ScrapeControlProps {
  onTaskAccepted?: (taskId: string) => void;
}

export default function ScrapeControl({ onTaskAccepted }: ScrapeControlProps) {
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [limitPerSource, setLimitPerSource] = useState(DEFAULT_LIMIT_PER_SOURCE);
  const [loading, setLoading] = useState(false);
  const [loadingOpts, setLoadingOpts] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoadingOpts(true);
    apiGet<{ categories: string[] }>("tasks/categories")
      .then((data) => {
        if (!cancelled && data?.categories) {
          setCategories(data.categories);
          setSelectedCategories(data.categories);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setCategories([]);
          setSelectedCategories([]);
        }
      })
      .finally(() => {
        if (!cancelled) setLoadingOpts(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const toggleCategory = (cat: string) => {
    setSelectedCategories((prev) =>
      prev.includes(cat) ? prev.filter((c) => c !== cat) : [...prev, cat]
    );
  };

  const handleSubmit = () => {
    setError(null);
    setLoading(true);
    const params = new URLSearchParams();
    params.set("limit_per_source", String(limitPerSource));
    if (selectedCategories.length > 0) {
      selectedCategories.forEach((c) => params.append("categories", c));
    }
    const url = `tasks/real-scrape?${params.toString()}`;
    apiRequest<{ task_id: string }>(url, { method: "POST" })
      .then((data) => {
        onTaskAccepted?.(data?.task_id ?? "");
      })
      .catch((err: Error) => {
        setError(err.message ?? "请求失败");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div className="bg-white border border-zinc-200 rounded-lg shadow-sm p-6">
      <h2 className="text-sm font-medium text-zinc-800 mb-4">动态抓取配置</h2>
      {loadingOpts ? (
        <p className="text-zinc-500 text-sm">加载分类...</p>
      ) : (
        <>
          <div className="mb-4">
            <span className="text-xs uppercase tracking-widest text-zinc-500 block mb-2">分类（多选）</span>
            <div className="flex flex-wrap gap-2">
              {categories.map((cat) => (
                <label
                  key={cat}
                  className="inline-flex items-center gap-1.5 text-sm cursor-pointer"
                >
                  <input
                    type="checkbox"
                    checked={selectedCategories.includes(cat)}
                    onChange={() => toggleCategory(cat)}
                    className="rounded border-zinc-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-zinc-700">{cat}</span>
                </label>
              ))}
            </div>
          </div>
          <div className="mb-4">
            <label className="text-xs uppercase tracking-widest text-zinc-500 block mb-2">
              每个源抓取条数
            </label>
            <input
              type="number"
              min={1}
              max={20}
              value={limitPerSource}
              onChange={(e) => setLimitPerSource(Number(e.target.value) || 1)}
              className="w-20 px-2 py-1.5 border border-zinc-300 rounded text-sm"
            />
          </div>
          {error && (
            <p className="text-red-600 text-sm mb-3">{error}</p>
          )}
          <button
            type="button"
            onClick={handleSubmit}
            disabled={loading}
            className="px-4 py-2 bg-zinc-900 text-white text-sm font-medium rounded hover:bg-zinc-800 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading ? "正在按需调度全球情报源..." : "开始抓取"}
          </button>
        </>
      )}
    </div>
  );
}
