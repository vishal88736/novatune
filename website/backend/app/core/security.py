import uuid

import httpx
from fastapi import Cookie, Depends

from app.core.config import settings
from app.core.exceptions import UnauthorizedError


class CurrentUser:
    """
    The authenticated caller.

    `id` is the raw Better Auth user id and is JSON-safe — it is what gets
    forwarded to ai-engine as an opaque `user_id`. `uuid_id` is the same value
    parsed into a UUID, which is what the domain tables key on (see
    `db/models/user.py`). Better Auth is configured to generate UUID ids so
    the two always agree.
    """

    def __init__(self, id: str, email: str, name: str | None = None):
        self.id = id
        self.email = email
        self.name = name

    @property
    def uuid_id(self) -> uuid.UUID:
        return uuid.UUID(self.id)


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
