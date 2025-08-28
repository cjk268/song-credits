from sqlalchemy.orm import Session
from app.core.schemas import Track
from app.clients.client_base import ClientBase
from app.clients.adapter_base import AdapterBase
from app.core.models import TrackModel 
from typing import List

class MusicService:
    def __init__(self, client: ClientBase, adapter: AdapterBase, db: Session):
        self.client = client
        self.adapter = adapter
        self.db = db
        
    async def get_auth_token(self):
        return await self.client.get_auth_token()
    
    
    async def get_client_token(self):
        return await self.client.get_client_token()


    def get_track_by_id(self, uri: str, check_cache: bool = True):
        if check_cache:
            track = self.db.query(Track).filter_by(spotify_id=uri).first()

            if track:
                return track

        raise NotImplementedError
    
    async def get_credits_by_track_id(self, track_id: str): 
        return await self.client.get_credits_by_track_id(track_id)
    
    async def get_playlist(self, playlist_id: str): 
        return await self.client.get_playlist_tracks(playlist_id)
    
    async def get_credits_by_playlist_id(self, playlist_id: str):
        response_json = await self.client.get_playlist_tracks(playlist_id)
        tracks: List[TrackModel] = self.adapter.to_normalised_playlist_tracks(response_json)
        track_ids = [track.id for track in tracks]
        return await self.client.get_credits_by_track_ids(track_ids)
