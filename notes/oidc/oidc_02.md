# FastAPI Identity Provider Code
<!--  -->
You're now stepping into **provider territory** — building a full-fledged **OpenID Connect-compliant Identity Provider (IdP)** using **FastAPI**.

This is an **enterprise-class move**, but you're in luck: `Authlib` has first-class support for building OAuth2 / OIDC **authorization servers**, not just clients.

---

## 🔐 Goal: FastAPI + Authlib as OAuth2 / OIDC Identity Provider (Authorization Server)

### ✅ It will:

* Handle `authorization_code` flow (with PKCE)
* Issue access tokens & ID tokens
* Provide OIDC metadata (`.well-known/openid-configuration`)
* Serve `/authorize`, `/token`, `/userinfo`, etc.

---

## 🧱 Project Structure

```
fastapi_oidc_provider/
├── main.py
├── authlib_server/
│   ├── models.py          # User, Client, Token models
│   ├── oauth2.py          # Authlib server setup
│   ├── endpoints.py       # OAuth2 endpoints
│   └── database.py        # SQLAlchemy DB session
└── .env
```

---

## 🛠️ Setup

### 1️⃣ Install Dependencies

```bash
pip install fastapi[all] authlib sqlalchemy python-jose
```

---

### 2️⃣ `models.py`: User, Client, Token

```python
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from authlib.oauth2.rfc6749 import ClientMixin, TokenMixin
from authlib.oidc.core import UserInfo

from .database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)  # Use hashing!

    def get_user_id(self):
        return self.id

    def get_user_info(self, scope):
        return UserInfo(sub=str(self.id), name=self.username, email=self.email)

class OAuth2Client(Base, ClientMixin):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    client_id = Column(String, unique=True, nullable=False)
    client_secret = Column(String)
    redirect_uris = Column(Text)
    scope = Column(Text)
    response_types = Column(Text)
    grant_types = Column(Text)
    token_endpoint_auth_method = Column(String)

class OAuth2Token(Base, TokenMixin):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    client_id = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    access_token = Column(String, unique=True)
    refresh_token = Column(String, unique=True)
    scope = Column(String)
    issued_at = Column(Integer)
    expires_in = Column(Integer)
```

---

### 3️⃣ `database.py`: SQLAlchemy Engine

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

---

### 4️⃣ `oauth2.py`: Authlib OAuth2 Server

```python
from authlib.integrations.starlette_oauth2 import AuthorizationServer
from authlib.oidc.core.grants import OpenIDCode
from authlib.oauth2.rfc7636 import CodeChallenge
from .models import OAuth2Client, OAuth2Token, User
from .database import SessionLocal

def query_client(client_id):
    db = SessionLocal()
    return db.query(OAuth2Client).filter_by(client_id=client_id).first()

def save_token(token, request):
    db = SessionLocal()
    item = OAuth2Token(**token, client_id=request.client.client_id, user_id=request.user.id)
    db.add(item)
    db.commit()

authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token
)

class MyOpenIDCode(OpenIDCode):
    def authenticate_user(self, authorization_code):
        return authorization_code.user

def configure_oauth_server(app):
    from authlib.oauth2.rfc6749.grants import AuthorizationCodeGrant

    class MyAuthorizationCodeGrant(AuthorizationCodeGrant):
        def create_authorization_code(self, client, grant_user, request):
            code = super().create_authorization_code(client, grant_user, request)
            code['code_challenge'] = request.data.get('code_challenge')
            code['code_challenge_method'] = request.data.get('code_challenge_method')
            return code

        def parse_authorization_code(self, code, client):
            # Lookup code in DB
            return super().parse_authorization_code(code, client)

    authorization.register_grant(MyOpenIDCode, [CodeChallenge(required=True)])
```

---

### 5️⃣ `endpoints.py`: Authorization, Token, Userinfo

```python
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, JSONResponse
from .oauth2 import authorization
from .models import User

router = APIRouter()

@router.get("/authorize")
async def authorize(request: Request, user: User = Depends(...)):
    # Authenticate user (use your own logic)
    grant = await authorization.get_consent_grant(request, end_user=user)
    return JSONResponse(grant)

@router.post("/authorize")
async def approve_authorize(request: Request, user: User = Depends(...)):
    return await authorization.create_authorization_response(request, grant_user=user)

@router.post("/token")
async def issue_token(request: Request):
    return await authorization.create_token_response(request)

@router.get("/userinfo")
async def userinfo(request: Request):
    token = await authorization.authenticate_token(request)
    user = ...  # lookup from token
    return JSONResponse(user.get_user_info(token.get_scope()))
```

---

### 6️⃣ `main.py`: App Init

```python
from fastapi import FastAPI
from authlib.integrations.starlette_app import StarletteOAuth2App
from authlib.oidc.discovery import create_metadata_response

from authlib_server.oauth2 import authorization, configure_oauth_server
from authlib_server.endpoints import router as oauth_router
from authlib_server.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)
configure_oauth_server(app)

@app.get("/.well-known/openid-configuration")
async def openid_config(request: Request):
    return create_metadata_response(request, issuer='http://localhost:8000')

app.include_router(oauth_router)
```

---

## 🔍 Testing

Once up, you’ll have:

* `/.well-known/openid-configuration` — OIDC discovery
* `/authorize` — user consent login
* `/token` — token endpoint (PKCE supported)
* `/userinfo` — identity claims

Use Postman or a frontend client (React with `oidc-client-ts`) to test the full **Authorization Code + PKCE flow**.

---

## 🏁 Next Steps

* 🔐 Add login UI or form-based authentication
* 🎫 Add client registration & admin UI
* 🕵️‍♂️ JWT signing (use `jose` or `jwcrypto`)
* 🧪 Pytest coverage & DB mocks
* 📜 JWKS endpoint (`/jwks.json`)

---

Would you like me to generate a **fully working GitHub project structure** with these components scaffolded and ready to run?
Or do you want it wired to **React/Next.js frontend** for testing right away?

Let’s scale this into a real IdP product.
