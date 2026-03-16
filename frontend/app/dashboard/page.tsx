"use client";

import React, { useState, useEffect, useMemo } from "react";
import { apiGet } from "@/lib/api";
import SentimentChart, { SentimentDataPoint } from "@/components/SentimentChart";
import CategorySelector from "@/components/CategorySelector";

interface Article {
  id: number;
  title_en: string;
  url?: string;
  created_at: string;
  published_at?: string | null;
  language?: string;
  source?: { id?: number; name: string; language: string };
  ai_result?: {
    summary_zh: string;
    category_tag: string;
    keywords?: string[];
    sentiment_score?: number | null;
  };
}

const MOCK_SENTIMENT_DATA: SentimentDataPoint[] = [
  { date: "03/10", score: 5.2 },
  { date: "03/11", score: 6.1 },
  { date: "03/12", score: 5.8 },
  { date: "03/13", score: 5.5 },
  { date: "03/14", score: 6.3 },
  { date: "03/15", score: 5.9 },
];

const formatTime = (isoString: string) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
};

function ArticleCard({ article }: { article: Article }) {
  const titleEl = (
    <h3 className="text-lg font-medium text-zinc-900 leading-snug group-hover:text-blue-600 transition-colors flex items-center gap-2">
      {article.url ? (
        <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:underline truncate">
          {article.title_en}
        </a>
      ) : (
        <span>{article.title_en}</span>
      )}
    </h3>
  );
  return (
    <div className="group bg-white p-6 border border-zinc-200 rounded-lg hover:border-zinc-400 transition-all duration-300">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1 pr-4 min-w-0">
          {titleEl}
        </div>
        <div className="flex flex-col items-end gap-2 shrink-0">
          <span className="text-[10px] text-zinc-400 font-mono">
            {formatTime(article.created_at)}
          </span>
          <span className="text-[10px] uppercase tracking-wider px-2 py-1 bg-zinc-100 text-zinc-600 rounded">
            {article.ai_result?.category_tag ?? "Uncategorized"}
          </span>
        </div>
      </div>
      <p className="text-sm text-zinc-600 leading-relaxed mt-2">
        {article.ai_result?.summary_zh ?? "等待 DeepSeek 分析中..."}
      </p>
    </div>
  );
}

export default function DashboardPage() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    apiGet<Article[]>("articles/")
      .then((data) => {
        if (!cancelled) {
          setArticles(Array.isArray(data) ? data : []);
        }
      })
      .catch((err: Error) => {
        if (!cancelled) {
          setError(err.message ?? "请求失败");
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const sentimentChartData = useMemo((): SentimentDataPoint[] => {
    if (!articles.length) return MOCK_SENTIMENT_DATA;
    const byDate: Record<string, { sum: number; count: number }> = {};
    for (const a of articles) {
      const score = a.ai_result?.sentiment_score;
      if (score == null || score < 1 || score > 10) continue;
      const dateStr = a.published_at
        ? new Date(a.published_at).toLocaleDateString("zh-CN", { month: "2-digit", day: "2-digit" })
        : new Date(a.created_at).toLocaleDateString("zh-CN", { month: "2-digit", day: "2-digit" });
      if (!byDate[dateStr]) byDate[dateStr] = { sum: 0, count: 0 };
      byDate[dateStr].sum += score;
      byDate[dateStr].count += 1;
    }
    const points = Object.entries(byDate).map(([date, { sum, count }]) => ({
      date,
      score: Math.round((sum / count) * 10) / 10,
      count,
    }));
    if (points.length === 0) return MOCK_SENTIMENT_DATA;
    points.sort((a, b) => a.date.localeCompare(b.date));
    return points;
  }, [articles]);

  return (
    <div className="min-h-screen bg-zinc-50 text-zinc-900 p-8 md:p-16 font-sans">
      <header className="mb-8 border-b border-zinc-200 pb-6 flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-light tracking-tight">卫报精准看板</h1>
          <p className="text-zinc-500 mt-2 text-sm tracking-wide">The Guardian / AI Briefing</p>
        </div>
        <div className="text-sm text-zinc-400 font-mono">Live Data Sync</div>
      </header>

      <div className="mb-8">
        <CategorySelector />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
        <div className="lg:col-span-4">
          <div className="bg-white p-4 border border-zinc-200 rounded-lg shadow-sm">
            <h2 className="text-xs uppercase tracking-widest text-zinc-500 mb-2">情绪趋势（辅助参考）</h2>
            <SentimentChart data={sentimentChartData} height={180} />
          </div>
        </div>
        <div className="lg:col-span-8" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-3 space-y-4">
          <div className="bg-white p-6 border border-zinc-200 rounded-lg shadow-sm">
            <h2 className="text-xs uppercase tracking-widest text-zinc-500 mb-4">Total Scraped</h2>
            <p className="text-5xl font-light">{loading ? "—" : articles.length}</p>
            <p className="text-xs text-zinc-400 mt-2">Articles in database</p>
          </div>
          <div className="bg-zinc-900 text-zinc-100 p-6 rounded-lg shadow-md">
            <h2 className="text-xs uppercase tracking-widest text-zinc-400 mb-4">System Status</h2>
            <div className="flex items-center gap-3">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
              </span>
              <span className="text-sm font-light tracking-wide">Backend Connected</span>
            </div>
          </div>
        </div>

        <div className="lg:col-span-9 space-y-4">
          <h2 className="text-sm font-medium text-zinc-800 mb-4">Latest Briefings</h2>

          {loading && (
            <p className="text-zinc-500 italic text-sm p-4 bg-white border border-zinc-200 rounded-lg">
              🍵 正在加载...
            </p>
          )}

          {!loading && error && (
            <p className="text-red-600 text-sm p-4 bg-red-50 border border-red-200 rounded-lg">
              {error}
            </p>
          )}

          {!loading && !error && articles.length === 0 && (
            <p className="text-zinc-500 italic text-sm p-4 bg-white border border-zinc-200 rounded-lg">
              暂无数据，请在上方选择卫报频道并开始抓取。
            </p>
          )}

          {!loading && !error && articles.length > 0 && (
            <div className="space-y-4">
              {articles.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
