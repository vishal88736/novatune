from typing import Any

from pydantic import BaseModel


class DiscoveryInput(BaseModel):
    user_id: str
    diversity_target: float = 0.2  # fraction of slots reserved for hidden gems


class DiscoveryOutput(BaseModel):
    tracks: list[dict[str, Any]]
    arc_label: str = "discovery"
    generated_for_mood: str = "exploratory"
