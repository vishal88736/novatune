from uuid import UUID

from fastapi import APIRouter, File, Form, UploadFile

from app.api.v1.deps import CurrentUserDep, DbDep
from app.core.exceptions import NotFoundError
from app.db.models.playlist import Playlist
from app.schemas.playlist import PlaylistStatusOut
from app.services.playlist_ingestion_service import playlist_ingestion_service
from sqlalchemy import select

router = APIRouter()


@router.post("/upload", response_model=PlaylistStatusOut)
async def upload_playlist(
    current_user: CurrentUserDep,
    db: DbDep,
    file: UploadFile = File(...),
    source: str = Form(default="upload_csv"),
) -> Playlist:
    raw = await file.read()
    playlist = await playlist_ingestion_service.ingest_csv(db, current_user.id, raw)
    return playlist


@router.get("", response_model=list[PlaylistStatusOut])
async def list_playlists(current_user: CurrentUserDep, db: DbDep) -> list[Playlist]:
    result = await db.execute(select(Playlist).where(Playlist.user_id == current_user.id))
    return list(result.scalars().all())


@router.get("/{playlist_id}", response_model=PlaylistStatusOut)
async def get_playlist(playlist_id: UUID, current_user: CurrentUserDep, db: DbDep) -> Playlist:
    result = await db.execute(select(Playlist).where(Playlist.id == playlist_id))
    playlist = result.scalar_one_or_none()
    if not playlist:
        raise NotFoundError("Playlist not found.")
    return playlist


@router.delete("/{playlist_id}", status_code=204)
async def delete_playlist(playlist_id: UUID, current_user: CurrentUserDep, db: DbDep) -> None:
    result = await db.execute(select(Playlist).where(Playlist.id == playlist_id))
    playlist = result.scalar_one_or_none()
    if not playlist:
        raise NotFoundError("Playlist not found.")
    await db.delete(playlist)
    await db.commit()
