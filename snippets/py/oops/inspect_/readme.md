Excellent. `inspect` is where Python stops being “dynamic” and starts being **transparent**.
This is runtime introspection done professionally—the kind used by debuggers, test frameworks, DI containers, and CLIs.

---

# `inspect` Module (Python 3.14)

## 1. What is `inspect`?

`inspect` is a **standard-library module** that lets you:

* Examine live objects
* Understand function signatures
* Read annotations and defaults
* Discover source code
* Analyze stack frames

In short:

> **`inspect` lets code ask intelligent questions about other code.**

---

## 2. Where is `inspect` used?

* Frameworks (FastAPI, pytest, Click)
* Dependency injection systems
* Decorators and wrappers
* Debugging and tooling
* Validation engines
* Plugin discovery

If a library “just knows” what arguments you passed — `inspect` is usually involved.

---

## 3. Why does `inspect` exist?

Because Python:

* Is interpreted
* Is dynamic
* Treats code as objects

`inspect` provides **safe, standardized access** to runtime metadata instead of hacks like `__dict__` spelunking.

> Opinionated truth:
> **If you’re writing reflection-heavy code without `inspect`, you’re reinventing it badly.**

---

## 4. When should you use `inspect`?

### Use it when

* You need function signatures at runtime
* You’re writing decorators
* You’re validating user-defined functions
* You’re building frameworks or tools
* You need stack or frame inspection

### Don’t use it when

* Static typing already solves the problem
* You’re doing normal business logic
* Performance is extremely tight (introspection has cost)

---

## 5. How `inspect` works (high level)

Internally, `inspect`:

* Reads function metadata (`__signature__`, `__annotations__`)
* Examines code objects
* Walks stack frames
* Normalizes behavior across Python implementations

You don’t need to know the internals — just the contracts.

---

## 6. Simple Example: Getting a Function Signature

```python
import inspect
from typing import Any


def add(a: int, b: int = 0) -> int:
    return a + b


signature: inspect.Signature = inspect.signature(add)
print(signature)
```

Output:

```
(a: int, b: int = 0) -> int
```

This is gold for validation and tooling.

---

## 7. Inspecting Parameters (Practical)

```python
def describe_function(func: callable) -> None:
    sig: inspect.Signature = inspect.signature(func)

    for name, param in sig.parameters.items():
        print(
            name,
            param.annotation,
            param.default,
            param.kind,
        )
```

Usage:

```python
describe_function(add)
```

You now know:

* Parameter names
* Types
* Defaults
* Whether they’re positional-only, keyword-only, etc.

---

## 8. Real-World Example: Dependency Injection (Clean Pattern)

### Use case

Auto-wire function arguments based on type hints.

```python
from typing import Dict, Type
import inspect


class Container:
    def __init__(self) -> None:
        self._services: Dict[type, object] = {}

    def register(self, cls: type, instance: object) -> None:
        self._services[cls] = instance

    def resolve(self, func: callable) -> None:
        sig: inspect.Signature = inspect.signature(func)
        kwargs: Dict[str, object] = {}

        for param in sig.parameters.values():
            if param.annotation in self._services:
                kwargs[param.name] = self._services[param.annotation]

        func(**kwargs)
```

Usage:

```python
class Database:
    pass


def handler(db: Database) -> None:
    print("DB injected:", db)


container: Container = Container()
container.register(Database, Database())
container.resolve(handler)
```

**Outcome:**
No configuration. No boilerplate. Type-driven wiring.

---

## 9. Inspecting Classes and Methods

```python
class User:
    def save(self) -> None:
        pass


methods: list[str] = [
    name
    for name, value in inspect.getmembers(User, inspect.isfunction)
]

print(methods)
```

This powers admin panels and serializers.

---

## 10. Real-World Example: Decorator That Preserves Signature

Bad decorators break introspection. Good ones don’t.

```python
import inspect
from functools import wraps
from typing import Callable


def validate_types(func: Callable) -> Callable:
    sig: inspect.Signature = inspect.signature(func)

    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        bound = sig.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            expected = sig.parameters[name].annotation
            if expected is not inspect._empty and not isinstance(value, expected):
                raise TypeError(f"{name} must be {expected}")
        return func(*args, **kwargs)

    return wrapper
```

This is production-grade decorator design.

---

## 11. Stack & Frame Inspection (Advanced)

```python
def who_called_me() -> str:
    frame = inspect.currentframe()
    assert frame is not None
    caller = frame.f_back
    assert caller is not None
    return caller.f_code.co_name
```

Use sparingly — powerful but sharp.

---

## 12. `inspect` vs `dir()` vs `__dict__`

| Tool       | Purpose                        |
| ---------- | ------------------------------ |
| `dir()`    | Quick exploration              |
| `__dict__` | Raw attributes                 |
| `inspect`  | Structured, safe introspection |

**Rule:**
If you’re writing tools or frameworks → `inspect`.

---

## 13. Common Mistakes (Straight Talk)

* Forgetting `functools.wraps`
* Using private `inspect._*` APIs
* Overusing stack inspection
* Ignoring performance cost

---

## 14. Executive Summary

* `inspect` is runtime reflection done right
* It reads signatures, annotations, and code metadata
* It enables DI, decorators, CLIs, and frameworks
* It should not leak into business logic
* Used correctly, it makes code self-describing

> Final thought:
> **`inspect` turns Python from “dynamic” into “intelligently dynamic.”**

If you want the natural next step:

* `functools.wraps` deep dive
* Building a mini FastAPI clone
* Stack frames & debugging tools
* Metaclasses (now fully unlocked)

Say where to go next.
