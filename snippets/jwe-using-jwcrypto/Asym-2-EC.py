import datetime
from pprint import pprint

import orjson
from jwcrypto import jwe, jwk


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
    #
    key: jwk.JWK = jwk.JWK.generate(kty='EC', crv='P-256')
    #
    private_key = key
    public_key = key.public()
    print(key.export_to_pem(private_key=True, password=b'Ghost Rider').decode())
    print(key.export_to_pem(private_key=False).decode())
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
            # print('Header : ', header)
            # print('  Data : ', data)
            #
            jwetoken = jwe.JWE(plaintext=payload, protected=header)  # type: ignore
            jwetoken.add_recipient(public_key)
            token = jwetoken.serialize()
            pprint(orjson.loads(token))
            print()
            #
            jwe_obj = jwe.JWE()
            jwe_obj.deserialize(token, private_key)
            pprint(orjson.loads(jwe_obj.payload))  # type: ignore
            print()
        print()
        print()
    #
    pass


if __name__ == '__main__':
    main()
    pass
