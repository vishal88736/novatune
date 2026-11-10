from fastapi import APIRouter

from app.api.v1.deps import CurrentDomainUserDep, CurrentUserDep
from app.schemas.user import UserProfileOut

router = APIRouter()


@router.post("/session/sync", response_model=UserProfileOut)
async def sync_session(
    current_user: CurrentUserDep, domain_user: CurrentDomainUserDep
) -> UserProfileOut:
    """
    Bridges the Better Auth session into the product's domain user profile.

    Better Auth owns credentials; website/backend owns the `users` profile
    row. This endpoint makes sure the two agree, and is safe to call on
    every sign-in — it provisions the row the first time and is a no-op
    afterwards.
    """
    return UserProfileOut.model_validate(domain_user)
