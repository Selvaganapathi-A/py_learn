# SQL Window functions
<!-- -->
Alright, let’s lock this in cleanly and correctly — **window functions with different FRAME ranges**, both conceptually and in **SQLAlchemy (SQLite-friendly)** terms. No fluff.

---

## 1️⃣ First: WINDOW FRAME ≠ PARTITION ≠ ORDER

A window function has **three independent knobs**:

```sql
FUNCTION(...) OVER (
    PARTITION BY ...
    ORDER BY ...
    ROWS | RANGE BETWEEN <start> AND <end>
)
```

* **PARTITION BY** → grouping (like GROUP BY, but keeps rows)
* **ORDER BY** → logical order inside the partition
* **FRAME (ROWS / RANGE)** → *which neighboring rows participate*

Default (important!):

* If `ORDER BY` exists →
  `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

---

## 2️⃣ FRAME TYPES

### 🔹 `ROWS`

Physical row offsets (position-based)

### 🔹 `RANGE`

Value-based (same ORDER BY value = included)

SQLite supports both, but **RANGE is subtle** and often misunderstood.

---

## 3️⃣ Common WINDOW FRAME RANGES (SQL)

### A. Entire Partition

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
```

Same value repeated on every row.

---

### B. Cumulative (Running Total)

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

Classic running sum.

---

### C. Moving Window (Previous + Current)

```sql
ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
```

---

### D. Moving Window (Centered)

```sql
ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
```

---

### E. Forward-looking Window

```sql
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
```

---

## 4️⃣ SQLAlchemy Syntax (THIS is what you want)

SQLAlchemy exposes frames via:

```python
rows=(start, end)
range_=(start, end)
```

Where:

* `None` → UNBOUNDED
* `0` → CURRENT ROW
* Positive / negative ints → FOLLOWING / PRECEDING

---

## 5️⃣ Real Examples (SQLAlchemy)

Assume model:

```python
class Sale(Base):
    __tablename__ = "sales"
    id = mapped_column(Integer, primary_key=True)
    store = mapped_column(String)
    day = mapped_column(Integer)
    amount = mapped_column(Integer)
```

---

### ✅ 1. Total per store (ENTIRE PARTITION)

```python
total_store = func.sum(Sale.amount).over(
    partition_by=Sale.store,
    rows=(None, None)   # UNBOUNDED PRECEDING → UNBOUNDED FOLLOWING
)
```

**SQL**

