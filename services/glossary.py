from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config import DATA_DIR
from services.common import GlossaryChange, ensure_dir


@dataclass(slots=True)
class GlossaryEntry:
    pattern: str
    replacement: str
    case_sensitive: bool = True
    kind: str = "literal"
    include_in_prompt: bool = True


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_glossary() -> list[GlossaryEntry]:
    entries = []
    for filename in ("glossary.json", "cantonese_common_glossary.json"):
        entries.extend(_load_json(DATA_DIR / filename, []))
    results: list[GlossaryEntry] = []
    for item in entries:
        if isinstance(item, dict) and item.get("pattern") and item.get("replacement"):
            results.append(
                GlossaryEntry(
                    pattern=str(item["pattern"]),
                    replacement=str(item["replacement"]),
                    case_sensitive=bool(item.get("case_sensitive", True)),
                    kind=str(item.get("kind", "literal")),
                    include_in_prompt=bool(item.get("include_in_prompt", True)),
                )
            )
    for code in load_stock_codes():
        normalized = code.zfill(5)
        base = normalized.lstrip("0") or normalized
        pattern = rf"(?<!\d)(?:HK[\s\-_#]*)?(?:0?{base}|{normalized})(?:\s*\.?\s*HK)?(?!\d)"
        results.append(
            GlossaryEntry(
                pattern=pattern,
                replacement=normalized,
                case_sensitive=False,
                kind="regex",
                include_in_prompt=False,
            )
        )
    return results


def load_stock_codes() -> list[str]:
    raw = _load_json(DATA_DIR / "stock_codes.json", [])
    if isinstance(raw, list):
        return [str(item).zfill(5) for item in raw if str(item).strip()]
    return []


def load_speaker_names() -> dict[str, str]:
    raw = _load_json(DATA_DIR / "speaker_names.json", {})
    if isinstance(raw, dict):
        return {str(key): str(value) for key, value in raw.items()}
    return {}


def apply_glossary(text: str, glossary: list[GlossaryEntry]) -> tuple[str, list[GlossaryChange]]:
    corrected = text
    changes: list[GlossaryChange] = []
    ordered = sorted(glossary, key=lambda item: len(item.pattern), reverse=True)
    for entry in ordered:
        flags = 0 if entry.case_sensitive else re.IGNORECASE
        if entry.kind == "regex":
            pattern = entry.pattern
        else:
            pattern = re.escape(entry.pattern)
            if re.fullmatch(r"[A-Za-z0-9_.-]+", entry.pattern):
                pattern = rf"\b{pattern}\b"
        corrected, count = re.subn(pattern, entry.replacement, corrected, flags=flags)
        if count:
            changes.append(GlossaryChange(pattern=entry.pattern, replacement=entry.replacement, count=count))
    return corrected, changes
