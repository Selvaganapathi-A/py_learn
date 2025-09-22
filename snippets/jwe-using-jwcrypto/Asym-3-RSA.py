import datetime
from pprint import pprint

import orjson
from cryptography.hazmat.primitives import hashes
from jwcrypto import jwe, jwk


def main():
    AsymmetricAlgorithms = (
        # 'RSA1_5',
        'RSA-OAEP',
        'RSA-OAEP-256',
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
    key: jwk.JWK = jwk.JWK.generate(kty='RSA', size=2048)
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
            header = {'alg': alg, 'enc': enc, 'typ': 'JWE', 'kid': key.thumb}
            print('Header : ', header)
            # print('  Data : ', data)
            #
            jwetoken = jwe.JWE(plaintext=payload, protected=header)  # type: ignore
            jwetoken.add_recipient(public_key)
            token = jwetoken.serialize()
            pprint(orjson.loads(token))
            jwe_obj = jwe.JWE()
            jwe_obj.deserialize(token, private_key)
            pprint(orjson.loads(jwe_obj.payload))  # type: ignore
    #
    AsymmetricAlgorithms = (
        'PBES2-HS256+A128KW',
        'PBES2-HS384+A192KW',
        'PBES2-HS512+A256KW',
    )
    password = b'Ghost Rider'
    for enc in ContentEncryptionOptions:
        # break
        for alg in AsymmetricAlgorithms:
            key = jwk.JWK(kty='oct', alg=alg, k=password.hex())
            header = {
                'alg': alg,
                'enc': enc,
                'typ': 'JWE',
                'kid': key.thumbprint(hashes.SHA3_512()),
            }
            pprint({'Header': header})
            # print('  Data : ', data)
            #
            jwetoken = jwe.JWE(plaintext=payload, protected=header)  # type: ignore
            jwetoken.add_recipient(key)
            token = jwetoken.serialize()
            pprint(orjson.loads(token))
            jwe_obj = jwe.JWE()
            jwe_obj.deserialize(token, key)
            pprint(orjson.loads(jwe_obj.payload))  # type: ignore


if __name__ == '__main__':
    main()
