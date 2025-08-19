import os
import time
import requests
import asyncio
from app.spotify_client.spotify_config import SpotifyConfig
from typing import Optional, Dict
from playwright.async_api import async_playwright

class SpotifyClient:

    def __init__(self, config=None, requests_timeout=5, proxies=None) -> None:
        self.config = config or SpotifyConfig()
        self.requests_timeout=requests_timeout
        self.proxies= proxies
        self.session = requests.Session()

        self.client_id: str | None = None
        self.client_token: str | None = None
        self.client_token_expiration_timestamp: int | None = None           # Unix in seconds
        self.access_token: str | None = None
        self.access_token_expiration_timestamp: int | None = None           # Unix in seconds
        self.client_version = os.environ.get("SPOTIFY_CLIENT_VERSION")      # To-do: Get this via Spotify


    def get_track_credits(self):
        raise NotImplementedError

    def _make_request(
            self, 
            method: str, 
            url: str, 
            payload = None, 
            headers: Optional[Dict[str, str]] = None,
            **kwargs
        ) -> requests.Response:

        default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        merged_headers = default_headers | (headers or {})

        try:
            response = self.session.request(
                method, 
                url, 
                headers=merged_headers, 
                proxies=self.proxies,
                json=payload,
                timeout=self.requests_timeout, 
                **kwargs
            )
            
            response.raise_for_status()

        except requests.exceptions.HTTPError as http_error:
            try:
                json_response = http_error.response.json()
                print(json_response)
            except ValueError:
                print(http_error.response.text)
            raise 

        return response


    def _make_auth_request(
            self, 
            method: str, 
            url: str, 
            payload = None, 
            headers: Optional[Dict[str, str]] = None
        ) -> requests.Response:

        if self._is_auth_token_expired():
            asyncio.run(self._get_auth_token())

        if self._is_client_token_expired():
            self.get_client_token()

        default_headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        merged_headers = default_headers | (headers or {})

        return self._make_request(
            method,
            url,
            payload=payload,
            headers=merged_headers,
            **kwargs
        )


    def get_client_token(self):
        payload = {
            "client_data": {
                "client_version": self.client_version,
                "client_id": self.client_id,
                "js_sdk_data": self.config.js_sdk_data
            }
        }

        response = self._make_request(
            "POST",
            self.config.client_token_url,
            payload=payload,
        )

        data = response.json()

        granted_token = data.get("granted_token", {})
        self.client_token = granted_token.get("token")
        self.client_expiration_in_seconds = granted_token.get("expires_after_seconds")

        return self.client_token


    async def get_auth_token(self):
        if self._is_auth_token_expired():
            return await self._get_auth_token()
        
        return self.auth_token


    async def _get_auth_token(self):
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
            print(self.client_id)
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
            self.client_token_expiration_unix
        )


    def _is_token_expired_seconds(
        self, 
        token: str|None, 
        expiration_timestamp: int|None,
        ) -> bool:
        
        if not (token and expiration_timestamp):
            return True
        
        current_timestamp = int(time.time())
        return current_timestamp > expiration_timestamp