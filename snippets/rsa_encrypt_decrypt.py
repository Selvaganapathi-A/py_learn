from typing import Any, NoReturn, Self

import rsa


class Person:
    def __init__(self, name: str) -> None:
        self.name = name
        self._public_key: rsa.PublicKey
        self._private_key: rsa.PrivateKey
        self._public_key, self._private_key = rsa.newkeys(512, poolsize=1)

    def sendMessage(self, to: Self, message: bytes):
        return rsa.encrypt(message=message, pub_key=to.pk)

    def readMessage(self, message: bytes):
        return rsa.decrypt(crypto=message, priv_key=self._private_key).decode()

    @property
    def pk(self) -> rsa.PublicKey:
        return self._public_key

    @pk.setter
    def pk(self, value: Any) -> NoReturn:
        raise ValueError('Readonly Property')

    @pk.getter
    def pk(self) -> rsa.PublicKey:
        return self._public_key


def main():
    ramesh = Person('ramesh')
    suresh = Person('suresh')

    message = 'Hello Suresh'.encode()
    encrypted_message_for_suresh = ramesh.sendMessage(
        to=suresh, message=message
    )

    print('Encrypted Message', encrypted_message_for_suresh)
    print()
    decrypted_message_for_suresh = suresh.readMessage(
        encrypted_message_for_suresh
    )

    print()
    print(decrypted_message_for_suresh)
    print('-' * 80)

    print()


if __name__ == '__main__':
    main()
