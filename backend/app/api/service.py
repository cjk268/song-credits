from sqlalchemy.orm import Session
from app.core.schemas import Track

async def get_track_by_uri(session: Session, spotify_id: str, check_cache: bool = True):
    if check_cache:
        track = session.query(Track).filter_by(spotify_id=spotify_id).first()

        if track:
            return track

    raise NotImplementedError

