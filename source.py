from datetime import datetime
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import sync_playwright

from config import NEWS_URL


CATEGORIES = ("公告", "活動")


def _article_id(url):
    return parse_qs(urlparse(url).query).get("id", [url])[0]


def _read_visible_articles(page, category):
    articles = page.evaluate(
        """
        () => Array.from(document.querySelectorAll('a[href*="/news/single"]'))
          .filter(link => link.offsetParent !== null)
          .map(link => {
            const card = link.closest('.i_lpqqn9zf9n') || link.parentElement;
            const date = card?.querySelector('.i_lpqqn9umj7')?.textContent || '';
            return {
              title: (link.textContent || '').trim(),
              date: date.trim(),
              url: link.href
            };
          })
          .filter(item => item.title && item.url)
        """
    )

    result = []
    for order, article in enumerate(articles):
        article["id"] = _article_id(article["url"])
        article["category"] = category
        article["order"] = order
        try:
            article["datetime"] = datetime.strptime(article["date"], "%Y/%m/%d")
        except ValueError:
            article["datetime"] = datetime.min
        result.append(article)
    return result


def fetch_news():
    news_by_id = {}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(locale="zh-TW")
        page.goto(NEWS_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector('a[href*="/news/single"]', timeout=45000)

        for category in CATEGORIES:
            tab = page.locator(".m-tap").filter(has_text=category)
            if tab.count() != 1:
                raise RuntimeError(f"找不到唯一的「{category}」分類按鈕")

            tab.click()
            page.wait_for_timeout(1000)

            for article in _read_visible_articles(page, category):
                existing = news_by_id.get(article["id"])
                if existing:
                    continue
                news_by_id[article["id"]] = article

        browser.close()

    news = list(news_by_id.values())
    news.sort(key=lambda item: (item["datetime"], -item["order"]), reverse=True)
    return news

