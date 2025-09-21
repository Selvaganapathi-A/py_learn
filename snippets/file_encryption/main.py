from typing import TypedDict

from nacl import encoding, exceptions
from nacl.public import PrivateKey, PublicKey, SealedBox


class Keys(TypedDict):
    publicKey: PublicKey
    privateKey: PrivateKey


def fetch_keys(users: tuple[str, ...]):
    keys: dict[str, Keys] = {}
    for user in users:
        pk = PrivateKey.generate()
        keys[user] = Keys(publicKey=pk.public_key, privateKey=pk)
        #
        print(user)
        print(pk.encode(encoder=encoding.Base64Encoder))
        print(pk.public_key.encode(encoder=encoding.Base64Encoder))
        print()
    return keys


def send_message(vault: dict[str, Keys], name: str, message: str):
    k = vault.get(name)
    if k is None:
        raise ValueError('No User Found.')
    box = SealedBox(k['publicKey'])
    encrypted_message = box.encrypt(message.encode())
    return encrypted_message


def receive_message(vault: dict[str, Keys], name: str, message: bytes):
    k = vault.get(name)
    if k is None:
        raise ValueError('No User Found.')
    box = SealedBox(k['privateKey'])
    try:
        decrypted_message = box.decrypt(message)
        return decrypted_message.decode()
    except exceptions.CryptoError:
        print('Not For', name)
        raise


def main():
    users = ('arun', 'mathu', 'john', 'jack', 'mike')
    vault = fetch_keys(users)
    #
    msg_from_mike = 'Hello John. This is Mike from Orlando.'
    msg = send_message(vault, 'john', msg_from_mike)
    print('Encrypted Message :', msg)
    print()
    #
    rec_msg = receive_message(vault, 'john', msg)
    print('Decrypted Message :', rec_msg)
    print()
    #
    # try decrypt message by another user. this whill raise Crypto Error.
    msg = receive_message(vault, 'mathu', msg)
    print('Decrypted Message :', msg)
    print('*' * 106)


if __name__ == '__main__':
    main()
