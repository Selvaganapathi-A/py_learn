# using jwcrypto

```md
 'PBES2-HS384+A192KW'+'A192CBC-HS384'
```

---

You're asking for a full working example of **JWE encryption and decryption** using:

* `alg`: `PBES2-HS384+A192KW` (password-based encryption with HMAC-SHA384 and AES-192 key wrap)
* `enc`: `A192CBC-HS384` (AES-CBC encryption with HMAC-SHA384 for integrity)

— using the [`jwcrypto`](https://jwcrypto.readthedocs.io/) library.

Let’s get into the **code-first, zero-BS walkthrough**. 🔥

---

## 🛠 Requirements

```bash
pip install jwcrypto
```

---

## ✅ Step-by-Step Using `jwcrypto`

```python
from jwcrypto import jwk, jwe
import json

# Step 1: Shared password (must be bytes)
password = b"UltraSecureP@ssw0rd123"

# Step 2: Create a symmetric JWK key with appropriate size
# 192-bit key (24 bytes) for A192KW/A192CBC
shared_key = jwk.JWK(kty='oct', alg='PBES2-HS384+A192KW', k=password.hex())

# Step 3: Create the payload
payload = {
    "email": "admin@corp.com",
    "access": "confidential",
    "scopes": ["read", "write"]
}

# Step 4: Set protected header
protected_header = {
    "alg": "PBES2-HS384+A192KW",
    "enc": "A192CBC-HS384"
}

# Step 5: Build JWE object and encrypt
jwetoken = jwe.JWE(
    plaintext=json.dumps(payload).encode('utf-8'),
    protected=protected_header
)

# Encrypt with password-derived key
jwetoken.add_recipient(shared_key)

print("🔐 Encrypted JWE (PBES2-HS384+A192KW + A192CBC-HS384):")
print(jwetoken.serialize(compact=True))
```

---

## 🔓 Decrypt the JWE Token

```python
# Re-create the same JWK from password (on receiving side)
decryption_key = jwk.JWK(kty='oct', alg='PBES2-HS384+A192KW', k=password.hex())

# Parse and decrypt token
jwetoken2 = jwe.JWE()
jwetoken2.deserialize(jwetoken.serialize(compact=True))
jwetoken2.decrypt(decryption_key)

# Read the payload
decrypted_payload = json.loads(jwetoken2.payload.decode())
print("📥 Decrypted Payload:")
print(decrypted_payload)
```

---

## 🧠 Key Notes

| Item                 | Detail                                                     |
| -------------------- | ---------------------------------------------------------- |
| `PBES2-HS384+A192KW` | Password-Based Encryption using HMAC-SHA384 + AES Key Wrap |
| `A192CBC-HS384`      | AES-CBC with 192-bit key and HMAC-SHA384 for integrity     |
| 🔐 Password          | Must be high-entropy; used to derive encryption key        |
| 💥 Security          | No public/private key needed; no key server required       |

---

## ⚠️ Gotchas with `jwcrypto` + PBES2

* The `k` (key material) in `JWK` **must be base64url or hex** if passed directly — here we hex-encoded the password for simplicity.
* JWEs with PBES2 are **not commonly supported in UI debuggers** (like [jwt.io](https://jwt.io)).

---

Would you like this exported to a Python module or CLI utility (e.g. `encrypt_jwe.py --password <pwd> --data <file.json>`)?

Happy to do it.
