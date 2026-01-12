Alright, **`typing.runtime_checkable`** is one of those features that *looks small* but fixes a very real “types vs runtime” gap. If you’ve ever tried `isinstance()` on a `Protocol` and got burned—this is the fix.

Let’s be precise.

---

## What is `runtime_checkable`?

**What**
`@runtime_checkable` is a decorator that allows a **`Protocol`** to be used with `isinstance()` and `issubclass()` **at runtime**.

```python
from typing import Protocol, runtime_checkable
```

By default, `Protocol` is **static-only**.
`runtime_checkable` opts it into runtime checks.

---

## Why does it exist?

**Why**
Protocols were designed for **static structural typing** (“duck typing for type checkers”).

But Python developers kept asking:

> “If it looks like a duck, why can’t I check it at runtime?”

Because runtime checks are expensive, incomplete, and potentially misleading.

So Python made it **explicit and opt-in**.

---

## Without `runtime_checkable` (common failure)

```python
from typing import Protocol

class HasClose(Protocol):
    def close(self) -> None: ...
```

```python
def shutdown(obj: object):
    if isinstance(obj, HasClose):   # 💥 TypeError
        obj.close()
```

**Boom**:

```
TypeError: Instance and class checks can only be used with @runtime_checkable protocols
```

---

## With `runtime_checkable` (correct usage)

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class HasClose(Protocol):
    def close(self) -> None: ...
```

```python
def shutdown(obj: object):
    if isinstance(obj, HasClose):
        obj.close()   # safe
```

Now it works.

---

## How does it actually work?

**How**

* `isinstance(obj, Protocol)` checks:

  * Does `obj` have the required **attributes**?
* It does **NOT** check:

  * Argument types
  * Return types
  * Method signatures in depth

It’s **shallow, attribute-based checking**.

---

## Real-world example (file-like objects)

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class FileLike(Protocol):
    def read(self, size: int = ...) -> str: ...
    def close(self) -> None: ...
```

Usage:

```python
def process(resource: object):
    if isinstance(resource, FileLike):
        data = resource.read()
        resource.close()
```

Works for:

* Files
* Sockets
* In-memory streams
* Custom objects

No inheritance required.

---

## Disaster Story 💣

A team used `isinstance(obj, FileLike)` **without** `runtime_checkable`.

They caught the exception and “fixed” it with:

```python
try:
    obj.close()
except AttributeError:
    pass
```

Result:

* Silent failures
* Leaked file descriptors
* Production outage

---

## Solution

Use `@runtime_checkable` + `Protocol`:

```python
if isinstance(obj, FileLike):
    obj.close()
else:
    raise TypeError("Resource is not closable")
```

Fail fast. Fail loud.

---

## Expert Advice 🧠 (Strong Opinions)

* Use `runtime_checkable` **sparingly**
* Prefer static checking first
* Runtime protocol checks are **best-effort**, not guarantees
* Never assume signature correctness at runtime

---

## What NOT to do in Development 🚫

* ❌ Use `isinstance()` on `Protocol` without `runtime_checkable`
* ❌ Expect deep validation
* ❌ Replace real validation logic with protocol checks

---

## What NOT to do in Production 🚫🚫

* ❌ Treat `runtime_checkable` as security validation
* ❌ Ignore missing methods after checks
* ❌ Swallow `TypeError` and move on

---

## `runtime_checkable` vs Alternatives

| Tool                | Purpose                      |
| ------------------- | ---------------------------- |
| `Protocol`          | Static structural typing     |
| `runtime_checkable` | Shallow runtime checks       |
| `TypeIs`            | Exact narrowing + validation |
| `ABC`               | Nominal runtime typing       |

If you need **guarantees**, use:

* explicit checks
* constructors
* validation logic

---

## pytest Test (yes, test it)

```python
class Resource:
    def read(self, size: int = 0) -> str:
        return "data"
    def close(self) -> None:
        pass

def test_filelike():
    r = Resource()
    assert isinstance(r, FileLike)
```

---

## Bottom Line (Executive Summary)

* `runtime_checkable` bridges static protocols to runtime
* Enables `isinstance()` for `Protocol`
* Shallow checks only
* Powerful, but not a silver bullet

---

### Want next?

* `Protocol` deep dive
* `Protocol` vs `ABC`
* Combining `Protocol` with `TypeIs`
* Designing clean plugin systems

Point to the next target.
