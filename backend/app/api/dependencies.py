from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from app.core.database import engine
from app.clients.spotify.client import SpotifyClient
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def get_spotify_client() -> Generator[SpotifyClient, None, None]:
    client = SpotifyClient()
    yield client

SessionDep = Annotated[Session, Depends(get_db)]
SpotifyClientDep = Annotated[SpotifyClient, Depends(get_spotify_client)]