```sql
SUM(amount) OVER (
  PARTITION BY store
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

---

### ✅ 2. Running total

```python
running_total = func.sum(Sale.amount).over(
    partition_by=Sale.store,
    order_by=Sale.day,
    rows=(None, 0)
)
```

---

### ✅ 3. Previous + Current row

```python
rolling_2 = func.sum(Sale.amount).over(
    partition_by=Sale.store,
    order_by=Sale.day,
    rows=(-1, 0)
)
```

---

### ✅ 4. Centered 3-row window

```python
rolling_3 = func.avg(Sale.amount).over(
    partition_by=Sale.store,
    order_by=Sale.day,
    rows=(-1, 1)
)
```

---

### ✅ 5. Forward-looking sum

```python
future_sum = func.sum(Sale.amount).over(
    partition_by=Sale.store,
    order_by=Sale.day,
    rows=(0, None)
)
```

---

## 6️⃣ RANGE vs ROWS (Critical Difference)

### RANGE (value-based)

```python
range_sum = func.sum(Sale.amount).over(
    partition_by=Sale.store,
    order_by=Sale.day,
    range_=(-2, 0)
)
```

**Meaning:**

> Include rows where
> `day BETWEEN (current_day - 2) AND current_day`

If multiple rows have the same `day`, **all are included**.

---

### ROWS (position-based)

```python
rows=(-2, 0)
```

> Exactly two rows before + current, regardless of values.

---

## 7️⃣ Functions that IGNORE frames

These **DO NOT CARE** about `ROWS / RANGE`:

* `ROW_NUMBER()`
* `RANK()`
* `DENSE_RANK()`
* `NTILE()`

Frames apply to:

* `SUM`
* `AVG`
* `COUNT`
* `MIN / MAX`
* `FIRST_VALUE / LAST_VALUE`

---

## 8️⃣ LAST_VALUE ⚠️ Gotcha (Very Important)

By default:

```sql
LAST_VALUE(x) OVER (ORDER BY ...)
```

Returns **current row**, not the last row of partition 🤦‍♂️

### Correct usage

```python
last_val = func.last_value(Sale.amount).over(
    partition_by=Sale.store,
    order_by=Sale.day,
    rows=(None, None)
)
```

---

## 9️⃣ Rule of Thumb (Tell-it-like-it-is)

* **Analytics / finance / running totals** → `ROWS`
* **Time-based windows** → `RANGE`
* **SQLite** → prefer `ROWS` unless you *really* know why you want `RANGE`
* Always **explicitly define frames** — never rely on defaults

---

If you want next:

* ✔️ **Lead/Lag with frame tricks**
* ✔️ **Dedup using window functions**
* ✔️ **Window + CTE patterns**
* ✔️ **Performance traps in SQLite window functions**

Say the word — we’ll take it to production-grade.

<!-- -->

<!-- -->
Cache invalidation
<!-- -->

<!-- -->
**Cache invalidation** is the process of removing or updating data in a cache when the underlying data changes, to ensure that clients don’t receive stale or outdated information.

### Why It's Important

Caching improves performance by storing expensive or frequently accessed data, but if the cache isn’t updated when the source data changes, it can lead to:

* **Stale data being served**
* **Inconsistent application behavior**
* **Security or business logic issues**

### Common Cache Invalidation Strategies

1. **Time-based Expiration (TTL - Time to Live):**

   * Cached data expires after a predefined time.
   * Easy to implement, but may serve stale data until TTL expires.

2. **Write-through Cache:**

   * Writes go through the cache and then to the database.
   * Ensures cache and database are consistent, but slower writes.

3. **Write-behind (Write-back) Cache:**

   * Writes are made to the cache first and then asynchronously to the database.
   * Fast writes, but risk of data loss on cache failure.

4. **Cache-aside (Lazy Loading):**

   * Application checks cache first. On a miss, it fetches from DB and updates the cache.
   * Manual cache invalidation required on updates/deletes.

5. **Event-driven Invalidation:**

   * Use database triggers, message queues, or pub/sub systems to invalidate or update cache when data changes.

### The Famous Saying

> "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

Let me know if you want code examples (e.g., in Python, Node.js, Django, etc.).

<!-- -->

<!-- -->
Python+ Fastapi +Postgresql + tinydb
<!-- -->

<!-- -->
To use **Python**, **FastAPI**, **PostgreSQL**, and **TinyDB** together, you're likely combining a **relational database (PostgreSQL)** for core persistent storage with a **lightweight NoSQL database (TinyDB)** for caching, logging, or temporary/local storage.

Here's an overview of how you might use these tools together, followed by a basic example:

---

### **Common Use Cases for This Stack**

* **PostgreSQL**: Primary database for structured, relational data.
* **TinyDB**: Secondary store for:

  * Caching lightweight or recent data
  * Storing settings/preferences
  * Temporary offline storage (esp. in desktop/local apps)
* **FastAPI**: Web framework to serve APIs
* **Python**: Core logic and ORM (e.g., SQLAlchemy or Tortoise ORM)

---

### **Example: Basic App**

A FastAPI app that stores user data in PostgreSQL and caches recent queries in TinyDB.

#### 1. **Install Dependencies**

```bash
pip install fastapi[all] sqlalchemy asyncpg tinydb uvicorn
```

#### 2. **Directory Structure**

```
app/
├── main.py
├── database.py
├── models.py
├── tinydb_cache.py
```

---

#### 3. **`database.py` – PostgreSQL Setup**

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://user:password@localhost/mydb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

---

#### 4. **`models.py` – SQLAlchemy Model**

```python
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
```

---

#### 5. **`tinydb_cache.py` – TinyDB Helper**

```python
from tinydb import TinyDB, Query
db = TinyDB('cache.json')

def cache_user(user_dict):
    db.upsert(user_dict, Query().id == user_dict['id'])

def get_cached_user(user_id):
    User = Query()
    result = db.search(User.id == user_id)
    return result[0] if result else None
```

---

#### 6. **`main.py` – FastAPI App**

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, models, tinydb_cache

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/user/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    # Try cache first
    cached = tinydb_cache.get_cached_user(user_id)
    if cached:
        return {"source": "cache", "data": cached}

    # Fallback to DB
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = {"id": user.id, "name": user.name, "email": user.email}
    tinydb_cache.cache_user(user_data)
    return {"source": "db", "data": user_data}
```

---

### **Considerations**

* TinyDB is not a replacement for Redis or Memcached in production.
* Use a real caching solution (like Redis) for large-scale apps.
* TinyDB is ideal for small-scale or desktop-based FastAPI apps.

