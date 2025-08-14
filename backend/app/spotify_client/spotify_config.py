import os
from dataclasses import dataclass

@dataclass(frozen=True)
class SpotifyConfig:

    open_spotify_url: str = os.environ.get(
        "SPOTIFY_BASE_URL",
        "https://open.spotify.com/
    )

    auth_token_url: str = os.environ.get(
        "SPOTIFY_AUTH_TOKEN_URL",
        "https://open.spotify.com/api/token"
    )

    client_token_url: str = os.environ.get(
        "SPOTIFY_CLIENT_TOKEN_URL",
        "https://clienttoken.spotify.com/v1/clienttoken"
    )

    js_sdk_data: Dict[str, str] = {
        "device_brand": "unknown",
        "device_model": "unknown",
        "os": "unknown",
        "os_version": "unknown",
        "device_id": "unknown",
        "device_type": "unknown"
    }
