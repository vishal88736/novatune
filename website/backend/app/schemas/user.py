from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserProfileOut(BaseModel):
    """
    The product-domain profile row. Credentials live in Better Auth's
    `auth.user` table and are never exposed here.
    """

    id: UUID
    display_name: str
    avatar_url: str | None = None
    onboarding_completed_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
