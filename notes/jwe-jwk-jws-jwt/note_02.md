# alg, enc all combos
<!--  -->
You're asking for **all possible valid combinations** of `alg` (JWE key management) and `enc` (JWE content encryption). Let’s go all in — complete reference chart, categorized by algorithm type.

---

## ✅ Valid `alg` + `enc` Combinations in JWE

> 📌 Note: Not every combo is equally secure or recommended. Some are legacy or niche.

---

### 🔐 1. **Asymmetric Key Encryption (`RSA`, `ECDH-ES`)**

| `alg`            | Valid `enc` options                                                                | 🔥 Recommended    |
| ---------------- | ---------------------------------------------------------------------------------- | ----------------- |
| `RSA1_5`         | `A128CBC-HS256`, `A192CBC-HS384`, `A256CBC-HS512`, `A128GCM`, `A192GCM`, `A256GCM` | ❌ Legacy only     |
| `RSA-OAEP`       | ✅ all above                                                                        | ✅ Production      |
| `RSA-OAEP-256`   | ✅ all above                                                                        | ✅ Production      |
| `ECDH-ES`        | ✅ all above                                                                        | ✅ Forward secrecy |
| `ECDH-ES+A128KW` | ✅ all above                                                                        | ✅                 |
| `ECDH-ES+A192KW` | ✅ all above                                                                        | ✅                 |
| `ECDH-ES+A256KW` | ✅ all above                                                                        | ✅                 |

---

### 🔐 2. **Symmetric Key Encryption (`dir`, `AES Key Wrap`)**

| `alg`                | Valid `enc` options                                                                       | 🔥 Recommended    |
| -------------------- | ----------------------------------------------------------------------------------------- | ----------------- |
| `dir`                | ✅ all: `A128GCM`, `A192GCM`, `A256GCM`, `A128CBC-HS256`, `A192CBC-HS384`, `A256CBC-HS512` | ✅ Simple & strong |
| `A128KW`             | ✅ all above                                                                               | ⚠️ Limited use    |
| `A192KW`             | ✅ all above                                                                               | ⚠️                |
| `A256KW`             | ✅ all above                                                                               | ✅ with wrap       |
| `PBES2-HS256+A128KW` | ✅ all above                                                                               | ✅ Passwords       |
| `PBES2-HS384+A192KW` | ✅ all above                                                                               | ✅                 |
| `PBES2-HS512+A256KW` | ✅ all above                                                                               | ✅                 |

---

### 🔐 3. **Content Encryption (`enc`) Options**

These are shared across all `alg`:

| `enc`           | Cipher                | Key Size | AEAD?  | 🔥 Recommended   |
| --------------- | --------------------- | -------- | ------ | ---------------- |
| `A128CBC-HS256` | AES-CBC + HMAC-SHA256 | 256 bits | ✅      | ⚠️ slower        |
| `A192CBC-HS384` | AES-CBC + HMAC-SHA384 | 384 bits | ✅      | ⚠️ slow, niche   |
| `A256CBC-HS512` | AES-CBC + HMAC-SHA512 | 512 bits | ✅      | ✅ high-integrity |
| `A128GCM`       | AES-GCM               | 128 bits | ✅ AEAD | ✅ fast & secure  |
| `A192GCM`       | AES-GCM               | 192 bits | ✅ AEAD | ⚠️ uncommon      |
| `A256GCM`       | AES-GCM               | 256 bits | ✅ AEAD | 🔥 Gold standard |

---

## 🚀 Full Matrix (All Combos)

Here’s a dense matrix of **valid pairs**. ✅ = commonly used; ⚠️ = works but not ideal; ❌ = avoid.

| `alg`                | `A128GCM` | `A192GCM` | `A256GCM` | `A128CBC-HS256` | `A192CBC-HS384` | `A256CBC-HS512` |
| -------------------- | --------- | --------- | --------- | --------------- | --------------- | --------------- |
| `RSA1_5`             | ❌         | ❌         | ❌         | ⚠️              | ⚠️              | ⚠️              |
| `RSA-OAEP`           | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `RSA-OAEP-256`       | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `ECDH-ES`            | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `ECDH-ES+A128KW`     | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `ECDH-ES+A192KW`     | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `ECDH-ES+A256KW`     | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `dir`                | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `A128KW`             | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `A192KW`             | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `A256KW`             | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `PBES2-HS256+A128KW` | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `PBES2-HS384+A192KW` | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |
| `PBES2-HS512+A256KW` | ✅         | ✅         | ✅         | ✅               | ✅               | ✅               |

---

## 🧠 Recommendations Recap

| Situation               | Recommended `alg` + `enc`        |
| ----------------------- | -------------------------------- |
| Asymmetric public key   | `RSA-OAEP` + `A256GCM`           |
| Ephemeral key agreement | `ECDH-ES` + `A256GCM`            |
| Symmetric shared secret | `dir` + `A256GCM`                |
| Password encryption     | `PBES2-HS256+A128KW` + `A128GCM` |

---

Would you like:

* ✅ A Python snippet to loop through these and test with `authlib`?
* ✅ Or a visual matrix exported as CSV / markdown / Excel?
* ✅ Or integration-ready helper functions?

Let me know — I’ll generate it on the fly.
