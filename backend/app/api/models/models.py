from pydantic import BaseModel

class PlaylistCreditsRequest(BaseModel):
    playlist_uris: List[str]

class TrackCreditsRequest(BaseModel):
    track_uri: str

class TrackCreditsResponse(BaseModel):
    pass
