# KL Multilingual Transcript Workbench

![KL Multilingual Transcript Workbench Logo](assets/kl-multilingual-transcript-workbench-logo.png)

GitHub: [disneydisney88/KLMultilingualTranscriptWorkbench](https://github.com/disneydisney88/KLMultilingualTranscriptWorkbench)

Version: `2026.08.05.1`
Release date: `2026-08-05`

KL Multilingual Transcript Workbench is a Windows 11 desktop app for local transcription, glossary-assisted correction, and export.

## What's New in v2026.08.05.1

- Long file names and symbol-heavy names are cleaned and shortened automatically for safer Windows paths.
- Batch jobs continue after single-item failures, and the report now separates completed items, skipped items, and reasons.
- Context limits are clearer: glossary files up to 5 MB, pasted text up to 2,000 characters, and a maximum of 100 tasks per batch.

## Features

- Local file transcription
- YouTube / Google Drive / direct URL import
- Cantonese, Mandarin, English, Japanese, Korean, and Filipino support
- Speaker diarization
- Context glossary for names, stock codes, financial terms, and custom terms
- Batch processing with skip-on-failure behavior
- One-click open for the latest output folder
- Export to `TXT`, `DOCX`, `SRT`, `VTT`, and `JSON`
- Local SQLite job tracking

## Recommended system requirements

- Windows 11 64-bit
- Intel Core i5/i7 or AMD Ryzen 5 or better
- 8 GB RAM minimum, 16 GB recommended for `medium` or `large-v3`
- SSD with at least 2 GB free for the app, plus extra space for models and outputs

## Install locations

Program files:

```text
C:\Program Files\KL Multilingual Transcript Workbench
```

User data:

```text
%LOCALAPPDATA%\KLMultilingualTranscriptWorkbench
```

## Quick start

1. Install the app.
2. Open the desktop shortcut.
3. Add local files or paste one link per line.
4. Select the language and model.
5. Add context terms if needed.
6. Start transcription.

## Notes

- `yue` is the Cantonese language code
- `zh` is Mandarin
- `en` is English
- `ja` is Japanese
- `ko` is Korean
- `tl` is Filipino / Tagalog

## Output behavior

- Each source produces one transcript bundle.
- Output folders and file names try to follow the original media title.
- For YouTube sources, the app tries to use the original video title.
- If one item fails during a batch, it is marked `SKIP` and the batch continues.
- The app shows a batch summary after processing.

## Model downloads

- Whisper is required.
- The installer downloads the small model automatically.
- Medium and large-v3 are optional and can be downloaded later from the app.

## In-app update

The desktop app reads `update.json` at startup and compares the manifest version with the installed version.

Example manifest:

```json
{
  "version": "2026.08.10.1",
  "title": "KL Multilingual Transcript Workbench v2026.08.10.1",
  "installer_url": "https://drive.google.com/drive/folders/1-ewn_aQ-knIPx-LXgLHlbD97vvfZdCV-?usp=sharing",
  "update_folder_url": "https://drive.google.com/drive/folders/14CHaAUOi6iJLe6L76qwpCT5-KUx7MTj4?usp=sharing",
  "release_notes": "Fix batch skip, update wording, and improve output naming.",
  "mandatory": false,
  "restart_after_update": true,
  "sha256": "optional-sha256-hash"
}
```

If a newer version is found, the app prompts the user to download/update and reminds them to restart the app after updating.
For testing, you can point `installer_url` to a Google Drive file or folder link. `update_folder_url` is the user-facing folder for release files and notes.

For automatic checking, place `update.json` next to the installed EXE or set the `KL_UPDATE_MANIFEST_URL` environment variable to a direct JSON file URL.

## Trial preparation

Trial data is prepared but not enforced yet.

Suggested placeholder manifest:

```json
{
  "trial_days": 7,
  "trial_enabled": false,
  "notes": "Reserved for future trial enforcement."
}
```

## Authenticode signing

The build pipeline supports Authenticode code signing, but you still need a real signing certificate.

```bat
set KL_CODE_SIGN_PFX=C:\path\to\certificate.pfx
set KL_CODE_SIGN_PASSWORD=your_password
```

Unsigned test builds may still trigger SmartScreen warnings.

## Disclaimer

This software was written with OpenAI Codex assistance under the user's instructions.
It is intended for internal research and evaluation only.
Use it at your own risk.
No warranty is provided.

## Contact

- KL CHOY
- Email: [klchoy226@yahoo.co.uk](mailto:klchoy226@yahoo.co.uk)
- LinkedIn: [www.linkedin.com/in/ka-leung-choy](http://www.linkedin.com/in/ka-leung-choy)