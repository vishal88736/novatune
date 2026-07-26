import httpx
from fastapi import Cookie, Depends

from app.core.config import settings
from app.core.exceptions import UnauthorizedError


class CurrentUser:
    def __init__(self, id: str, email: str, name: str | None = None):
        self.id = id
        self.email = email
        self.name = name


async def get_current_user(
    better_auth_session_token: str | None = Cookie(default=None, alias="better-auth.session_token"),
) -> CurrentUser:
    """
    Verifies the Better Auth session cookie issued by website/frontend by
    calling its session-verification endpoint. website/backend never issues
    or stores sessions itself — Better Auth (Next.js side) remains the
    single source of truth for authentication state.
    """
    if not better_auth_session_token:
        raise UnauthorizedError()

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{settings.cors_origins_list[0]}/api/auth/get-session",
                cookies={"better-auth.session_token": better_auth_session_token},
                timeout=5.0,
            )
        except httpx.HTTPError as exc:
            raise UnauthorizedError("Couldn't verify your session.") from exc

    if resp.status_code != 200 or not resp.json():
        raise UnauthorizedError()

    payload = resp.json()
    user = payload.get("user", {})
    return CurrentUser(id=user["id"], email=user["email"], name=user.get("name"))


CurrentUserDep = Depends(get_current_user)
