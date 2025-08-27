import time
import asyncio
import httpx
from app.core.logging import logger
from app.clients.spotify.config import SpotifyConfig
from app.clients.client_base import ClientBase
from typing import Optional, Dict, Union
from playwright.async_api import async_playwright


class SpotifyClient(ClientBase):

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


    async def _prepare_headers(self, headers: Optional[Dict[str, str]] = None, auth: bool = True) -> Dict[str, str]:
        default_headers = {"Accept": "application/json", "Content-Type": "application/json"}
        merged_headers = default_headers | (headers or {})

        if auth:
            merged_headers["Authorization"] = f"Bearer {await self.get_auth_token()}"
            merged_headers["client-token"] = await self.get_client_token()
        return merged_headers
    
    
    def _handle_http_error(self, error: httpx.HTTPError) -> None:
        try:
            json_response = error.response.json()
            logger.warning(json_response)
        except ValueError:
            logger.warning(error.response.text)
        raise error
    

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
            self._handle_http_error(http_error)

        return response

    
    async def async_request(
            self, 
            method: str, 
            url: str, 
            payload = None, 
            headers: Optional[Dict[str, str]] = None,
            auth: bool = True,
            **kwargs
        ) -> httpx.Response:
        try:
            headers = await self._prepare_headers(headers=headers, auth=auth)
            
            response = await self.async_client.request(
                method, 
                url, 
                headers=headers, 
                json=payload,
                **kwargs
            )
            
            response.raise_for_status()

        except httpx.HTTPError as http_error:
            self._handle_http_error(http_error)

        return response


    async def _batch_request(
            self, 
            method: str, 
            urls: list[str],
            payload = None, 
            headers: Optional[Dict[str, str]] = None,
            auth: bool = True,
            **kwargs
        ):

        async def req(url):
            response = await self.async_request(method, url, payload, headers, auth, **kwargs)
            return response.json()
        
        tasks = [req(url) for url in urls]
        return await asyncio.gather(*tasks)


    async def get_client_token(self):
        if self.client_token is None:
            await self.get_auth_token() # Assigns client id

        payload = {
            "client_data": {
                "client_version": self.config.client_version,
                "client_id": self.client_id,
                "js_sdk_data": self.config.js_sdk_data
            }
        }

        response = await self.async_request(
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


    async def get_auth_token(self):
        """Opens spotify in a browser, waits for the auth token request and stores/returns the token"""
        if not self._is_auth_token_expired():
            return self.access_token

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            async with page.expect_response(lambda r: self.config.auth_token_url in r.url) as response_info:
                await page.goto(self.config.open_spotify_url)

            response = await response_info.value
            data = await response.json()
            
            await browser.close()
            if "accessToken" not in data:
                raise RuntimeError("accessToken not found in Spotify API response.")

            self.client_id = data.get("clientId")
            self.access_token = data.get("accessToken")
            self.access_token_expiration_timestamp = (data.get("accessTokenExpirationTimestampMs") / 1000)
            
            logger.info(
                "New auth token fetched: access_token=%s, expires_at=%s",
                self.access_token,
                time.gmtime(int(self.access_token_expiration_timestamp)) # UTC format
            )
            
            return self.access_token


    async def get_credits_by_track_id(self, track_id: str):
        url = f"{self.config.credits_base_url}/{track_id}/credits"
        response = await self.async_request('GET', url)
        return response.json()
    
    
    async def get_playlist_tracks(self, playlist_id: str): 
        logger.info("Test")
        url = f"{self.config.api_base_url}/playlists/{playlist_id}"
        response = await self.async_request('GET', url)
        return response.json()

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
