from fastapi import APIRouter, HTTPException, Query

from app.api.dependencies import ServiceDep
from typing_extensions import Annotated

router = APIRouter(prefix="/credits", tags=["credits"])

@router.get("/track/{track_id}")
async def get_track_credits_by_track_id(
    service: ServiceDep, 
    track_id: str,
    check_cache: Annotated[bool, Query(description="Check DB before fetching from the music service")] = True
):
    result = await service.get_credits_by_track_id(track_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Track with id '{track_id}' not found")
    return result
