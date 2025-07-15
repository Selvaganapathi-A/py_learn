import datetime

import orjson
from authlib.jose import JsonWebEncryption, JsonWebKey, JWSObject, RSAKey


def main():
    AsymmetricAlgorithms = (
        'RSA1_5',
        'RSA-OAEP',
        'RSA-OAEP-256',
        # * Not Supported by authlib
        # 'PBES2-HS256+A128KW',
        # 'PBES2-HS384+A192KW',
        # 'PBES2-HS512+A256KW',
    )
    ContentEncryptionOptions = (
        'A128GCM',
        'A192GCM',
        'A256GCM',
        'A128CBC-HS256',
        'A192CBC-HS384',
        'A256CBC-HS512',
    )
    #
    key: RSAKey = JsonWebKey.generate_key('RSA', 2048, is_private=True)
    #
    private_key = key.as_dict(True)
    public_key = key.as_dict(False)
    print(key.as_pem(True, 'Ghost Rider').decode())
    print(key.as_pem(False).decode())
    #
    data = {
        'name': 'John Doe',
        'sub': 1234567890,
        'exp': datetime.datetime(2025, 8, 1).timestamp(),
        'iat': datetime.datetime(2024, 8, 1).timestamp(),
    }
    payload = orjson.dumps(data)

    for enc in ContentEncryptionOptions:
        # break
        for alg in AsymmetricAlgorithms:
            header = {'alg': alg, 'enc': enc, 'typ': 'JWE'}
            print('Header : ', header)
            print('  Data : ', data)
            #
            jwe = JsonWebEncryption()
            #
            mx = jwe.serialize(
                header,
                payload,
                public_key,
                # private_key,
            )
            print(mx.decode())
            #
            mt: JWSObject = jwe.deserialize(mx, private_key)
            print(orjson.loads(mt.get('payload', b'{}')))  # type: ignore
            print()
        print()
        print()
    #
    pass


if __name__ == '__main__':
    main()
    pass
