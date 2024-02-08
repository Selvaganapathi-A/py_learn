from cryptography.fernet import Fernet


def main():
    key = Fernet.generate_key()
    suite = Fernet(key)
    message = b"Hi Susan! What are you Doing?"
    cipher_text = suite.encrypt(message)
    decipher_text = suite.decrypt(cipher_text)

    print(key)
    print(cipher_text)
    print(decipher_text)
    pass


if __name__ == "__main__":
    main()