Would you like to expand this with JWT auth, async DB handling, or frontend integration?

<!-- -->

<!-- -->
Yes
<!-- -->

<!-- -->
Great! Let’s expand your stack step-by-step with:

1. **JWT Authentication** (using `fastapi-jwt-auth` or `fastapi-users`)
2. **Async PostgreSQL Access** (using `SQLModel` or `Tortoise ORM`)
3. **Frontend Integration** (likely React, let me know if different)

---

### **Step 1: Add JWT Authentication**

We'll use `fastapi-jwt-auth` for simplicity.

#### Install

```bash
pip install fastapi-jwt-auth passlib[bcrypt] python-dotenv
```

#### Example Snippet

```python
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key: str = "super-secret"

@AuthJWT.load_config
def get_config():
    return Settings()
```

Then create `/login` and `/protected` endpoints. Want a full working auth example?

---

### **Step 2: Use Async PostgreSQL**

If you're moving from SQLAlchemy sync to async, use:

```bash
pip install asyncpg sqlalchemy[asyncio]
```

Or consider switching to **SQLModel** or **Tortoise ORM** (fully async and FastAPI-friendly). Tortoise example:

```bash
pip install tortoise-orm
```

Let me know your preference (continue with SQLAlchemy async or use SQLModel/Tortoise).

---

### **Step 3: Frontend Integration**

Assuming you're using **React**:

* Use `axios` or `fetch` to call FastAPI endpoints.
* Store JWT tokens in localStorage or httpOnly cookies.
* Use protected routes with token validation.

Would you like a sample login page in React with FastAPI backend token auth?

---

Tell me which part you want to build out next:

* Full JWT auth (login/register/protected)
* Async PostgreSQL with migration
* React login + dashboard with protected API calls
* Or all of the above in a mini project?

I can generate the full codebase step-by-step.

<!-- -->

<!-- -->
Jwt Authentication with login get user  and authentication
<!-- -->

<!-- -->
Let’s implement **JWT authentication with FastAPI** to support:

1. **User registration**
2. **Login with JWT token generation**
3. **Authenticated route to get current user**

We’ll use:

* `fastapi`
* `fastapi-jwt-auth`
* `sqlalchemy` (sync or async)
* `passlib` for password hashing

---

### **Step 1: Install Dependencies**

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary passlib[bcrypt] fastapi-jwt-auth python-dotenv
```

---

### **Step 2: `models.py` – User Table**

```python
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
```

---

### **Step 3: `schemas.py` – Pydantic Schemas**

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        orm_mode = True
```

---

### **Step 4: `auth.py` – JWT & Auth Logic**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from passlib.hash import bcrypt
from models import User
from schemas import UserCreate, UserLogin, UserOut
from database import get_db

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed = bcrypt.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not bcrypt.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = Authorize.create_access_token(subject=db_user.username)
    return {"access_token": access_token}

@router.get("/me", response_model=UserOut)
def get_user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    username = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

### **Step 5: `main.py`**

```python
from fastapi import FastAPI
from database import engine, Base
from auth import router as auth_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
```

---

### **Step 6: JWT Settings (`main.py` or separate)**

```python
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key: str = "super-secret"  # Load from .env in prod

@AuthJWT.load_config
def get_config():
    return Settings()
```

---

### Optional: `.env` and load with `python-dotenv`

---

Would you like this upgraded to **async** with `asyncpg` or use `Tortoise ORM`? Or should I show you the **React frontend** to connect to these endpoints?

<!-- -->

<!-- -->
Whata tortoise orm and explain with fastapi

What it is different from sqlalchemy
<!-- -->

<!-- -->
**Tortoise ORM** is a modern, easy-to-use **async ORM** for Python, designed with simplicity and asyncio support in mind. It integrates very smoothly with **FastAPI**, which is also async-native.

---

### **How It Differs from SQLAlchemy**

| Feature            | **Tortoise ORM**                 | **SQLAlchemy**                            |
| ------------------ | -------------------------------- | ----------------------------------------- |
| **Style**          | Django-like, simple, declarative | Very flexible, but more verbose           |
| **Async support**  | Native, built-in                 | Only supported in newer versions (`1.4+`) |
| **Learning curve** | Easier for beginners             | Steeper, more powerful and lower-level    |
| **Migrations**     | Uses `aerich`                    | Uses `alembic`                            |
| **Best use case**  | FastAPI, asyncio-based apps      | Works in any sync/async Python project    |

