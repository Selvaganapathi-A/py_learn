import asyncio

from authlib.jose import JWTClaims, OKPKey, jwt


async def main():
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
    #
    # ! Claims are set to expire on 2026
    # * create jwk
    # Generate Ed25519 key
    key = OKPKey.generate_key('Ed25519', is_private=True)
    # public_jwk = key.as_dict(is_private=False)
    # print('Public JWK:', public_jwk)
    print('Public JWK:', key.as_json(True))
    #
    Private_PEM = key.as_pem(is_private=True, password=b'Hello World').decode()
    Public_PEM = key.as_pem(is_private=False).decode()
    print(Private_PEM, Public_PEM, sep='\n\n')
    #
    # * sign jwt
    header = {'alg': 'EdDSA', 'typ': 'JWT'}
    token = jwt.encode(header, payload=claims, key=key)
    print('JWT:', token.decode())
    #
    decoded: JWTClaims = jwt.decode(token, key)
    decoded.validate()
    print(decoded)


if __name__ == '__main__':
    asyncio.run(main=main())
