Good choice. **Iterators** are one of those concepts that feel simple… until you realize they’re the backbone of Python’s performance, laziness, and memory model. We’ll do this properly, end-to-end.

---

# Iterators (Python 3.14)

## 1. What is an Iterator?

An **iterator** is an object that:

1. Knows how to return the **next value**
2. Knows when it is **exhausted**

Formally, an iterator implements **two methods**:

* `__iter__()` → returns the iterator itself
* `__next__()` → returns the next value or raises `StopIteration`

> In plain terms:
> **An iterator is a stateful object that produces values one at a time.**

---

## 2. Where do Iterators show up?

Everywhere:

* `for` loops
* `list()`, `tuple()`, `set()`
* `sum()`, `min()`, `max()`
* File objects
* Database cursors
* Network streams
* Generators
* `map`, `filter`, `zip`

If something works in a `for` loop, it’s using the iterator protocol.

---

## 3. Why do Iterators exist?

Because **not everything should be loaded into memory**.

Iterators enable:

* Lazy evaluation
* Streaming data
* Infinite sequences
* High performance
* Clean APIs

> Strong take:
> **Iterators are Python’s answer to scalability without complexity.**

---

## 4. Iterator vs Iterable (Critical Distinction)

| Concept      | Meaning                        |
| ------------ | ------------------------------ |
| **Iterable** | Something you can iterate over |
| **Iterator** | The thing doing the iterating  |

### Iterable

* Implements `__iter__`
* Returns a **new iterator** each time

### Iterator

* Implements `__iter__` **and** `__next__`
* Is **stateful**
* Gets exhausted

---

## 5. Simple Example: Using an Iterator

```python
numbers: list[int] = [1, 2, 3]

it: Iterator[int] = iter(numbers)

print(next(it))  # 1
print(next(it))  # 2
print(next(it))  # 3
# next(it) → StopIteration
```

---

## 6. How `for` Works (Under the Hood)

```python
for x in iterable:
    ...
```

Is equivalent to:

```python
it = iter(iterable)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
```

No magic. Just protocol.

---

## 7. Writing Your Own Iterator (Manual)

### Simple Counter Iterator

```python
from typing import Iterator


class Counter:
    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self.current: int = 0

    def __iter__(self) -> "Counter":
        return self

    def __next__(self) -> int:
        if self.current >= self.limit:
            raise StopIteration
        value: int = self.current
        self.current += 1
        return value
```

Usage:

```python
counter: Counter = Counter(3)

for n in counter:
    print(n)
```

Output:

```
0
1
2
```

---

## 8. Real-World Example: File Streaming

```python
from typing import Iterator


def read_lines(path: str) -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.rstrip("\n")
```

Why this matters:

* Reads line-by-line
* Constant memory
* Works for huge files

---

## 9. Generators Are Iterators (Important Truth)

Any function with `yield`:

* Returns an **iterator**
* Automatically implements the protocol

### Generator version of Counter

```python
from typing import Iterator


def counter(limit: int) -> Iterator[int]:
    current: int = 0
    while current < limit:
        yield current
        current += 1
```

> Professional rule:
> **If your iterator logic fits in a function, use a generator.**

---

## 10. Iterator Exhaustion (Common Pitfall)

```python
it: Iterator[int] = iter([1, 2, 3])

list(it)  # [1, 2, 3]
list(it)  # []
```

Once consumed, it’s done.

### Fix: Re-create the iterator

```python
iterable: list[int] = [1, 2, 3]

list(iter(iterable))
list(iter(iterable))
```

---

## 11. Typing Iterators (Modern Python)

### Returning an iterator

```python
from typing import Iterator

def generate_ids() -> Iterator[int]:
    ...
```

### Accepting an iterable (more flexible)

```python
from typing import Iterable

def sum_all(values: Iterable[int]) -> int:
    return sum(values)
```

> API design rule:
> **Accept `Iterable`, return `Iterator`.**

---

## 12. Real-World Example: Database Cursor Pattern

```python
from typing import Iterator


class User:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id


class UserRepository:
    def fetch_all(self) -> Iterator[User]:
        for i in range(3):
            yield User(i)
```

Why this scales:

* No list allocation
* Stream-friendly
* Plays well with pagination

---

## 13. Iterator vs Generator vs Comprehension

| Tool               | Use When                |
| ------------------ | ----------------------- |
| Iterator class     | Complex state, reuse    |
| Generator          | Sequential logic        |
| List comprehension | You need all values now |

> Opinionated take:
> **Default to generators. Reach for custom iterators only when necessary.**

---

## 14. Infinite Iterators (Real Use Case)

```python
from typing import Iterator


def infinite_ids(start: int = 0) -> Iterator[int]:
    current: int = start
    while True:
        yield current
        current += 1
```

Used in:

* Message queues
* Event IDs
* Simulations

Consume carefully.

---

## 15. Executive Summary

* Iterators power all iteration in Python
* They implement `__iter__` + `__next__`
* They enable lazy, memory-efficient code
* Generators are the preferred iterator tool
* Accept `Iterable`, return `Iterator`
* Exhaustion is real — design for it

> Final truth:
> **If your code scales, it’s probably because iterators are doing the heavy lifting.**

If you want to keep climbing:

* `Iterable` vs `Iterator` vs `Generator`
* `itertools` power tools
* Async iterators (`async for`)
* Custom lazy pipelines

Say where to go next.
<!--  -->
Perfect. **Async iterators** are where Python’s iteration model meets real-world I/O. This is how you stream **network data, database rows, events, and messages** without blocking threads or melting memory.

No fluff. Full stack view.

