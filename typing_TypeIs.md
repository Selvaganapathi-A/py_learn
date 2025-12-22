Excellent — **`TypeIs`** is the grown-up evolution of `TypeGuard`. This is modern, precise typing. Let’s get straight to business.

---

## What is `TypeIs`?

**What**
`TypeIs[T]` tells a **static type checker**:

> “If this function returns `True`, the value **is exactly of type `T`**.”

It is a **stronger, stricter form of `TypeGuard`**.

```python
from typing import TypeIs
```

---

## Why does `TypeIs` exist?

**Why**
`TypeGuard` has a weakness:

> It allows **widening** and **lying by omission**.

`TypeIs` fixes that by enforcing **exact narrowing**.

---

## Which Python versions support it?

* Python **3.13+** → `typing.TypeIs`
* Python 3.14 → ✅ supported
* Earlier → ❌ not available

You’re perfectly aligned.

---

## How does `TypeIs` work?

### Simple example

```python
from typing import TypeIs

def is_int(val: object) -> TypeIs[int]:
    return isinstance(val, int)
```

Usage:

```python
def process(x: int | str):
    if is_int(x):
        reveal_type(x)  # int
        print(x + 1)
    else:
        reveal_type(x)  # str
        print(x.upper())
```

Same surface behavior as `TypeGuard` — **stronger guarantees underneath**.

---

## The KEY difference: `TypeGuard` vs `TypeIs`

### 🚨 This is the money slide

### ❌ `TypeGuard` (can widen)

```python
def is_sequence(val: object) -> TypeGuard[list[int]]:
    return isinstance(val, list)
```

This is **lying**:

* It doesn’t check element types
* Type checker still trusts it

---

### ✅ `TypeIs` (must be exact)

```python
def is_int_list(val: object) -> TypeIs[list[int]]:
    return (
        isinstance(val, list)
        and all(isinstance(x, int) for x in val)
    )
```

Now:

* No widening
* No partial truth
* Checker enforces correctness

---

## Real-world example (TypedDict – production-grade)

```python
from typing import TypedDict, TypeIs

class User(TypedDict):
    id: int
    name: str

def is_user(val: object) -> TypeIs[User]:
    return (
        isinstance(val, dict)
        and isinstance(val.get("id"), int)
        and isinstance(val.get("name"), str)
    )
```

Usage:

```python
def handle(val: object):
    if is_user(val):
        print(val["id"] + 1)      # safe
        print(val["name"].upper())
```

---

## Disaster Story 💣

A team used `TypeGuard` for dict validation but forgot a field.

Static checker believed the dict was valid.
Runtime crashed accessing a missing key.
Production incident.

**Root cause:** `TypeGuard` didn’t force completeness.

---

## Solution

Use **`TypeIs`** for **complete, exact checks**.

If the function returns `True`, the value **must fully conform**.

---

## Expert Advice 🧠 (Strong Opinions)

* Prefer `TypeIs` over `TypeGuard` in new code
* Only use `TypeGuard` when **widening is intentional**
* Never “half-check” in `TypeIs`
* If a `TypeIs` function is long, **test it thoroughly**

---

## What NOT to do in Development 🚫

* ❌ Use `TypeIs` with partial validation
* ❌ Skip element checks in containers
* ❌ Replace runtime validation with typing logic

---

## What NOT to do in Production 🚫🚫

* ❌ Trust unchecked external data
* ❌ Silence type errors with `cast()`
* ❌ Treat `TypeIs` as optional documentation

---

## pytest Test (mandatory for `TypeIs`)

```python
def test_is_user_valid():
    assert is_user({"id": 1, "name": "Alice"})

def test_is_user_missing_field():
    assert not is_user({"id": 1})

def test_is_user_wrong_type():
    assert not is_user({"id": "1", "name": "Alice"})
```

If these fail, your typing guarantees are lies.

---

## `TypeIs` vs `TypeGuard` vs `cast()` (Executive Matrix)

| Tool        | Strength | Risk      |
| ----------- | -------- | --------- |
| `cast()`    | Fast     | Very high |
| `TypeGuard` | Flexible | Medium    |
| `TypeIs`    | Exact    | Low       |

---

## Bottom Line (Executive Summary)

* `TypeIs` = **truthful narrowing**
* Stronger than `TypeGuard`
* Ideal for validation-heavy code
* Forces discipline, rewards correctness

---

### Want next?

* `TypeIs` vs `assert_never`
* Migrating from `TypeGuard` to `TypeIs`
* Writing reusable guard libraries
* Static exhaustiveness checking patterns

Say the direction.
