from __future__ import annotations

import os
import sys
from pathlib import Path


def _resolve_root_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


ROOT_DIR = _resolve_root_dir()
RESOURCE_ROOT = (
    Path(getattr(sys, "_MEIPASS"))
    if getattr(sys, "frozen", False) and getattr(sys, "_MEIPASS", None)
    else ROOT_DIR
)
DATA_DIR = RESOURCE_ROOT / "data"
ASSETS_DIR = RESOURCE_ROOT / "assets"
USER_DATA_DIR = (
    Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "KLMultilingualTranscriptWorkbench"
    if getattr(sys, "frozen", False)
    else ROOT_DIR
)
MODELS_DIR = USER_DATA_DIR / "models"
TEMP_DIR = USER_DATA_DIR / "temp"
JOBS_DIR = TEMP_DIR / "jobs"
OUTPUTS_DIR = USER_DATA_DIR / "outputs"
LOGS_DIR = USER_DATA_DIR / "logs"
DB_PATH = USER_DATA_DIR / "transcripts.sqlite3"


DEFAULT_SETTINGS: dict[str, object] = {
    "language": "yue",
    "model_size": "small",
    "device": "cpu",
    "compute_type": "int8",
    "cpu_threads": 6,
    "workers": 1,
    "beam_size": 5,
    "vad_filter": True,
    "word_timestamps": True,
    "condition_on_previous_text": False,
    "temperature": 0.0,
    "initial_prompt": "",
}


SUPPORTED_AUDIO_EXTENSIONS = {
    ".aac",
    ".flac",
    ".m4a",
    ".mp3",
    ".ogg",
    ".wav",
}


SUPPORTED_VIDEO_EXTENSIONS = {
    ".mkv",
    ".mov",
    ".mp4",
    ".webm",
}


MAX_DOWNLOAD_BYTES = 3 * 1024 * 1024 * 1024


def ensure_workspace() -> None:
    for folder in (MODELS_DIR, TEMP_DIR, JOBS_DIR, OUTPUTS_DIR, LOGS_DIR):
        folder.mkdir(parents=True, exist_ok=True)
