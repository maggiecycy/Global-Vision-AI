import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from html import escape

import httpx
from app.core.config import settings


def _send_via_resend(receiver_email: str, subject: str, body_text: str, html_body: str) -> None:
    """通过 Resend HTTP API 发送（HF 环境 SMTP 被封时使用）"""
    api_key = settings.RESEND_API_KEY
    if not api_key:
        raise RuntimeError("RESEND_API_KEY is not configured")
    from_header = settings.RESEND_FROM or (f"Global Vision <{settings.SMTP_USER}>" if settings.SMTP_USER else "Global Vision <onboarding@resend.dev>")

    resp = httpx.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "from": from_header,
            "to": [receiver_email],
            "subject": subject,
            "text": body_text,
            "html": html_body,
        },
        timeout=20.0,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"Resend API error: {resp.status_code} {resp.text}")


def send_brief_email(
    receiver_email: str,
    subject: str,
    items: list[dict] | None = None,
    body_text: str | None = None,
) -> None:
    """
    发送简报邮件（极简黑白报刊风 HTML + 纯文本 fallback）。
    - 若 RESEND_API_KEY 已设置：走 Resend HTTP API（HF 等 SMTP 被封环境）
    - 否则：走 SMTP（本地 / 自托管）
    """
    if not receiver_email:
        raise RuntimeError("receiver_email is empty")
    use_resend = bool(settings.RESEND_API_KEY)
    if use_resend:
        if not settings.SMTP_USER:
            raise RuntimeError("使用 Resend 时需设置 SMTP_USER 作为发件人邮箱（或在 Resend 后台验证域名后改为 RESEND_FROM）")
    else:
        if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASS:
            raise RuntimeError("SMTP 未配置，或设置 RESEND_API_KEY 使用 Resend")

    today_str = datetime.now().strftime("%B %d, %Y")
    items = items or []

    if body_text is None:
        if not items:
            body_text = f"GLOBAL VISION.\n{today_str} · 精选简报\n\n过去 12 小时内暂无新文章。"
        else:
            lines: list[str] = [f"GLOBAL VISION.\n{today_str} · 精选简报\n"]
            for it in items:
                lines.append(f"- {it.get('title','')}\n  {it.get('summary','')}\n  {it.get('url','')}")
            body_text = "\n\n".join(lines)

    if not items:
        items_html = (
            "<div style=\"padding: 16px 0;\">"
            "<p style=\"margin:0;color:#4b5563;font-size:14px;\">过去 12 小时内暂无新文章。</p>"
            "</div>"
        )
    else:
        blocks: list[str] = []
        for it in items:
            title = escape(str(it.get("title", "")))
            summary = escape(str(it.get("summary", "")))
            url = escape(str(it.get("url", "")))
            meta = escape(str(it.get("meta", "")))
            blocks.append(
                "\n".join(
                    [
                        "<div style=\"padding: 18px 0; border-bottom: 1px solid #eee;\">",
                        f"  <div style=\"font-size:16px;font-weight:700;margin:0 0 6px 0;\">{title}</div>",
                        (f"  <div style=\"margin:0 0 10px 0;color:#111;font-size:12px;letter-spacing:.02em;\">{meta}</div>" if meta else ""),
                        f"  <div style=\"margin:0 0 10px 0;color:#4b5563;font-size:14px;line-height:1.6;\">{summary}</div>",
                        f"  <a href=\"{url}\" style=\"color:#111;text-decoration:none;border-bottom:1px solid #111;font-size:12px;\">查看全文</a>",
                        "</div>",
                    ]
                )
            )
        items_html = "\n".join(blocks)

    html_template = f"""
<html>
  <body style="font-family:-apple-system,system-ui,sans-serif;color:#111;max-width:600px;margin:0 auto;padding:40px 20px;line-height:1.6;">
    <div style="border-bottom:3px solid #000;padding-bottom:20px;margin-bottom:26px;">
      <div style="margin:0;font-size:28px;letter-spacing:-0.5px;font-weight:800;">GLOBAL VISION.</div>
      <div style="margin:6px 0 0;color:#666;font-size:12px;text-transform:uppercase;">{today_str} · 精选简报</div>
    </div>
    {items_html}
    <div style="margin-top:44px;padding-top:16px;border-top:1px solid #eee;text-align:center;color:#999;font-size:12px;">
      <p style="margin:0;">Maggie, 今天的法语进度也要继续加油 🇫🇷</p>
    </div>
  </body>
</html>
""".strip()

    if use_resend:
        _send_via_resend(receiver_email, subject, body_text, html_template)
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr(("DailyBrief", settings.SMTP_USER))
    msg["To"] = receiver_email
    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_template, "html", "utf-8"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
        server.ehlo()
        if settings.SMTP_USE_TLS:
            server.starttls()
            server.ehlo()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.sendmail(settings.SMTP_USER, [receiver_email], msg.as_string())
