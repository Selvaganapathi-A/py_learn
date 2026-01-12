Alright Element, time to get **Alembic migrations** straight — clean, practical, production-grade. This is one of those things that saves careers when done right 😄📈.

I’ll cover **what, why, how, and the sharp edges**.

---

# What is Alembic (in one sentence)

**Alembic is SQLAlchemy’s schema migration engine** — it versions your database schema so code and database evolve together without chaos.

Think **Git for your database schema**.

---

# Why you absolutely need it

Without Alembic:

* Manual `ALTER TABLE` (human error factory)
* Prod ≠ Dev ≠ Test
* Rollbacks are nightmares

With Alembic:

* Versioned, repeatable schema changes
* Upgrade + downgrade support
* CI/CD friendly
* Zero-guesswork deployments

---

# Basic Setup (SQLAlchemy 2.x)

### 1️⃣ Install

```bash
pip install alembic
```

---

### 2️⃣ Initialize Alembic

Run this **once** in your project root:

```bash
alembic init alembic
```

Creates:

```
alembic/
 ├── versions/
 ├── env.py
 ├── script.py.mako
alembic.ini
```

---

### 3️⃣ Configure `alembic.ini`

Set your DB URL:

```ini
sqlalchemy.url = sqlite:///app.db
```

(or PostgreSQL / MySQL etc.)

---

### 4️⃣ Connect Alembic to your models (CRITICAL)

In `alembic/env.py`:

```python
from myapp.db.base import Base   # your declarative Base

target_metadata = Base.metadata
```

If you skip this → **autogenerate does nothing**.

---

# Creating Migrations

### 🔹 Autogenerate (99% of use cases)

```bash
alembic revision --autogenerate -m "add users table"
```

This:

* Compares **models vs DB**
* Generates `upgrade()` and `downgrade()`

---

### 🔹 Manual migration (when autogen fails)

```bash
alembic revision -m "custom migration"
```

You write SQL yourself.

---

# Migration File Anatomy

```python
def upgrade():
    op.add_column(
        "user",
        sa.Column("email", sa.String(), nullable=True)
    )

def downgrade():
    op.drop_column("user", "email")
```

**Rules:**

* `upgrade()` → move schema forward
* `downgrade()` → reverse it (don’t be lazy)

---

# Running Migrations

### Apply all pending migrations

```bash
alembic upgrade head
```

### Roll back one version

```bash
alembic downgrade -1
```

### Roll back to specific revision

```bash
alembic downgrade <revision_id>
```

---

# Common Operations (Cookbook)

## Add Column

```python
op.add_column(
    "user",
    sa.Column("age", sa.Integer(), nullable=True)
)
```

---

## Drop Column

```python
op.drop_column("user", "age")
```

---

## Rename Column (SQLite pain point ⚠️)

SQLite does NOT support rename column natively pre-3.25.

Alembic workaround:

```python
with op.batch_alter_table("user") as batch:
    batch.alter_column("old_name", new_column_name="new_name")
```

Use **batch mode** always for SQLite.

---

## Create Index

```python
op.create_index(
    "ix_user_email",
    "user",
    ["email"],
    unique=True
)
```

---

## Foreign Key

```python
op.create_foreign_key(
    "fk_post_user",
    "post", "user",
    ["user_id"], ["id"]
)
```

---

## Unique Constraint

```python
op.create_unique_constraint(
    "uq_user_email",
    "user",
    ["email"]
)
```

---

# SQLite-Specific Rules (Read This Twice)

SQLite is **schema-limited**. Alembic handles it via **batch mode**.

### Always do this for ALTERs

```python
with op.batch_alter_table("user") as batch:
    batch.add_column(sa.Column("phone", sa.String()))
```

Alembic will:

* Create temp table
* Copy data
* Drop old table
* Rename

Slow? Yes.
Safe? Also yes.

---

# Version Table (alembic_version)

Alembic stores applied migrations in:

```sql
alembic_version
```

**Never modify manually** unless you know exactly what you’re doing.

---

# Production Best Practices (Non-Negotiable)

✔ One migration per logical change
✔ Never edit old migrations after prod
✔ Always test `downgrade()`
✔ Run migrations in CI
✔ Use **explicit naming** (constraints, indexes)
✔ Avoid data + schema change in same migration (if possible)

---

# Data Migration Example

```python
def upgrade():
    op.execute("""
        UPDATE user
        SET email = lower(email)
    """)
```

Yes, raw SQL is allowed. Use it wisely.

---

# Disaster Story (Real World 💣)

> Team deleted a column in models, ran `autogenerate`, deployed.
> Alembic happily dropped the column in prod.
> No backup. No downgrade.
> Career-limiting event.

### Fix

* Review migrations
* Protect destructive ops
* Use `--sql` mode to preview:

```bash
alembic upgrade head --sql
```

---

# Mental Model (Remember This)

* **Models describe desired state**
* **Alembic describes the path**
* **Database only knows history**

---

If you want next:

* ✔️ Alembic + SQLAlchemy 2.0 async
* ✔️ Multiple DBs / multiple metadata
* ✔️ Data backfills safely
* ✔️ Zero-downtime migrations
* ✔️ Squashing migrations

Say the word — we’ll make your migrations bulletproof 🚀
