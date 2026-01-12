# PKCE.ts file and FastApi route example

---

Absolutely — here’s a **battle-tested `pkce.ts` file for React** and a matching **FastAPI route** to complete the **OAuth2 Authorization Code with PKCE** flow like a pro. This combo works seamlessly with providers like **Google, GitHub, Auth0**, etc.

---

## ⚛️ `pkce.ts` — React (PKCE Utilities)

```ts
// pkce.ts
export function generateCodeVerifier(length = 64): string {
 const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
 let verifier = '';
 for (let i = 0; i < length; i++) {
  verifier += possible.charAt(Math.floor(Math.random() * possible.length));
 }
 return verifier;
}

export async function generateCodeChallenge(codeVerifier: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await window.crypto.subtle.digest('SHA-256', data);
  const base64Digest = btoa(String.fromCharCode(...new Uint8Array(digest)))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
  return base64Digest;
}
```

---

## 🔁 Example Usage in React

```tsx
// LoginButton.tsx
import { generateCodeVerifier, generateCodeChallenge } from './pkce';

const CLIENT_ID = "your-client-id.apps.googleusercontent.com";
const REDIRECT_URI = "http://localhost:3000/callback";

export async function handleOAuthLogin() {
  const verifier = generateCodeVerifier();
  localStorage.setItem('pkce_verifier', verifier);

  const challenge = await generateCodeChallenge(verifier);

  const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?` +
    new URLSearchParams({
      response_type: "code",
      client_id: CLIENT_ID,
      redirect_uri: REDIRECT_URI,
      scope: "openid email profile",
      code_challenge: challenge,
      code_challenge_method: "S256",
      access_type: "offline",
    }).toString();

  window.location.href = authUrl;
}
```

---

## 🐍 FastAPI Backend — Callback + Token Exchange

### 🔑 Required Environment Setup

```env
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret (optional with PKCE)
REDIRECT_URI=http://localhost:3000/callback
TOKEN_URL=https://oauth2.googleapis.com/token
```

---

### 🔧 FastAPI Route: `/auth/callback`

```python
# auth_routes.py
from fastapi import APIRouter, Request, HTTPException, Form
import httpx
import os

router = APIRouter()

@router.post("/auth/exchange")
async def exchange_code_for_token(
    code: str = Form(...),
    code_verifier: str = Form(...),
):
    token_url = "https://oauth2.googleapis.com/token"  # or GitHub/Auth0 token URL
    redirect_uri = os.getenv("REDIRECT_URI")
    client_id = os.getenv("CLIENT_ID")

    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "code_verifier": code_verifier,
        "redirect_uri": redirect_uri,
    }

    headers = { "Content-Type": "application/x-www-form-urlencoded" }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Token exchange failed")

    token_response = response.json()
    return token_response  # or issue your own JWT here
```

---

## 🔁 React Callback Page Example

```tsx
// Callback.tsx
import { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';

export function Callback() {
 const [searchParams] = useSearchParams();

 useEffect(() => {
  const code = searchParams.get('code');
  const verifier = localStorage.getItem('pkce_verifier');

  if (code && verifier) {
   const form = new FormData();
   form.append("code", code);
   form.append("code_verifier", verifier);

   fetch("http://localhost:8000/auth/exchange", {
    method: "POST",
    body: form,
   })
    .then((res) => res.json())
    .then((data) => {
     console.log("Token response:", data);
     // store token or redirect
    });
  }
 }, []);

 return <div>Loading...</div>;
}
```

---

## 🔐 Next Steps

* 🔄 Add **refresh token flow** to stay logged in.
* 🛡️ Optionally **issue your own JWT** in FastAPI instead of returning Google’s access token.
* 🍪 Store tokens in **HTTP-only cookies** for secure session handling.
* 🚫 Add logout and token revocation.

---

Want a full GitHub/Google OAuth2 FastAPI+React boilerplate repo scaffolded out? I can generate it like a production starter kit.
