import asyncio
from datetime import datetime

from authlib.jose import ECKey, JWTClaims, jwt
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey


async def main():
    alg = 'ES256'
    curve = {
        'ES256': 'P-256',
        'ES256K': 'secp256k1',
        'ES384': 'P-384',
        'ES512': 'P-521',
    }
    # * create jwk
    key: ECKey = ECKey.generate_key(
        curve[alg],
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
    print('Public JWK:', public_jwk)
    print()
    #
    # * sign jwt
    header = {'alg': alg}
    # alg must be one of ES256, ES256K, ES384, ES512
    claims = {
        'sub': 'Hello',
        'iss': 'https://example.com/.well-known/public-jwks/',
        'iat': datetime.now().timestamp(),
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
    json_token = jwt.encode(header, payload=claims, key=key)
    print(json_token.decode())
    print()
    await asyncio.sleep(1)
    #
    # * verify
    received: JWTClaims = jwt.decode(json_token, public_key)
    received.validate()
    print(received)
    #


if __name__ == '__main__':
    asyncio.run(main=main())
