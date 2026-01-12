Good question set. These five form **Python’s object model spine**. If you really get them, inheritance, mixins, and metaclasses stop feeling “magical” and start feeling mechanical (in a good way).

I’ll go **top-down, lifecycle-first**, with sharp rules and typed examples.

---

# `class`, `__new__`, `__init__`, `super()`, `__init_subclass__`

## Big Picture (Read This First)

Object creation happens in **this exact order**:

```text
class statement
  ↓
metaclass.__new__      → class object created
metaclass.__init__
  ↓
__init_subclass__      → runs on parent classes
  ↓
instance = Class()
  ↓
Class.__new__          → instance created
Class.__init__         → instance initialized
```

If this flow clicks, everything else follows.

---

## 1️⃣ `class` — Class Definition Time

`class` is **executable code**, not a declaration.

```python
class User:
    role: str = "user"
```

What Python really does:

```python
User = type(
    "User",
    (),
    {"role": "user"}
)
```

Key truths:

* Class bodies execute top-to-bottom
* Variables become class attributes
* Methods are functions stored on the class
* The result is a **class object**

Classes are **objects**, not keywords pretending to be types.

---

## 2️⃣ `__new__` — Object Creation (Rare, Powerful)

### What It Is

`__new__` **creates** the instance.
It runs **before** `__init__`.

Signature:

```python
def __new__(cls, *args, **kwargs) -> Self
```

### When You Use It

Use `__new__` only when you must:

* Control instance creation
* Enforce singletons
* Return cached / pooled objects
* Subclass immutable types (`int`, `str`, `tuple`)

### Example: Singleton (Clean, Typed)

```python
from typing import Self

class Singleton:
    _instance: Self | None = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

If you don’t know *why* you need `__new__`, you probably don’t.

---

## 3️⃣ `__init__` — Object Initialization (Common)

### What It Is

`__init__` **configures** an already-created object.

Signature:

```python
def __init__(self, ...) -> None
```

### Key Rule

> `__init__` **must not return anything**

### Example

```python
class User:
    def __init__(self, name: str) -> None:
        self.name = name
```

Think of `__new__` as **allocating memory**,
and `__init__` as **setting values**.

---

## 4️⃣ `super()` — Cooperative Inheritance (Not “Parent Call”)

### What `super()` Really Does

`super()` does **not** mean “call my parent”.

It means:

> **Call the next method in the MRO**

That distinction matters a lot with mixins.

---

### Example: Correct `super()` Usage

```python
class Base:
    def __init__(self) -> None:
        print("Base")

class AuditMixin:
    def __init__(self) -> None:
        print("Audit")
        super().__init__()

class Service(AuditMixin, Base):
    def __init__(self) -> None:
        print("Service")
        super().__init__()
```

Execution:

```text
Service → Audit → Base
```

If even **one** class skips `super()`, the chain breaks.

---

### Rule of Thumb

✔ Always use `super()` in multiple inheritance
🚫 Never hardcode parent class names

---

## 5️⃣ `__init_subclass__` — Hook Into Subclass Creation

### What It Is

`__init_subclass__` runs **when a class is subclassed**.

It is:

* Lighter than metaclasses
* Safer
* Easier to reason about

### Signature

```python
def __init_subclass__(cls, **kwargs) -> None
```

---

### Example: Enforcing Class Rules

```python
class Base:
    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "id"):
            raise TypeError(f"{cls.__name__} must define 'id'")
        super().__init_subclass__()
```

```python
class User(Base):
    id: int = 1   # OK
```

```python
class Bad(Base):
    pass          # 💥 TypeError
