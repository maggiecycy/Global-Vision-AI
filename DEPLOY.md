# 部署与联调指南

## Bug 1：前端 Vercel 请求 `net::ERR_CONNECTION_REFUSED`

**现象**：前端请求 `http://127.0.0.1:8000/api/v1/...`，连接被拒绝。

**原因**：`NEXT_PUBLIC_API_BASE_URL` 在 **Build Time** 注入，未 Redeploy 则仍为旧值。

**修复步骤**：
1. 打开 **Vercel 项目 → Settings → Environment Variables**
2. 添加/修改 `NEXT_PUBLIC_API_BASE_URL`，值为：
   ```
   https://maggiecycy-Global-Vision-Backend.hf.space/api/v1
   ```
3. **Redeploy**：Deployments → 最近部署 → `...` → Redeploy（不勾选缓存）

---

## Bug 2：CORS

已确认 `backend/app/main.py` 包含：
- `https://global-vision-ai.vercel.app`
- `https://maggiecycys-projects.vercel.app`
- `allow_origin_regex=r"^https://.*\.vercel\.app$"`

无需额外修改。

---

## Bug 3：将 backend 单独推送到 Hugging Face

backend 目录是**独立 Git 仓库**，remote `hf` 指向 HF Spaces。

**安全推送序列**：

```bash
cd /Users/caoyan/Desktop/DailyBrief_Project/backend

# 1. 确认 remote
git remote -v
# 应看到 hf -> https://huggingface.co/spaces/maggiecycy/Global-Vision-Backend

# 2. 若有冲突（rejected fetch first），先 fetch 再强制覆盖
git fetch hf
git push -f hf main
```

若仍被拒绝，检查 HF Token 是否有效，或使用：
```bash
git remote set-url hf https://maggiecycy:YOUR_HF_TOKEN@huggingface.co/spaces/maggiecycy/Global-Vision-Backend
git push -f hf main
```

---

## Bug 4：HF 环境 SMTP 端口被封 → 使用 Resend

在 HF Spaces **Variables and Secrets** 中添加：

| 变量名 | 值 |
|--------|-----|
| `RESEND_API_KEY` | 你的 Resend API Key（如 `re_xxxxxxxx`） |
| `RESEND_FROM` | 可选，格式 `Global Vision <onboarding@resend.dev>` |

当 `RESEND_API_KEY` 存在时，邮件会走 Resend HTTP API，不再使用 SMTP。本地开发仍可用 SMTP。

Resend 免费额度：100 封/天。注册 https://resend.com 获取 API Key。
