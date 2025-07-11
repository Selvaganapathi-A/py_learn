import asyncio
from datetime import datetime

from authlib.jose import JsonWebKey, JWTClaims, RSAKey, jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


async def main():
    alg = 'RS512'
    # alg must be one of RS256, RS384, RS512
    # * create jwk
    private_key: rsa.RSAPrivateKey = rsa.generate_private_key(65537, 2048)
    public_key: rsa.RSAPublicKey = private_key.public_key()
    #
    private_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.PKCS1,
    )
    print(private_pem.decode(), public_pem.decode(), sep='\n\n\n', end='\n\n')
    print()
    #
    # Import into Authlib
    key: RSAKey = JsonWebKey.import_key(private_pem, {'alg': 'RS256'})  # type: ignore
    public_jwk = key.as_json(is_private=False)
    print(public_jwk)
    #
    #
    # * sign jwt
    header = {'alg': alg}
    claims = {
        'sub': 'Hello',
        'iss': 'https://example.com/.well-known/public-jwks/',
        'iat': datetime.now().timestamp(),
        'exp': datetime(2025, 12, 31, 23, 59, 59, 999999).timestamp(),
        'typ': 'JWT',
    }
    json_token = jwt.encode(header, payload=claims, key=key)
    print(json_token.decode())
    print()
    #
    #
    await asyncio.sleep(1)
    # * verify
    received: JWTClaims = jwt.decode(json_token, public_key)
    received.validate()
    print(received)


if __name__ == '__main__':
    asyncio.run(main=main())
