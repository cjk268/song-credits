from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from app.core.database import engine
from app.api.service import MusicService
from app.clients.spotify.client import SpotifyClient
from app.clients.spotify.adapter import SpotifyAdapter
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_service(session: Session = Depends(get_db)) -> Generator[MusicService, None, None]:
    spotify_client = SpotifyClient()
    spotify_adapter = SpotifyAdapter()
    yield MusicService(spotify_client, spotify_adapter, session)


SessionDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[MusicService, Depends(get_service)]