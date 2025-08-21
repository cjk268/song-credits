import os
import time
import asyncio
import httpx
from app.clients.spotify.config import SpotifyConfig
from typing import Optional, Dict, Union
from playwright.sync_api import sync_playwright

class SpotifyClient:

    def __init__(
            self, 
            config: Optional[SpotifyConfig] = None, 
            requests_timeout: Union[int, float] = 5, 
            proxy: Optional[str] = None
        ) -> None:
        self.config = config if config is not None else SpotifyConfig()
        self.sync_client: httpx.Client = httpx.Client(timeout=requests_timeout, proxy=proxy)
        self.async_client: httpx.AsyncClient = httpx.AsyncClient(timeout=requests_timeout, proxy=proxy)

        self.client_id: Optional[str] = None
        self.client_token: Optional[str] = None
        self.client_token_expiration_timestamp: Optional[int] = None           # Unix in seconds
        self.access_token: Optional[str] = None
        self.access_token_expiration_timestamp: Optional[int] = None           # Unix in seconds
        self.client_version: Optional[str] = os.environ.get("SPOTIFY_CLIENT_VERSION")      # To-do: Get this via Spotify


    def _prepare_headers(self, headers: Optional[Dict[str, str]] = None, auth: bool = True) -> Dict[str, str]:
        default_headers = {"Accept": "application/json", "Content-Type": "application/json"}
        merged_headers = default_headers | (headers or {})

        if auth:
            merged_headers["Authorization"] = f"Bearer {self.get_auth_token()}"
            merged_headers["client-token"] = self.get_client_token()
        return merged_headers
    

    def sync_request(
            self, 
            method: str, 
            url: str, 
            payload = None, 
            headers: Optional[Dict[str, str]] = None,
            auth: bool = True,
            **kwargs
        ) -> httpx.Response:

        try:
            response = self.sync_client.request(
                method, 
                url, 
                headers=self._prepare_headers(headers=headers, auth=auth), 
                json=payload,
                **kwargs
            )
            
            response.raise_for_status()

        except httpx.HTTPError as http_error:
            try:
                json_response = http_error.response.json()
                print(json_response)
            except ValueError:
                print(http_error.response.text)
            raise 

        return response


    def get_client_token(self):
        if self.client_token is None:
            self.get_auth_token() # Assigns client id

        payload = {
            "client_data": {
                "client_version": self.client_version,
                "client_id": self.client_id,
                "js_sdk_data": self.config.js_sdk_data
            }
        }

        response = self.sync_request(
            "POST",
            self.config.client_token_url,
            payload=payload,
            auth=False
        )

        data = response.json()

        granted_token = data.get("granted_token", {})
        self.client_token = granted_token.get("token")
        self.client_token_expiration_timestamp = granted_token.get("expires_after_seconds")

        return self.client_token


    def get_auth_token(self):
        if not self._is_auth_token_expired():
            return self.access_token

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            with page.expect_response(lambda r: self.config.auth_token_url in r.url) as response_info:
                page.goto(self.config.open_spotify_url)

            response = response_info.value
            data = response.json()
            
            browser.close()
            if "accessToken" not in data:
                raise RuntimeError("accessToken not found in Spotify API response.")

            self.client_id = data.get("clientId")
            self.access_token = data.get("accessToken")
            self.access_token_expiration_timestamp = (data.get("accessTokenExpirationTimestampMs") / 1000)
            
            return self.access_token


    def _is_auth_token_expired(self) -> bool:
        return self._is_token_expired_seconds(
            self.access_token,
            self.access_token_expiration_timestamp
        )


    def _is_client_token_expired(self) -> bool:
        return self._is_token_expired_seconds(
            self.client_token,
            self.client_token_expiration_timestamp
        )


    def _is_token_expired_seconds(
        self, 
        token: str|None, 
        expiration_timestamp: int|None,
        ) -> bool:
        
        if not (token and expiration_timestamp):
            return True
        
        current_timestamp = int(time.time())
        return current_timestamp >= expiration_timestamp
