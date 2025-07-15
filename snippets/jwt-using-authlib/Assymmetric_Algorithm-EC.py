import asyncio


from authlib.jose import ECKey, JWTClaims, jwt
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey


async def main():
    ALGORITHMS: tuple[str, ...] = (
        'ES256',
        'ES256K',
        'ES384',
        'ES512',
    )
    CURVE: dict[str, str] = {
        'ES256': 'P-256',
        'ES256K': 'secp256k1',
        'ES384': 'P-384',
        'ES512': 'P-521',
    }
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
    #
    # ! Claims are set to expire on 2026
    #
    for algorithm in ALGORITHMS:
        # * create jwk
        key: ECKey = ECKey.generate_key(
            CURVE[algorithm],
            is_private=True,
        )
        public_key: EllipticCurvePublicKey = key.as_key(False)
        print(public_key.public_numbers())
        #
        Private_PEM = key.as_pem(is_private=True, password=b'Hello World').decode()
        Public_PEM = key.as_pem(is_private=False).decode()
        print(Private_PEM, Public_PEM, sep='\n\n')
        #
        # ! generate new key for eackh application
        public_jwk = key.as_json(is_private=False)
        print('Private JWK:', key.as_json(True))
        print(' Public JWK:', public_jwk)
        print()
        #
        # * sign jwt
        header = {'alg': algorithm, 'typ': 'JWT'}
        print(header)
        # alg must be one of ES256, ES256K, ES384, ES512
        json_token = jwt.encode(header, payload=claims, key=key)
        print(json_token.decode())
        print()
        #
        # * verify
        received: JWTClaims = jwt.decode(json_token, public_key)
        received.validate()
        print(received)
        print()
        #


if __name__ == '__main__':
    asyncio.run(main=main())
