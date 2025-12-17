import asyncio

from jwcrypto import jwk, jwt


async def main():
    # * create jwk
    key = jwk.JWK.generate(
        kty='RSA',
        kid='RSA-PSS Based Algorithms.',
        size=2048,
    )
    # public_key = jwk.JWK.from_json(key.export(private_key=False))
    public_key = key.public()
    print(public_key)
    print(key.export(private_key=False))
    print(key.export_to_pem(private_key=True, password=b'Google').decode())
    print(key.export_to_pem(private_key=False).decode())
    #
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
        'jti': ('6fdddab7d670f202629531c1a51b32ca30696d0af4dd5b0fbb5f82c0aba5e505110455f37d7ef73950c2bb0495a38f56'),
        'name': 'John Doe',
    }
    for algorithm in ALGORITHMS:
        # * sign jwt
        header = {'alg': algorithm}
        # alg must be one of PS384, PS512
        token = jwt.JWT(
            header,
            claims=claims,
        )
        token.make_signed_token(key)
        json_token = token.serialize()
        print(json_token)
        #
        # * verify
        received = jwt.JWT(key=public_key, jwt=json_token)
        print(received.claims)


if __name__ == '__main__':
    asyncio.run(main=main())
