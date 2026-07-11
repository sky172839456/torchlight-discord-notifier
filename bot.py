import argparse
import json
from pathlib import Path

from config import TEST_WEBHOOK_URL, WEBHOOK_URL
from discord_webhook import send_article
from source import CATEGORIES, fetch_news


STATE_FILE = Path("sent_ids.json")


def load_sent_ids():
    if not STATE_FILE.exists():
        return None
    try:
        return set(json.loads(STATE_FILE.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError):
        return set()


def save_sent_ids(ids):
    STATE_FILE.write_text(
        json.dumps(sorted(ids), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


def category_samples(news):
    samples = []
    for category in CATEGORIES:
        sample = next((item for item in news if item["category"] == category), None)
        if not sample:
            raise RuntimeError(f"官網目前找不到「{category}」內容")
        samples.append(sample)
    return samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    news = fetch_news()
    if not news:
        raise RuntimeError("官網沒有抓到任何公告或活動")

    if args.test:
        if not TEST_WEBHOOK_URL:
            raise RuntimeError("尚未設定 TEST_WEBHOOK_URL")
        targets = category_samples(news)
        for article in reversed(targets):
            send_article(TEST_WEBHOOK_URL, article)
        print(f"測試通知完成：{len(targets)} 則")
        return

    if not WEBHOOK_URL:
        raise RuntimeError("尚未設定 WEBHOOK_URL")

    sent_ids = load_sent_ids()
    current_ids = {item["id"] for item in news}

    if sent_ids is None:
        save_sent_ids(current_ids)
        print("首次執行：已建立基準，不補發舊公告")
        return

    targets = [item for item in news if item["id"] not in sent_ids]
    for article in reversed(targets):
        send_article(WEBHOOK_URL, article)
        sent_ids.add(article["id"])
        save_sent_ids(sent_ids)

    print(f"新通知完成：{len(targets)} 則")


if __name__ == "__main__":
    main()

