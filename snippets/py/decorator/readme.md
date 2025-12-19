# Decorators in Python

## What is a Decorator?

A **decorator** is a callable that **wraps another callable** to **extend or modify its behavior without changing its source code**.

In plain business terms:

> *It’s middleware for functions and methods.*

Under the hood:

* Functions are **first-class objects**
* You can pass them around
* You can return them from other functions
* A decorator exploits that fact

```python
@decorator
def fn(): ...
```

is exactly the same as:

```python
fn = decorator(fn)
```

No mysticism. Just assignment.

---

## Why Decorators Exist (The Real Reason)

Decorators exist to solve **cross-cutting concerns** cleanly:

| Problem       | Without decorators              | With decorators      |
| ------------- | ------------------------------- | -------------------- |
| Logging       | Copy-paste everywhere           | One reusable wrapper |
| Authorization | Manual checks in every function | Centralized policy   |
| Timing        | Ad-hoc `time()` calls           | Declarative          |
| Caching       | Hand-rolled logic               | Clean annotation     |
| Validation    | Boilerplate                     | Zero clutter         |

Bottom line:
**Decorators reduce duplication and enforce consistency.**

---

## Where Decorators Are Used

You already use them, whether you realize it or not:

* `@staticmethod`
* `@classmethod`
* `@property`
* FastAPI: `@app.get`, `@app.post`
* Dataclasses: `@dataclass`
* Testing: `@pytest.mark.parametrize`

If Python were a company, decorators would be its **policy layer**.

---

## How Decorators Work (Step-by-Step)

### 1. Functions Are Objects

```python
def greet(name: str) -> str:
    return f"Hello {name}"

alias: callable[[str], str] = greet
```

### 2. Functions Can Return Functions

```python
def outer() -> callable[[], str]:
    def inner() -> str:
        return "Hi"
    return inner
```

### 3. A Decorator Is Just a Wrapper

```python
from collections.abc import Callable
from functools import wraps

def my_decorator(fn: Callable[..., str]) -> Callable[..., str]:
    @wraps(fn)
    def wrapper(*args: object, **kwargs: object) -> str:
        print("Before call")
        result: str = fn(*args, **kwargs)
        print("After call")
        return result

    return wrapper
```

Usage:

```python
@my_decorator
def say_hi() -> str:
    return "Hi!"
```

Execution flow:

1. `say_hi = my_decorator(say_hi)`
2. `say_hi()` → calls `wrapper()`

That’s the whole trick.

---

## Use Cases (Real-World, No Toy Examples)

---

## 1️⃣ Logging Decorator

```python
from collections.abc import Callable
from functools import wraps
import time

def log_call(fn: Callable[..., object]) -> Callable[..., object]:
    @wraps(fn)
    def wrapper(*args: object, **kwargs: object) -> object:
        start: float = time.perf_counter()
        result: object = fn(*args, **kwargs)
        elapsed: float = time.perf_counter() - start
        print(f"{fn.__name__} took {elapsed:.4f}s")
        return result

    return wrapper
```

```python
@log_call
def compute(x: int, y: int) -> int:
    return x * y
```

---

## 2️⃣ Authorization / Guard Decorator

```python
from collections.abc import Callable
from functools import wraps

def requires_admin(fn: Callable[..., str]) -> Callable[..., str]:
    @wraps(fn)
    def wrapper(user_role: str, *args: object, **kwargs: object) -> str:
        if user_role != "admin":
            raise PermissionError("Admin access required")
        return fn(user_role, *args, **kwargs)

    return wrapper
```

```python
@requires_admin
def delete_user(user_role: str, user_id: int) -> str:
    return f"User {user_id} deleted"
```

---

## 3️⃣ Caching (Memoization)

```python
from collections.abc import Callable
from functools import wraps

def simple_cache(fn: Callable[[int], int]) -> Callable[[int], int]:
    cache: dict[int, int] = {}

    @wraps(fn)
    def wrapper(n: int) -> int:
        if n not in cache:
            cache[n] = fn(n)
        return cache[n]

    return wrapper
```

```python
@simple_cache
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

---

## 4️⃣ Validation Decorator

```python
from collections.abc import Callable
from functools import wraps

def positive_only(fn: Callable[[int], int]) -> Callable[[int], int]:
    @wraps(fn)
    def wrapper(value: int) -> int:
        if value <= 0:
            raise ValueError("Value must be positive")
        return fn(value)

    return wrapper
