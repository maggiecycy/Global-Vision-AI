"use client";

import React, { useState, useEffect, useMemo } from "react";
import { apiGet, apiRequest } from "@/lib/api";
import CategorySelector from "@/components/CategorySelector";
import MoodScoreBadge from "@/components/MoodScoreBadge";

interface Article {
  id: number;
  title_en: string;
  snippet?: string;
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
interface KeywordItem {
  text: string;
  value: number;
}

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
  const score = article.ai_result?.sentiment_score;
  const titleEl = (
    <h3 className="text-lg font-medium text-zinc-900 leading-snug group-hover:text-blue-600 transition-colors flex items-center gap-2">
      {article.url ? (
        <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:underline truncate">
          {article.title_en}
        </a>
      ) : (
        <span>{article.title_en}</span>
      )}
      <MoodScoreBadge score={score} />
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
  const [emailSending, setEmailSending] = useState(false);
  const [emailMsg, setEmailMsg] = useState<string | null>(null);
  const [keywords, setKeywords] = useState<KeywordItem[]>([]);
  const [kwLoading, setKwLoading] = useState(false);
  const [kwError, setKwError] = useState<string | null>(null);
  const [selectedKeyword, setSelectedKeyword] = useState<string | null>(null);

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

  useEffect(() => {
    let cancelled = false;
    setKwLoading(true);
    setKwError(null);
    apiGet<KeywordItem[]>("articles/keywords")
      .then((data) => {
        if (!cancelled) setKeywords(Array.isArray(data) ? data : []);
      })
      .catch((e: Error) => {
        if (!cancelled) setKwError(e.message ?? "关键词请求失败");
      })
      .finally(() => {
        if (!cancelled) setKwLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const filteredArticles = useMemo(() => {
    if (!selectedKeyword) return articles;
    const kw = selectedKeyword.toLowerCase();
    return articles.filter((a) => {
      const hay = `${a.title_en ?? ""} ${a.snippet ?? ""} ${(a.ai_result?.summary_zh ?? "")}`.toLowerCase();
      return hay.includes(kw);
    });
  }, [articles, selectedKeyword]);

  const kwStats = useMemo(() => {
    let min = Infinity;
    let max = -Infinity;
    for (const k of keywords) {
      if (typeof k.value !== "number") continue;
      min = Math.min(min, k.value);
      max = Math.max(max, k.value);
    }
    if (!isFinite(min) || !isFinite(max)) return { min: 0, max: 0 };
    return { min, max };
  }, [keywords]);

  return (
    <div className="min-h-screen bg-zinc-50 text-zinc-900 p-8 md:p-16 font-sans">
      <header className="mb-8 border-b border-zinc-200 pb-6 flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-extralight tracking-tight">卫报精准看板</h1>
          <p className="text-zinc-500 mt-2 text-sm tracking-wide">The Guardian / AI Briefing</p>
        </div>
        <div className="flex items-center gap-3">
          {emailMsg && (
            <span className="text-xs text-zinc-500">{emailMsg}</span>
          )}
          <button
            type="button"
            onClick={() => {
              setEmailMsg(null);
              setEmailSending(true);
              apiRequest<{ task_id: string }>("tasks/test-email", { method: "POST" })
                .then((d) => setEmailMsg(`已触发邮件任务：${d?.task_id ?? ""}`))
                .catch((e: Error) => setEmailMsg(e.message ?? "邮件触发失败"))
                .finally(() => setEmailSending(false));
            }}
            disabled={emailSending}
            className="text-xs px-3 py-1.5 rounded border border-zinc-300 bg-white hover:bg-zinc-50 text-zinc-700 disabled:opacity-60 disabled:cursor-not-allowed"
            title="触发一次邮件发送测试（异步任务）"
          >
            {emailSending ? "邮件测试中..." : "邮件测试"}
          </button>
          <div className="text-sm text-zinc-400 font-mono">Live Data Sync</div>
        </div>
      </header>

      <div className="mb-8">
        <CategorySelector />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
        <div className="lg:col-span-12">
          <div className="bg-white p-6 border border-zinc-200 rounded-lg shadow-sm font-serif">
            <div className="flex items-center justify-between gap-4 mb-4">
              <h2 className="text-xs uppercase tracking-widest text-zinc-500">关键词云（过去 24 小时）</h2>
              <div className="flex items-center gap-2">
                {selectedKeyword && (
                  <>
                    <span className="text-xs text-zinc-600">
                      筛选：<span className="font-semibold text-zinc-900">{selectedKeyword}</span>
                    </span>
                    <button
                      type="button"
                      onClick={() => setSelectedKeyword(null)}
                      className="text-xs px-2 py-1 rounded border border-zinc-300 bg-white hover:bg-zinc-50 text-zinc-700"
                    >
                      清除
                    </button>
                  </>
                )}
              </div>
            </div>

            {kwLoading && <p className="text-zinc-500 text-sm">加载关键词...</p>}
            {!kwLoading && kwError && (
              <p className="text-red-600 text-sm">{kwError}</p>
            )}
            {!kwLoading && !kwError && keywords.length === 0 && (
              <p className="text-zinc-500 text-sm">暂无关键词数据</p>
            )}
            {!kwLoading && !kwError && keywords.length > 0 && (
              <div className="flex flex-wrap gap-3 md:gap-4">
                {keywords.map((k) => {
                  const range = Math.max(1, kwStats.max - kwStats.min);
                  const t = (k.value - kwStats.min) / range;
                  const fontSize = Math.round(12 + t * 18); // 12-30px
                  const isActive = selectedKeyword === k.text;
                  return (
                    <button
                      key={k.text}
                      type="button"
                      onClick={() => setSelectedKeyword((prev) => (prev === k.text ? null : k.text))}
                      className={[
                        "px-2.5 py-1.5 rounded border transition-transform",
                        "hover:scale-[1.03] active:scale-[0.99]",
                        isActive ? "border-zinc-900 bg-zinc-900 text-white" : "border-zinc-200 bg-white text-zinc-900 hover:border-zinc-500",
                      ].join(" ")}
                      style={{ fontSize }}
                      title={`value=${k.value}`}
                    >
                      {k.text}
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        </div>
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

          {!loading && !error && filteredArticles.length === 0 && (
            <p className="text-zinc-500 italic text-sm p-4 bg-white border border-zinc-200 rounded-lg">
              暂无数据{selectedKeyword ? "（或当前关键词筛选无结果）" : ""}，请在上方选择频道并开始抓取。
            </p>
          )}

          {!loading && !error && filteredArticles.length > 0 && (
            <div className="space-y-4">
              {filteredArticles.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
