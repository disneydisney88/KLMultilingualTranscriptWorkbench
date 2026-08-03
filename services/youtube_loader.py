from __future__ import annotations

from pathlib import Path

from yt_dlp import YoutubeDL

from services.common import ensure_dir, sanitize_filename


def download_youtube_media(url: str, destination_dir: Path, progress=None) -> Path:
    ensure_dir(destination_dir)
    outtmpl = str(destination_dir / "%(title).200s-%(id)s.%(ext)s")
    state: dict[str, object] = {"path": None}

    def hook(data: dict[str, object]) -> None:
        if data.get("status") == "finished":
            state["path"] = data.get("filename")
        if progress and data.get("status") == "downloading":
            total = data.get("total_bytes") or data.get("total_bytes_estimate")
            downloaded = data.get("downloaded_bytes") or 0
            if total:
                progress(min(0.95, float(downloaded) / float(total)), desc="銝? YouTube ?唾?")

    options = {
        "extract_flat": False,
        "noplaylist": True,
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": False,
        "continuedl": True,
        "retries": 3,
        "outtmpl": outtmpl,
        "progress_hooks": [hook],
        "postprocessors": [],
    }

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        candidate = state["path"]
        if isinstance(candidate, str) and candidate:
            return Path(candidate)
        requested = ydl.prepare_filename(info)
        return Path(requested)