```

```python
@positive_only
def square(x: int) -> int:
    return x * x
```

---

## 5️⃣ Decorators With Arguments (Very Important)

Decorator factory → decorator → wrapper

```python
from collections.abc import Callable
from functools import wraps

def repeat(times: int) -> Callable[[Callable[..., None]], Callable[..., None]]:
    def decorator(fn: Callable[..., None]) -> Callable[..., None]:
        @wraps(fn)
        def wrapper(*args: object, **kwargs: object) -> None:
            for _ in range(times):
                fn(*args, **kwargs)
        return wrapper
    return decorator
```

```python
@repeat(3)
def ping() -> None:
    print("Ping")
```

---

## 6️⃣ Class Decorators (Underrated, Powerful)

```python
from typing import Type

def add_repr(cls: Type[object]) -> Type[object]:
    def __repr__(self: object) -> str:
        return f"{cls.__name__}()"

    cls.__repr__ = __repr__  # type: ignore[attr-defined]
    return cls
```

```python
@add_repr
class User:
    pass
```

---

## Key Rules (Tell-It-Like-It-Is)

* Always use `functools.wraps`
  → Without it, introspection breaks
* Keep decorators **small and focused**
* Don’t hide heavy logic inside decorators
* Avoid decorators when:

  * Simple function calls are clearer
  * Control flow becomes invisible

Decorators are **power tools**, not syntactic sugar.

---

## Mental Model to Remember

> **A decorator is a function transformer.**

Input:

```
function
```

Output:

```
function with extra behavior
```

No inheritance. No magic. Just composition.

---

If you want next:

* async decorators (`async def`)
* method vs function decorators
* decorator order (`@a @b`)
* typing decorators with `ParamSpec` & `TypeVar`
* FastAPI-style decorators built from scratch

Say the word.

Excellent—this is **real typing**, not checkbox annotations.
If you understand this well, you stop breaking APIs silently and your decorators become **first-class citizens** instead of `Any` factories.

I’ll be direct, progressive, and precise. Python **3.14**, modern typing.

---

# Typing Decorators with `ParamSpec` & `TypeVar`

## The Problem (Why This Exists)

A decorator:

* wraps a function
* changes behavior
* **must not destroy the function’s signature**

Naive decorators do this:

```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

Type checkers see this as:

```text
Callable[..., Any]
```

Congratulations—you’ve erased your API.

---

## The Core Tools (Memorize These)

```python
from typing import TypeVar, ParamSpec, Callable
```

* `TypeVar[R]` → return type
* `ParamSpec[P]` → captures *all* parameters
* `Callable[P, R]` → fully preserved signature

---

# 1️⃣ The Canonical Typed Decorator

```python
from typing import Callable, TypeVar, ParamSpec
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")

def identity_decorator(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)
    return wrapper
```

### What You Get

* Exact argument types preserved
* Exact return type preserved
* IDE autocompletion survives
* mypy & pyright stay quiet

This is the **minimum bar**.

---

# 2️⃣ Decorator That Changes Behavior (Still Typed)

Example: logging execution time.

```python
import time
from typing import Callable, TypeVar, ParamSpec
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")

def timed(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            duration = time.perf_counter() - start
            print(f"{func.__name__} took {duration:.3f}s")
    return wrapper
```

Signature stays intact. No lies.

---

# 3️⃣ Decorators with Arguments (Most People Get This Wrong)

### Goal

```python
@retry(times=3)
def fetch(url: str) -> bytes: ...
```

---

### Correctly Typed Version

```python
from typing import Callable, TypeVar, ParamSpec
from functools import wraps
import time

P = ParamSpec("P")
R = TypeVar("R")

def retry(times: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times - 1:
                        raise
                    time.sleep(0.1)
            raise RuntimeError("unreachable")
        return wrapper
    return decorator
```

### Key Insight

> Decorator with arguments = **function returning a decorator**

The type signature must reflect that nesting.

---

# 4️⃣ Decorators That Change Return Type (Be Honest)

Example: caching → returns same type.

```python
from functools import lru_cache

def cached(func: Callable[P, R]) -> Callable[P, R]:
    return lru_cache(maxsize=128)(func)
```

Typed cleanly because return type is unchanged.

---

