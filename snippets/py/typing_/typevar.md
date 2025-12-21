Excellent question. This is **core typing theory applied to a very real API design problem**. We’ll go step-by-step, no hand-waving.

---

# TypeVar — bounded, unbounded, variance

…and enforcing **“both arguments must be the same type”**

(Target: Python **3.14** and **3.10 and earlier**)

---

## 1. What is `TypeVar` (at its core)?

A `TypeVar` represents a **type placeholder** that must be **consistently substituted**.

> If `T` becomes `int`, it must be `int` everywhere
> If `T` becomes `str`, it must be `str` everywhere

That property is exactly what you need.

---

## 2. Unbounded TypeVar (default)

### What

An **unbounded** `TypeVar` can be *any* type.

### Syntax (3.10+)

```python
from typing import TypeVar

T = TypeVar("T")
```

### Meaning

* `T` can be `int`, `str`, `Decimal`, or any duck-typed object
* But once chosen, it must stay the same

---

## 3. Enforcing “`a` and `b` must be the same type”

### Your requirement (formalized)

> If `a` is type `X`, then `b` must also be type `X`

This is **exactly** what an unbounded `TypeVar` does.

---

## 4. Generic Function — Python 3.10 and earlier

```python
from typing import TypeVar

T = TypeVar("T")

def fn(a: T, b: T) -> T:
    return a
```

### What this enforces

| Call                             | Valid? | Reason            |
| -------------------------------- | ------ | ----------------- |
| `fn(1, 2)`                       | ✅      | both `int`        |
| `fn("a", "b")`                   | ✅      | both `str`        |
| `fn(Decimal("1"), Decimal("2"))` | ✅      | both `Decimal`    |
| `fn(1, "x")`                     | ❌      | `T` can’t be both |
| `fn(Duck(), Duck())`             | ✅      | same duck type    |

This is **static enforcement** (mypy, pyright, pylance).

---

## 5. Generic Function — Python 3.14 (modern syntax)

Python ≥3.12 introduces **type parameter syntax** (PEP 695).

```python
def fn[T](a: T, b: T) -> T:
    return a
```

Same semantics.
Cleaner.
Less boilerplate.

> Opinionated take:
> **This is the future. Use it wherever allowed.**

---

## 6. Duck typing (your “duck” requirement)

Duck typing works **automatically** as long as both arguments are the same concrete type.

```python
class Duck:
    def quack(self) -> str:
        return "quack"


d1: Duck = Duck()
d2: Duck = Duck()

fn(d1, d2)  # ✅
```

No inheritance required.
No protocol required **unless** you want structural typing across *different* classes.

---

## 7. Bounded TypeVar

### What

A **bounded** `TypeVar` restricts `T` to subclasses of a given type.

### Example

```python
from typing import TypeVar
from numbers import Number

TNum = TypeVar("TNum", bound=Number)

def add(a: TNum, b: TNum) -> TNum:
    return a
```

### Effect

* `int`, `float`, `Decimal` → allowed
* `str` → rejected
* Still enforces **same type**

---

## 8. Constrained TypeVar (explicit options)

```python
from typing import TypeVar
from decimal import Decimal

T = TypeVar("T", int, str, Decimal)
```

This means:

* Only these types are allowed
* Still enforces sameness

Use this **sparingly**. It scales poorly.

---

## 9. Invariance, Covariance, Contravariance (The Truth)

### Default: **Invariant**

```python
T = TypeVar("T")
```

Invariant means:

> `Box[int]` is NOT a `Box[object]`

This is **correct and safe** for most code.

---

## 10. Covariant TypeVar (`out` position)

### What

Allows substitutability in **output-only** positions.

```python
from typing import TypeVar

T_co = TypeVar("T_co", covariant=True)
```

### Example (container)

```python
from typing import Generic

class ReadOnlyBox(Generic[T_co]):
    def __init__(self, value: T_co) -> None:
        self._value = value

    def get(self) -> T_co:
        return self._value
```

Why:

* You never *put* values in
* Only *read* them

---

## 11. Contravariant TypeVar (`in` position)

### What

Used for **consumers** (functions, handlers).

```python
T_contra = TypeVar("T_contra", contravariant=True)
```

### Example

```python
from typing import Protocol

class Consumer(Protocol[T_contra]):
    def consume(self, value: T_contra) -> None: ...
```

This matters in callback-heavy APIs.

---

## 12. Important Rule (Non-Negotiable)

| Variance      | Can be used for your `fn(a, b)`? |
| ------------- | -------------------------------- |
| Invariant     | ✅ REQUIRED                       |
| Covariant     | ❌ unsafe                         |
| Contravariant | ❌ unsafe                         |

Your function needs **invariance** to enforce sameness.

---

## 13. Why `TypeVar` is the *only* correct solution here

Alternatives that **do not work**:

* `Union[int, str, Decimal]` ❌ (allows mixing)
* `Any` ❌ (no enforcement)
* Overloads ❌ (combinatorial explosion)

Only this works:

```python
T = TypeVar("T")

def fn(a: T, b: T) -> T: ...
```

or (3.14):

```python
def fn[T](a: T, b: T) -> T: ...
```

---

## 14. Runtime enforcement? (Important reality check)

Type annotations:

* **Do not enforce at runtime**
* Are for **static analysis**

If you want runtime checks:

```python
def fn(a: T, b: T) -> T:
    if type(a) is not type(b):
        raise TypeError("a and b must be the same type")
    return a
```

