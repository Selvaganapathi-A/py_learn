import rsa

if __name__ == '__main__':
    public_key: rsa.PublicKey
    private_key: rsa.PrivateKey
    encrypted_message: bytes
    decrypted_message: str
    number_of_bytes: int
    max_message_len_in_bytes: int
    message: str

    # public_key, private_key = rsa.newkeys(128)
    #
    private_key = rsa.PrivateKey.load_pkcs1(
        (
            b'-----BEGIN RSA PRIVATE KEY-----\n'
            b'MGICAQACEQCl4njb9pwdRgx5nKBGAQLVA'
            b'gMBAAECEQCal9iyhb0vsB8fSAh24z7x\n'
            b'AgkLd5ToXeERTicCCA53U4mSCcCjAgkE4'
            b'qh1KvHlXocCB3qQiDgOHJMCCQtV9C4D\n'
            b'zXzTZQ==\n'
            b'-----END RSA PRIVATE KEY-----\n'
        )
    )
    public_key = rsa.PublicKey.load_pkcs1(
        (
            b'-----BEGIN RSA PUBLIC KEY-----\n'
            b'MBgCEQCl4njb9pwdRgx5nKBGAQLVAgMBAAE=\n'
            b'-----END RSA PUBLIC KEY-----\n'
        )
    )
    #
    message = 'Hello'
    encrypted_message = rsa.encrypt(message.encode(), public_key)
    decrypted_message = rsa.decrypt(encrypted_message, private_key).decode()
    number_of_bytes = 2048
    max_message_len_in_bytes = (number_of_bytes // 8) - 11
    #
    #
    print()
    # print(public_key.save_pkcs1())
    # print(private_key.save_pkcs1())
    # print()
    print(max_message_len_in_bytes)
    print()
    print((public_key, private_key))
    print()
    print((encrypted_message, decrypted_message))
    print()
