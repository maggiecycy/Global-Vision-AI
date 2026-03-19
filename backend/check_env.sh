#!/bin/sh
# HF Spaces 启动前检查：缺失关键环境变量时打印到 stdout，便于在日志中看到
set -e

missing=""
[ -z "$DATABASE_URL" ] && missing="${missing}DATABASE_URL "
[ -z "$DEEPSEEK_API_KEY" ] && missing="${missing}DEEPSEEK_API_KEY "

if [ -n "$missing" ]; then
  echo "=========================================="
  echo "FATAL: 以下环境变量未设置: $missing"
  echo "请在 HF Spaces > Settings > Variables and Secrets 中添加"
  echo "DATABASE_URL 示例: postgresql://user:pass@host:5432/dbname"
  echo "=========================================="
  exit 1
fi
