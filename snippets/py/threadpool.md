This is a **very real production problem**, and you’re asking the right question. Waiting for *all* threads to finish before processing results is a scalability anti-pattern.

Let’s fix it properly.

---

# ThreadPoolExecutor — Consume Results *As They Complete*

## The Core Problem

You have:

* Thousands of tasks
* A thread pool
* Results you want **immediately**, not at the end

### ❌ The naïve approach (don’t do this)

```python
with ThreadPoolExecutor() as pool:
    results = list(pool.map(work, data))  # blocks until ALL done
```

This:

* Buffers everything
* Delays downstream processing
* Increases memory pressure
* Kills latency

> Straight talk:
> **`executor.map()` is eager and blocking. It’s not for streaming.**

---

# ✅ The Correct Tool: `as_completed`

`concurrent.futures.as_completed()` yields futures **as soon as they finish**.

This is exactly what you want.

---

## 1️⃣ Basic Pattern (Streaming Results)

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable


def work(x: int) -> int:
    return x * x


data: Iterable[int] = range(1_000)

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(work, x) for x in data]

    for future in as_completed(futures):
        result: int = future.result()
        print(result)
```

### What’s happening

* Tasks execute concurrently
* Results are yielded **out of order**
* Processing starts immediately
* Memory stays bounded

✔ Low latency
✔ High throughput
✔ Production-safe

---

## 2️⃣ Real-World Example: I/O-Bound Workload

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from typing import Iterable


def fetch(url: str) -> str:
    response = requests.get(url, timeout=5)
    return response.text


urls: Iterable[str] = [
    "https://example.com",
    "https://example.org",
    # thousands more
]

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(fetch, url): url for url in urls}

    for future in as_completed(futures):
        url: str = futures[future]
        try:
            content: str = future.result()
            print(f"{url}: {len(content)} bytes")
        except Exception as exc:
            print(f"{url} failed: {exc}")
```

### Why this scales

* Slow URLs don’t block fast ones
* Failures are isolated
* Results flow continuously

---

## 3️⃣ Backpressure-Friendly Pattern (Bounded Submission)

Submitting *all* tasks at once can still overwhelm memory.

### Solution: submit in batches

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque
from typing import Iterator


def work(x: int) -> int:
    return x * 2


def batched(iterable: Iterator[int], size: int) -> Iterator[list[int]]:
    batch: list[int] = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


with ThreadPoolExecutor(max_workers=10) as executor:
    for batch in batched(iter(range(10_000)), size=100):
        futures = [executor.submit(work, x) for x in batch]

        for future in as_completed(futures):
            print(future.result())
```

> Corporate takeaway:
> **Bounded submission + `as_completed` = predictable systems.**

---

## 4️⃣ Advanced Pattern: Producer → Thread Pool → Consumer

This mimics **streaming pipelines**.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from typing import NoReturn


def work(x: int) -> int:
    return x * x


def producer(queue: Queue[int]) -> None:
    for i in range(1_000):
        queue.put(i)
    queue.put(-1)  # sentinel


def consumer() -> None:
    queue: Queue[int] = Queue()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        producer(queue)

        while True:
            item = queue.get()
            if item == -1:
                break
            futures.append(executor.submit(work, item))

        for future in as_completed(futures):
            print(future.result())
```

This is the **threaded equivalent of async streams**.

---

## 5️⃣ `submit + as_completed` vs `map`

| Feature         | `map()` | `submit() + as_completed()` |
| --------------- | ------- | --------------------------- |
| Streaming       | ❌       | ✅                           |
| Error handling  | Weak    | Strong                      |
| Order preserved | ✅       | ❌                           |
| Backpressure    | ❌       | ✅                           |
| Large workloads | ❌       | ✅                           |

> Opinionated rule:
> **Use `map()` only for small, fast, homogeneous jobs.**

---

## 6️⃣ Handling Exceptions Correctly

```python
for future in as_completed(futures):
    try:
        result = future.result()
    except Exception as exc:
        log_error(exc)
    else:
        process(result)
```

No silent failures. No swallowed exceptions.

---

## 7️⃣ Thread Pool Sizing (Reality Check)

* CPU-bound → **don’t use threads**
* I/O-bound → `max_workers = 5–50` depending on latency
* Thousands of threads = disaster

> Rule of thumb:
> **Threads hide latency, not CPU limits.**

---

## 8️⃣ Executive Summary

* `executor.map()` waits — avoid it for large workloads
* `submit()` + `as_completed()` enables streaming
* Consume results immediately
* Handle errors per-task
* Batch submissions to control memory
* This pattern scales cleanly to thousands of tasks

> Final truth:
> **Concurrency without streaming is just parallel waiting.**

If you want the *next escalation*:

* Thread pools + async event loops
* Hybrid async + thread pipelines
* Cancellation & timeouts
* Priority queues in thread pools
* Turning this into a reusable executor abstraction

Say the word.
