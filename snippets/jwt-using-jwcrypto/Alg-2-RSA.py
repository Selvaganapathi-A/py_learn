import asyncio
from datetime import datetime

import jwcrypto
import jwcrypto.jwk
import jwcrypto.jwt


async def main():
    # * create jwk
    key = jwcrypto.jwk.JWK.generate(
        kty='RSA',
        kid='RSA Based Algorithms.',
        size=2048,
    )
    public_key = jwcrypto.jwk.JWK.from_json(key.export(private_key=False))
    print(public_key)
    print(key.export(private_key=False))
    #
    # * sign jwt
    header = {'alg': 'RS512'}
    # alg must be one of RS256, RS384, RS512
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
    received = jwcrypto.jwt.JWT(key=public_key, jwt=json_token)
    print(received.claims)


if __name__ == '__main__':
    asyncio.run(main=main())
