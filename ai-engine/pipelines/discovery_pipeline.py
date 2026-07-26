"""Filters a candidate pool down to underexposed tracks matching taste."""

POPULARITY_CEILING = 0.35


def filter_hidden_gems(candidates: list[dict]) -> list[dict]:
    return [c for c in candidates if c.get("popularity_score", 0) <= POPULARITY_CEILING]
