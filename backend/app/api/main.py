from fastapi import APIRouter

from app.api.routers import credits_network, utils

api_router = APIRouter()
api_router.include_router(credits_network.router)
api_router.include_router(utils.router)
