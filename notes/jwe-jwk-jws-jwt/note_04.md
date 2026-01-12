# Question

```md
'PBES2-HS384+A192KW'+'A192CBC-HS384'
```

---
Let’s go full-throttle into this 🔐 advanced JWE combo using `authlib`:

* `alg`: **PBES2-HS384+A192KW** (Password-Based Encryption with AES-192 Key Wrap)
* `enc`: **A192CBC-HS384** (AES-CBC with HMAC-SHA-384 for integrity)

This combo is **password-based**, meaning:

* No key pairs or JWKS.
* You encrypt/decrypt purely using a shared password (e.g., `"myStrongP@ssw0rd!"`).

---

## ✅ Prerequisites

```bash
pip install authlib
```

---

## 🛠 Full Example using `authlib.jose.JsonWebEncryption`

```python
from authlib.jose import JsonWebEncryption

# Initialize JWE handler
jwe = JsonWebEncryption()

# Password to use for encryption and decryption
password = b"UltraSecureP@ssw0rd123"  # bytes

# Define protected header
protected_header = {
    "alg": "PBES2-HS384+A192KW",
    "enc": "A192CBC-HS384",
    "typ": "JWE"
}

# Payload to encrypt
payload = {
    "email": "secret@corp.com",
    "scopes": ["admin", "read:all"]
}

# 🔐 Encrypt the payload using the password
token = jwe.serialize_json(
    protected_header,
    payload,
    password
)

print("🔐 JWE Token (PBES2-HS384+A192KW + A192CBC-HS384):")
print(token)
```

---

## 🔓 Decrypt the Token

```python
# Decrypt using the same password
decrypted = jwe.deserialize_json(token, password)

print("📥 Decrypted Payload:")
print(decrypted["payload"])
```

---

## 🧠 Why Use This?

| Feature                                                     | Value                                                |
| ----------------------------------------------------------- | ---------------------------------------------------- |
| 🔐 **Password-based encryption**                            | No need for RSA/EC keys                              |
| 🧱 **High-integrity with HMAC**                             | `A192CBC-HS384` ensures payload + metadata integrity |
| ✅ **Safe for secure file blobs or client-specific secrets** | Great for temporary access or secrets stored in DB   |

---

## ⚠️ Security Notes

* Never hardcode passwords in production.
* Use strong passphrases.
* Rotate password-based keys like any other key.

---

Want me to wrap this into a CLI tool or class-based reusable module? Just say the word.
