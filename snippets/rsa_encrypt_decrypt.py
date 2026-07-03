from typing import Any, NoReturn, Self

import rsa


class Person:
    name: str
    public_key: rsa.PublicKey
    private_key: rsa.PrivateKey

    def __init__(self, name: str) -> None:
        self.name = name
        self.public_key, self.private_key = rsa.newkeys(512, poolsize=1)

    @property
    def pk(self) -> rsa.PublicKey:
        return self.public_key

    @pk.setter
    def pk(self, _value: Any) -> NoReturn:
        raise ValueError('Readonly Property')

    @pk.getter
    def pk(self) -> rsa.PublicKey:
        return self.public_key


def send_message(to: Person, /, message: bytes) -> bytes:
    return rsa.encrypt(message=message, pub_key=to.pk)


def read_message(receipient: Person, /, message: bytes) -> str:
    return rsa.decrypt(crypto=message, priv_key=receipient.private_key).decode()


def main() -> None:
    suresh = Person('suresh')

    message = b'Hello Suresh'
    encrypted_message_for_suresh = send_message(suresh, message=message)

    print('Encrypted Message', encrypted_message_for_suresh)
    print()
    decrypted_message_for_suresh = read_message(suresh, encrypted_message_for_suresh)

    print()
    print(decrypted_message_for_suresh)
    print('-' * 80)

    print()


if __name__ == '__main__':
    main()
