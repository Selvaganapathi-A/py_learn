Alright, let’s talk about `super()` — the most misunderstood *yet* most mission-critical function in modern Python. This is inheritance hygiene. Get it right, or your architecture rots quietly.

---

# `super()` (Python 3.14)

## 1. What is `super()`?

`super()` returns a **proxy object** that delegates method calls to the **next class in the Method Resolution Order (MRO)**.

Key point:

> `super()` does **not** mean “call the parent class”.

It means:

> **“Call the next implementation in the MRO.”**

That distinction is everything.

---

## 2. Where does `super()` operate?

`super()` is used inside:

* Instance methods
* Class methods
* Special methods (`__init__`, `__init_subclass__`, etc.)

It works with:

* Single inheritance
* Multiple inheritance
* Mixins
* Cooperative class hierarchies

If you’re building extensible systems, `super()` is non-negotiable.

---

## 3. Why does `super()` exist?

Because Python supports **multiple inheritance**, and calling base classes directly:

```python
Base.__init__(self)
```

…is a design trap.

`super()` exists to:

* Prevent duplicated method calls
* Preserve execution order
* Enable mixins
* Keep inheritance chains extensible
* Avoid hard-coding class names

> Strong take:
> **Direct base-class calls are technical debt on day one.**

---

## 4. When should you use `super()`?

### Use `super()` when

* Overriding methods
* Writing mixins
* Designing frameworks or libraries
* You expect your class to be subclassed
* Multiple inheritance is even *possible*

### Don’t use `super()` when

* You are intentionally bypassing cooperative behavior (rare, explicit)
* You’re writing a final, sealed class (and even then… think twice)

---

## 5. How `super()` works (mechanics)

### The MRO (Method Resolution Order)

Python determines method lookup order using **C3 linearization**.

Example:

```python
class A: ...
class B(A): ...
class C(A): ...
class D(B, C): ...
```

MRO of `D`:

```python
[D, B, C, A, object]
```

`super()` walks **forward** through this list.

---

## 6. Simple Example (Correct Usage)

```python
class Base:
    def greet(self) -> None:
        print("Hello from Base")


class Child(Base):
    def greet(self) -> None:
        super().greet()
        print("Hello from Child")
```

Usage:

```python
c: Child = Child()
c.greet()
```

Output:

```
Hello from Base
Hello from Child
```

Clean. Predictable. Extensible.

---

## 7. What `super()` is NOT

### ❌ Not “call my parent”

This breaks in multiple inheritance:

```python
class BadChild(Base):
    def greet(self) -> None:
        Base.greet(self)  # brittle
```

Why this is bad:

* Skips other classes in the MRO
* Breaks mixins
* Locks inheritance structure

---

## 8. Real-World Example: Cooperative Mixins

### Use case

* Logging
* Authentication
* Metrics
* Caching

```python
class LoggerMixin:
    def process(self) -> None:
        print("Logging")
        super().process()


class AuthMixin:
    def process(self) -> None:
        print("Authenticating")
        super().process()


class Service:
    def process(self) -> None:
        print("Processing request")
```

Composition:

```python
class APIService(LoggerMixin, AuthMixin, Service):
    pass
```

Usage:

```python
svc: APIService = APIService()
svc.process()
```

Output:

```
Logging
Authenticating
Processing request
```

**Why this works:**
Every class cooperates using `super()`.

---

## 9. `super()` in `__init__` (Critical Pattern)

```python
class Base:
    def __init__(self, name: str) -> None:
        self.name: str = name


class User(Base):
    def __init__(self, name: str, email: str) -> None:
        super().__init__(name)
        self.email: str = email
```

Rule:

> If your class has `__init__`, it should **almost always** call `super().__init__()`.

Breaking this rule breaks subclassing later.

---

## 10. `super()` in Class Methods

```python
class Base:
    @classmethod
    def describe(cls) -> str:
        return "Base"


class Child(Base):
    @classmethod
    def describe(cls) -> str:
        return f"{super().describe()} -> Child"
```

Result:

```python
print(Child.describe())
# Base -> Child
```

Yes, `super()` works with `cls` too.

---

## 11. `super()` in `__init_subclass__` (Advanced, Real)

```python
class FrameworkBase:
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        print(f"Registered subclass: {cls.__name__}")
```

Skipping `super()` here:

* Breaks other base classes
* Kills extensibility

Framework authors *care deeply* about this.

---

## 12. Python 3+ `super()` vs Old Style

Modern Python:

```python
super().method()
```

Old Python 2 style (don’t use):

```python
super(ClassName, self).method()
```

Python 3.14:

* Zero arguments
* Faster
* Safer
* Cleaner

There is no reason not to use it.

---

## 13. Executive Summary (Blunt and Useful)

* `super()` follows the MRO, not the parent
* It enables safe multiple inheritance
* It is mandatory for mixins
* Direct base calls are a dead end
* Skipping `super()` silently breaks extensibility

> Final truth:
> **If your class might ever be subclassed, use `super()` or expect pain later.**

If you want to keep leveling up, next logical stops:

* MRO deep dive
* Mixins done right
* `__class_getitem__`
* Metaclasses vs `super()`

Point the compass.
