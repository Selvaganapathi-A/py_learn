Alright, **`typing.overload`**. This is how you give Python **multiple function signatures** without writing multiple functions—and without lying to the type checker. Used right, it’s elegant. Used wrong, it’s a maintenance hazard.

Let’s get clinical.

---

## What is `@overload`?

**What**
`@overload` lets you define **multiple static type signatures** for **one runtime implementation**.

```python
from typing import overload
```

Key rule:

> **Only one implementation runs at runtime.**
> The rest exist **only for type checkers**.

---

## Why does `overload` exist?

**Why**
Because Python functions often:

* Accept different input types
* Return different output types
* Change behavior based on arguments

Without `overload`, you end up with:

```python
def f(x: Any) -> Any: ...
```

That’s not typing. That’s surrender.

---

## How `overload` works (rules you must follow)

1. Overload signatures:

   * Have **no body** (or `...`)
   * Are stacked
2. The **final function** has the real implementation
3. Runtime ignores overloads entirely

---

## Simple example

```python
from typing import overload

@overload
def parse(value: int) -> int: ...

@overload
def parse(value: str) -> int: ...

def parse(value):
    return int(value)
```

Type checker:

* `parse(10)` → `int`
* `parse("10")` → `int`

Runtime:

* Only the last `parse()` exists

---

## Real-world example (different return types)

```python
from typing import overload

@overload
def get(key: str) -> str: ...

@overload
def get(key: str, default: None) -> str | None: ...

@overload
def get(key: str, default: str) -> str: ...

def get(key, default=None):
    return store.get(key, default)
```

Now callers get **precise return types**.

---

## Disaster Story 💣

A team skipped `@overload` and wrote:

```python
def get(key: str, default=None) -> str | None:
    ...
```

Result:

* Every caller had to handle `None`
* Massive boilerplate
* Missed bugs
* Developer revolt

---

## Solution

Use `@overload` to encode **intent**.

Let the checker enforce correct handling.

---

## `overload` vs runtime branching

### ❌ Wrong

```python
def f(x: int | str) -> int | str:
    ...
```

This tells the checker nothing about *which input gives which output*.

---

### ✅ Correct

```python
@overload
def f(x: int) -> int: ...

@overload
def f(x: str) -> str: ...
```

Now behavior is explicit.

---

## Advanced example (containers)

```python
from typing import overload, Sequence, TypeVar

T = TypeVar("T")

@overload
def first(items: Sequence[T]) -> T: ...

@overload
def first(items: Sequence[T], default: T) -> T: ...

def first(items, default=None):
    return items[0] if items else default
```

---

## Expert Advice 🧠 (Strong Opinions)

* Prefer `@overload` over `Any`
* Keep overload count small (2–4 max)
* Overloads must match implementation behavior exactly
* If overloads get complex → redesign API

---

## What NOT to do in Development 🚫

* ❌ Put logic in overload bodies
* ❌ Mismatch overloads vs implementation
* ❌ Overload everything “just in case”

---

## What NOT to do in Production 🚫🚫

* ❌ Rely on overloads for runtime safety
* ❌ Forget default argument behavior
* ❌ Change implementation without updating overloads

---

## pytest? (Minimal relevance)

Overloads don’t run at runtime.
Test the **implementation behavior**, not the overloads.

```python
def test_parse():
    assert parse("10") == 10
```

Static correctness is handled by the type checker.

---

## Bottom Line (Executive Summary)

* `@overload` = **precise static APIs**
* Zero runtime cost
* Essential for polymorphic functions
* Abuse it and your codebase rots

---

### Want next?

* `@overload` with `Literal`
* Overloads vs `TypeVar`
* Overloads for methods
* Async overload patterns

Call the next topic.
