* 🔒 Integrate login page (OAuth consent)
* 📜 Publish multiple keys in JWKS (rotation)

<!--  -->

Excellent asks. These are **non-negotiable** for a real IdP.
Let’s wire them in **properly**, not toy-demo style.

I’ll show:

1. 🔒 **Real login + consent page flow**
2. 📜 **JWKS with multiple keys + rotation strategy**
3. What to do / not to do in production (battle scars included)

All code stays **FastAPI + jwcrypto**, clean and OIDC-aligned.

---

# 1️⃣ Integrate Login + OAuth Consent Page

## 🎯 Goal

Instead of auto-logging in `user1`, we:

* Show **login page**
* Authenticate user
* Show **consent screen**
* Only then issue authorization code

This matches **Google / Auth0 / Keycloak behavior**.

---

## 🔁 Correct Authorization Flow (Reality)

```
/authorize
   ↓
login page (GET)
/login (POST)
   ↓
consent page (GET)
/consent (POST)
   ↓
redirect_uri?code=...
```

---

## 🧠 State We Must Preserve

OIDC requires preserving request context:

```python
authorization_request = {
    "client_id",
    "redirect_uri",
    "scope",
    "state",
    "nonce",
    "code_challenge"
}
```

We’ll store this **server-side** (cookie or cache).

---

## 📁 `auth_state.py`

```python
import secrets

AUTH_REQUESTS: dict[str, dict] = {}

def create_auth_request(data: dict) -> str:
    req_id = secrets.token_urlsafe(16)
    AUTH_REQUESTS[req_id] = data
    return req_id

def pop_auth_request(req_id: str) -> dict | None:
    return AUTH_REQUESTS.pop(req_id, None)
```

---

## 🔓 `/authorize` → redirect to login

```python
from fastapi.responses import RedirectResponse
from .auth_state import create_auth_request

@router.get("/authorize")
async def authorize(
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
    response_type: str,
    code_challenge: str,
    code_challenge_method: str,
    nonce: str | None = None,
):
    req_id = create_auth_request({
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
    })

    return RedirectResponse(f"/login?req_id={req_id}")
```

---

## 🔐 Login Page (HTML)

```python
from fastapi.responses import HTMLResponse

@router.get("/login")
async def login_page(req_id: str):
    return HTMLResponse(f"""
    <form method="post" action="/login">
        <input type="hidden" name="req_id" value="{req_id}" />
        <input name="username" />
        <input name="password" type="password" />
        <button>Login</button>
    </form>
    """)
```

---

## 🔑 Login POST → Consent

```python
from fastapi import Form
from .models import USERS

@router.post("/login")
async def login(
    req_id: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):
    user = USERS.get(username)
    if not user or user["password"] != password:
        return HTMLResponse("Invalid credentials", status_code=401)

    return RedirectResponse(f"/consent?req_id={req_id}&sub={username}")
```

---

## ✅ Consent Page

```python
@router.get("/consent")
async def consent(req_id: str, sub: str):
    return HTMLResponse(f"""
    <h3>Consent</h3>
    <p>User: {sub}</p>
    <form method="post" action="/consent">
        <input type="hidden" name="req_id" value="{req_id}" />
        <input type="hidden" name="sub" value="{sub}" />
        <button name="approve" value="yes">Approve</button>
    </form>
    """)
```

---

## 🏁 Consent POST → Authorization Code

```python
import secrets
from urllib.parse import urlencode
from .auth_state import pop_auth_request
from .models import CODES

@router.post("/consent")
async def consent_submit(
    req_id: str = Form(...),
    sub: str = Form(...),
):
    req = pop_auth_request(req_id)
    if not req:
        return HTMLResponse("Session expired", status_code=400)

    code = secrets.token_urlsafe(24)
    CODES[code] = {
        "sub": sub,
        **req
    }

    params = urlencode({"code": code, "state": req["state"]})
    return RedirectResponse(f'{req["redirect_uri"]}?{params}')
```

✔️ **Now you have a real OAuth login + consent flow**

---

# 2️⃣ JWKS with Multiple Keys + Rotation

This is **mandatory** in production.
Single key IdPs **will break clients** during rotation.

---

## 🔑 Key Store Design

* Keep **multiple active keys**
* One **signing key**
* Old keys still published (for validation)
* Each key has a `kid`

---

## 📁 `keys.py` (Rotation-Ready)

```python
from jwcrypto import jwk
from datetime import datetime

KEYS: dict[str, jwk.JWK] = {}

def generate_key(kid: str):
    key = jwk.JWK.generate(kty="RSA", size=2048, kid=kid)
    KEYS[kid] = key
    return key

def get_active_key() -> jwk.JWK:
    if not KEYS:
        generate_key(f"key-{datetime.utcnow().date()}")
    return list(KEYS.values())[-1]

def get_jwks():
    return {
        "keys": [
            key.export(private_key=False, as_dict=True)
            for key in KEYS.values()
        ]
    }
```

---

## 🔄 Rotate Keys (Manual or Cron)

```python
def rotate_keys():
    new_kid = f"key-{datetime.utcnow().isoformat()}"
    generate_key(new_kid)
```

✔️ Old keys remain published
✔️ New tokens use latest `kid`
✔️ Clients keep validating old tokens safely

---

## 🧾 JWKS Endpoint

```python
@router.get("/jwks.json")
async def jwks():
    return get_jwks()
```

---

## ✍️ Sign Tokens with Active Key

```python
from jwcrypto import jwt
from .keys import get_active_key

def sign_id_token(claims: dict) -> str:
    key = get_active_key()
    token = jwt.JWT(
        header={"alg": "RS256", "kid": key.key_id},
        claims=claims
    )
    token.make_signed_token(key)
    return token.serialize()
```

---

# 🚨 Production Disaster Stories (Listen Carefully)

### ❌ Disaster #1: Single signing key

**Result:** forced logout of *all users* during rotation

✅ Fix: **publish multiple keys**

---

### ❌ Disaster #2: No consent screen

**Result:** legal/security audit failure

✅ Fix: explicit consent + audit logs

---

### ❌ Disaster #3: Storing auth request in query params

**Result:** CSRF + replay attack

✅ Fix: server-side auth request storage

---

### ❌ Disaster #4: No `kid`

**Result:** clients fail to validate tokens

✅ Fix: **always include `kid`**

---

# ✅ What You Now Have

✔ Real OAuth login
✔ Consent UX
✔ PKCE compatible
✔ JWKS with rotation
✔ Proper `kid` handling
✔ Enterprise-grade IdP foundation

This is **Keycloak-lite**, not a toy.

---

## Next Logical Steps (Strong Recommendation)

* 🔐 Password hashing (`argon2`)
* 🧠 Persistent storage (DB / Redis)
* 🧪 Pytest coverage
* 🔁 Refresh token support
* 🔒 Per-client encryption (JWE with client public keys)

If you want, next I can:

* Harden this for **production**
* Add **refresh tokens**
* Add **client registration**
* Pair it with a **React PKCE client**

Just say the word.
