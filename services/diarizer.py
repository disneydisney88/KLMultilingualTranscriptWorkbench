from __future__ import annotations

import re
from functools import lru_cache
from dataclasses import replace
from typing import Iterable

from services.common import TranscriptSegment, WordTiming


DIARIZATION_MODEL = "pyannote/speaker-diarization-3.1"


def _overlap(start_a: float, end_a: float, start_b: float, end_b: float) -> float:
    return max(0.0, min(end_a, end_b) - max(start_a, start_b))


def _normalize_speaker_label(label: str) -> str:
    raw = str(label).strip()
    match = re.search(r"(\d+)", raw)
    if match:
        return f"Speaker {int(match.group(1))}"
    cleaned = raw.replace("_", " ").replace("-", " ").strip()
    if not cleaned:
        return "Speaker"
    pieces = cleaned.split()
    if pieces and pieces[0].lower() == "speaker":
        return "Speaker " + " ".join(pieces[1:]) if len(pieces) > 1 else "Speaker"
    return cleaned


def _extract_turns(diarization) -> list[tuple[float, float, str]]:
    turns: list[tuple[float, float, str]] = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        turns.append((float(turn.start), float(turn.end), _normalize_speaker_label(str(speaker))))
    turns.sort(key=lambda item: (item[0], item[1]))
    return turns


def _best_speaker_for_interval(
    start: float,
    end: float,
    turns: list[tuple[float, float, str]],
    fallback: str | None = None,
) -> tuple[str | None, float]:
    if not turns:
        return fallback, 0.0
    scored: dict[str, float] = {}
    for turn_start, turn_end, speaker in turns:
        overlap = _overlap(start, end, turn_start, turn_end)
        if overlap > 0:
            scored[speaker] = scored.get(speaker, 0.0) + overlap
    if not scored:
        return fallback, 0.0
    speaker, overlap = max(scored.items(), key=lambda item: item[1])
    total = max(0.0001, end - start)
    return speaker, overlap / total


def _assign_word_speakers(
    words: list[WordTiming],
    turns: list[tuple[float, float, str]],
    fallback: str | None,
) -> tuple[str | None, float]:
    if not words:
        return fallback, 0.0
    totals: dict[str, float] = {}
    total_duration = 0.0
    for word in words:
        duration = max(0.0, float(word.end) - float(word.start))
        total_duration += duration or 0.0
        speaker, ratio = _best_speaker_for_interval(float(word.start), float(word.end), turns, fallback)
        if speaker is None:
            continue
        totals[speaker] = totals.get(speaker, 0.0) + (duration or ratio)
    if not totals:
        return fallback, 0.0
    dominant_speaker, dominant_duration = max(totals.items(), key=lambda item: item[1])
    denominator = total_duration if total_duration > 0 else sum(item[1] for item in totals.items())
    if denominator <= 0:
        denominator = 1.0
    return dominant_speaker, round(min(1.0, dominant_duration / denominator), 3)


def _merge_adjacent_segments(segments: list[TranscriptSegment], gap_threshold: float = 0.8) -> list[TranscriptSegment]:
    if not segments:
        return []
    merged: list[TranscriptSegment] = [segments[0]]
    for segment in segments[1:]:
        last = merged[-1]
        same_speaker = last.speaker == segment.speaker
        close_enough = segment.start - last.end <= gap_threshold
        if same_speaker and close_enough:
            last.end = max(last.end, segment.end)
            last.text_raw = f"{last.text_raw} {segment.text_raw}".strip()
            last.text_corrected = f"{last.text_corrected} {segment.text_corrected}".strip()
            last.words.extend(segment.words)
            if segment.confidence is not None:
                last.confidence = max(last.confidence or 0.0, segment.confidence)
            if segment.speaker_confidence is not None:
                last.speaker_confidence = max(last.speaker_confidence or 0.0, segment.speaker_confidence)
        else:
            merged.append(segment)
    for index, segment in enumerate(merged, start=1):
        segment.index = index
    return merged


@lru_cache(maxsize=2)
def _load_pipeline(hf_token: str):
    from pyannote.audio import Pipeline  # type: ignore

    pipeline = Pipeline.from_pretrained(DIARIZATION_MODEL, use_auth_token=hf_token)
    return pipeline


def diarize_segments(
    audio_path: str,
    segments: list[TranscriptSegment],
    hf_token: str | None = None,
) -> tuple[list[TranscriptSegment], str]:
    try:
        _ = _load_pipeline  # noqa: F841
        import pyannote.audio  # noqa: F401
    except Exception:
        return segments, "pyannote.audio not available; skipped diarization"

    if not hf_token:
        return segments, "Missing Hugging Face token; skipped diarization"

    try:
        pipeline = _load_pipeline(hf_token)
        diarization = pipeline(audio_path)
        turns = _extract_turns(diarization)
    except Exception as exc:
        return segments, f"Diarization failed: {exc}"

    labelled: list[TranscriptSegment] = []
    speaker_set: set[str] = set()

    for segment in segments:
        fallback = segment.speaker
        if segment.words:
            speaker, confidence = _assign_word_speakers(segment.words, turns, fallback)
        else:
            speaker, confidence = _best_speaker_for_interval(segment.start, segment.end, turns, fallback)
        if speaker:
            speaker_set.add(speaker)
        labelled.append(
            replace(
                segment,
                speaker=speaker or fallback,
                speaker_confidence=confidence if confidence > 0 else segment.speaker_confidence,
            )
        )

    merged = _merge_adjacent_segments(labelled)
    merged_count = len(labelled) - len(merged)
    speakers = ", ".join(sorted(speaker_set)) if speaker_set else "none"
    status = f"Speaker diarization completed: {len(speaker_set)} speaker(s) identified ({speakers}); merged {merged_count} segment(s)."
    return merged, status
