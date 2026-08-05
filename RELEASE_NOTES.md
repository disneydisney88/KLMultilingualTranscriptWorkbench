# Release Notes

## v2026.08.05.1

Release date: `2026-08-05`

### Highlights / 重點

- Long titles, filenames, and symbol-heavy names are cleaned and shortened automatically to reduce Windows path errors.
  - 長標題、檔名同符號較多嘅名稱會自動清理同縮短，減少 Windows 路徑錯誤。
- Batch runs keep going after single-item failures, and the report now separates completed items, skipped items, and reasons.
  - 批次轉寫遇到單項失敗會繼續跑，報告會分開列出完成、跳過同原因。
- Context limits are clearer: files up to 5 MB, pasted text up to 2,000 characters, and 100 tasks per batch.
  - 背景資料限制更清楚：檔案最多 5 MB、貼上文字最多 2,000 字元、每批最多 100 個 task。

### Included output files / 產出檔案

- Windows installer EXE / Windows 安裝程式
- Source ZIP / 原始碼 ZIP
- README and handoff Markdown files / README 同交接 Markdown 檔

### Test status / 測試狀態

- Desktop app launch verified / 已確認桌面版可啟動
- Installer build verified / 已確認安裝程式可打包
- Output package verified / 已確認輸出包可用
