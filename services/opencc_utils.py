from __future__ import annotations

from functools import lru_cache


@lru_cache(maxsize=8)
def _get_converter(config_name: str):
    from opencc import OpenCC  # type: ignore

    return OpenCC(config_name)


def convert_text(text: str, config_name: str | None) -> str:
    if not config_name or config_name == "none":
        return text
    try:
        converter = _get_converter(config_name)
    except Exception:
        return text
    try:
        return converter.convert(text)
    except Exception:
        return text
