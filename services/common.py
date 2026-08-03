from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def sanitize_filename(name: str, fallback: str = "output") -> str:
    cleaned = re.sub(r"[<>:\"/\\|?*\x00-\x1F]", "_", name.strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned or fallback


def seconds_to_timestamp(seconds: float, milliseconds: bool = True) -> str:
    seconds = max(0.0, float(seconds))
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis == 1000:
        secs += 1
        millis = 0
    if seconds >= 3600:
        base = f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        base = f"{minutes:02d}:{secs:02d}"
    if milliseconds:
        return f"{base},{millis:03d}"
    return base


def seconds_to_vtt_timestamp(seconds: float) -> str:
    stamp = seconds_to_timestamp(seconds, milliseconds=True)
    return stamp.replace(",", ".")


@dataclass(slots=True)
class WordTiming:
    word: str
    start: float
    end: float
    probability: float | None = None


@dataclass(slots=True)
class GlossaryChange:
    pattern: str
    replacement: str
    count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class TranscriptSegment:
    index: int
    start: float
    end: float
    text_raw: str
    text_corrected: str
    speaker: str | None = None
    speaker_confidence: float | None = None
    confidence: float | None = None
    avg_logprob: float | None = None
    no_speech_prob: float | None = None
    words: list[WordTiming] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["words"] = [asdict(word) for word in self.words]
        return payload


@dataclass(slots=True)
class TranscriptResult:
    job_id: str
    source_type: str
    source_url: str | None
    original_filename: str | None
    media_title: str | None
    duration_seconds: float | None
    language: str
    model_size: str
    settings: dict[str, Any]
    segments: list[TranscriptSegment]
    glossary_changes: list[GlossaryChange]
    summary: str
    raw_text: str
    corrected_text: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["segments"] = [segment.to_dict() for segment in self.segments]
        payload["glossary_changes"] = [change.to_dict() for change in self.glossary_changes]
        return payload
