# Song Credits 

## Dev Notes
Run `uv lock` to generate a new `uv.lock` file.

`source .venv/bin/activate`

`alembic revision --autogenerate -m "create ..."`
`alembic upgrade head` to migrate.

In container, `python /app/app/core/seed_data.py` to seed dev data.


## Reverse engineering
curl 'https://spclient.wg.spotify.com/track-credits-view/v0/experimental/2TxCwUlqaOH3TIyJqGgR91/credits' \
  --compressed \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0' \
  -H 'Accept: application/json' \
  -H 'Accept-Language: en-GB' \
  -H 'Accept-Encoding: gzip, deflate, br, zstd' \
  -H 'Referer: https://open.spotify.com/' \
  -H 'app-platform: WebPlayer' \
  -H 'spotify-app-version: 1.2.71.29.g888c49af' \
  -H 'client-token: AAC8m/lTDyX6qvEO9GMSYlqjTP8J5d2e/54JF9s0xkeSza3dSl7DEneDRZMd54dYVySaJgpDT2oxEIsibphqpzkYhgafnnIjJLiHCDdUW/FCEVoHzxy8i48zwNterhssCfB2Px+eY9YZwEeO4RIQH2ZMk3qlDl0tcWhiR7dyvl1cm/PHvxTZUTRP2c1+yddXcqOo0xLee0HD1Ba6uermOZ7WncVPG9FGg1ollfJ3ysYe7UnvIBXoKSlH1Gbjm5TCwTLayqM6xe89TYOaI2H8qdGZr7y4jZQrvTbq/s5xGGZ7' \
  -H 'Origin: https://open.spotify.com' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'authorization: Bearer BQCRfTCmPsDTV7FpzbnyyFAsUNQEtztlqjYc9_FaBwyjMFtyi9WsJqidjqDCh9oyfKXyEv5QPOj0Sc33YSdUgMEhUd5XsOhr8wnFxthz8CDpiWQ8ZroQuKNEF8RYs_OhCE8rC9DFKCQ' \
  -H 'Connection: keep-alive'


curl 'https://open.spotify.com/api/token?reason=init^&productType=web-player^&totp=458278^&totpServer=458278^&totpVer=26' \
  --compressed \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-GB,en;q=0.5' \
  -H 'Accept-Encoding: gzip, deflate, br, zstd' \
  -H 'Referer: https://open.spotify.com/' \
  -H 'sentry-trace: e1eac6d1f1a545cfbb267ec158c8790a-abb8aa3d6ee6b3e7-0' \
  -H 'baggage: sentry-environment=production,sentry-release=web-player_2025-08-09_1754732015557_888c49a,sentry-public_key=de32132fc06e4b28965ecf25332c3a25,sentry-trace_id=e1eac6d1f1a545cfbb267ec158c8790a,sentry-sample_rate=0.008,sentry-sampled=false' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Connection: keep-alive' \
  -H 'Cookie: sp_t=3793b6ec7cd68c71fbcb9b6cc807f76a; sp_landing=https%3A%2F%2Fopen.spotify.com%2F%3Fsp_cid%3D3793b6ec7cd68c71fbcb9b6cc807f76a%26device%3Ddesktop' \
  -H 'Priority: u=4' \
  -H 'TE: trailers'

curl 'https://clienttoken.spotify.com/v1/clienttoken' \
  --compressed \
  -X POST \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0' \
  -H 'Accept: application/json' \
  -H 'Accept-Language: en-GB,en;q=0.5' \
  -H 'Accept-Encoding: gzip, deflate, br, zstd' \
  -H 'Content-Type: application/json' \
  -H 'Referer: https://open.spotify.com/' \
  -H 'Origin: https://open.spotify.com' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'Connection: keep-alive' \
  -H 'Priority: u=4' \
  -H 'TE: trailers' \
  --data-raw '{"client_data":{"client_version":"1.2.71.29.g888c49af","client_id":"d8a5ed958d274c2e8ee717e6a4b0971d","js_sdk_data":{"device_brand":"unknown","device_model":"unknown","os":"linux","os_version":"unknown","device_id":"3793b6ec7cd68c71fbcb9b6cc807f76a","device_type":"computer"}}}'


OPTIONS /v1/clienttoken HTTP/2
Host: clienttoken.spotify.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br, zstd
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type
Referer: https://open.spotify.com/
Origin: https://open.spotify.com
Connection: keep-alive
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
Priority: u=4


https://github.com/Thereallo1026/spotify-secrets?tab=readme-ov-file
https://github.com/Aran404/SpotAPI/blob/main/spotapi/client.py
