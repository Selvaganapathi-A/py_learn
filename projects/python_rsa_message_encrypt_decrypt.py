import rsa

if __name__ == "__main__":
    public_key, private_key = rsa.newkeys(128)
    message = "Hello"
    encrypted_message = rsa.encrypt(message.encode(), public_key)

    decrypted_message = rsa.decrypt(
        encrypted_message, private_key
    ).decode()

    print(encrypted_message)
    print(decrypted_message)

    n = 128
    max_message_len_in_bytes = (n // 8) - 11
    print(max_message_len_in_bytes)
    pass
