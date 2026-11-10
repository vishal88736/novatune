from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import CurrentUser, get_current_user
from app.db.models.user import User
from app.db.session import get_db
from app.services.user_provisioning_service import user_provisioning_service

DbDep = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]


async def get_current_domain_user(
    current_user: CurrentUserDep, db: DbDep
) -> User:
    """
    The authenticated caller's domain profile row, created on first request.

    Every user-scoped table carries a foreign key to `users`, so endpoints
    that write user-scoped data depend on this rather than on
    `CurrentUserDep` alone.
    """
    return await user_provisioning_service.ensure_user(db, current_user)


CurrentDomainUserDep = Annotated[User, Depends(get_current_domain_user)]
