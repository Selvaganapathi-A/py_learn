import asyncio
import os
from datetime import datetime

import jwcrypto
import jwcrypto.jwk
import jwcrypto.jwt


async def main():
    # * create jwk
    secret = os.urandom(64)
    key = jwcrypto.jwk.JWK(kty='oct', k=secret.hex(), kid='HMAC Based Algorithms.')
    print(secret)
    print(secret.hex())
    print(key)
    #
    # * sign jwt
    header = {'alg': 'HS256'}
    # alg must be one of HS256, HS384, HS512
    claims = {
        'sub': 'Hello',
        'iss': 'https://example.com/.well-known/public-jwks/',
        'exp': datetime(2025, 12, 31, 23, 59, 59, 999999).timestamp(),
        'typ': 'JWT',
    }
    token = jwcrypto.jwt.JWT(
        header,
        claims=claims,
    )
    token.make_signed_token(key)
    json_token = token.serialize()
    print(json_token)
    #
    # * verify
    received = jwcrypto.jwt.JWT(key=key, jwt=json_token)
    print(received.claims)


if __name__ == '__main__':
    asyncio.run(main=main())
