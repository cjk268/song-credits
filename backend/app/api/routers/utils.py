from fastapi import APIRouter
from app.api.dependencies import SpotifyClientDep

router = APIRouter(prefix="/utils", tags=["utils"])

@router.get("/health")
async def health() -> bool:
    return True

@router.get("/authtoken")
async def auth_token(spotify_client: SpotifyClientDep) -> str: 
    return await spotify_client.get_auth_token()

@router.get("/clienttoken")
async def client_token(spotify_client: SpotifyClientDep) -> str: 
    return spotify_client.get_client_token()
