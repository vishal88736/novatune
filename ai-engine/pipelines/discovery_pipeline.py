"""Filters a candidate pool down to underexposed tracks matching taste."""

from typing import Any

POPULARITY_CEILING = 0.35


def filter_hidden_gems(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [c for c in candidates if c.get("popularity_score", 0) <= POPULARITY_CEILING]
