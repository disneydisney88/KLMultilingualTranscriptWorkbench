from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from imageio_ffmpeg import get_ffmpeg_exe

from services.common import ensure_dir, sanitize_filename


def resolve_ffmpeg() -> str:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg
    return get_ffmpeg_exe()


def resolve_ffprobe() -> str | None:
    return shutil.which("ffprobe")


def probe_media(path: Path) -> dict[str, Any]:
    ffprobe = resolve_ffprobe()
    if ffprobe:
        command = [
            ffprobe,
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    ffmpeg = resolve_ffmpeg()
    command = [ffmpeg, "-hide_banner", "-i", str(path)]
    result = subprocess.run(command, capture_output=True, text=True)
    return {"raw": result.stderr}


def convert_to_wav16k_mono(source: Path, destination_dir: Path) -> Path:
    ensure_dir(destination_dir)
    ffmpeg = resolve_ffmpeg()
    destination = destination_dir / f"{sanitize_filename(source.stem)}.wav"
    command = [
        ffmpeg,
        "-y",
        "-i",
        str(source),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(destination),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    return destination
