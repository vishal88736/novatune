import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    App-specific profile, keyed to the same id Better Auth assigns in its
    own `auth.user` table (Better Auth owns credentials; this table owns
    product-domain profile fields).
    """

    __tablename__ = "users"

    display_name: Mapped[str] = mapped_column(String(120))
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    onboarding_completed_at: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
