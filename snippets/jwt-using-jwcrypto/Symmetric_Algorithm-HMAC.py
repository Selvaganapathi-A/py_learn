import asyncio
import os

from jwcrypto import jwk, jwt


async def main():
    #
    # * create jwk
    secret = os.urandom(64)
    #
    key = jwk.JWK(kty='oct', k=secret.hex(), kid='HMAC Based Algorithms.')
    print(secret)
    print(secret.hex())
    print(key)
    ALGORITHMS: tuple[str, ...] = (
        'HS256',
        'HS384',
        'HS512',
    )
    claims = {
        'iss': 'https://example.com/.well-known/jwks.json',
        'sub': '1234567890',
        'aud': 'John Doe',
        'iat': 157746600.0,
        'nbf': 946665000.0,
        'exp': 1765564199.999999,
        'jti': (
            '6fdddab7d670f202629531c1a51b32ca30696d0af4dd5b0f'
            'bb5f82c0aba5e505110455f37d7ef73950c2bb0495a38f56'
        ),
        'name': 'John Doe',
    }
    # ! Claims are set to expire on 2026
    # 'exp': (datetime(2025, 12, 12, 23, 59, 59, 999999).timestamp()),
    # print(timezone.localize(datetime.fromtimestamp(claims['iat'])))
    # print(timezone.localize(datetime.fromtimestamp(claims['nbf'])))
    # print(timezone.localize(datetime.fromtimestamp(claims['exp'])))
    #
    for algorithm in ALGORITHMS:
        # * sign jwt
        header = {
            'alg': algorithm,
            'typ': 'JWT',
        }
        token = jwt.JWT(
            header,
            claims=claims,
        )
        token.make_signed_token(key)
        json_token = token.serialize()
        print(json_token)
        # * verify
        received = jwt.JWT(key=key, jwt=json_token)
        print(received.claims)
        print()
    print()


if __name__ == '__main__':
    asyncio.run(main=main())
