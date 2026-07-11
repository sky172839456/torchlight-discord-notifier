# Torchlight Discord Notifier

《火炬之光：無限》繁體中文官網公告與活動 Discord 通知機器人。

## 功能

- 分別讀取官網「公告」與「活動」分類。
- 依官方文章 ID 去重，避免重複通知。
- 第一次排程只建立基準，不補發所有舊文章。
- Discord 卡片固定提供公告、官網與官方 Facebook 連結。
- 每 30 分鐘透過 GitHub Actions 自動檢查。

## 官方來源

- [新聞列表](https://torchlight.xd.com/tw/news/list)
- [台港澳官網](https://torchlight.starforce.tw/)
- [官方 Facebook](https://www.facebook.com/TorchlightInfiniteTW)

## GitHub Secrets

- `WEBHOOK_URL`：正式通知頻道的 Discord Webhook。
- `TEST_WEBHOOK_URL`：測試通知頻道的 Discord Webhook。

Webhook 僅存放於 GitHub Secrets，不得提交至程式碼。
