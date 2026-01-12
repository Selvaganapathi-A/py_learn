Let’s be precise and cut through the noise.

---

## What is a **Coroutine**?

A **coroutine** is a special function that can **pause execution**, **yield control**, and **resume later**—without blocking the thread.

In Python **3.14**, a coroutine is created **only** by calling an `async def` function.

```python
async def work():
    return 42

coro = work()   # ← this is a coroutine object
```

It does **nothing** until it is:

* `await`ed, or
* scheduled on an event loop

---

## Why Coroutines Exist

Because blocking is expensive.

Coroutines allow:

* High concurrency with **one thread**
* Efficient I/O (network, disk, APIs)
* Predictable scaling without thread chaos

They are the backbone of:

* Web servers (FastAPI, aiohttp)
* Async workers
* Streaming pipelines

---

## Which Things Are Coroutines (and Which Are Not)

| Thing                    | Is it a coroutine? | Notes                    |
| ------------------------ | ------------------ | ------------------------ |
| `async def f()`          | ❌                  | This is a *function*     |
| `f()` where `f` is async | ✅                  | Coroutine object         |
| `await f()`              | ❌                  | Execution of coroutine   |
| `asyncio.Task`           | ❌                  | Wrapper around coroutine |
| Generator (`yield`)      | ❌                  | Different beast          |
| `asyncio.coroutine`      | ❌                  | Dead and removed         |

---

## When a Coroutine Actually Runs

A coroutine runs **only when awaited**:

```python
async def job():
    print("running")

job()          # does nothing
await job()    # actually runs
```

This is a **very common bug** in production code.

---

## Where Coroutines Live

* Inside an **event loop**
* Usually created in:

  * async web handlers
  * async workers
  * async CLI tools
* Never at top-level without `asyncio.run()`

---

## How Coroutines Work (Mental Model)

Think of a coroutine as:

> “A paused function with bookmarks”

At every `await`, control goes back to the event loop:

```python
async def pipeline():
    data = await fetch()
    result = await process(data)
    await save(result)
```

Each `await` is a **yield point**.

---

## Simple Example (Correct Usage)

```python
import asyncio

async def fetch():
    await asyncio.sleep(1)
    return "data"

async def main():
    result = await fetch()
    print(result)

asyncio.run(main())
```

---

## Real-World Example (Concurrent I/O)

```python
async def worker(n: int):
    await asyncio.sleep(1)
    return f"done {n}"

async def main():
    results = await asyncio.gather(
        worker(1),
        worker(2),
        worker(3),
    )
    print(results)

asyncio.run(main())
```

**Why this matters:**
3 tasks → ~1 second total, not 3 seconds.

---

## Pytest Example

```python
import pytest

@pytest.mark.asyncio
async def test_worker():
    result = await worker(1)
    assert result == "done 1"
```

---

## Disaster Story (Classic Failure)

**Incident:**
Team created coroutines but never awaited them.

```python
async def send_email():
    ...

send_email()  # ← silent failure
```

**Symptoms**

* No errors
* No emails
* No logs

**Why**

* Coroutine objects are lazy
* Garbage-collected without execution

**Prevention**

* Lint rule: ban unused coroutines
* Use `asyncio.create_task()` when fire-and-forget
* Enable `RuntimeWarning: coroutine was never awaited`

---

## What To Do / Not To Do

### ✅ Do

* Always `await` coroutines
* Use `asyncio.create_task()` for background work
* Keep async functions small and composable
* Add timeouts to all I/O

### ❌ Do NOT

* Don’t call async functions without awaiting
* Don’t block (`time.sleep`, sync DB calls)
* Don’t mix threads and async blindly
* Don’t swallow `CancelledError`

---

## Expert Take (Blunt Truth)

If you don’t know **where** your coroutines are awaited,
you **don’t control your program**.

Async code rewards discipline and punishes laziness.

If you want next:

* coroutine vs task vs future (deep dive)
* debugging “coroutine never awaited”
* async memory leaks
* designing safe fire-and-forget jobs

Say the word.
