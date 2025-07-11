import asyncio
from datetime import datetime


async def main():
    # * create jwk
    from authlib.jose import JWTClaims, OKPKey, jwt

    # Generate Ed25519 key
    key = OKPKey.generate_key('Ed25519', is_private=True)
    public_jwk = key.as_dict(is_private=False)

    header = {'alg': 'EdDSA'}
    payload = {
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
        'iat': datetime(
            2023,
            12,
            31,
            23,
            59,
            59,
            999999,
        ).timestamp(),
        'typ': 'JWT',
    }

    token = jwt.encode(header, payload, key)
    print('JWT:', token)

    decoded: JWTClaims = jwt.decode(token, key)
    decoded.validate()
    print(decoded)

    print('Public JWK:', public_jwk)


if __name__ == '__main__':
    asyncio.run(main=main())
