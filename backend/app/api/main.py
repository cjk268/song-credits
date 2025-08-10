from fastapi import APIRouter

from app.api.routers import credits, utils

api_router = APIRouter()
api_router.include_router(credits.router)
api_router.include_router(utils.router)
