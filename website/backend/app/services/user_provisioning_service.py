"""
Keeps the domain `users` table in step with Better Auth's `auth.user` table.

Better Auth owns credentials and the identity itself; website/backend owns
the product-domain profile. The two are keyed by the same id, so every
authenticated request needs a matching row in `users` before anything
user-scoped can be written (playlists, listening sessions, mood logs and
so on all carry a foreign key to it).

Provisioning is idempotent and safe to run on every request: the row is
looked up first and only written when it is missing.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import CurrentUser
from app.db.models.user import User


class UserProvisioningService:
    async def ensure_user(self, db: AsyncSession, current_user: CurrentUser) -> User:
        """
        Returns the domain user for the authenticated caller, creating it on
        first sight.
        """
        user_id = current_user.uuid_id

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is not None:
            return user

        user = User(
            id=user_id,
            display_name=current_user.name or current_user.email.split("@")[0][:120],
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


user_provisioning_service = UserProvisioningService()
