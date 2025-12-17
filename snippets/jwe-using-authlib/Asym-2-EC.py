import datetime

import orjson
from authlib.jose import ECKey, JsonWebEncryption, JsonWebKey, JWSObject


def main():
    AsymmetricAlgorithms = (
        'ECDH-ES',
        'ECDH-ES+A128KW',
        'ECDH-ES+A192KW',
        'ECDH-ES+A256KW',
    )
    ContentEncryptionOptions = (
        'A128GCM',
        'A192GCM',
        'A256GCM',
        'A128CBC-HS256',
        'A192CBC-HS384',
        'A256CBC-HS512',
    )
    key: ECKey = JsonWebKey.generate_key('EC', 'P-521', is_private=True)
    private_key = key.as_dict(True)
    public_key = key.as_dict(False)
    data = {
        'name': 'John Doe',
        'sub': 1234567890,
        'exp': datetime.datetime(2025, 8, 1).timestamp(),
        'iat': datetime.datetime(2024, 8, 1).timestamp(),
    }
    payload = orjson.dumps(data)
    for alg in AsymmetricAlgorithms:
        for enc in ContentEncryptionOptions:
            header = {'alg': alg, 'enc': enc, 'typ': 'JWE'}
            print('Header : ', header)
            print('  Data : ', data)
            # pprint(private_key)
            # pprint(public_key)
            jwe = JsonWebEncryption()
            mx = jwe.serialize(
                header,
                payload,
                public_key,
                # private_key,
            )
            print(mx.decode())
            mt: JWSObject = jwe.deserialize(mx, private_key)
            print(orjson.loads(mt.get('payload', b'{}')))  # type: ignore


if __name__ == '__main__':
    main()
