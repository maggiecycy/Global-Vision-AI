import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from html import escape

from app.core.config import settings


def send_brief_email(
    receiver_email: str,
    subject: str,
    items: list[dict] | None = None,
    body_text: str | None = None,
) -> None:
    """
    发送简报邮件（极简黑白报刊风 HTML + 纯文本 fallback）。
    依赖环境变量：SMTP_HOST/SMTP_PORT/SMTP_USER/SMTP_PASS。
    """
    if not settings.SMTP_HOST:
        raise RuntimeError("SMTP_HOST is not configured")
    if not settings.SMTP_USER:
        raise RuntimeError("SMTP_USER is not configured")
    if not settings.SMTP_PASS:
        raise RuntimeError("SMTP_PASS is not configured")
    if not receiver_email:
        raise RuntimeError("receiver_email is empty")

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
