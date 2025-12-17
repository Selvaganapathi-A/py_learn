import asyncio

from jwcrypto import jwk, jwt


async def main():
    #
    # * Read Public Key from file
    #     key = jwk.JWK.from_pem(
    #         """-----BEGIN ENCRYPTED PRIVATE KEY-----
    # MIH0MF8GCSqGSIb3DQEFDTBSMDEGCSqGSIb3DQEFDDAkBBDw5Ir9M3tMGe0KqKA3
    # CQPPAgIIADAMBggqhkiG9w0CCQUAMB0GCWCGSAFlAwQBKgQQ61NRFW27iA1ovjc8
    # XoDY0QSBkGfBK9QHUfhlTonAggM8MpewBD0w25cnmhKZfhodfE9YlbkwO4yBHfZG
    # WzPLi52tElpRZvLPMk/KNmxhznmYiXCc79P21c50kjb6QFtNcA/A7PqcGKM0a2ya
    # BOI2cE1UPr2KbtRubNL3mP+xsgtxEY7RPCpXVe+LK2bbtqVojfNN8bTX+XF1N2gb
    # UvLJBlF8xw==
    # -----END ENCRYPTED PRIVATE KEY-----""".encode(),
    #         password=b'Google',
    #     )
    # Use crv and alg pairs:
    # P-256 → ES256
    # P-384 → ES384
    # P-521 → ES512
    # secp256k1 → ES256K
    # * Generate new Key Pair
    curve = {
        'ES256': 'P-256',
        'ES256K': 'secp256k1',
        'ES384': 'P-384',
        'ES512': 'P-521',
    }
    #
    # * sign jwt
    # alg must be one of ES256, ES256K, ES384, ES512
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
    ALGORITHMS: tuple[str, ...] = ('ES256', 'ES256K', 'ES384', 'ES512')
    for algorithm in ALGORITHMS:
        # * Create Key
        key = jwk.JWK.generate(
            kty='EC',
            kid='Elliptic Curve Based Algorithms.',
            crv=curve[algorithm],
        )
        public_key = key.public()
        print(key.export_to_pem(private_key=True, password=b'Google').decode())
        print(key.export_to_pem(private_key=False).decode())
        # * Export as JWK
        # print(key.export(private_key=False))
        #
        header = {'alg': algorithm}
        # * Sign JWT
        token = jwt.JWT(
            header,
            claims=claims,
        )
        token.make_signed_token(key)
        json_token = token.serialize()
        print(json_token)
        #
        # * verify JWT
        received = jwt.JWT(key=public_key, jwt=json_token)
        print(received.claims)


if __name__ == '__main__':
    asyncio.run(main=main())
