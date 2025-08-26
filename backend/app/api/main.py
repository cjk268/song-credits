from fastapi import APIRouter

from app.api.routers import credits, playlists, utils

api_router = APIRouter()
api_router.include_router(credits.router)
api_router.include_router(playlists.router)
api_router.include_router(utils.router)
