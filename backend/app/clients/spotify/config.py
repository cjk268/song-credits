import os
from dataclasses import dataclass, field
from typing import Dict

def get_env_url(var_name: str, default: str) -> str:
    value = os.environ.get(var_name, default)
    if not value:
        raise ValueError(f"{var_name} must not be empty")
    return value.rstrip("/")

@dataclass(frozen=True)
class SpotifyConfig:
    open_spotify_url: str = field(default_factory=lambda: get_env_url(
        "SPOTIFY_BASE_URL", "https://open.spotify.com/"
    ))
    
    auth_token_url: str = field(default_factory=lambda: get_env_url(
        "SPOTIFY_AUTH_TOKEN_URL", "https://open.spotify.com/api/token"
    ))
    
    client_token_url: str = field(default_factory=lambda: get_env_url(
        "SPOTIFY_CLIENT_TOKEN_URL", "https://clienttoken.spotify.com/v1/clienttoken"
    ))
    
    credits_base_url: str = field(default_factory=lambda: get_env_url(
        "SPOTIFY_CREDITS_URL", "https://spclient.wg.spotify.com/track-credits-view/v0/experimental/"
    ))
    
    api_base_url: str = field(default_factory=lambda: get_env_url(
        "SPOTIFY_DEV_BASE_URL", "https://api.spotify.com/v1"
    ))

    client_version: str = field(default_factory=lambda: os.environ.get(
        "SPOTIFY_CLIENT_VERSION", "1.2.71.297.gcbeaa555"
    ))

    js_sdk_data: Dict[str, str] = field(default_factory=lambda: {
        "device_brand": "unknown",
        "device_model": "unknown",
        "os": "unknown",
        "os_version": "unknown",
        "device_id": "unknown",
        "device_type": "unknown",
    })
