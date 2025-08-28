from fastapi import FastAPI

from app.api.main import api_router
from app.api.dependencies import spotify_client

app = FastAPI()

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    await spotify_client.get_auth_token()
