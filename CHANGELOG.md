# Changelog

## [2026.08.05.1] - 2026-08-05

### Added

- Bilingual update notes for the new release
  - 新版本已加入中英雙語更新說明。
- Clearer batch summary with completed, skipped, and reason sections
  - 批次報告更清楚，分開顯示完成、跳過同原因。

### Changed

- Windows filenames and output folders now use shorter, safer sanitized names
  - Windows 檔名同輸出資料夾改用更短、更安全嘅清理名稱。
- Batch jobs keep running after individual failures instead of stopping the worker
  - 批次工作遇到單項失敗時會繼續跑，唔會停低 worker。
- Context limits and batch limits are shown more clearly in the UI and docs
  - 介面同文件會更清楚顯示背景資料限制同批次上限。
