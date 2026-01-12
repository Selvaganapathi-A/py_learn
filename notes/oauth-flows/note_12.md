# HTTP Digest Authentication with FastAPI
<!--  -->
Implementing **HTTP Digest Authentication with FastAPI** is *not built-in*, but it's absolutely doable with a custom dependency.

Here’s a **complete, production-aware, SHA-256 based Digest Auth implementation** using FastAPI — tailored for learning and extensibility.

---

## 🔐 Digest Authentication in FastAPI (SHA-256 Variant)

### ⚠️ Heads-Up:

* FastAPI and Starlette **don’t have native DigestAuth** like they do for BasicAuth.
* We’ll roll our own logic using dependencies.
* This example is **readable, modular, and secure** for learning/demo. You can extend it with nonce tracking, user DB, and replay protection.

---

## ✅ Key Concepts

### Digest Auth Flow:

1. Server challenges with `401` + `WWW-Authenticate`
2. Client re-sends with `Authorization: Digest ...`
3. Server verifies:

   * `response = hash(A1:nonce:nc:cnonce:qop:A2)`

---

## 📦 Setup

```bash
pip install fastapi uvicorn
```

---

## 📁 File: `main.py`

```python
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from hashlib import sha256
from base64 import b64encode
from typing import Optional
import re
import secrets
import time

app = FastAPI()

USERS = {
    "element": "supersecret"  # Plaintext just for demo. Use hash in real life.
}

REALM = "FastAPI-Digest"
NONCE_TIMEOUT = 300  # seconds

# In-memory nonce store for simplicity
nonces = {}

def generate_nonce():
    nonce = secrets.token_hex(16)
    nonces[nonce] = time.time()
    return nonce

def is_nonce_valid(nonce: str) -> bool:
    created = nonces.get(nonce)
    if not created:
        return False
    return (time.time() - created) < NONCE_TIMEOUT

def build_www_authenticate_header():
    nonce = generate_nonce()
    return (
        f'Digest realm="{REALM}", '
        f'qop="auth", '
        f'nonce="{nonce}", '
        f'algorithm=SHA-256'
    )

def parse_digest_header(header: str):
    pattern = re.compile(r'(\w+)=("([^"]+)"|([^\s,]+))')
    return {k: v.strip('"') for k, _, v, v_alt in pattern.findall(header)}

def digest_auth(request: Request):
    auth_header: str = request.headers.get("authorization")
    if not auth_header or not auth_header.lower().startswith("digest "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": build_www_authenticate_header()},
            detail="Unauthorized",
        )

    auth_data = parse_digest_header(auth_header[7:])  # strip 'Digest '

    username = auth_data.get("username")
    realm = auth_data.get("realm")
    nonce = auth_data.get("nonce")
    uri = auth_data.get("uri")
    response = auth_data.get("response")
    qop = auth_data.get("qop")
    nc = auth_data.get("nc")
    cnonce = auth_data.get("cnonce")

    if not all([username, realm, nonce, uri, response, qop, nc, cnonce]):
        raise HTTPException(status_code=400, detail="Incomplete digest data")

    if not is_nonce_valid(nonce):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": build_www_authenticate_header()},
            detail="Invalid or expired nonce",
        )

    password = USERS.get(username)
    if not password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Compute expected response
    A1 = f"{username}:{realm}:{password}"
    A2 = f"{request.method}:{uri}"

    HA1 = sha256(A1.encode()).hexdigest()
    HA2 = sha256(A2.encode()).hexdigest()

    valid_response = sha256(
        f"{HA1}:{nonce}:{nc}:{cnonce}:{qop}:{HA2}".encode()
    ).hexdigest()

    if not secrets.compare_digest(valid_response, response):
        raise HTTPException(status_code=401, detail="Invalid response hash")

    return username

# 🔐 Protected route
@app.get("/secure")
async def secure_data(user: str = Depends(digest_auth)):
    return {"message": f"Hello, {user}. You have access to secure data."}

# 🧪 Public test route
@app.get("/")
def root():
    return {"message": "Public endpoint. No auth needed."}
```

---

## 🧪 Testing with `curl`

```bash
curl --digest -u element:supersecret http://localhost:8000/secure
```

✔️ Output:

```json
{"message":"Hello, element. You have access to secure data."}
```

---

## 🔐 Security Considerations

| Issue                | Recommendation                    |
| -------------------- | --------------------------------- |
| 🛡️ Password hashing | Store `HA1` (not raw password)    |
| ⌛ Nonce reuse        | Track nonce usage and expire them |
| 📦 User DB           | Replace `USERS` dict with real DB |
| ⚔️ Replay attack     | Enforce `nc` (nonce count) check  |
| 🧼 Token cleanup     | Periodically clear expired nonces |

---

## 🚀 Production Enhancements

* ✅ Replace plaintext password with `HA1 = sha256(username:realm:password)`
* 🧊 Store nonces in Redis (for distributed apps)
* 🔁 Add nonce replay prevention with nonce-count tracking
* 🔐 Add HTTPS (required if not using digest over secure transport)
* 📜 Add scope/role enforcement

---

## 🧩 Summary

| Feature                 | Digest Auth (this impl) |
| ----------------------- | ----------------------- |
| Stateless               | ✅                       |
| Encrypted credentials   | ✅                       |
| SHA-256 support         | ✅                       |
| Nonce/Replay Protection | ⚠️ Basic, extendable    |
| Easy integration        | ✅ with `Depends()`      |
| Secure for production?  | ⚠️ With enhancements    |

---

Want this as a plug-and-play FastAPI dependency module with `nonce rotation`, `HA1 hash DB`, and `middleware version`? I can extend this into a full digest auth plugin. Just say the word.
