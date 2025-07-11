import asyncio
import os
from datetime import datetime
from typing import NotRequired, TypedDict

from authlib.jose import ECKey, JsonWebKey, JWTClaims, OctKey, OKPKey, RSAKey, jwt


class Claims(TypedDict):
    sub: NotRequired[str | None]
    typ: NotRequired[str | None]
    aud: NotRequired[str | None]
    jti: NotRequired[str | None]
    iss: NotRequired[str | None]
    iat: NotRequired[float | None]
    nbf: NotRequired[float | None]
    exp: NotRequired[float | None]


def create_token(
    header: dict[str, str], payload: Claims, key: ECKey | OctKey | OKPKey | RSAKey
) -> str:
    token = jwt.encode(header, payload=payload, key=key)
    raise token


async def alt_main():
    # * create jwk
    # key: OctKey = OctKey.generate_key(32, {'kid': 'halwa'})
    # * Generate New Key on Each run
    # key: OctKey = OctKey.generate_key(256, {'kid': 'mohammad'})
    # * Reuse Existing Key
    key: OctKey = OctKey.import_key(
        {
            'kty': 'oct',
            'k': 'o1X8HwkSSCiJQfWsto5IjkH8ZvTs9alZjHXcMbPQbO4',
            'kid': 'mohammad',
        }
    )
    print('Import this on App Starts', key.as_json())
    print('Secret', key.as_dict().get('k'))
    print()
    #
    # * sign jwt
    header = {'alg': 'HS256'}
    # alg must be one of HS256, HS384, HS512
    claims: Claims = {
        'sub': 'Hello',
        'iss': 'https://example.com/.well-known/public-jwks/',
        'iat': datetime.now().timestamp(),
        'exp': datetime(2025, 12, 31, 23, 59, 59, 999999).timestamp(),
        'typ': 'JWT',
    }
    json_token = jwt.encode(header, payload=claims, key=key)
    print(json_token.decode())
    print()
    #
    await asyncio.sleep(1.15)
    # * verify
    received: JWTClaims = jwt.decode(json_token, key=key)
    received.validate()
    print(received)
    print()


async def main():
    # * create jwk
    # key: OctKey = OctKey.generate_key(32, {'kid': 'halwa'})
    key: OctKey = OctKey.generate_key(128, {'kid': 'mohammad'})
    print(key.as_json())
    print()
    #
    shared_key = os.urandom(64)
    # * sign jwt
    header = {'alg': 'HS256'}
    # alg must be one of HS256, HS384, HS512
    claims = {
        'sub': 'Hello',
        'iss': 'https://example.com/.well-known/public-jwks/',
        'iat': datetime.now().timestamp(),
        'exp': datetime(2025, 12, 31, 23, 59, 59, 999999).timestamp(),
        'typ': 'JWT',
    }
    json_token = jwt.encode(header, payload=claims, key=shared_key)
    print(json_token.decode())
    print()
    #
    await asyncio.sleep(1.15)
    # * verify
    received: JWTClaims = jwt.decode(json_token, key=shared_key)
    received.validate()
    print(received)
    print()
    # * extract key for jwt Verification
    # ! generate new key for eackh application
    key: OctKey = JsonWebKey.import_key(
        shared_key,  # type: ignore
        {
            'kty': 'oct',
            # 'k': shared_key,
        },
    )
    # print(key.as_json())
    print(key.as_json(is_private=False))
    print()
    print(key.as_json(is_private=True))
    print()
    #


if __name__ == '__main__':
    asyncio.run(main=alt_main())
