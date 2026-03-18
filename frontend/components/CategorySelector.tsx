"use client";

import React, { useState, useEffect } from "react";
import { apiGet, apiRequest } from "@/lib/api";

const GUARDIAN_CATEGORIES = [
  "World",
  "Politics",
  "Technology",
  "Science",
  "Environment",
  "Football",
];

interface CategorySelectorProps {
  onTaskAccepted?: (taskId: string) => void;
}

export default function CategorySelector({ onTaskAccepted }: CategorySelectorProps) {
  const [categories, setCategories] = useState<string[]>(GUARDIAN_CATEGORIES);
  const [selectedCategories, setSelectedCategories] = useState<string[]>(GUARDIAN_CATEGORIES);
  const [loading, setLoading] = useState(false);
  const [loadingOpts, setLoadingOpts] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    apiGet<{ categories: string[] }>("tasks/categories")
      .then((data) => {
        if (!cancelled && data?.categories?.length) {
          setCategories(data.categories);
          setSelectedCategories(data.categories);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setCategories(GUARDIAN_CATEGORIES);
          setSelectedCategories(GUARDIAN_CATEGORIES);
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
    selectedCategories.forEach((c) => params.append("selected_categories", c));
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
      <h2 className="text-sm font-medium text-zinc-800 mb-4">卫报频道选择</h2>
      {loadingOpts ? (
        <p className="text-zinc-500 text-sm">加载分类...</p>
      ) : (
        <>
          <div className="mb-4">
            <span className="text-xs uppercase tracking-widest text-zinc-500 block mb-2">
              勾选要抓取的频道（每频道最新 1 条）
            </span>
            <div className="flex flex-wrap gap-3">
              {categories.map((cat) => {
                const active = selectedCategories.includes(cat);
                return (
                  <button
                    key={cat}
                    type="button"
                    onClick={() => toggleCategory(cat)}
                    className={[
                      "px-3 py-1.5 rounded-md border text-sm transition-transform",
                      "hover:scale-[1.03] active:scale-[0.99]",
                      active
                        ? "bg-zinc-900 text-white border-zinc-900"
                        : "bg-white text-zinc-800 border-zinc-300 hover:border-zinc-500",
                    ].join(" ")}
                    aria-pressed={active}
                  >
                    {cat}
                  </button>
                );
              })}
            </div>
          </div>
          {error && (
            <p className="text-red-600 text-sm mb-3">{error}</p>
          )}
          <button
            type="button"
            onClick={handleSubmit}
            disabled={loading || selectedCategories.length === 0}
            className="px-4 py-2 bg-zinc-900 text-white text-sm font-medium rounded hover:bg-zinc-800 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading ? "正在抓取卫报..." : "开始抓取"}
          </button>
        </>
      )}
    </div>
  );
}
