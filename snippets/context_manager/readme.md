# Context Managers

## 🔹 What Is a Context Manager?

A **context manager** is an object that **controls a block of code** by defining:

* **setup logic** (before block)
* **teardown logic** (after block)
* **guaranteed cleanup**, even on exceptions

Syntax:

```python
with resource:
    ...
```

Under the hood:

```python
obj.__enter__()
try:
    ...
finally:
    obj.__exit__()
```

---

## 🔹 Why Context Managers Exist

Without context managers:

```python
file: TextIO = open("data.txt")
try:
    process(file)
finally:
    file.close()
```

With context managers:

```python
with open("data.txt") as file:
    process(file)
```

✔ Safer
✔ Shorter
✔ Exception-proof
✔ Idiomatic

---

## 🔹 Where Context Managers Are Used

Common real-world resources:

* Files
* Database connections / transactions
* Locks / semaphores
* Network sockets
* Temporary files / directories
* Progress bars
* Logging scopes
* Performance timers
* Feature flags
* Dependency lifetimes

If something must be **cleaned up**, it wants a context manager.

---

## 🔹 When You Should Create One

Create a context manager when:

* Resource acquisition & release must be paired
* Cleanup must always happen
* You want **scope-based behavior**
* You want to eliminate `try/finally`
* Lifetime must be explicit

---

## 1️⃣ Built-in Example (File)

```python
from typing import TextIO

with open("example.txt", "w") as file:  # type: TextIO
    file.write("hello")
```

---

## 2️⃣ Custom Context Manager (Class-Based)

### Step-by-step, fully typed

```python
from typing import Self

class DatabaseConnection:
    def __enter__(self) -> Self:
        print("Connecting")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: object | None,
    ) -> bool:
        print("Disconnecting")
        return False  # propagate exceptions
```

Usage:

```python
with DatabaseConnection() as db:
    print("Using database")
```

---

## 3️⃣ Exception Handling Behavior (Important)

```python
class SuppressErrors:
    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: object | None,
    ) -> bool:
        return True  # suppress exception
```

```python
with SuppressErrors():
    raise ValueError("ignored")
```

⚠ Returning `True` **suppresses** the exception.
Returning `False` lets it propagate.

---

## 4️⃣ Context Manager Using `contextlib`

### Simple and Pythonic

```python
from contextlib import contextmanager
from typing import Iterator

@contextmanager
def open_resource(name: str) -> Iterator[str]:
    print(f"Acquire {name}")
    try:
        yield name
    finally:
        print(f"Release {name}")
```

Usage:

```python
with open_resource("cache") as res:
    print(res)
```

This is ideal for:

* Small managers
* One-off resources
* Readability

---

## 5️⃣ Context Manager + Lock (Thread Safety)

```python
from threading import Lock

lock: Lock = Lock()

with lock:
    critical_section()
```

No risk of forgetting `release()`.

---

## 6️⃣ Context Manager + Timing (Practical Utility)

```python
import time

class Timer:
    def __enter__(self) -> Self:
        self.start: float = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: object | None,
    ) -> None:
        elapsed: float = time.perf_counter() - self.start
        print(f"Elapsed: {elapsed:.3f}s")
```

Usage:

```python
with Timer():
    heavy_work()
```

---

## 7️⃣ Async Context Managers (Modern Systems)

```python
from typing import Self

class AsyncResource:
    async def __aenter__(self) -> Self:
        print("Async acquire")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: object | None,
    ) -> None:
        print("Async release")
```

Usage:

```python
async with AsyncResource():
    await async_work()
```

Used in:

* FastAPI
* async DB drivers
* async locks
* network clients

---

## 8️⃣ Context Managers vs `try/finally`

| Feature        | try/finally | context manager |
| -------------- | ----------- | --------------- |
| Cleanup safety | ✅           | ✅               |
| Readability    | ❌           | ✅               |
| Reusability    | ❌           | ✅               |
| Composability  | ❌           | ✅               |
| Idiomatic      | ❌           | ✅               |

---

## 🎤 Interview-Grade Definition

> A context manager is an object that defines setup and teardown behavior around a code block using `__enter__` and `__exit__`, guaranteeing resource cleanup even in the presence of exceptions.

---

## 🔥 Engineering Truth (No Sugar-Coating)

If your code:

* opens something
* allocates something
* locks something
* starts something
* modifies global state

…and doesn’t use a context manager —
👉 it’s a **latent bug**.

---

## 🚀 Where You Already Used Them (Even If You Didn’t Notice)

* `with open(...)`
* `with lock`
* `with Progress(...)`
* `with Session()`
* `with tempfile.TemporaryDirectory()`

You were using **IoC** and **RAII-style resource management** without realizing it.

---

If you want next:

* Context managers + DI
* Context managers + pipelines
* Context managers + database transactions
* Writing reusable library-grade context managers
* Debugging common `__exit__` mistakes

Say the word.

With context managers, you can perform any pair of operations that needs to be done before and after another operation or procedure, such as:

* `Open` and `close`
* `Lock` and `release`
* `Change` and `reset`
* `Create` and `delete`
* `Enter` and `exit`
* `Start` and `stop`
* `Setup` and `teardown`