---

### **Tortoise ORM + FastAPI Example**

#### 1. **Install**

```bash
pip install tortoise-orm fastapi uvicorn passlib[bcrypt] python-dotenv
pip install aerich  # For migrations
```

---

#### 2. **Define Models (`models.py`)**

```python
from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=128)

    def __str__(self):
        return self.username
```

---

#### 3. **Tortoise Config (`tortoise_config.py`)**

```python
TORTOISE_ORM = {
    "connections": {"default": "postgres://user:password@localhost:5432/mydb"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # Add aerich for migrations
            "default_connection": "default",
        },
    },
}
```

---

#### 4. **FastAPI Integration (`main.py`)**

```python
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise_config import TORTOISE_ORM

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
```

---

#### 5. **Using Async in Endpoints**

```python
from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
from models import User

router = APIRouter()

@router.post("/register")
async def register(username: str, email: str, password: str):
    hashed = bcrypt.hash(password)
    user = await User.create(username=username, email=email, hashed_password=hashed)
    return {"id": user.id, "username": user.username}
```

---

#### 6. **Run Migrations with Aerich**

```bash
aerich init -t tortoise_config.TORTOISE_ORM
aerich init-db
aerich migrate
aerich upgrade
```

---

### **Summary**

* **Use Tortoise ORM** if you're building an async app (like with FastAPI) and want something lightweight, simple, and async-native.
* **Use SQLAlchemy** if you need advanced features, complex queries, or want a more established ecosystem with sync/async flexibility.

---

Want me to give you a full FastAPI + Tortoise + JWT setup next?

<!-- -->

<!-- -->
Document based database like mongodb

<!-- -->

<!-- -->
A **document-based database** like **MongoDB** is a type of **NoSQL database** that stores data in **JSON-like documents** (usually BSON internally). Unlike relational databases (e.g., PostgreSQL), document databases are **schema-less**, which means you can store flexible, nested, and dynamic data structures.

---

### **Key Features of Document-Based Databases (e.g., MongoDB)**

| Feature                         | Description                                                   |
| ------------------------------- | ------------------------------------------------------------- |
| **Schema-less**                 | Each document can have a different structure                  |
| **JSON-like storage**           | Data is stored as documents (key-value pairs, nested objects) |
| **Great for unstructured data** | Ideal for logs, user-generated content, configs               |
| **Flexible querying**           | Use rich query languages (filters, projections, etc.)         |
| **Scalability**                 | Easy to shard and scale horizontally                          |
| **Embedded documents**          | Supports nested/related data within a single document         |

---

### **MongoDB with FastAPI**

You can use `motor` (an async MongoDB driver) with FastAPI.

#### 1. **Install**

```bash
pip install motor pymongo fastapi uvicorn
```

---

#### 2. **Connect to MongoDB**

```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["mydatabase"]
collection = db["users"]
```

---

#### 3. **Define a Document Schema (Optional with Pydantic)**

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
```

---

#### 4. **CRUD Example**

```python
from fastapi import FastAPI
from bson import ObjectId

app = FastAPI()

@app.post("/users")
async def create_user(user: User):
    result = await collection.insert_one(user.dict())
    return {"id": str(result.inserted_id)}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
        return user
    return {"error": "User not found"}
