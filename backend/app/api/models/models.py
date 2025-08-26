from pydantic import BaseModel

class PlaylistCredits(BaseModel):
    playlist_uris: List[str]

class TrackCredits(BaseModel):
    track_uri: str

class TrackCreditsResponse(BaseModel):
    pass
