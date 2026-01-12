# Other Authendication Mechanisms
<!--  -->
Here's a no-nonsense breakdown of the **most widely used authentication mechanisms** in modern software systems — what they are, how they work, and when to use them. This is your quick-reference playbook when choosing the right auth strategy.

---

## 🔐 Top Authentication Mechanisms — Explained Like a Pro

| Mechanism                         | Stateless | Use Case                        | Security Level | Complexity           |
| --------------------------------- | --------- | ------------------------------- | -------------- | -------------------- |
| 🔑 API Key                        | ✅         | Public APIs, internal tools     | 🔸 Medium      | 🟢 Easy              |
| 🧾 Basic Auth                     | ✅         | CLI, legacy systems             | 🔸 Medium-Low  | 🟢 Easy              |
| 🍪 Cookie-Session                 | ❌         | Web apps, dashboards            | 🔹 High        | 🟡 Medium            |
| 🪙 JWT (Bearer Token)             | ✅         | SPAs, Mobile APIs               | 🔹 High        | 🟡 Medium            |
| 🌐 OAuth2                         | ✅ / ❌     | 3rd-party login, federated auth | 🔷 Very High   | 🔴 Hard              |
| 🧬 OpenID Connect                 | ✅         | Identity layer on OAuth2        | 🔷 Very High   | 🔴 Hard              |
| 📜 SAML                           | ❌         | Enterprise SSO (HR, ERP)        | 🔷 Very High   | 🔴 Hard              |
| 🔐 Mutual TLS (mTLS)              | ✅         | Backend services                | 🔷 Very High   | 🔴 Hard              |
| 📦 HMAC                           | ✅         | Webhooks, API calls             | 🔹 High        | 🟡 Medium            |
| 🧊 OAuth2 + PKCE                  | ✅         | Mobile, SPA                     | 🔷 Very High   | 🔴 Hard              |
| 🔄 Session Token Rotation         | ❌         | Secure web login                | 🔷 Very High   | 🟡 Medium            |
| 📲 Biometric Auth                 | ✅         | Device-level auth               | 🔷 Very High   | 🔴 Platform-specific |
| 🔁 Passwordless (Magic Link, OTP) | ✅         | Modern apps                     | 🔹 High        | 🟡 Medium            |
| 📧 Email Link Login               | ✅         | SaaS/consumer apps              | 🔹 High        | 🟡 Medium            |
| 🔏 Encrypted JWT (JWE)            | ✅         | Secure token sharing            | 🔷 Very High   | 🔴 Complex           |

---

## 🔍 Detailed Overview of Popular Mechanisms

---

### 1. **Basic Auth**

* 🔁 Sends `username:password` in Base64 on **every request**.
* Must use HTTPS.
* **No session or token**.
* ✅ Good for internal CLI tools.
* ❌ Terrible for modern frontend apps.

---

### 2. **API Key**

* Sends a **key** (like a password) with every request.
* Common for external APIs and microservices.
* 🔐 Use rate limits, scopes, and key rotation.

---

### 3. **Cookie-Based Session**

* Client logs in → server sets a cookie → cookie sent with each request.
* Server maintains session (e.g., in Redis).
* 🔒 Great for SSR web apps.
* Works with CSRF protection and secure cookies.

---

### 4. **JWT (Bearer Token)**

* After login, server issues a **signed token**.
* Client stores in `localStorage` or `memory`.
* Sent via `Authorization: Bearer <token>`.
* ✅ Stateless. Scalable.
* ❗Needs protection from XSS, token expiry, and rotation strategy.

---

### 5. **OAuth 2.0**

* Delegated login via third-party (Google, GitHub).
* Uses **authorization server** to issue access tokens.
* Complex but powerful.
* Grant types: `Authorization Code`, `Client Credentials`, `Password`, `Refresh Token`.

---

### 6. **OpenID Connect (OIDC)**

* Layer on top of OAuth2 to **verify user identity**.
* Returns `id_token` (JWT) with user info.
* Standard for “Sign in with Google”, etc.
* 🔥 Go-to for Single Sign-On (SSO).

---

### 7. **SAML 2.0**

* Enterprise SSO protocol using XML.
* Used in corporate HR systems, intranets.
* Identity Provider (IdP) ↔ Service Provider (SP).
* Complex to implement manually, usually outsourced to Okta, Azure AD.

---

### 8. **Mutual TLS (mTLS)**

* Both server *and* client present certificates.
* Hardcore security: banking, backend microservices.
* Requires PKI infra.
* ✅ Super secure, ❌ not user-friendly.

---

### 9. **HMAC (Hash-based Message Authentication Code)**

* API provider shares a secret with client.
* Client signs each request with a hash (e.g., `HMAC-SHA256`).
* Server recalculates and verifies signature.
* Popular in webhooks (e.g., GitHub, Stripe).

---

### 10. **Passwordless (Magic Link / OTP)**

* User enters email → receives a login link or code → clicks → logged in.
* Removes passwords entirely.
* Frontline tech in modern apps (e.g., Slack, Notion).

---

### 11. **Biometric Auth (Face ID, Touch ID)**

* Used on devices with secure enclaves (TPM).
* Usually tied to device PIN or fallback password.
* Requires platform integration (Android/iOS SDKs).

---

### 12. **OAuth 2.0 + PKCE (Proof Key for Code Exchange)**

* Secure extension for OAuth2 for mobile and SPA apps.
* Prevents interception of the authorization code.
* Standard for secure public clients with no backend (e.g., React frontend).

---

### 13. **Session Token Rotation**

* Session token is rotated on each request or periodically.
* Prevents session fixation or token reuse.
* Harder to hijack even if a token leaks.

---

### 14. **Encrypted JWTs (JWE)**

* Instead of just signing JWTs, encrypt them too.
* Ensures **confidentiality** of payload.
* Used when passing sensitive data across services or trust domains.

---

## 🧠 Choosing the Right Auth Mechanism

| If you're building...  | Use                               |
| ---------------------- | --------------------------------- |
| Public REST API        | API Key or OAuth2                 |
| Web dashboard          | Session Cookie + CSRF             |
| SPA (React, Vue, etc.) | JWT (with refresh token)          |
| Mobile App             | OAuth2 with PKCE                  |
| B2B SSO                | OpenID Connect or SAML            |
| Webhook verification   | HMAC                              |
| Internal microservices | mTLS or API Key with IP whitelist |
| No-password login      | Magic Link / OTP                  |

---

## 🧰 Want Sample Implementations?

I can spin up example code for:

* 🧬 **FastAPI JWT with refresh rotation**
* 🌐 **OAuth2 + PKCE with React**
* 🧾 **Cookie-based session auth**
* 🔏 **JWE-based encrypted token**
* 🔐 **API key management & middleware**

Just say the word.

Let’s build your own **auth layer like a boss**, not a beginner. Want to start with a particular mechanism?
