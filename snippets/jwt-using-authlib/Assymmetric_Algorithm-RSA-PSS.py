import asyncio

from authlib.jose import JsonWebKey, JWTClaims, RSAKey, jwt


async def main():
    ALGORITHMS: tuple[str, ...] = (
        'PS384',
        'PS512',
    )
    claims = {
        'iss': 'https://example.com/.well-known/jwks.json',
        'sub': '1234567890',
        'aud': 'John Doe',
        'iat': 157746600.0,
        'nbf': 946665000.0,
        'exp': 1765564199.999999,
        'jti': (
            '6fdddab7d670f202629531c1a51b32ca30696d0af4dd5b0fbb5f82c0aba5e505110455f37d7ef73950c2bb0495a38f56'
        ),
        'name': 'John Doe',
    }
    # ! Claims are set to expire on 2026
    # * create jwk
    key: RSAKey = JsonWebKey.generate_key(
        kty='RSA', crv_or_size=2048, is_private=True
    )
    public_jwk = key.as_json(is_private=False)
    print(public_jwk)
    Private_PEM = key.as_pem(is_private=True, password=b'Hello World').decode()
    Public_PEM = key.as_pem(is_private=False).decode()
    print(Private_PEM, Public_PEM, sep='\n\n')
    # print(key.export(private_key=False))
    for algorithm in ALGORITHMS:
        # * sign jwt
        header = {'alg': algorithm, 'typ': 'JWT'}
        # alg must be one of PS384, PS512
        json_token = jwt.encode(header, payload=claims, key=key)
        print(json_token.decode())
        # * verify
        received: JWTClaims = jwt.decode(json_token, public_jwk)
        received.validate()
        print(received)


if __name__ == '__main__':
    asyncio.run(main=main())