Static + runtime = enterprise-grade robustness.

---

## 15. Executive Summary

* **Unbounded `TypeVar`** enforces “same type everywhere”
* This is **exactly** your requirement
* Invariance is mandatory
* Python 3.14 syntax is cleaner, not different in behavior
* Duck typing works naturally
* This pattern is foundational to:

  * math libraries
  * serializers
  * ORMs
  * DI containers

> Final verdict:
> **If two parameters must rise and fall together type-wise, they share a `TypeVar`. Period.**

If you want next-level follow-ups:

* `Protocol` + `TypeVar`
* `TypeGuard`
* Overloads vs generics
* Variance pitfalls in real APIs

Say the next target.
<!--  -->
This warning is **100% correct**, and it’s exposing a **fundamental rule of Python’s type system** that trips up even strong developers.

Let’s break it down cleanly and then fix it **the right way** for **Python 3.14** and **Python ≤3.10**.

---

## Why Pylance Is Complaining (No BS)

Your code:

```python
T = TypeVar("T", int, str, Duck)

def incubate(a: T, b: T) -> T:
    return a + b
```

### What you *intend*

> “`a` and `b` are the same type, and that type supports `+`.”

### What the type checker *actually sees*

* `T` can be **int OR str OR Duck**
* Python typing **does not assume operators exist**
* `Duck` has **no guarantee** of `__add__`
* Even worse: `int + int → int`, `str + str → str`, **but the checker must reason about all possibilities**

### Key rule

> **TypeVar constraints restrict *what* T can be — not *what operations* T supports.**

That’s the core issue.

---

## 🚨 Critical Insight (Tell-it-like-it-is)

`TypeVar("T", int, str, Duck)`
❌ **does NOT mean** “anything with `+`”
✅ **means** “exactly one of these concrete types”

Python typing **does not infer operator compatibility** from that.

---

# ✅ Correct Solutions (Ranked by Professionalism)

---

## ✅ SOLUTION 1 — Structural typing with `Protocol` (BEST PRACTICE)

This is how you express **“supports + and returns same type”**.

### Python 3.10+

```python
from typing import Protocol, TypeVar


T = TypeVar("T", bound="Addable")


class Addable(Protocol):
    def __add__(self: T, other: T) -> T: ...


class Duck:
    def __add__(self, other: "Duck") -> "Duck":
        return Duck()


def incubate(a: T, b: T) -> T:
    return a + b
```

### Why this works

* `Protocol` defines **behavior**, not inheritance
* `self: T` enforces **same-type addition**
* Works for:

  * `int`
  * `str`
  * `Decimal`
  * `Duck`
  * Any duck-typed object

✔ Pylance happy
✔ mypy happy
✔ Extensible
✔ Framework-grade typing

---

## ✅ SOLUTION 2 — Python 3.14+ (Cleaner Syntax, Same Semantics)

Using **PEP 695** syntax:

```python
from typing import Protocol


class Addable[T](Protocol):
    def __add__(self, other: T) -> T: ...


class Duck:
    def __add__(self, other: "Duck") -> "Duck":
        return Duck()


def incubate[T: Addable[T]](a: T, b: T) -> T:
    return a + b
```

> This is the **modern, future-proof form**.

Strong opinion:
**This is how all operator-based generics should be written going forward.**

---

## ⚠️ SOLUTION 3 — Constrained `TypeVar` + overloads (NOT scalable)

```python
from typing import overload
from decimal import Decimal


@overload
def incubate(a: int, b: int) -> int: ...

@overload
def incubate(a: str, b: str) -> str: ...

@overload
def incubate(a: Decimal, b: Decimal) -> Decimal: ...

def incubate(a, b):
    return a + b
```

### Why this is inferior

* Combinatorial explosion
* Every new type = new overload
* Not extensible
* Maintenance nightmare

Use **only** for public APIs with fixed types.

---

## ❌ WHAT DOES NOT WORK (Important)

### ❌ Constrained TypeVar alone

```python
T = TypeVar("T", int, str, Duck)  # ❌ insufficient
```

### ❌ Union

```python
def incubate(a: int | str, b: int | str):  # ❌ allows mixing
```

### ❌ Any

```python
def incubate(a: Any, b: Any):  # ❌ no safety
```

---

## 🧠 Why `Protocol` Is the Right Mental Model

| Concept          | Expresses                     |
| ---------------- | ----------------------------- |
| `TypeVar`        | “same type everywhere”        |
| `Protocol`       | “supports this behavior”      |
| `bound=Protocol` | “same type **with** behavior” |

Your requirement needs **both**.

---

## 🧪 Runtime Enforcement (Optional but Honest)

Typing is static only.
If you want runtime guarantees:

```python
def incubate(a: T, b: T) -> T:
    if type(a) is not type(b):
        raise TypeError("a and b must be same type")
    return a + b
```

Static + runtime = enterprise-grade robustness.

---

## Final Verdict (Straight Talk)

* Pylance is **right**
* Your intent requires **behavioral typing**
* `Protocol + TypeVar` is the **only scalable solution**
* Python 3.14 syntax makes it elegant, not different
* This pattern is used by:

  * numeric libraries
  * ORMs
  * serializers
  * operator-heavy APIs

> **If a type must *do* something, constrain behavior — not identity.**

If you want next-level follow-ups:

* `SupportsAdd` vs custom protocols
* Numeric tower typing
* `TypeGuard` + operator logic
* Async operator protocols

Say the word.
