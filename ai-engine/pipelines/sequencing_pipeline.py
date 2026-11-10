"""Pure arc-construction logic reused by the Sequencing Agent."""

from typing import Any


def build_arc(tracks: list[dict[str, Any]], arc: str) -> list[dict[str, Any]]:
    scored = [(t, (t.get("duration_seconds", 200) % 60) / 60) for t in tracks]
    if arc == "build":
        scored.sort(key=lambda x: x[1])
    elif arc == "wind_down":
        scored.sort(key=lambda x: -x[1])
    return [t for t, _ in scored]