---

# Async Iterators (Python 3.14)

## 1. What is an Async Iterator?

An **async iterator** is the asynchronous version of a normal iterator.

It:

* Produces values **over time**
* Can `await` between values
* Is consumed with `async for`

Formally, an async iterator implements:

* `__aiter__()`
* `__anext__()` → returns an awaitable, raises `StopAsyncIteration`

> In plain English:
> **Async iterators stream values that require waiting.**

---

## 2. Where are Async Iterators Used?

Real systems use them everywhere:

* WebSocket streams
* HTTP chunked responses
* Async database drivers
* Message queues
* Event consumers
* Background workers

If it’s I/O-bound and incremental, async iterators are the right abstraction.

---

## 3. Why Async Iterators Exist

Blocking iteration is unacceptable for:

* Network calls
* Disk I/O
* External services

Async iterators allow:

* High concurrency
* Low memory usage
* Backpressure
* Clean async APIs

> Strong take:
> **Async iterators are the backbone of scalable async systems.**

---

## 4. Async Iterator vs Async Iterable (Critical)

| Concept            | Meaning                              |
| ------------------ | ------------------------------------ |
| **Async Iterable** | Something you can use in `async for` |
| **Async Iterator** | The object doing the iteration       |

* Async iterable → implements `__aiter__`
* Async iterator → implements `__aiter__` **and** `__anext__`

---

## 5. How `async for` Works (Mechanics)

```python
async for item in async_iterable:
    ...
```

Equivalent to:

```python
ait = async_iterable.__aiter__()

while True:
    try:
        item = await ait.__anext__()
    except StopAsyncIteration:
        break
```

Same protocol. Async flavor.

---

## 6. Simple Example: Async Generator (Recommended)

### The clean way

```python
from typing import AsyncIterator
import asyncio


async def async_counter(limit: int) -> AsyncIterator[int]:
    for i in range(limit):
        await asyncio.sleep(1)
        yield i
```

Usage:

```python
async def main() -> None:
    async for value in async_counter(3):
        print(value)
```

This is:

* Lazy
* Readable
* Efficient
* Idiomatic

> Rule:
> **If it fits in a function, use an async generator.**

---

## 7. Manual Async Iterator (Low-Level)

Only do this when you need fine-grained control.

```python
from typing import AsyncIterator
import asyncio


class AsyncCounter:
    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self.current: int = 0

    def __aiter__(self) -> "AsyncCounter":
        return self

    async def __anext__(self) -> int:
        if self.current >= self.limit:
            raise StopAsyncIteration
        await asyncio.sleep(1)
        value: int = self.current
        self.current += 1
        return value
```

Usage:

```python
async for n in AsyncCounter(3):
    print(n)
```

---

## 8. Real-World Example: Streaming HTTP Response

```python
from typing import AsyncIterator
import aiohttp


async def stream_response(url: str) -> AsyncIterator[bytes]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for chunk in response.content.iter_chunked(1024):
                yield chunk
```

Why this matters:

* No buffering entire response
* Backpressure-aware
* Production-grade streaming

---

## 9. Async Iterator Exhaustion

Same rule as sync iterators:

* They are **single-use**

```python
ait = async_counter(3)

async for _ in ait:
    pass

async for _ in ait:
    pass  # ❌ nothing happens
```

Design APIs accordingly.

---

## 10. Typing Async Iterators (Modern Python)

### Returning an async iterator

```python
from typing import AsyncIterator

async def fetch_rows() -> AsyncIterator[dict[str, object]]:
    ...
```

### Accepting async iterables (more flexible)

```python
from typing import AsyncIterable

async def consume(stream: AsyncIterable[int]) -> None:
    async for item in stream:
        print(item)
```

> API design rule (async too):
> **Accept `AsyncIterable`, return `AsyncIterator`.**

---

## 11. Real-World Example: Async Event Consumer

```python
from typing import AsyncIterator
import asyncio


class Event:
    def __init__(self, name: str) -> None:
        self.name = name


async def event_stream() -> AsyncIterator[Event]:
    events = ["start", "process", "end"]
    for name in events:
        await asyncio.sleep(0.5)
        yield Event(name)
```

Used in:

* Observability
* Messaging systems
* Event-driven services

---

## 12. Async Iterators vs Awaitables vs Streams

| Concept        | Use                        |
| -------------- | -------------------------- |
| `await`        | Single result              |
| Async iterator | Multiple results over time |
| Callback       | Legacy / hard to reason    |
| Thread         | Heavy                      |

> Opinionated take:
> **Async iterators are the cleanest streaming abstraction Python has.**

---

## 13. Common Mistakes (Straight Talk)

* Forgetting `await` in `__anext__`
* Returning values instead of yielding
* Mixing sync iterators with `async for`
* Blocking inside async iterators
* Forgetting exhaustion semantics

---

## 14. Async Iterators + `itertools` (Missing Piece)

There is **no built-in async `itertools`**.

Frameworks provide helpers:

* `aiostream`
* `asyncstdlib`

Or you roll small utilities yourself.

---

## 15. Executive Summary

* Async iterators stream values asynchronously
* Powered by `__aiter__` and `__anext__`
* Consumed via `async for`
* Async generators are the preferred approach
* Accept `AsyncIterable`, return `AsyncIterator`
* Essential for scalable I/O-bound systems

> Final truth:
> **If you’re doing async I/O and returning lists, you’re leaving performance on the table.**

If you want to go deeper next:

* Async generators + `yield from` alternatives
* Backpressure patterns
* Async pipelines
* Async context managers
* Designing streaming APIs

Call the next play.
