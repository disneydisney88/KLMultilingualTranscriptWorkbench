# KL 多語言逐字稿工作台

![KL Multilingual Transcript Workbench Logo](assets/kl-multilingual-transcript-workbench-logo.png)

GitHub: [disneydisney88/KLMultilingualTranscriptWorkbench](https://github.com/disneydisney88/KLMultilingualTranscriptWorkbench)

版本：`2026.08.05.1`
發佈日期：`2026-08-05`

KL 多語言逐字稿工作台係一個 Windows 11 本機逐字稿工作台，用嚟做本地轉寫、詞彙輔助修正同輸出。

## 今次更新 / What's New in v2026.08.05.1

- 長檔名、符號多嘅名稱會自動清理同縮短，減少 Windows 路徑錯誤。
- 批次轉寫遇到單項失敗會繼續跑，報告會分開列出完成、跳過同原因。
- 背景資料限制更清楚：檔案最多 5 MB、貼上文字最多 2,000 字元、每批最多 100 個 task。

## 功能

- 本機檔案轉寫
- YouTube / Google Drive / 直接 URL 匯入
- 廣東話、普通話、英文、日文、韓文、菲律賓文
- speaker diarization
- 名稱、股票代號、財技詞彙同自訂 terms
- 批次處理，單項失敗會 skip
- 一按開最新輸出資料夾
- 輸出 TXT / DOCX / SRT / VTT / JSON

## 建議系統要求

- Windows 11 64-bit
- Intel Core i5 / i7 或 AMD Ryzen 5 以上
- 8 GB RAM 起，建議 16 GB 以上配 `medium` / `large-v3`
- SSD 最少預留 2 GB 作程式，另加模型同輸出空間

## 安裝位置

Program Files:

```text
C:\Program Files\KL Multilingual Transcript Workbench
```

User data:

```text
%LOCALAPPDATA%\KLMultilingualTranscriptWorkbench
```

## 快速開始

1. 安裝程式。
2. 開啟桌面捷徑。
3. 加本機檔案，或者每行貼一條 link。
4. 揀語言同模型。
5. 需要時加入背景 terms。
6. 開始轉寫。

## 語言代碼

- `yue` = 廣東話
- `zh` = 普通話
- `en` = 英文
- `ja` = 日文
- `ko` = 韓文
- `tl` = 菲律賓文 / Tagalog

## 輸出規則

- 每個來源會輸出一個 transcript bundle。
- 輸出資料夾同檔名會盡量跟原名。
- YouTube 來源會盡量用原始影片標題。
- 如果批次中有一項失敗，會標示 `SKIP`，然後繼續下一項。
- 完成後會顯示批次 summary。

## 模型下載

- Whisper 係必要元件。
- 安裝程式會自動下載 small model。
- `medium` 同 `large-v3` 可以之後喺程式內按需要下載。

## 更新機制

程式啟動時會讀 `update.json`，再比對已安裝版本同清單版本。

範例：

```json
{
  "version": "2026.08.10.1",
  "title": "KL Multilingual Transcript Workbench v2026.08.10.1",
  "installer_url": "https://example.com/download/KLMultilingualTranscriptWorkbench-Setup.exe",
  "update_folder_url": "https://drive.google.com/drive/folders/your-folder-id",
  "release_notes": "Fix batch skip, update wording, and improve output naming.",
  "mandatory": false,
  "restart_after_update": true,
  "sha256": "optional-sha256-hash"
}
```

如果有新版本，程式會提示下載 / 更新，更新後需要重新啟動程式。

## 試用預備

暫時只預留，未正式啟用。

## Authenticode 簽署

Build pipeline 支援 Authenticode code signing，但仍然需要真正嘅簽署證書。

```bat
set KL_CODE_SIGN_PFX=C:\path\to\certificate.pfx
set KL_CODE_SIGN_PASSWORD=your_password
```

未簽署嘅測試版仍然可能會觸發 SmartScreen 警告。

## 免責聲明

本軟件係根據用戶指示，由 OpenAI Codex 輔助編寫。
只限內部研究同評估用途。
使用風險自負。
不提供任何保證。

## 聯絡

- KL CHOY
- Email: [klchoy226@yahoo.com.hk](mailto:klchoy226@yahoo.com.hk)
- LinkedIn: [www.linkedin.com/in/ka-leung-choy](http://www.linkedin.com/in/ka-leung-choy)
