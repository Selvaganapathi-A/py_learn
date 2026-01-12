# React + FastAPI : Authorization Code + PKCE

---
Perfect. You're aiming for a **production-grade** OAuth2 setup using **Authorization Code Flow with PKCE**, ideal for a **React frontend + FastAPI backend**.

Let’s break it down like a battle plan.

---

## ⚙️ What’s Authorization Code + PKCE?

PKCE = **Proof Key for Code Exchange**
It’s a security booster for public clients (like browsers/mobile apps) that **can’t safely store secrets**.

---

## 🧭 Flow Overview — React + FastAPI

### 1. **React Frontend**

* Generates a `code_verifier` (random string)
* Derives a `code_challenge` (hashed `code_verifier`)
* Redirects user to **OAuth provider** (Google/GitHub/etc.) with:

  * `client_id`
  * `redirect_uri`
  * `code_challenge`
  * `response_type=code`
  * `code_challenge_method=S256`

### 2. **OAuth Provider (e.g., Google)**

* Authenticates user.
* Redirects back to your frontend’s `redirect_uri` with an **authorization code**.

### 3. **React → FastAPI**

* React sends the `authorization_code` **and** `code_verifier` to FastAPI backend.

### 4. **FastAPI Backend**

* Exchanges the `authorization_code` + `code_verifier` for:

  * `access_token`
  * `refresh_token` (optional)

### 5. **Backend stores/returns token or JWT**

* Now, your backend has a valid access token (can be stored, exchanged for a session, or JWT issued to frontend).

---

## 🔐 Why PKCE?

Because **React can’t hide secrets**, but PKCE removes the need for one by using the `code_verifier` as a *temporary secret* that only your client knows.

---

## 📦 Project Structure (Basic Sketch)

```text
┌─ project/
│
├───┬─ backend/
│   ├─── main.py
│   └─── oauth_routes.py
│
└───┬─ frontend/
    └──┬─ src/
       ├─── App.tsx
       └─── pkce.ts
```

---

## 🔑 Key Components (Simplified)

### 🔧 React (Frontend)

#### `pkce.ts` (PKCE utils)

```ts
export function generateCodeVerifier(): string {
  const array = new Uint32Array(56 / 2);
  window.crypto.getRandomValues(array);
  return Array.from(array, dec => ('0' + dec.toString(16)).substr(-2)).join('');
}

export async function generateCodeChallenge(verifier: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return btoa(String.fromCharCode(...new Uint8Array(digest)))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}
```

#### Redirect to Auth Provider

```ts
const verifier = generateCodeVerifier();
localStorage.setItem('code_verifier', verifier);
const challenge = await generateCodeChallenge(verifier);

window.location.href = `https://oauth.provider.com/auth?` +
  `response_type=code&client_id=...&redirect_uri=...&code_challenge=${challenge}&code_challenge_method=S256`;
```

---

### 🐍 FastAPI (Backend)

#### `/callback` endpoint

```python
@app.post("/auth/callback")
async def auth_callback(code: str = Form(...), verifier: str = Form(...)):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "code_verifier": verifier,
    }

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(TOKEN_ENDPOINT, data=data)
        token_data = token_resp.json()

    # Optional: generate your own JWT/session, or forward access token
    return token_data
```

---

## 🧪 Want It Real?

Let me know:

* OAuth provider (Google, GitHub, Auth0, etc.)
* Do you want **access token forwarding** or custom **JWT issuance**?
* Do you want **refresh token flow**, **secure cookie handling**, and **logout flow**?

I can wire the whole pipeline for you. Want the full [React + FastAPI PKCE template](f), or a [Google OAuth2 example](f)?
