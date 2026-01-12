# File Encryption

## AES RSA File Encryption

You're looking to **encrypt a file using AES**, then **encrypt the AES key using the receiver's RSA public key** — a standard hybrid encryption pattern used in secure systems. This combines **fast symmetric encryption** (AES) with **secure key exchange** (RSA).

Let’s break it down using the `cryptography` library in Python.

---

### ✅ Requirements

Install the library (if not already):

```bash
pip install cryptography
```

---

### ✅ High-Level Steps

1. Generate a random AES key (symmetric key).
2. Encrypt the file with AES (CBC mode).
3. Load the receiver's RSA public key.
4. Encrypt the AES key with the RSA public key.
5. Save both:

   * AES-encrypted file
   * RSA-encrypted AES key (e.g., in `.key` file)

---

### ✅ Code Implementation

```python
from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import keywrap
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import os

# === Step 1: Generate AES key and IV ===
aes_key = os.urandom(32)  # AES-256
iv = os.urandom(16)       # 16-byte IV for CBC

# === Step 2: Encrypt the file content using AES ===
def encrypt_file(input_file_path, output_file_path, aes_key, iv):
    backend = default_backend()

    with open(input_file_path, 'rb') as f:
        plaintext = f.read()

    # Pad the plaintext to block size (AES block = 128 bits)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    with open(output_file_path, 'wb') as f:
        f.write(iv + ciphertext)  # Prepend IV for decryption

# === Step 3: Encrypt AES key with RSA public key ===
def encrypt_aes_key_with_rsa_public_key(aes_key, public_key_path, output_key_file):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    encrypted_key = public_key.encrypt(
        aes_key,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_key_file, 'wb') as f:
        f.write(encrypted_key)

# === Run Everything ===
input_file = "example.txt"
encrypted_file = "example.enc"
rsa_public_key_file = "receiver_pub.pem"
encrypted_key_file = "example.key"

encrypt_file(input_file, encrypted_file, aes_key, iv)
encrypt_aes_key_with_rsa_public_key(aes_key, rsa_public_key_file, encrypted_key_file)

print("Encryption complete: Encrypted file and key saved.")
```

---

### 🔐 Example of RSA Public Key (`receiver_pub.pem`)

```bash
# Use OpenSSL to generate RSA key pair
openssl genrsa -out receiver_priv.pem 2048
openssl rsa -in receiver_priv.pem -pubout -out receiver_pub.pem
```

---

### 🔓 Decryption Flow (Receiver side)

1. Use their **RSA private key** to decrypt the AES key.
2. Use the **decrypted AES key and IV** to decrypt the file.

Let me know if you want the **decryption code** as well or to **embed the RSA public key directly** in the script.
