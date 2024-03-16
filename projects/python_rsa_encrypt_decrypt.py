import rsa


def generateKeys():
    (publicKey, privateKey) = rsa.newkeys(1024)

    with open("publicKey.pem", "wb") as p:
        p.write(publicKey.save_pkcs1("PEM"))
        p.flush()
        p.close()

    with open("privateKey.pem", "wb") as p:
        p.write(privateKey.save_pkcs1("PEM"))
        p.flush()
        p.close()


def loadKeys() -> tuple[rsa.PrivateKey, rsa.PublicKey]:
    with open("publicKey.pem", "rb") as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
        p.flush()
        p.close()

    with open("privateKey.pem", "rb") as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
        p.flush()
        p.close()
    return privateKey, publicKey


def encrypt(message: str, key: rsa.PublicKey) -> bytes:
    return rsa.encrypt(message.encode("ascii"), key)


def decrypt(ciphertext: bytes, key: rsa.PrivateKey) -> str:
    return rsa.decrypt(ciphertext, key).decode("ascii")


def sign(message: str, key: rsa.PrivateKey):
    return rsa.sign(message.encode("ascii"), key, "SHA-1")


def verify(message: str, signature: bytes, key: rsa.PublicKey):
    try:
        return (rsa.verify(
            message.encode("ascii"),
            signature,
            key,
        ) == "SHA-1")
    except Exception:
        return False


def main():
    generateKeys()

    privateKey, publicKey = loadKeys()

    message = input("Write your message here:")
    ciphertext = encrypt(message, publicKey)

    signature = sign(message, privateKey)

    text = decrypt(ciphertext, privateKey)

    print(f"Cipher text: {ciphertext}")
    print(f"Signature: {signature}")

    if text:
        print(f"Message text: {text}")
    else:
        print("Unable to decrypt the message.")

    if verify(text, signature, publicKey):
        print("Successfully verified signature")
    else:
        print("The message signature could not be verified")


if __name__ == "__main__":
    main()
