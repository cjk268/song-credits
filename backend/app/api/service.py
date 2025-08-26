from sqlalchemy.orm import Session
from app.core.schemas import Track
from app.clients.client_base import ClientBase

class MusicService:
    def __init__(self, client: ClientBase, db: Session):
        self.client = client
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

