Session Cookie in FastApi and react for access token usage

---

Ah, now we’re shifting gears into **session-based token handling** — a **modern hybrid** approach where you use **access tokens (e.g., JWT)** but deliver them securely through **HTTP-only cookies**, instead of exposing them to JavaScript (which is the usual cause of XSS).

### 🚨 TL;DR: Use Access Tokens in Secure Cookies

> ✅ Good for SPAs (React)
> ✅ More secure than `localStorage`
> ✅ Compatible with OAuth2, PKCE, JWT
> ✅ Easy refresh-token rotation possible

---

## 🍪 Cookie-Based Token Architecture: FastAPI + React

### 🔐 Flow Overview (Access Token in HTTP-Only Cookie)

```
1. React frontend logs in via OAuth2 (or password form)
2. FastAPI returns a Set-Cookie (HttpOnly, Secure) with access_token
3. React doesn't see the token — browser stores it automatically
4. React calls protected FastAPI APIs → browser auto-sends cookie
5. FastAPI reads token from cookie → verifies JWT → processes request
```

---

## ✅ FastAPI Code: Cookie Handling for Token

### 📦 Utility: Set Cookie

```python
from fastapi import Response

def set_access_token_cookie(response: Response, token: str):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  # set False for localhost dev only
        samesite="Lax",  # or "Strict" or "None" for cross-site
        max_age=3600,
    )
```

---

### 🎯 Login Route Example

```python
@app.post("/login")
async def login(response: Response, form: OAuth2PasswordRequestForm = Depends()):
    # 1. Authenticate user
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(401)

    # 2. Generate JWT
    token = create_jwt_token(user.id)

    # 3. Set token as HTTP-only cookie
    set_access_token_cookie(response, token)

    return {"message": "Logged in"}
```

---

### 🛡️ Dependency: Read JWT from Cookie

```python
from fastapi import Request, Depends, HTTPException

def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(401, detail="Token missing")
    return token

def get_current_user(token: str = Depends(get_token_from_cookie)):
    payload = decode_jwt(token)
    return get_user_by_id(payload["sub"])
```

---

## 🔁 Optional: Refresh Token Cookie

You can:

* Set **access token cookie (short-lived)**
* Set **refresh token cookie (long-lived, HttpOnly)**
* Provide a **`/refresh` route** to rotate tokens.

---

## 🌐 React Setup (Client-Side)

### 👉 Login Request (Example)

```tsx
await fetch("http://localhost:8000/login", {
  method: "POST",
  credentials: "include", // <---- 🔥 CRUCIAL
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ username, password }),
});
```

### 👉 API Call With Token Auto-Sent

```tsx
await fetch("http://localhost:8000/protected", {
  method: "GET",
  credentials: "include",  // browser sends cookie automatically
});
```

---

## 🛡️ CORS and Cookie Settings in FastAPI

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧩 Cookie Flags to Remember

| Flag       | Purpose                     | Should Be Set?  |
| ---------- | --------------------------- | --------------- |
| `HttpOnly` | JS can't access cookie      | ✅ Yes           |
| `Secure`   | Only over HTTPS             | ✅ Yes (in prod) |
| `SameSite` | Prevent CSRF                | Lax or Strict   |
| `Domain`   | Controls cookie scope       | Optional        |
| `Path`     | Limits where cookie is sent | Optional        |

---

## 💥 Summary: Why Cookies?

| Storage             | Secure? | Auto-sent? | JS accessible? | Refresh-friendly? |
| ------------------- | ------- | ---------- | -------------- | ----------------- |
| `localStorage`      | ❌       | ❌          | ✅              | ❌                 |
| `cookie` (HttpOnly) | ✅       | ✅          | ❌              | ✅                 |

---

## 🚀 Want Full Implementation?

If you're ready, I can:

* Scaffold `login`, `logout`, and `refresh` endpoints
* Add cookie-based JWT auth logic
* Provide full CORS + frontend integration
* Add optional CSRF protection

Let me know: “Single-file demo” or “Modular full project”?
