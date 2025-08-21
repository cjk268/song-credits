from typing import Optional
from app.clients.spotify.client import SpotifyClient
from app.clients.spotify.config import SpotifyConfig

class CreditsService:
    def __init__(
        self, 
        client: Optional[SpotifyClient] = None, 
        config: Optional[SpotifyConfig] = None
    ):
        self.client: SpotifyClient = client if client is not None else SpotifyClient()
        self.config: SpotifyConfig = config if config is not None else SpotifyConfig()


    def get_credits_by_track(self, track_id: str):
        url = f"{self.config.base_credits_url.rstrip('/')}/{track_id}/credits"

        response = self.client.sync_request('GET', url)
        raise NotImplementedError