from pprint import pprint

import orjson
from jwcrypto import jwe, jwk

# from authlib.jose import JsonWebEncryption, JWSObject, OctKey


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
    #
    #
    data = {
        'iss': 'https://example.com/.well-known/jwk.json',
        'sub': 1234567890,
        'aud': 'John Doe',
        'exp': 1752450600.0,
        'nbf': 1732450600.0,
        'iat': 1722450600.0,
        'jti': (
            '6fdddab7d670f202629531c1a51b32ca30696d0af4dd5b0f'
            'bb5f82c0aba5e505110455f37d7ef73950c2bb0495a38f56'
        ),
        'name': 'John Doe',
    }
    payload = orjson.dumps(data)
    #
    for alg in SymmetricAlgorithms:
        # print(alg)
        alg_size = 128
        if alg.startswith('A128'):
            alg_size = 128
        elif alg.startswith('A192'):
            alg_size = 192
        elif alg.startswith('A256'):
            alg_size = 256
        key: jwk.JWK = jwk.JWK.generate(kty='oct', size=alg_size)
        for enc in ContentEncryptionOptions:
            header = {'alg': alg, 'enc': enc, 'typ': 'JWE'}
            print('Header : ', header)
            #
            jwetoken = jwe.JWE(plaintext=payload, protected=header)  # type: ignore
            jwetoken.add_recipient(key)
            token = jwetoken.serialize()
            pprint(orjson.loads(token))
            #
            #
            jwe_obj = jwe.JWE()
            jwe_obj.deserialize(token, key)
            pprint(orjson.loads(jwe_obj.payload))  # type: ignore
            print()
            print()
        print()
        print()
    #
    pass
    #
    password = b'Ghost Rider'
    for enc in ContentEncryptionOptions:
        # break
        for alg in (
            'PBES2-HS256+A128KW',
            'PBES2-HS384+A192KW',
            'PBES2-HS512+A256KW',
        ):
            key = jwk.JWK(kty='oct', alg=alg, k=password.hex())
            header = {'alg': alg, 'enc': enc, 'typ': 'JWE'}
            print('Header : ', header)
            # print('  Data : ', data)
            #
            jwetoken = jwe.JWE(plaintext=payload, protected=header)  # type: ignore
            jwetoken.add_recipient(key)
            token = jwetoken.serialize()
            pprint(orjson.loads(token))
            #
            #
            jwe_obj = jwe.JWE()
            jwe_obj.deserialize(token, key)
            pprint(orjson.loads(jwe_obj.payload))  # type: ignore
            print()
        print()
        print()
    #


if __name__ == '__main__':
    main()
    pass
