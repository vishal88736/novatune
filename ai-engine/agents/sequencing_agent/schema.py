from pydantic import BaseModel


class SequencingInput(BaseModel):
    user_id: str
    candidate_track_ids: list[str]
    target_arc: str = "steady"  # plateau | build | wind_down | steady


class SequencingOutput(BaseModel):
    ordered_track_ids: list[str]
    arc_label: str
