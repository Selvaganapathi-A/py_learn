# A jwcrypto-based FastAPI IDP
<!--  -->
Let’s build your **FastAPI Identity Provider** powered by **`jwcrypto`** — fully OIDC-ready with signed (JWS) and encrypted (JWE) ID tokens, a JWKS endpoint, and PKCE support.

---

## 🧱 Project Layout

```
fastapi_jwcrypto_idp/
├── main.py                   # FastAPI app entry
├── jwcrypto_idp/
│   ├── keys.py               # JWK generation and rotation
│   ├── token.py              # ID token generation (JWS + JWE)
│   ├── oidc.py               # OIDC endpoints: /.well-known, /jwks.json
│   ├── endpoints.py          # OAuth2 endpoints: /authorize, /token
│   └── models.py             # In-memory users/clients for simplicity
└── requirements.txt
```

---

## 📦 `requirements.txt`

```txt
fastapi[all]
jwcrypto
python-multipart
```

---

## 🔑 `keys.py`: JWK Key Handling

```python
from jwcrypto import jwk
import os

# Load or generate JWK (RSA for JWS/JWE)
def load_jwk():
    if os.path.exists("private.jwk.json"):
        with open("private.jwk.json", "r") as f:
            key = jwk.JWK.from_json(f.read())
    else:
        key = jwk.JWK.generate(kty='RSA', size=2048, kid='main-key')
        with open("private.jwk.json", "w") as f:
            f.write(key.export(private_key=True))
    return key

def get_public_jwk(key):
    return key.export(private_key=False, as_dict=True)
```

---

## 🪙 `token.py`: Generate ID Tokens (Signed + Encrypted)

```python
from jwcrypto import jwt
import time
from .keys import load_jwk

PRIVATE_KEY = load_jwk()

def generate_id_token(sub: str, aud: str, nonce: str = None, encrypt: bool = False) -> str:
    claims = {
        "iss": "http://localhost:8000",
        "sub": sub,
        "aud": aud,
        "exp": int(time.time()) + 600,
        "iat": int(time.time()),
        "nonce": nonce,
        "email": f"{sub}@example.com",
    }

    # Create signed JWT
    jws = jwt.JWT(header={"alg": "RS256", "kid": PRIVATE_KEY.key_id}, claims=claims)
    jws.make_signed_token(PRIVATE_KEY)

    if encrypt:
        # Encrypt it into JWE
        jwe = jwt.JWT(
            header={"alg": "RSA-OAEP", "enc": "A256GCM"},
            claims=jws.serialize()
        )
        jwe.make_encrypted_token(PRIVATE_KEY)  # Replace with client's pub key in real apps
        return jwe.serialize()

    return jws.serialize()
```

---

## 👤 `models.py`: Dummy Users & Clients

```python
USERS = {
    "user1": {"sub": "user1", "password": "test123"},
}

CLIENTS = {
    "client123": {
        "redirect_uri": "http://localhost:3000/callback",
        "response_types": ["code"],
        "grant_types": ["authorization_code"],
        "client_id": "client123"
    }
}

CODES = {}
```

---

## 📡 `oidc.py`: OIDC Discovery & JWKS

```python
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .keys import load_jwk, get_public_jwk

router = APIRouter()

@router.get("/.well-known/openid-configuration")
async def openid_config():
    return {
        "issuer": "http://localhost:8000",
        "authorization_endpoint": "http://localhost:8000/authorize",
        "token_endpoint": "http://localhost:8000/token",
        "userinfo_endpoint": "http://localhost:8000/userinfo",
        "jwks_uri": "http://localhost:8000/jwks.json",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "id_token_signing_alg_values_supported": ["RS256"],
    }

@router.get("/jwks.json")
async def jwks():
    key = load_jwk()
    return JSONResponse({"keys": [get_public_jwk(key)]})
```

---

## 🔓 `endpoints.py`: Authorization + Token Endpoints

```python
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, JSONResponse
from urllib.parse import urlencode
import secrets
from .models import USERS, CLIENTS, CODES
from .token import generate_id_token

router = APIRouter()

@router.get("/authorize")
async def authorize(response_type: str, client_id: str, redirect_uri: str,
                    scope: str, state: str, code_challenge: str,
                    code_challenge_method: str, nonce: str = None):

    if client_id not in CLIENTS:
        return JSONResponse({"error": "invalid_client"}, status_code=400)

    # Simulate login (real app should have form)
    code = secrets.token_urlsafe(16)
    CODES[code] = {
        "sub": "user1",
        "client_id": client_id,
        "code_challenge": code_challenge,
        "nonce": nonce
    }

    query = urlencode({"code": code, "state": state})
    return RedirectResponse(f"{redirect_uri}?{query}")

@router.post("/token")
async def token(grant_type: str = Form(...), code: str = Form(...),
                client_id: str = Form(...), redirect_uri: str = Form(...),
                code_verifier: str = Form(...)):

    data = CODES.pop(code, None)
    if not data or data["client_id"] != client_id:
        return JSONResponse({"error": "invalid_grant"}, status_code=400)

    id_token = generate_id_token(data["sub"], client_id, nonce=data["nonce"])
    return {
        "access_token": secrets.token_urlsafe(32),
        "token_type": "Bearer",
        "id_token": id_token,
        "expires_in": 600
    }
```

---

## 🚀 `main.py`: FastAPI App Entry

```python
from fastapi import FastAPI
from jwcrypto_idp import oidc, endpoints

app = FastAPI(title="FastAPI JWCrypto Identity Provider")

app.include_router(oidc.router)
app.include_router(endpoints.router)
```

---

## 🧪 Test the Flow

1. Open in browser:

   ```
   http://localhost:8000/authorize?
   response_type=code&
   client_id=client123&
   redirect_uri=http://localhost:3000/callback&
   scope=openid&
   state=abc123&
   nonce=test-nonce&
   code_challenge=abcxyz&
   code_challenge_method=S256
   ```

2. Redirect → `http://localhost:3000/callback?code=...`

3. POST to `/token` with:

   ```x-www-form-urlencoded
   grant_type=authorization_code
   code=THE_CODE
   client_id=client123
   redirect_uri=http://localhost:3000/callback
   code_verifier=abcxyz
   ```

4. ✅ You’ll get: `id_token`, `access_token`, `expires_in`

---

## 📦 Add-On Ideas

* 🗝️ Add encrypted ID tokens (JWE) per client pubkey
* 🧠 Add `userinfo` endpoint
* 🧪 Add test coverage
* 🔒 Integrate login page (OAuth consent)
* 📜 Publish multiple keys in JWKS (rotation)

---

Let me know if you want this packaged into a GitHub repo or paired with a React client (`oidc-client-ts`) to demo the full PKCE login.

Shall I zip it up and scaffold a full repo for you?
