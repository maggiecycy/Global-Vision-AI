"use client";

import React, { useState } from 'react';

export default function SettingsPage() {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  // 1. 触发爬虫任务
  const handleTriggerScraper = async () => {
    setStatus('loading');
    setMessage('正在唤醒后端爬虫引擎...');
  
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/tasks/real-scrape?limit=5', {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
      });
  
      if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
  
      const data = await response.json();
      setStatus('success');
      setMessage(`指令已下达！任务 ID: ${data.task_id || '未知'}`);
      setTimeout(() => setStatus('idle'), 3000);
  
    } catch (error) {
      console.error('Trigger failed:', error);
      setStatus('error');
      setMessage('触发失败，请检查后端状态。');
    }
  };

  // 2. 核心修改：一键清空数据库逻辑
  const handleClearDatabase = async () => {
    // 安全检查，防止误触
    if (!window.confirm("🚨 警告：此操作将永久清空数据库中所有的文章和 AI 分析结果。确定继续吗？")) {
      return;
    }

    setStatus('loading');
    setMessage('正在清理数据库...');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/articles/clear-all', {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

      setStatus('success');
      setMessage('数据库已清空，系统已重置。');
      setTimeout(() => setStatus('idle'), 3000);

    } catch (error) {
      console.error('Clear failed:', error);
      setStatus('error');
      setMessage('清理失败，请确认后端 DELETE 接口已就绪。');
    }
  };

  return (
    <div className="min-h-screen bg-zinc-50 text-zinc-900 p-8 md:p-16 font-sans">
      <header className="mb-12 border-b border-zinc-200 pb-6">
        <h1 className="text-4xl font-light tracking-tight">Settings.</h1>
        <p className="text-zinc-500 mt-2 text-sm tracking-wide">SYSTEM CONFIGURATION & CONTROLS</p>
      </header>

      <div className="max-w-2xl space-y-8">
        <section className="bg-white p-8 border border-zinc-200 rounded-xl shadow-sm">
          <h2 className="text-lg font-medium text-zinc-800 mb-2">数据管理 (Data Management)</h2>
          <p className="text-sm text-zinc-500 mb-6 leading-relaxed">
            在此手动控制数据流。你可以启动自动化抓取任务，或在必要时彻底重置本地数据库。
          </p>

          <div className="flex flex-col gap-6">
            <div className="flex items-center gap-4">
              {/* 启动按钮 */}
              <button
                onClick={handleTriggerScraper}
                disabled={status === 'loading'}
                className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all duration-300 ${
                  status === 'loading'
                    ? 'bg-zinc-200 text-zinc-400 cursor-not-allowed'
                    : 'bg-zinc-900 text-zinc-50 hover:bg-zinc-800 shadow-md active:scale-95'
                }`}
              >
                {status === 'loading' ? '引擎运转中...' : '启动抓取引擎 (Run Scraper)'}
              </button>

              {/* 清空按钮 - 极简红色描边风格 */}
              <button
                onClick={handleClearDatabase}
                disabled={status === 'loading'}
                className="px-6 py-2.5 rounded-lg text-sm font-medium border border-red-200 text-red-600 hover:bg-red-50 transition-all active:scale-95 disabled:opacity-30"
              >
                清空数据库
              </button>
            </div>

            {/* 状态提示文字 */}
            {message && (
              <div className={`text-sm py-2 px-4 rounded-md inline-block ${
                status === 'success' ? 'bg-emerald-50 text-emerald-600 border border-emerald-100' : 
                status === 'error' ? 'bg-red-50 text-red-600 border border-red-100' : 
                'bg-zinc-100 text-zinc-500 animate-pulse'
              }`}>
                {message}
              </div>
            )}
          </div>
        </section>

        <section className="bg-zinc-50 p-8 border border-zinc-200 rounded-xl border-dashed">
          <h2 className="text-sm font-medium text-zinc-400 mb-2">Advanced Config (Coming Soon)</h2>
          <p className="text-xs text-zinc-400 italic">API Endpoints: http://127.0.0.1:8000/api/v1</p>
        </section>
      </div>
    </div>
  );
}