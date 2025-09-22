import asyncio

from authlib.jose import JsonWebKey, JWTClaims, RSAKey, jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


async def main():
    ALGORITHMS: tuple[str, ...] = (
        'RS256',
        'RS384',
        'RS512',
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
    #
    # ! Claims are set to expire on 2026
    #
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
    #
    # Import into Authlib
    key: RSAKey = JsonWebKey.import_key(private_pem, {'alg': 'RS256'})  # type: ignore
    public_jwk = key.as_json(is_private=False)
    print(public_jwk)
    #
    for algorithm in ALGORITHMS:
        #
        # * sign jwt
        header = {'alg': algorithm, 'typ': 'JWT'}
        # alg must be one of RS256, RS384, RS512
        json_token = jwt.encode(header, payload=claims, key=key)
        print(json_token.decode())
        #
        # * verify
        received: JWTClaims = jwt.decode(json_token, public_key)
        received.validate()
        print(received)


if __name__ == '__main__':
    asyncio.run(main=main())
