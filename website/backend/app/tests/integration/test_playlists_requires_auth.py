import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_playlists_requires_auth(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/playlists")
    assert resp.status_code == 401
