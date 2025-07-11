import asyncio
from datetime import datetime

from authlib.jose import JsonWebKey, JWTClaims, RSAKey, jwt


async def main():
    # * create jwk
    key: RSAKey = JsonWebKey.generate_key(kty='RSA', crv_or_size=2048, is_private=True)
    public_jwk = key.as_json(is_private=False)
    print(public_jwk)
    # print(key.export(private_key=False))
    #
    # * sign jwt
    header = {'alg': 'PS512'}
    # alg must be one of PS384, PS512
    claims = {
        'sub': 'Hello',
        'iss': 'https://example.com/.well-known/public-jwks/',
        'exp': datetime(
            2025,
            12,
            31,
            23,
            59,
            59,
            999999,
        ).timestamp(),
        'typ': 'JWT',
    }
    json_token = jwt.encode(header, claims, key)
    print(json_token)
    #
    # * verify
    received: JWTClaims = jwt.decode(json_token, public_jwk)
    received.validate()
    print(received)


if __name__ == '__main__':
    asyncio.run(main=main())
