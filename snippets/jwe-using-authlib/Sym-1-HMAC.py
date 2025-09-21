import datetime

import orjson
from authlib.jose import JsonWebEncryption, JWSObject, OctKey


def main():
    SymmetricAlgorithms = (
        # ! not upported by authlib
        # 'dir',
        'A128KW',
        'A192KW',
        'A256KW',
        'A128GCMKW',
        'A192GCMKW',
        'A256GCMKW',
    )

    ContentEncryptionOptions = (
        'A128GCM',
        'A192GCM',
        'A256GCM',
        'A128CBC-HS256',
        'A192CBC-HS384',
        'A256CBC-HS512',
    )
    data = {
        'name': 'John Doe',
        'sub': 1234567890,
        'exp': datetime.datetime(2025, 8, 1).timestamp(),
        'iat': datetime.datetime(2024, 8, 1).timestamp(),
    }
    payload = orjson.dumps(data)

    for alg in SymmetricAlgorithms:
        key: OctKey
        if alg.startswith('A128'):
            key = OctKey.generate_key(128)
        elif alg.startswith('A192'):
            key = OctKey.generate_key(192)
        else:
            key = OctKey.generate_key(256)
        print(key.as_json())
        for enc in ContentEncryptionOptions:
            header = {'alg': alg, 'enc': enc, 'typ': 'JWE'}
            print('Header : ', header)
            print('  Data : ', data)
            # pprint(private_key)
            # pprint(public_key)
            #
            jwe = JsonWebEncryption()
            mx = jwe.serialize(
                header,
                payload,
                key,
                # private_key,
            )
            print(mx.decode())
            #
            mt: JWSObject = jwe.deserialize(mx, key)
            print(orjson.loads(mt.get('payload', b'{}')))  # type: ignore
            print()
        print()
        print()


if __name__ == '__main__':
    main()
