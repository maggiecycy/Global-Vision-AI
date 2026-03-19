FROM python:3.11-slim

# 安装系统依赖：Redis 和 Supervisor
RUN apt-get update && apt-get install -y \
    redis-server \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制依赖并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端所有代码
COPY . .

# 启动检查脚本可执行
RUN chmod +x /app/check_env.sh

# 禁用 Python 输出缓冲，便于在 HF 日志中看到错误
ENV PYTHONUNBUFFERED=1

# 创建 Celery 需要的运行目录
RUN mkdir -p /var/run/celery /var/log/celery

# 暴露 HF 要求的端口
EXPOSE 7860

# 启动 Supervisord
CMD ["supervisord", "-c", "/app/supervisord.conf"]
