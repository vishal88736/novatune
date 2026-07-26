from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class PlaylistSourceEnum(str, Enum):
    upload_csv = "upload_csv"
    upload_url = "upload_url"
    spotify_export = "spotify_export"
    manual = "manual"


class PlaylistStatusOut(BaseModel):
    id: UUID
    status: str
    source: PlaylistSourceEnum

    model_config = {"from_attributes": True}