```

This is **class-time validation**, not runtime.

---

## `__init_subclass__` vs Metaclass

| Need                       | Use                 |
| -------------------------- | ------------------- |
| Simple subclass validation | `__init_subclass__` |
| Modify class namespace     | Metaclass           |
| Enforce contracts          | `__init_subclass__` |
| Build ORMs / DSLs          | Metaclass           |

Use `__init_subclass__` **by default**.
Escalate to metaclasses only when forced.

---

## Side-by-Side Summary (Straight Talk)

| Feature             | Operates On  | When           | Typical Use              |
| ------------------- | ------------ | -------------- | ------------------------ |
| `class`             | Class object | Definition     | Structure                |
| `__new__`           | Instance     | Creation       | Control allocation       |
| `__init__`          | Instance     | Initialization | Assign state             |
| `super()`           | MRO          | Method call    | Cooperative inheritance  |
| `__init_subclass__` | Subclass     | Class creation | Validation, registration |

---

## One Mental Model (Keep This)

> **`__new__` creates
> `__init__` configures
> `super()` cooperates
> `__init_subclass__` enforces
> `class` executes**

That’s the whole system.

---

## Hard Advice (No Sugar-Coating)

* 90% of Python devs never need `__new__`
* 80% misuse `super()`
* 70% overuse inheritance
* 100% benefit from understanding `__init_subclass__`

Master these and Python stops fighting you.

---

If you want next:

* full lifecycle diagram with metaclasses
* `__slots__` interaction
* async `__init__` patterns (and why they’re tricky)
* how Django / SQLAlchemy wire this together
* real bug stories caused by bad `super()` usage

Say the word.
<!--  -->
<!--

Oh yes. These are **real, expensive, production-grade bugs** caused by bad `super()` usage. Not toy examples. These are the kind that pass tests, ship to prod, and then light dashboards on fire.

I’ll give you **patterns**, **why they happen**, and **how to bullet-proof yourself**.

-->

---

# Real Bug Stories Caused by `super()` Misuse

## 🧨 Bug #1: “Why Is My Base Class Not Running?”

### Symptom

* Logs missing
* DB session not initialized
* Middleware silently skipped

### Root Cause

One class in the inheritance chain **forgot to call `super()`**.

### Code That Caused It

```python
class Base:
    def __init__(self) -> None:
        self.db_ready = True

class LoggingMixin:
    def __init__(self) -> None:
        print("Logging started")
        # 🚫 forgot super()

class Service(LoggingMixin, Base):
    def __init__(self) -> None:
        super().__init__()
```

### What Happened

```python
Service()  # Base.__init__ NEVER RUNS
```

No error. No warning. Just broken state.

### Why This Is Dangerous

* Python assumes cooperative inheritance
* One bad actor breaks the entire chain
* Debugging takes hours because nothing crashes

### Fix (Non-Negotiable)

```python
class LoggingMixin:
    def __init__(self) -> None:
        print("Logging started")
        super().__init__()
```

---

## 🧨 Bug #2: “super() Called the Wrong Parent”

### Symptom

* Methods execute out of order
* Business rules applied incorrectly
* Side effects doubled or skipped

### Root Cause

Misunderstanding that `super()` ≠ “call my parent”

### Code

```python
class A:
    def process(self) -> None:
        print("A")

class B(A):
    def process(self) -> None:
        print("B")
        super().process()

class C(A):
    def process(self) -> None:
        print("C")
        super().process()

class D(B, C):
    pass
```

### Output

```text
B → C → A
```

Developer expected:

```text
B → A
```

### Why This Happens

MRO for `D`:

```python
(D, B, C, A, object)
```

`super()` follows **MRO**, not the inheritance tree you imagine.

### Fix

Know your MRO:

```python
print(D.__mro__)
```

Design mixins to be **order-agnostic**.

---

## 🧨 Bug #3: Double Initialization (Silent Data Corruption)

### Symptom

* Counters increment twice
* Resources allocated twice
* Locks acquired twice

### Root Cause

Calling parent explicitly **and** using `super()`

### Code

```python
class Base:
    def __init__(self) -> None:
        print("Base init")

class Child(Base):
    def __init__(self) -> None:
        Base.__init__(self)   # 🚫
        super().__init__()    # 🚫
