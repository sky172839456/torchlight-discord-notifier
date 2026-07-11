from datetime import datetime, timezone

import requests

from config import OFFICIAL_FACEBOOK_URL, OFFICIAL_SITE_URL


def build_payload(article):
    category = article.get("category", "公告")
    color = 0xE67E22 if category == "活動" else 0x3498DB

    return {
        "embeds": [{
            "title": "🔥 火炬之光：無限",
            "color": color,
            "description": (
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"# 📌 {article['title']}\n\n"
                f"📅 **日期**\n{article.get('date', '-')}\n\n"
                f"🏷️ **類別**\n{category}\n\n"
                f"🔗 **公告連結：** <{article['url']}>\n"
                f"🌐 **官方網站：** <{OFFICIAL_SITE_URL}>\n"
                f"📘 **官方 FB：** <{OFFICIAL_FACEBOOK_URL}>\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            ),
            "footer": {"text": "🔥 火炬情報雷達"},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }]
    }


def send_article(webhook_url, article):
    response = requests.post(
        webhook_url,
        json=build_payload(article),
        timeout=20
    )
    response.raise_for_status()
