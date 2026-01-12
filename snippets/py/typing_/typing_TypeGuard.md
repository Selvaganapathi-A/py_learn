Alright, **`TypeGuard`** is where Python typing stops being passive documentation and starts acting like a **control system**. This one matters.

---

## What is `TypeGuard`?

**What**
`TypeGuard[T]` tells a **static type checker**:

> “If this function returns `True`, the input value is of type `T`.”

It is used to write **custom type-narrowing functions**.

```python
from typing import TypeGuard
```

---

## Why does `TypeGuard` exist?

**Why**
Because `isinstance()` isn’t enough.

Type checkers **cannot infer**:

* Structural checks
* Value-based logic
* Complex validation
* Dictionary shapes
* Protocol-like behavior

`TypeGuard` lets *you* teach the checker.

---

## Which Python versions support it?

* Python **3.10+** → `typing.TypeGuard`
* Earlier → `typing_extensions.TypeGuard`

You’re on **Python 3.14** → you’re good.

---

## How does `TypeGuard` work?

### Simple example (basic narrowing)

```python
from typing import TypeGuard

def is_int(val: object) -> TypeGuard[int]:
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

Type checker understands the narrowing.

---

## Real-world example (dict validation)

### Problem (classic pain)

```python
def handle(data: dict):
    print(data["id"] + 1)  # 💥 maybe not int
```

---

### Solution with `TypeGuard`

```python
from typing import TypeGuard, TypedDict

class User(TypedDict):
    id: int
    name: str

def is_user(data: dict) -> TypeGuard[User]:
    return (
        isinstance(data.get("id"), int)
        and isinstance(data.get("name"), str)
    )
```

Usage:

```python
def handle(data: dict):
    if is_user(data):
        print(data["id"] + 1)   # safe
        print(data["name"].upper())
    else:
        raise ValueError("Invalid user")
```

---

## Disaster Story 💣

A backend accepted JSON as `dict[str, Any]`.

A missing key caused:

* KeyError
* Partial DB writes
* Inconsistent state

They *assumed* validation happened upstream.

---

## Solution to That Disaster

`TypeGuard` forces:

* Explicit checks
* Type-safe access
* Cleaner control flow

Your checker will scream if you forget to validate.

---

## How `TypeGuard` differs from `bool`

### ❌ Wrong

```python
def is_user(data: dict) -> bool:
    ...
```

Type checker learns **nothing**.

---

### ✅ Correct

```python
def is_user(data: dict) -> TypeGuard[User]:
    ...
```

Now narrowing happens.

---

## Advanced example (list narrowing)

```python
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)
```

Usage:

```python
def process(values: list[object]):
    if is_str_list(values):
        values.append("ok")   # safe
```

---

## Expert Advice 🧠 (Strong Opinions)

* `TypeGuard` is **for checkers, not runtime**
* Runtime safety is **your responsibility**
* Never lie in a `TypeGuard` — that’s worse than `cast()`
* Prefer `TypeGuard` over `cast()` whenever possible

---

## What NOT to do in Development 🚫

* ❌ Return `True` without full validation
* ❌ Use `TypeGuard` to silence errors
* ❌ Assume it enforces anything at runtime

---

## What NOT to do in Production 🚫🚫

* ❌ Trust unvalidated data
* ❌ Skip error handling after guards
* ❌ Mix partial validation with full access

---

## pytest Test (YES, necessary)

You **must** test guards — lies cause bugs.

```python
def test_is_user_valid():
    assert is_user({"id": 1, "name": "Alice"})

def test_is_user_invalid():
    assert not is_user({"id": "1"})
```

---

## TypeGuard vs Alternatives (Quick Matrix)

| Tool           | Use case         |
| -------------- | ---------------- |
| `isinstance`   | Simple types     |
| `TypeGuard`    | Custom narrowing |
| `cast()`       | Last resort      |
| `assert_never` | Exhaustiveness   |
| `TypedDict`    | Structured dicts |

---

## Bottom Line (Executive Summary)

* `TypeGuard` teaches the type checker
* It unlocks safe, expressive narrowing
* It beats `cast()` every time
* It requires honesty and tests

---

## Pro Tip (Next Level)

Python 3.13+ adds **`TypeIs`** (stronger guarantees).
If you want, we can compare **`TypeGuard` vs `TypeIs`** next.

Say the word.