```

### Result

```text
Base init
Base init
```

### Real-World Impact

* Double DB connections
* Double API calls
* Double billing (yes, this has happened)

### Fix (Hard Rule)

> **Never mix explicit parent calls with `super()`**

Use one. Always `super()`.

---

## 🧨 Bug #4: Diamond Inheritance Explosion

### Symptom

* Base logic executed multiple times
* Hard-to-reproduce bugs
* Behavior differs by class order

### Code

```python
class Base:
    def __init__(self) -> None:
        print("Base")

class Left(Base):
    def __init__(self) -> None:
        print("Left")
        super().__init__()

class Right(Base):
    def __init__(self) -> None:
        print("Right")
        super().__init__()

class Child(Left, Right):
    def __init__(self) -> None:
        print("Child")
        super().__init__()
```

### Output (Correct)

```text
Child → Left → Right → Base
```

### Now the Bug

If **any** class does this:

```python
Base.__init__(self)
```

Base runs **multiple times**.

### Fix

* Everyone uses `super()`
* Nobody cheats
* Ever

---

## 🧨 Bug #5: `super()` Without Arguments (Python 2 Muscle Memory)

### Symptom

* Code works in one context, breaks in another
* AttributeError on `super`

### Code

```python
class Bad:
    def __init__(self) -> None:
        super(Bad, self).__init__()  # 🚫
```

Fails when:

* Class is renamed
* Class is subclassed
* Code is refactored

### Fix

Always use:

```python
super().__init__()
```

Zero arguments. Let Python resolve context.

---

## 🧨 Bug #6: `__init_subclass__` Chain Break

### Symptom

* Subclass validation randomly stops working
* Registration logic disappears

### Code

```python
class Base:
    def __init_subclass__(cls) -> None:
        print("Base hook")

class Plugin(Base):
    def __init_subclass__(cls) -> None:
        print("Plugin hook")
        # 🚫 forgot super()
```

### Result

`Base.__init_subclass__` never runs.

### Fix

```python
class Plugin(Base):
    def __init_subclass__(cls) -> None:
        print("Plugin hook")
        super().__init_subclass__()
```

Same rules. Different lifecycle.

---

## 🧨 Bug #7: Async + super() = Hidden Time Bomb

### Symptom

* Background tasks never start
* Event loop warnings
* Random race conditions

### Code

```python
class Base:
    async def start(self) -> None:
        print("Base start")

class Service(Base):
    async def start(self) -> None:
        super().start()  # 🚫 forgot await
```

### Result

Coroutine created. Never awaited. No immediate crash.

### Fix

```python
await super().start()
```

---

## The Golden Rules (Non-Negotiable)

1. **Every class in a cooperative chain must call `super()`**
2. **Never call parent classes directly**
3. **Never mix explicit calls with `super()`**
4. **Assume someone will subclass you**
5. **Print `__mro__` when confused**
6. **If you don’t need multiple inheritance, keep it single**

---

## Corporate-Grade Takeaway

> `super()` is not a convenience.
> It is a **contract**.

Break the contract, and Python will let you.
Quietly. Politely. Catastrophically.

---
<!--
If you want next:

* real Django / SQLAlchemy `super()` bugs
* how to write “super-safe” mixins
* detecting broken super() chains in tests
* refactoring legacy code that abuses inheritance

Say the word.
-->

<!--

Alright, let’s talk about **`__slots__`** — one of Python’s most *misunderstood performance features*. Used right, it’s a scalpel. Used wrong, it’s technical debt with a smile.

I’ll be direct, typed, and practical.

---

 -->

# `__slots__` in Python

## What Is `__slots__`?

`__slots__` tells Python:

> **“These are the only attributes this class will ever have.”**

Instead of storing attributes in a per-instance `__dict__`, Python stores them in a **fixed, compact layout**.

Result:

* Lower memory usage
* Faster attribute access
* Stricter objects

---

## Why `__slots__` Exists

Without slots:

```python
obj.__dict__  # dynamic hash table per instance
```

With slots:

* No `__dict__` (unless you add it)
* No accidental attributes
* Predictable structure

This matters when:

* You have **many instances**
* Objects are **long-lived**
* Memory pressure is real

ORMs, ASTs, compilers, caches — they all care.

---

## Basic Usage (Typed)

```python
class User:
    __slots__ = ("name", "age")

    name: str
    age: int

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
```

```python
u = User("Element", 30)
u.name = "New"
u.email = "x@y.com"  # ❌ AttributeError
```

That error is a **feature**, not a bug.

---

## What You Gain (and Lose)

### ✅ Gains

* ~30–50% memory reduction per instance
* Faster attribute access
* Early detection of typos

### ❌ Losses

* No dynamic attributes
* Some tooling assumes `__dict__`
* Inheritance needs care

This is a trade-off. Always.

---

## `__slots__` + Inheritance (Where Bugs Are Born)

### Parent With Slots

```python
class Base:
    __slots__ = ("id",)

    id: int
