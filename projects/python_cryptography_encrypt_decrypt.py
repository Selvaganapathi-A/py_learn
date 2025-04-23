from anyio import Path
from cryptography.fernet import Fernet


def generate_key() -> None:
    """
    Generates a key and save it into a file
    """
    secret_key = Path(__file__).parent / 'secret.key'
    with open(secret_key, 'wb') as key_file:
        key_file.write(Fernet.generate_key())
    return None


def load_key() -> bytes:
    """
    Load the previously generated key
    """
    secret_key = Path(__file__).parent / 'secret.key'
    with open(secret_key, 'rb') as reader:
        data = reader.read()
    return data


def encrypt_message(message: bytes) -> bytes:
    """
    Encrypts a message
    """
    f = Fernet(load_key())
    return f.encrypt(message)


def decrypt_message(encrypted_message: bytes) -> bytes:
    """
    Decrypts an encrypted message
    """
    f = Fernet(load_key())
    return f.decrypt(encrypted_message)


if __name__ == '__main__':
    # generate_key()
    message = 'This is Potato'

    message_encrypt = encrypt_message(message.encode())
    message_decrypt = decrypt_message(message_encrypt)

    print(message)
    print(message_encrypt)
    print(message_decrypt.decode())