### But If Return Type Changes…

```python
def to_str(func: Callable[P, int]) -> Callable[P, str]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
        return str(func(*args, **kwargs))
    return wrapper
```

Be explicit. Lying to the type system is worse than verbosity.

---

# 5️⃣ Async Decorators (Common Pitfall)

```python
from typing import Awaitable

def async_timed(
    func: Callable[P, Awaitable[R]],
) -> Callable[P, Awaitable[R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return await func(*args, **kwargs)
    return wrapper
```

⚠️ Don’t forget `Awaitable[R]`.
This mistake is everywhere.

---

# 6️⃣ Method Decorators (`self` Is Not Special)

```python
class Service:
    @timed
    def compute(self, x: int) -> int:
        return x * 2
```

Works because:

* `self` is just part of `ParamSpec`
* No special handling needed

---

# 7️⃣ Class Decorators (Typed, Rare but Real)

```python
T = TypeVar("T", bound=type)

def sealed(cls: T) -> T:
    cls.__sealed__ = True  # type: ignore[attr-defined]
    return cls
```

Used sparingly. Document invariants.

---

# 8️⃣ When NOT to Use `ParamSpec`

Don’t use it if:

* you intentionally collapse the signature
* you accept arbitrary callables
* you are building dynamic proxies

Use `Callable[..., R]` *explicitly* in those cases.

---

# mypy / pyright Gotchas (From the Trenches)

### ❗ Missing `@wraps`

* Breaks introspection
* Confuses frameworks
* Loses metadata

Always use it.

---

### ❗ Over-constraining `TypeVar`

```python
R = TypeVar("R", bound=int)  # usually wrong
```

Let callers decide return types unless enforcing contracts.

---

### ❗ Decorating Overloaded Functions

You’ll need `@overload` on the decorator itself.
Messy, but sometimes unavoidable.

---

# The Golden Rule

> **If your decorator erases the signature, it’s broken—
> even if it “works”.**

---

## Executive Summary

* `ParamSpec` preserves parameters
* `TypeVar` preserves return types
* Nested decorators require nested types
* Async decorators need `Awaitable`
* Honesty beats cleverness

---

If you want next:

* typing decorators that add parameters
* decorators + Protocols
* composing multiple typed decorators
* Django/FastAPI decorators done right
* runtime enforcement + static typing combo

Say the word.

<!--  -->

Alright. This is the **deep end of decorator engineering**.
What you’re asking for is exactly where most “typed Python” tutorials stop—and real frameworks begin.

I’ll go **systematically**, opinionated, and production-aligned.
Python **3.14**, modern typing, no fairy dust.

---

# 1️⃣ Typing Decorators That **Add Parameters**

This is the hardest category because **you are changing the callable contract**.

## Example: decorator that injects a parameter

Goal:

```python
@with_request_id
def handler(user_id: int, request_id: str) -> None:
    ...
```

Caller does **not** pass `request_id`. Decorator injects it.

---

## Correct Typed Approach (Explicit Split)

You **must** expose two signatures:

* external (caller-facing)
* internal (wrapped)

### Step 1: Define the internal callable

```python
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

Internal = Callable[P, R]
```

---

### Step 2: Decorator changes signature → be honest

```python
from functools import wraps
import uuid

def with_request_id(
    func: Callable[[*P.args, str], R]
) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        request_id = str(uuid.uuid4())
        return func(*args, request_id, **kwargs)
    return wrapper
```

### Key Truth

> **If a decorator adds parameters, it must remove them from the public signature**

There is **no safe way** to “hide” parameters without lying to the type system.

Frameworks that do otherwise rely on runtime magic.

---

# 2️⃣ Decorators + `Protocol` (Structural Contracts)

Protocols are how you **type behavior**, not inheritance.

---

## Example: decorator requiring a callable contract

```python
from typing import Protocol

class HasUserId(Protocol):
    def __call__(self, user_id: int) -> None: ...
```

---

## Decorator Enforcing the Contract

```python
from typing import TypeVar

T = TypeVar("T", bound=HasUserId)

def audit(func: T) -> T:
    def wrapper(user_id: int) -> None:
        print(f"audit user={user_id}")
        return func(user_id)
    return wrapper  # type: ignore[return-value]
```

### Why This Matters

* No inheritance required
* Duck typing
* Static + runtime alignment

