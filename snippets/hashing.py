import hashlib


def main():
    print(hashlib.algorithms_guaranteed)
    print(
        hashlib.blake2b(
            b'123',
            digest_size=64,
            salt=b'google',
            key=b'andromeda',
            leaf_size=7,
        ).hexdigest()
    )
    print(
        hashlib.blake2b(
            b'123',
            digest_size=64,
            salt=b'google',
            key=b'andromeda',
            leaf_size=7,
        ).hexdigest()
    )
    print(
        hashlib.blake2b(
            b'meercat',
            digest_size=5,
            salt=b'element',
            key=b'surprize',
            leaf_size=7,
        ).hexdigest()
    )
    print(
        hashlib.pbkdf2_hmac(
            hash_name='sha3_512',
            password=b'google@lion',
            salt=b'dolphin',
            iterations=4,
        ).hex()
    )
    print(
        hashlib.pbkdf2_hmac(
            hash_name='sha3_512',
            password=b'google@tiger',
            salt=b'dolphin',
            iterations=2,
        ).hex()
    )
    print(
        hashlib.pbkdf2_hmac(
            hash_name='sha3_512',
            password=b'google@tiger',
            salt=b'dolphin',
            iterations=2,
        ).hex()
    )


if __name__ == '__main__':
    main()