```

---

### **When to Use MongoDB over PostgreSQL**

Use MongoDB when:

* Your data is **semi-structured or unstructured**
* You want **flexibility** in schemas
* You need **fast iteration** or **rapid prototyping**
* You’re dealing with **IoT, analytics, logs, or CMS-style apps**

---

Would you like a full **FastAPI + MongoDB + JWT auth** template next?

<!-- -->

<!-- -->
execute .cmd file in git bash in windows 11
<!-- -->

<!-- -->
To execute a `.cmd` file in **Git Bash** on **Windows 11**, you need to run it through the Windows **Command Prompt (cmd.exe)**, because Git Bash itself doesn't natively understand `.cmd` scripts.

---

### ✅ **Correct Syntax (in Git Bash):**

```bash
cmd.exe /c your-script.cmd
```

* `cmd.exe` is the Windows command interpreter.
* `/c` tells it to run the command and then exit.
* `your-script.cmd` is your script file (use the full or relative path).

---

### 📝 **Example:**

```bash
cmd.exe /c "C:\Users\You\Documents\setup.cmd"
```

If the file is in your current directory:

```bash
cmd.exe /c ./setup.cmd
```

---

### 🧠 Pro Tip

If your script uses Windows-only commands (like `dir`, `set`, `call`, `pause`, etc.), it must be run via `cmd.exe`, not Bash.

---

### ❌ Avoid

```bash
./setup.cmd
```

This will fail or behave unpredictably because Git Bash treats it as a shell script, not a Windows command script.

---

Let me know if you want to trigger it from Python, FastAPI, or via VS Code terminal too.

<!-- -->

<!-- -->
it just opens command prompt. not executing script
<!-- -->

<!-- -->
If running a `.cmd` file from **Git Bash** using `cmd.exe /c script.cmd` **just opens a command prompt but doesn’t execute the script**, here are a few things to troubleshoot and fix:

---

## ✅ **Checklist to Fix `.cmd` Execution in Git Bash**

### 1. **Ensure the file path is correct**

If you're using `./script.cmd`, Git Bash might not resolve it correctly. Use the **full Windows-style path** or convert the path properly.

#### ✅ Working example

```bash
cmd.exe /c "C:\\Users\\YourName\\scripts\\test.cmd"
```

Or convert the path using `pwd -W`:

```bash
cmd.exe /c "$(pwd -W)/test.cmd"
```

---

### 2. **Script Must Have Windows Line Endings**

Make sure the `.cmd` file has **CRLF (Windows)** line endings, not LF (Unix). Use Notepad++ or VS Code to change line endings.

---

### 3. **Check File Content**

Make sure your `.cmd` file contains actual commands, for example:

```cmd
@echo off
echo Hello from CMD script!
pause
```

If it’s blank or has Linux-style commands (`#!/bin/bash`, etc.), it won’t work.

---

### 4. **Run with Elevated Permissions (if needed)**

Some `.cmd` scripts require administrator rights. Git Bash won't automatically elevate. Try running Git Bash as Administrator, or manually run the script elevated.

---

### 5. **Try from another shell to confirm**

Test from PowerShell or regular Command Prompt to verify the script works:

```powershell
cmd /c "C:\path\to\your\script.cmd"
```

If it doesn't work there either, the script might be broken.

---

### ✅ Final Working Example (Git Bash)

Assuming `my_script.cmd` is in your current directory:

```bash
cmd.exe /c "$(pwd -W)/my_script.cmd"
```

* `pwd -W` converts Git Bash path to a Windows path (`C:\...`).
* Quotes ensure spaces in paths are handled correctly.

---

Let me know if you want to run it from a Python/FastAPI script or pass arguments to it.

<!-- -->

<!-- -->
Thanks for sharing the code. The issue is that **your table isn't being created** when running `database.py`. Let's break down why:

---

## 🔍 Issue Summary

In your `models.py`:

```python
Column('title', Integer, nullable=False),
Column('description', Integer, nullable=True),
```

You're using `Integer` for both `title` and `description`, which should **probably be `String`**, not `Integer`. This might be causing the metadata binding to misbehave silently or skip due to an invalid schema definition.

Also, in:

```python
Column('created', DateTime(timezone=True), nullable=False, default=func.now),
```

You're passing `func.now` instead of `func.now()` — that’s another likely issue.

---

## ✅ Fix: `models.py` (Update Types + Defaults)

```python
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table, func
from database import table_meta

tasks = Table(
    'tasks',
    table_meta,
    Column('pk', Integer, primary_key=True, autoincrement=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=True),
    Column('is_completed', Boolean, default=False),
    Column('created', DateTime(timezone=True), nullable=False, default=func.now()),
    Column('modified', DateTime(timezone=True), nullable=True),
)
```

---

## 🧪 Also, Confirm `create()` is Called Properly

Your `database.py` does this right:

```python
if __name__ == '__main__':
    main()
```

But make sure you’re running the file like:

```bash
python database.py
```

---

## ✅ Optional: Confirm Table Exists (Debugging Tip)

You can log tables being created:

```python
print(table_meta.tables)
```

Also, turn on echo:

```python
engine: AsyncEngine = create_async_engine(URL, echo=True)
```

This shows SQL being run, which helps verify if `CREATE TABLE` is executed.

---

## ✅ After Fixing

1. Delete `todo.db3` if it already exists (so schema recreates).
2. Run:

```bash
python database.py
```

3. You should now see SQL statements like:

```sql
CREATE TABLE tasks ...
```

---

Let me know if you want to switch to SQLAlchemy ORM models instead of raw `Table`, or need the CRUD endpoints too.

<!-- -->
