# Changelog

## [2026.08.01.5] - 2026-08-01

### Added

- KL app name and logo
- Bilingual README and installer help text
- GitHub repository link
- Release notes and handoff docs
- Authenticode signing support in the build pipeline

### Changed

- Default install path now uses `C:\Program Files\KL Multilingual Transcript Workbench`
- User data now lives under `%LOCALAPPDATA%\KLMultilingualTranscriptWorkbench`
- Desktop shortcut and Start Menu shortcut branding updated

### Fixed

- Cleaner uninstall flow
- Better output packaging and documentation

### Notes

- Unsigned builds may still trigger SmartScreen
- A trusted code-signing certificate is required for proper Authenticode signing