This is how **FastAPI dependency callables** work.

---

# 3️⃣ Composing Multiple Typed Decorators (Order Matters)

This is where teams accidentally destroy signatures.

---

## Two Decorators (Correctly Typed)

```python
def logged(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("log")
        return func(*args, **kwargs)
    return wrapper


def timed(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)
    return wrapper
```

---

## Composition (Safe)

```python
@logged
@timed
def compute(x: int) -> int:
    return x * 2
```

Because:

* both decorators preserve `Callable[P, R]`
* composition is associative

---

## ❌ Composition Failure Case

```python
def stringify(func: Callable[P, int]) -> Callable[P, str]: ...
```

Now:

```python
@logged
@stringify
def f(x: int) -> int: ...
```

💥 Type mismatch.

### Rule

> **Composable decorators must preserve the same signature**

Otherwise, document ordering explicitly.

---

# 4️⃣ Django / FastAPI Decorators Done Right

## FastAPI Route Decorators (Simplified)

FastAPI decorators **do not wrap the function**.
They **register metadata**.

---

### Correct Pattern

```python
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable[..., object])

def route(path: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        setattr(func, "__route__", path)
        return func
    return decorator
```

### Why This Works

* Signature untouched
* Tooling intact
* No ParamSpec needed

---

## Django-style View Decorator (Wrapping)

```python
from typing import Callable

def require_auth(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("auth check")
        return func(*args, **kwargs)
    return wrapper
```

---

### Framework Rule

| Framework | Strategy             |
| --------- | -------------------- |
| FastAPI   | annotate, don’t wrap |
| Django    | wrap carefully       |
| Flask     | mix of both          |

---

# 5️⃣ Runtime Enforcement + Static Typing Combo

Typing alone is **advisory**.
Sometimes you must **fail fast**.

---

## Example: enforcing return type at runtime

```python
from typing import Type, TypeVar

R = TypeVar("R")

def enforce_return(expected: Type[R]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = func(*args, **kwargs)
            if not isinstance(result, expected):
                raise TypeError("Invalid return type")
            return result
        return wrapper
    return decorator
```

This is common in:

* validation layers
* plugin systems
* sandboxed execution

---

# 6️⃣ FastAPI-Style Decorators Built from Scratch

Let’s build a **dependency injection decorator**.

---

## Dependency Decorator

```python
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable[..., object])

def depends(dep: Callable[[], object]) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        setattr(func, "__dependency__", dep)
        return func
    return decorator
```

Usage:

```python
def get_db() -> object: ...

@depends(get_db)
def handler(user_id: int) -> None:
    ...
```

FastAPI inspects metadata later—**no wrapping**.

This is the secret sauce.

---

# 7️⃣ Async Decorators (`async def`)

## Correctly Typed Async Decorator

```python
from typing import Awaitable

def async_logged(
    func: Callable[P, Awaitable[R]],
) -> Callable[P, Awaitable[R]]:
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("async log")
        return await func(*args, **kwargs)
    return wrapper
```

---

## ❌ Common Bug

```python
def bad_async(func):
    async def wrapper(*args, **kwargs):
        return func(*args, **kwargs)  # missing await
```

This compiles. It breaks at runtime.

---

# 8️⃣ Method vs Function Decorators

### Key Truth

> **Methods are functions with an extra first argument**

No special typing required.

---

## Method Decorator

```python
class Service:
    @logged
    def run(self, x: int) -> int:
        return x + 1
```

`self` is part of `ParamSpec`.

---

## When You Need to Care

* classmethod
* staticmethod
* descriptor-based decorators

Then you must handle binding manually.

---

# Final Rules (Non-Negotiable)

1. **If you change the signature, type it explicitly**
2. **Prefer metadata decorators over wrappers**
3. **Composable decorators must preserve `Callable[P, R]`**
4. **Async decorators must return `Awaitable[R]`**
5. **Protocols > inheritance**
6. **Runtime checks complement typing, not replace it**

---

## One-Line Mental Model

> **Decorators are API surface area.
> If you don’t type them, you’re shipping `Any`.**

---

If you want next (very natural continuation):

* decorator typing with `Concatenate`
* dependency injection patterns
* decorators + dataclasses
* testing decorators correctly
* refactoring decorators into context managers
* future typing improvements (PEP 695, 544, 612 implications)

Say the word.
