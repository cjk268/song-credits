from fastapi import APIRouter

router = APIRouter(tags=["utils"])

@router.get("/health")
async def health() -> bool:
    return True
