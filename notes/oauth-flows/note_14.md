 4. **JWT (Bearer Token)**
---
Good. **JWT (Bearer Token)** is where many systems either scale cleanly **or** explode spectacularly. I’ll give you the **real mechanics**, not blog fluff.

We’ll cover **what / why / full flow / request–response / client vs server / FastAPI example / security failures / when NOT to use it**.

---

# 🪙 JWT (Bearer Token) Authentication — Deep, Practical Breakdown

---

## 1️⃣ What Is a JWT?

**JWT = JSON Web Token**

A **self-contained, signed token** that proves:

* **Who** the user is
* **What** they can do
* **When** the token expires

Sent on every request as:

```http
Authorization: Bearer <JWT>
```

👉 Server does **not** store session state.

---

## 2️⃣ Why JWT Exists (The Scaling Argument)

JWT was invented because:

* Sessions don’t scale easily across services
* APIs needed **stateless auth**
* Mobile apps don’t use cookies well
* Microservices needed a portable identity

JWT trades **control** for **scalability**.

---

## 3️⃣ JWT Structure (Critical to Understand)

A JWT has **three parts**, Base64URL encoded:

```
header.payload.signature
```

### 🔹 Header

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### 🔹 Payload (Claims)

```json
{
  "sub": "42",
  "email": "element@example.com",
  "role": "admin",
  "iat": 1730000000,
  "exp": 1730003600
}
```

### 🔹 Signature

```
HMACSHA256(
  base64(header) + "." + base64(payload),
  secret
)
```

🔐 Signature = integrity, **not encryption**
Anyone can read payload. Only server can **verify**.

---

## 4️⃣ Full JWT Authentication Flow

---

## 🔹 STEP 1: Login

### 🧑 Client → Server

```http
POST /login
{
  "username": "element",
  "password": "supersecret"
}
```

### 🧠 Server

* Verifies credentials
* Generates JWT

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

---

## 🔹 STEP 2: Client Stores Token

| Storage         | Verdict        |
| --------------- | -------------- |
| Memory          | ✅ Best         |
| HttpOnly Cookie | ✅ Best         |
| localStorage    | ❌ Dangerous    |
| sessionStorage  | ⚠️ Still risky |

**Hard truth:**
JWT + browser + localStorage = **security incident waiting to happen**

---

## 🔹 STEP 3: Authenticated Request

### 🧑 Client → Server

```http
GET /api/data
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
```

---

## 🔹 STEP 4: Server Validates Token

Server checks:

1. Signature is valid
2. Token not expired
3. `iss`, `aud` correct
4. Required claims exist

👉 **No DB call required**

---

## 🔹 STEP 5: Server Responds

```http
200 OK
{
  "data": "secure info"
}
```

---

## 5️⃣ Client vs Server Responsibilities

### 🧑 Client

* Store token securely
* Attach token to every request
* Handle expiration / refresh

### 🧠 Server

* Sign tokens
* Verify tokens
* Enforce authorization (roles/scopes)
* Rotate keys (advanced)

---

## 6️⃣ FastAPI JWT Example (Correct & Clean)

### 📦 Install

```bash
pip install fastapi uvicorn python-jose passlib[bcrypt]
```

---

### 🔐 JWT Utilities

```python
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"])

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(tz=timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

---

### 🔐 Login Endpoint

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login")
def login():
    token = create_access_token({"sub": "42", "role": "admin"})
    return {"access_token": token, "token_type": "bearer"}
```

---

### 🔐 Protected Endpoint

```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

@app.get("/secure")
def secure(user=Depends(get_current_user)):
    return {"user": user}
```

---

## 7️⃣ Refresh Tokens (Mandatory in Real Life)

### Why?

Access tokens should be **short-lived** (5–15 min).

Refresh token:

* Long-lived
* Stored securely (HttpOnly cookie)
* Used to mint new access tokens

Without refresh tokens:
❌ Forced re-login
❌ Terrible UX

---

## 8️⃣ Security Failures You MUST Avoid 💥

### ❌ Failure #1: Long-lived JWTs

Stolen token = permanent access

✅ **Short expiry + refresh token**

---

### ❌ Failure #2: Storing JWT in localStorage

XSS → token exfiltration

✅ **HttpOnly cookie or memory**

---

### ❌ Failure #3: No audience / issuer checks

Token reuse across services

✅ **Validate `aud`, `iss`**

---

### ❌ Failure #4: Using JWT for logout

You **cannot** revoke JWTs easily

✅ Use:

* Short expiry
* Token blacklist (if absolutely needed)

---

## 9️⃣ JWT vs Cookie Sessions (Brutal Truth)

| Feature        | JWT | Cookie Session |
| -------------- | --- | -------------- |
| Stateless      | ✅   | ❌              |
| Easy logout    | ❌   | ✅              |
| Browser safety | ❌   | ✅              |
| Microservices  | ✅   | ⚠️             |
| Mobile apps    | ✅   | ❌              |

---

## 🔟 When SHOULD You Use JWT?

✅ Use JWT when:

* Mobile apps
* Public APIs
* Microservices
* SPA + backend (carefully)

❌ Avoid JWT when:

* Admin dashboards
* Banking apps
* High-security browser apps

---

## Final Verdict (No Sugarcoating)

> **JWT is powerful, but unforgiving.**
> If you misuse it, attackers will thank you.

Use JWT when:

* You need stateless auth
* You control token lifecycle
* You understand refresh + storage

Otherwise:
👉 **Cookie-based sessions are safer and simpler**

---

If you want next:

* 🔄 **JWT Refresh Token rotation**
* 🍪 **JWT stored in HttpOnly cookies**
* 🧬 **JWT + OAuth2 hybrid**
* 🔐 **Key rotation (RS256)**

Say the word.
