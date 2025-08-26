from fastapi import APIRouter
from app.api.dependencies import ServiceDep

router = APIRouter(prefix="/utils", tags=["utils"])

@router.get("/health")
async def health() -> bool:
    return True

@router.get("/authtoken")
async def auth_token(service: ServiceDep) -> str: 
    return await service.get_auth_token()

@router.get("/clienttoken")
async def client_token(service: ServiceDep) -> str: 
    return await service.get_client_token()
