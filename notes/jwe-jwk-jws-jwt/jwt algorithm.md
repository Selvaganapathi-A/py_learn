# JWT Algorithms used

n| Algorithm | jwt.io Support | Key Type       | Notes                                      |
| --------- | -------------- | -------------- | ------------------------------------------ |
| HS256     | ✅              | Symmetric      | Simple shared secret                       |
| HS384     | ✅              | Symmetric      | —                                          |
| HS512     | ✅              | Symmetric      | —                                          |
| RS256     | ✅              | RSA            | —                                          |
| RS384     | ✅              | RSA            | —                                          |
| RS512     | ✅              | RSA            | —                                          |
| ES256     | ✅              | EC (P-256)     | Good browser support                       |
| ES256K    | ❌              | EC (secp256k1) | Used in blockchain, not jwt.io             |
| ES384     | ✅              | EC (P-384)     | —                                          |
| ES512     | ✅              | EC (P-521)     | —                                          |
| PS384     | ❌              | RSA (PSS)      | More secure than RS*, not jwt.io supported |
| PS512     | ❌              | RSA (PSS)      | —                                          |
| EdDSA     | 🔁             | OKP (Ed25519)  | Minimal size, high performance             |
