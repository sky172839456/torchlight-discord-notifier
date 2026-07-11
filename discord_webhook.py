from datetime import datetime, timezone

import requests

from config import OFFICIAL_FACEBOOK_URL, OFFICIAL_SITE_URL


def build_payload(article):
    category = article.get("category", "公告")
    color = 0xE67E22 if category == "活動" else 0x3498DB

    return {
        "embeds": [{
            "title": "🔥 火炬之光：無限",
            "url": article["url"],
            "color": color,
            "description": (
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"# 📌 {article['title']}\n\n"
                f"📅 **日期**\n{article.get('date', '-')}\n\n"
                f"🏷️ **類別**\n{category}\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            ),
            "footer": {"text": "🔥 火炬情報雷達"},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }],
        "components": [{
            "type": 1,
            "components": [
                {"type": 2, "style": 5, "label": "📖 公告連結", "url": article["url"]},
                {"type": 2, "style": 5, "label": "🌐 官方網站", "url": OFFICIAL_SITE_URL},
                {"type": 2, "style": 5, "label": "📘 官方 Facebook", "url": OFFICIAL_FACEBOOK_URL}
            ]
        }]
    }


def send_article(webhook_url, article):
    response = requests.post(
        webhook_url,
        params={"with_components": "true"},
        json=build_payload(article),
        timeout=20
    )
    response.raise_for_status()
