Alright, **`NewType`** — this is where Python typing stops being decorative and starts enforcing **real domain boundaries**. Used well, it saves you from subtle, expensive bugs. Used poorly, it confuses everyone.

Let’s do this properly.

---

## What is `NewType`?

**What**
`NewType` creates a **distinct type** for static type checkers, **without runtime overhead**.

```python
from typing import NewType
```

Example:

```python
UserId = NewType("UserId", int)
```

* Static type: **UserId ≠ int**
* Runtime: `UserId` **is just an `int`**

---

## Why does `NewType` exist?

**Why**
Because *not all ints are equal*.

```python
user_id: int
order_id: int
```

Mix these up → no error → production bug.

`NewType` introduces **semantic correctness**.

---

## Which Python versions support it?

* Python **3.5+**
* Python **3.14** → fully supported

---

## How does `NewType` work?

### Simple example

```python
from typing import NewType

UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)

def get_user(uid: UserId) -> None:
    ...

get_user(UserId(5))     # ✅
get_user(OrderId(5))    # ❌ type checker error
get_user(5)             # ❌ type checker error
```

Runtime:

```python
UserId(5) == 5   # True
```

No wrapper, no class, no cost.

---

## When should you use `NewType`?

Use it when:

* Values share the same underlying type
* Mixing them would be catastrophic
* You want compile-time safety
* You’re modeling **business concepts**

---

## Real-world example (production-grade)

```python
UserId = NewType("UserId", int)
ProductId = NewType("ProductId", int)
Quantity = NewType("Quantity", int)

def place_order(user: UserId, product: ProductId, qty: Quantity):
    ...
```

This prevents entire classes of bugs **before runtime**.

---

## Disaster Story 💣

A payments system used raw `int` IDs.

User IDs were accidentally passed as Account IDs.

Money moved.
Wrong accounts.
Audit nightmare.

All preventable with `NewType`.

---

## Solution

Introduce `NewType` at **API boundaries**:

* Database IDs
* External identifiers
* Money units
* Security tokens

---

## `NewType` vs `TypeAlias` (critical difference)

| Feature          | TypeAlias | NewType |
| ---------------- | --------- | ------- |
| Distinct type    | ❌         | ✅       |
| Prevents mixing  | ❌         | ✅       |
| Runtime cost     | None      | None    |
| Requires casting | Sometimes | Yes     |

### Example

```python
UserId: TypeAlias = int      # alias only
UserId = NewType("UserId", int)  # real distinction
```

---

## How to convert between `NewType` and base type

```python
uid = UserId(10)

raw: int = int(uid)     # unwrap
uid2: UserId = UserId(raw)
```

Be explicit — clarity wins.

---

## Advanced example (NewType + validation)

```python
from typing import NewType

UserId = NewType("UserId", int)

def make_user_id(val: int) -> UserId:
    if val <= 0:
        raise ValueError("Invalid UserId")
    return UserId(val)
```

Now:

* Runtime safety
* Static safety
* Clean API

---

## Expert Advice 🧠 (Strong Opinions)

* Use `NewType` at **system boundaries**
* Don’t wrap everything — be strategic
* Pair with factory functions
* Don’t bypass it with casts casually

---

## What NOT to do in Development 🚫

* ❌ Use `NewType` without naming discipline
* ❌ Skip validation
* ❌ Convert back and forth casually

---

## What NOT to do in Production 🚫🚫

* ❌ Accept raw primitives where `NewType` exists
* ❌ Cast to silence the checker
* ❌ Assume `NewType` enforces runtime checks

---

## pytest Test Example

```python
def test_user_id_valid():
    uid = UserId(5)
    assert int(uid) == 5

def test_user_id_invalid():
    import pytest
    with pytest.raises(ValueError):
        make_user_id(-1)
```

---

## Bottom Line (Executive Summary)

* `NewType` = **domain safety**
* Zero runtime overhead
* Static enforcement only
* Perfect for IDs, units, tokens

---

### Want next?

* `NewType` vs dataclasses
* Using `NewType` with `TypeIs`
* Migrating a legacy codebase
* Units (meters vs feet) done right

Say the direction.
