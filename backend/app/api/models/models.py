from pydantic import BaseModel

class PlaylistRequest(BaseModel):
    playlist_uris: List[str]