from fastapi import APIRouter, Query

from app.api.dependencies import SessionDep
from app.api.service import get_track_by_uri
from typing_extensions import Annotated

router = APIRouter(prefix="/credits", tags=["credits"])

@router.get("/track/{spotify_id}")
async def get_track_credits_by_uri(
    session: SessionDep, 
    spotify_id: str,
    check_cache: Annotated[bool, Query(description="Check DB before fetching from Spotify")] = True
):
    return await get_track_by_uri(session, spotify_id, check_cache)
