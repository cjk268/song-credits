from app.clients.adapter_base import AdapterBase
from app.core.models import ContributorModel, CreditModel, RoleModel, TrackModel 
from typing import List

class SpotifyAdapter(AdapterBase):
    def to_normalised_playlist_tracks(self, raw_data: dict) -> List[TrackModel]:
        tracks = []
        for item in raw_data.get('tracks', {}).get('items', []):
            track_info = item.get('track', {})
            if track_info:
                tracks.append(
                    TrackModel(
                        id=track_info.get('id', ''),
                        name=track_info.get('name', '')
                    )
                )
        return tracks


    def to_normalised_track_credits(self, raw_data: dict) -> List[CreditModel]:
        credits: List[CreditModel] = []

        for role_credit in raw_data.get('roleCredits', []):
            role_title = role_credit.get('roleTitle', '')
            role_model = RoleModel(title=role_title)  

            for artist in role_credit.get('artists', []):
                uri = artist.get('uri', '')
                artist_id = uri.split(":")[-1] if uri else "" # Data comes back as "spotify:artist:some_string"
                
                contributor_model = ContributorModel(
                    id=artist_id,
                    name=artist.get('name', ''),
                    uri=uri,
                    image_uri=artist.get('imageUri', '')
                )
                credits.append(
                    CreditModel(
                        role=role_model,
                        contributor=contributor_model
                    )
                )
        return credits