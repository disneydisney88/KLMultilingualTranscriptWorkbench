from __future__ import annotations

import mimetypes
from pathlib import Path
from urllib.parse import urlparse, unquote

import requests

from config import MAX_DOWNLOAD_BYTES
from services.common import ensure_dir, sanitize_filename
from services.url_validator import validate_public_url


def _filename_from_response(url: str, response: requests.Response) -> str:
    disposition = response.headers.get("content-disposition", "")
    if "filename=" in disposition:
        filename = disposition.split("filename=", 1)[1].strip().strip('"')
        return sanitize_filename(filename)
    parsed = urlparse(url)
    base = Path(unquote(parsed.path)).name
    if base:
        return sanitize_filename(base)
    content_type = response.headers.get("content-type", "application/octet-stream").split(";")[0]
    extension = mimetypes.guess_extension(content_type) or ".bin"
    return sanitize_filename(f"download{extension}")


def _safe_fetch(url: str) -> requests.Response:
    session = requests.Session()
    current = validate_public_url(url)
    for _ in range(5):
        response = session.get(current, stream=True, timeout=60, allow_redirects=False)
        if response.is_redirect or response.is_permanent_redirect:
            location = response.headers.get("location")
            if not location:
                raise ValueError("銝?憭望?嚗??啣??撩撠?location")
            current = validate_public_url(requests.compat.urljoin(current, location))
            continue
        response.raise_for_status()
        return response
    raise ValueError("銝???????憭?)


def download_direct_url(url: str, destination_dir: Path) -> Path:
    ensure_dir(destination_dir)
    response = _safe_fetch(url)
    length = response.headers.get("content-length")
    if length and int(length) > MAX_DOWNLOAD_BYTES:
        raise ValueError("瑼??之嚗歇銝剜迫銝?")

    content_type = response.headers.get("content-type", "").lower()
    if content_type.startswith("text/html"):
        raise ValueError("?湔 URL ?絲靘蝬脤??嚗??臬頧神??擃?")

    filename = _filename_from_response(url, response)
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
