Perfect follow-up. `functools.wraps` is one of those *small-looking* tools that quietly determines whether your code is professional or a ticking maintenance bomb.

---

# `functools.wraps` (Python 3.14)

## 1. What is `functools.wraps`?

`functools.wraps` is a **decorator for decorators**.

Its job is to **copy metadata** from the original function to the wrapper function.

Metadata includes:

* `__name__`
* `__doc__`
* `__module__`
* `__annotations__`
* `__wrapped__` (critical for introspection)

> In one sentence:
> **`wraps` preserves the identity of the original function.**

---

## 2. Where is `wraps` used?

Everywhere decorators are used correctly:

* Web frameworks (FastAPI, Flask)
* CLI tools (Click)
* Test frameworks (pytest)
* Authorization, logging, caching
* Validation layers

If a decorator breaks tooling, it’s usually missing `wraps`.

---

## 3. Why does `wraps` exist?

Because decorators **replace functions**.

Without `wraps`:

* Function names lie
* Docstrings vanish
* Type hints disappear
* `inspect.signature()` breaks
* Stacked decorators become unreadable

> Strong opinion:
> **A decorator without `wraps` is a bug, not a style choice.**

---

## 4. When should you use `wraps`?

### Always use it when:

* Writing decorators
* Writing wrappers around callables
* You expect introspection, typing, or tooling to work

### Only skip it when:

* You intentionally want to hide the original function (rare, explicit)

---

## 5. How `wraps` works (Mechanics)

Internally, `wraps` calls `functools.update_wrapper()`.

Simplified:

```python
wrapper.__dict__.update(original.__dict__)
wrapper.__name__ = original.__name__
wrapper.__wrapped__ = original
```

The `__wrapped__` attribute is the secret sauce — tools like `inspect` rely on it.

---

## 6. Simple Example (The Bug)

### ❌ Without `wraps`

```python
def my_decorator(func: callable) -> callable:
    def wrapper(*args: object, **kwargs: object) -> object:
        return func(*args, **kwargs)
    return wrapper
```

Result:

```python
print(wrapper.__name__)  # "wrapper"
```

You just erased the function’s identity.

---

## 7. Simple Example (Correct)

```python
from functools import wraps
from typing import Callable


def my_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        return func(*args, **kwargs)
    return wrapper
```

Now:

```python
print(wrapper.__name__)  # original function name
```

Clean. Professional. Tool-friendly.

---

## 8. Real-World Example: Logging Decorator (Typed)

```python
from functools import wraps
from typing import Callable, TypeVar, Any

T = TypeVar("T")


def log_call(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

Usage:

```python
@log_call
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
```

Now all of this works:

* `add.__name__ == "add"`
* `add.__doc__` preserved
* `inspect.signature(add)` correct
* Type checkers stay sane

---

## 9. `wraps` + `inspect` (Critical Pairing)

```python
import inspect

print(inspect.signature(add))
```

Without `wraps`:

```
(*args, **kwargs)
```

With `wraps`:

```
(a: int, b: int) -> int
```

Frameworks live or die on this.

---

## 10. Stacked Decorators (Where `wraps` Really Matters)

```python
def deco_a(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        return func(*args, **kwargs)
    return wrapper


def deco_b(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        return func(*args, **kwargs)
    return wrapper
```

If **any** decorator in the stack skips `wraps`, introspection breaks.

---

## 11. Advanced: Customizing `wraps`

You can control what gets copied:

```python
@wraps(func, assigned=("__name__", "__doc__"))
```

But default behavior is almost always correct.

> Don’t get clever here unless you’re writing a framework.

---

## 12. Common Mistakes (No Sugar-Coating)

* Forgetting `@wraps(func)`
* Using `wraps` on the wrong function
* Assuming it’s optional
* Breaking signatures in public APIs

---

## 13. Executive Summary

* `wraps` preserves function identity
* It enables `inspect`, typing, and tooling
* It should be muscle memory
* Skipping it causes silent, cascading bugs
* Small decorator, massive architectural impact

> Final truth:
> **If you write decorators and don’t use `wraps`, you’re shipping broken abstractions.**

If you want to keep climbing:

* Writing type-safe decorators
* Async decorators done right
* Decorators vs descriptors
* How FastAPI uses `wraps` + `inspect`

Point the next target.
