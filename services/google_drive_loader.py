from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import requests

from config import MAX_DOWNLOAD_BYTES
from services.common import ensure_dir, sanitize_filename


FILE_ID_PATTERNS = (
    re.compile(r"/file/d/([a-zA-Z0-9_-]+)"),
    re.compile(r"[?&]id=([a-zA-Z0-9_-]+)"),
)


def extract_drive_file_id(value: str) -> str | None:
    text = value.strip()
    if re.fullmatch(r"[a-zA-Z0-9_-]{10,}", text):
        return text
    for pattern in FILE_ID_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(1)
    return None


def build_drive_download_url(file_id: str) -> str:
    return f"https://drive.google.com/uc?export=download&id={file_id}"


def _get_confirmed_response(session: requests.Session, url: str) -> requests.Response:
    response = session.get(url, stream=True, timeout=60)
    response.raise_for_status()
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            confirmed = session.get(url, params={"confirm": value}, stream=True, timeout=60)
            confirmed.raise_for_status()
            return confirmed

    body = ""
    try:
        body = response.text
    except Exception:
        body = ""
    match = re.search(r"confirm=([0-9A-Za-z_]+)", body)
    if match:
        confirmed = session.get(url, params={"confirm": match.group(1)}, stream=True, timeout=60)
        confirmed.raise_for_status()
        return confirmed
    return response


def download_google_drive_file(source: str, destination_dir: Path) -> Path:
    ensure_dir(destination_dir)
    file_id = extract_drive_file_id(source)
    if file_id is None:
        raise ValueError("?⊥?敺?Google Drive ???閫??瑼? ID")

    session = requests.Session()
    url = build_drive_download_url(file_id)
    response = _get_confirmed_response(session, url)

    content_disposition = response.headers.get("content-disposition", "")
    filename_match = re.search(r'filename="?([^"]+)"?', content_disposition)
    if filename_match:
        filename = sanitize_filename(filename_match.group(1))
    else:
        filename = sanitize_filename(f"drive-{file_id}")

    destination = destination_dir / filename
    downloaded = 0
    with destination.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if not chunk:
                continue
            downloaded += len(chunk)
            if downloaded > MAX_DOWNLOAD_BYTES:
                raise ValueError("瑼??之嚗歇銝剜迫銝?")
            handle.write(chunk)
    return destination
