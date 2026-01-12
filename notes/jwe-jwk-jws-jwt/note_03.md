# Question

``` md
'ECDH-ES',
'ECDH-ES+A128KW',

'A128GCM',
'A256CBC-HS512' example with authlib
```

---

Great — you want **JWE encryption and decryption using `authlib`** for:

* `alg`: `ECDH-ES`, `ECDH-ES+A128KW`
* `enc`: `A128GCM`, `A256CBC-HS512`

Let’s break it down with **real code examples** using `authlib.jose.JsonWebEncryption` and EC keys.

---

## 🔧 Setup

```bash
pip install authlib
```

---

## ⚙️ Example: ECDH-ES + A128GCM

> ✅ Ephemeral EC key agreement + Authenticated encryption

### 🔑 Key Generation

```python
from authlib.jose import JsonWebEncryption, JsonWebKey

# Generate recipient EC key (P-256)
recipient_key = JsonWebKey.generate_key(kty='EC', crv_or_size='P-256', is_private=True)
recipient_public = recipient_key.as_dict(is_private=False)
recipient_private = recipient_key.as_dict(is_private=True)
```

### 🔐 Encryption (ECDH-ES + A128GCM)

```python
jwe = JsonWebEncryption()

protected_header = {
    "alg": "ECDH-ES",
    "enc": "A128GCM",
    "typ": "JWE"
}

payload = {"user": "element", "role": "admin"}

token = jwe.serialize_json(
    protected_header,
    payload,
    recipient_public
)

print("🔐 ECDH-ES + A128GCM JWE:", token)
```

### 🔓 Decryption

```python
decrypted = jwe.deserialize_json(token, recipient_private)
print("📥 Decrypted:", decrypted["payload"])
```

---

## ⚙️ Example: ECDH-ES+A128KW + A256CBC-HS512

> ✅ Key agreement + AES Key Wrap + CBC encryption with HMAC integrity

### 🔐 Encryption

```python
header = {
    "alg": "ECDH-ES+A128KW",
    "enc": "A256CBC-HS512",
    "typ": "JWE"
}

token2 = jwe.serialize_json(
    header,
    {"data": "confidential payload"},
    recipient_public
)

print("🔐 ECDH-ES+A128KW + A256CBC-HS512 JWE:", token2)
```

### 🔓 Decryption

```python
decrypted2 = jwe.deserialize_json(token2, recipient_private)
print("📥 Decrypted:", decrypted2["payload"])
```

---

## 🧠 TL;DR Differences

| Combo                              | Key Management      | Content Encryption | Integrity | Notes             |
| ---------------------------------- | ------------------- | ------------------ | --------- | ----------------- |
| `ECDH-ES` + `A128GCM`              | Ephemeral ECDH      | AES GCM            | AEAD      | 🔥 Fast & modern  |
| `ECDH-ES+A128KW` + `A256CBC-HS512` | ECDH + AES key wrap | AES CBC + HMAC     | Yes       | 🧱 High integrity |

---

Would you like this wrapped in reusable utility functions or test suite for PyTest?
