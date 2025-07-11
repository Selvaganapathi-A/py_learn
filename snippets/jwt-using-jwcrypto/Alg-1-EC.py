import asyncio
from datetime import datetime

import jwcrypto
import jwcrypto.jwk
import jwcrypto.jwt


async def main():
    curve = {
        'ES256': 'P-256',
        'ES256K': 'secp256k1',
        'ES384': 'P-384',
        'ES512': 'P-521',
    }
    #
    alg_choosen = 'ES256'
    # * create jwk
    # * Read Public Key from file
    key = jwcrypto.jwk.JWK.from_pem(
        """-----BEGIN ENCRYPTED PRIVATE KEY-----
MIH0MF8GCSqGSIb3DQEFDTBSMDEGCSqGSIb3DQEFDDAkBBDw5Ir9M3tMGe0KqKA3
CQPPAgIIADAMBggqhkiG9w0CCQUAMB0GCWCGSAFlAwQBKgQQ61NRFW27iA1ovjc8
XoDY0QSBkGfBK9QHUfhlTonAggM8MpewBD0w25cnmhKZfhodfE9YlbkwO4yBHfZG
WzPLi52tElpRZvLPMk/KNmxhznmYiXCc79P21c50kjb6QFtNcA/A7PqcGKM0a2ya
BOI2cE1UPr2KbtRubNL3mP+xsgtxEY7RPCpXVe+LK2bbtqVojfNN8bTX+XF1N2gb
UvLJBlF8xw==
-----END ENCRYPTED PRIVATE KEY-----""".encode(),
        password=b'Google',
    )
    # Use crv and alg pairs:
    # P-256 → ES256
    # P-384 → ES384
    # P-521 → ES512
    # secp256k1 → ES256K
    # * Generate new Key Pair
    # key = jwcrypto.jwk.JWK.generate(
    #     kty='EC',
    #     kid='Elliptic Curve Based Algorithms.',
    #     crv=curve[alg_choosen],
    # )
    #
    public_key = key.public()
    # public_key = jwcrypto.jwk.JWK.from_json(key.export(private_key=False))
    # print(public_key)
    print(key.export_to_pem(private_key=True, password=b'Google').decode())
    print(key.export_to_pem(private_key=False).decode())
    # * Export as JWK
    print(key.export(private_key=False))
    #
    # * sign jwt
    header = {'alg': alg_choosen}
    # alg must be one of ES256, ES256K, ES384, ES512
    claims = {
        'sub': 'Hello',
        'iss': 'https://example.com/.well-known/public-jwks/',
        'exp': datetime(2025, 12, 31, 23, 59, 59, 999999).timestamp(),
        'typ': 'JWT',
    }
    token = jwcrypto.jwt.JWT(
        header,
        claims=claims,
    )
    token.make_signed_token(key)
    json_token = token.serialize()
    print(json_token)
    #
    # * verify
    received = jwcrypto.jwt.JWT(key=public_key, jwt=json_token)
    print(received.claims)


if __name__ == '__main__':
    asyncio.run(main=main())