```

### Child Must Declare Its Own Slots

```python
class User(Base):
    __slots__ = ("name",)

    name: str
```

Slots are **not merged automatically**.

---

## Allowing `__dict__` Explicitly

If you want slots *and* flexibility:

```python
class Flexible:
    __slots__ = ("name", "__dict__")

    name: str
```

Now:

```python
f = Flexible()
f.name = "ok"
f.extra = 123  # allowed
```

Memory savings partially gone. Be honest about this.

---

## `__slots__` + `super()` (Critical Rule)

When using inheritance **and** `__slots__`:

* Avoid defining `__init__` that skips `super()`
* Slots don’t initialize themselves magically

```python
class Base:
    __slots__ = ("id",)

    def __init__(self, id: int) -> None:
        self.id = id

class User(Base):
    __slots__ = ("name",)

    def __init__(self, id: int, name: str) -> None:
        super().__init__(id)
        self.name = name
```

Miss `super()` → broken state.

---

## `__slots__` + Multiple Inheritance (Danger Zone)

Python requires **slot layout compatibility**.

Bad:

```python
class A:
    __slots__ = ("a",)

class B:
    __slots__ = ("b",)

class C(A, B):
    pass  # 💥 TypeError
```

Fix (shared base):

```python
class Base:
    __slots__ = ()

class A(Base):
    __slots__ = ("a",)

class B(Base):
    __slots__ = ("b",)

class C(A, B):
    __slots__ = ()
```

If this looks painful — that’s your signal to rethink design.

---

## `__slots__` vs `@dataclass(slots=True)`

Modern Python made this sane.

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Point:
    x: int
    y: int
```

Benefits:

* Automatic `__init__`
* Cleaner typing
* Inheritance handled better
* Much harder to screw up

Strong opinion:

> **Prefer `@dataclass(slots=True)` unless you have a reason not to.**

---

## Slots + Descriptors (Advanced, Powerful)

Descriptors work **perfectly** with slots.

```python
class Positive:
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type | None) -> int:
        return getattr(instance, self.name)

    def __set__(self, instance: object, value: int) -> None:
        if value <= 0:
            raise ValueError("Must be positive")
        setattr(instance, self.name, value)
```

```python
class Account:
    __slots__ = ("balance",)
    balance: int = Positive()
```

Descriptors store data **outside `__dict__`**, so slots don’t block them.

---

## When NOT to Use `__slots__` (Tell-It-Like-It-Is)

Don’t use slots if:

* You’re writing business logic
* Objects are few
* You need flexibility
* You expect frequent refactors

Slots are a **scaling optimization**, not a style choice.

---

## One-Line Mental Model

> **`__slots__` replaces per-instance dictionaries with a fixed memory layout.**

---

## Hard-Won Advice

* Measure memory before and after
* Avoid mixing slots + deep multiple inheritance
* Use dataclasses unless you *need* control
* Document slot usage clearly
* Never add slots “just in case”

---

## Quick Comparison

| Feature     | `__slots__` | Normal class |
| ----------- | ----------- | ------------ |
| Memory      | Low         | Higher       |
| Flexibility | Low         | High         |
| Safety      | High        | Medium       |
| Debugging   | Harder      | Easier       |

---

If you want next:

* real bugs caused by slots
* slots + metaclasses
* slots + pickling
* performance benchmarks
* migrating large codebases to slots safely

Say the word.
