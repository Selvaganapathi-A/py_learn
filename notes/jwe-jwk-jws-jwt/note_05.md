# Example for

```md
'alg':'dir','enc':'A128CBC-HS256'
```

---
You're asking for the **simplest but still secure symmetric JWE combo** using `authlib`:

* `alg`: **`dir`** → direct encryption (no key wrapping)
* `enc`: **`A128CBC-HS256`** → AES-CBC with HMAC-SHA256 (authenticated encryption)

This is **shared-key encryption** — both parties must have the same symmetric key (`kty: oct`).

---

## 🔧 Requirements

```bash
pip install authlib
```

---

## 🔐 Example: `dir` + `A128CBC-HS256`

```python
from authlib.jose import JsonWebEncryption, OctKey

# Create symmetric key (128-bit key for AES-CBC)
key = OctKey.generate_key({
    "kty": "oct",
    "alg": "A128CBC-HS256"
}, is_private=True)

# Convert to dict for use with JsonWebEncryption
jwk_dict = key.as_dict()

# Create JWE handler
jwe = JsonWebEncryption()

# Protected Header
header = {
    "alg": "dir",               # Direct use of symmetric key
    "enc": "A128CBC-HS256",     # AES-CBC with HMAC-SHA256
    "typ": "JWE"
}

# Payload to encrypt
payload = {
    "username": "element",
    "permission": "read:secure"
}

# 🔐 Encrypt
token = jwe.serialize_json(header, payload, jwk_dict)

print("🔐 Encrypted JWE (dir + A128CBC-HS256):")
print(token)
```

---

## 🔓 Decrypt

```python
# 🔓 Decrypt using the same shared key
decrypted = jwe.deserialize_json(token, jwk_dict)

print("📥 Decrypted Payload:")
print(decrypted["payload"])
```

---

## 🧠 Use Case

| Scenario                   | Why Use `dir` + `A128CBC-HS256` |
| -------------------------- | ------------------------------- |
| Internal microservices     | Low overhead, shared key        |
| Encrypted cookies / tokens | Fast, no key negotiation        |
| IoT / embedded devices     | Memory-efficient                |

---

## ⚠️ Security Considerations

* **Key management** is entirely up to you.
* Always **generate keys using proper cryptographic methods** — no hardcoding or reuse.
* CBC mode requires IVs — `authlib` handles this internally.

---

✅ Want this wrapped in a CLI, FastAPI dependency, or utility module? Just say the word — I'll deliver.
