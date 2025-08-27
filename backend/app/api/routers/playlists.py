from fastapi import APIRouter, Query

from app.api.dependencies import ServiceDep
from typing_extensions import Annotated

router = APIRouter(prefix="/playlist", tags=["playlist"])

@router.get("/{playlist_id}")
async def get_playlist(
        service: ServiceDep,
        playlist_id: str
    ):
    return await service.get_playlist(playlist_id)
