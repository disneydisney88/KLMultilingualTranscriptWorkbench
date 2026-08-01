# KL Multilingual Transcript Workbench

![KL Multilingual Transcript Workbench Logo](assets/kl-multilingual-transcript-workbench-logo.png)

GitHub: [disneydisney88/KLMultilingualTranscriptWorkbench](https://github.com/disneydisney88/KLMultilingualTranscriptWorkbench)

Version: `2026.08.01.5`
Release date: `2026-08-01`

KL Multilingual Transcript Workbench is a Windows 11 desktop app for local transcription, glossary-assisted correction, and export.

## Features

- Local file transcription
- YouTube / Google Drive / direct URL import
- Cantonese, Mandarin, English, Japanese, Korean, and Filipino support
- Speaker diarization
- Context glossary for names, stock codes, and financial terms
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
3. Add local files or paste links.
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
- Email: [klchoy226@yahoo.com.hk](mailto:klchoy226@yahoo.com.hk)
- LinkedIn: [www.linkedin.com/in/ka-leung-choy](http://www.linkedin.com/in/ka-leung-choy)