Alright. **Processes** are the blunt instrument Python uses when the GIL says “nope.” This is where you go for **real parallelism**, **fault isolation**, and **CPU saturation**—and where mistakes get expensive fast.

Let’s do this properly.

---

# Process (Python 3.14)

## 1. What is a Process?

A **process** is:

* An independent OS execution unit
* With its **own Python interpreter**
* Its **own GIL**
* Its **own memory space**

> In plain English:
> **Processes don’t share memory. They share results.**

This is why they scale CPU and why they’re harder to use than threads.

---

## 2. Where Processes Are Used

Processes shine when:

* Work is CPU-bound
* Isolation matters
* Crashes must not take down the system
* You want to bypass the GIL

Real-world examples:

* Image/video processing
* Data science / ML
* Compilers / linters
* Encryption / compression
* Batch ETL jobs

---

## 3. Why Processes Exist (The GIL Escape Hatch)

### Threads vs Processes

| Dimension       | Threads | Processes |
| --------------- | ------- | --------- |
| Memory          | Shared  | Isolated  |
| GIL             | Shared  | Separate  |
| CPU parallelism | ❌       | ✅         |
| Startup cost    | Low     | High      |
| IPC overhead    | Low     | High      |
| Safety          | Risky   | Strong    |

> Strong take:
> **If you need CPU speedup in Python, processes are not optional.**

---

## 4. The `multiprocessing` Module (Core API)

### Simple Example

```python
from multiprocessing import Process


def worker() -> None:
    print("Hello from process")


if __name__ == "__main__":
    p = Process(target=worker)
    p.start()
    p.join()
```

### Why the guard is mandatory

```python
if __name__ == "__main__":
```

* Required on Windows & macOS (spawn mode)
* Prevents infinite process creation
* Always include it. No excuses.

---

## 5. Data Sharing: The Hard Truth

> **Processes do not share memory by default.**

You must use:

* IPC (queues, pipes)
* Shared memory
* Serialization (pickle)

---

## 6. Inter-Process Communication (IPC)

### `multiprocessing.Queue`

```python
from multiprocessing import Process, Queue
from typing import NoReturn


def producer(queue: Queue[int]) -> None:
    for i in range(5):
        queue.put(i)


def consumer(queue: Queue[int]) -> None:
    while True:
        item = queue.get()
        print(item)
        if item == 4:
            break


if __name__ == "__main__":
    q: Queue[int] = Queue()

    Process(target=producer, args=(q,)).start()
    Process(target=consumer, args=(q,)).start()
```

### Tradeoff

* Safe
* Simple
* Serialization overhead

---

## 7. Process Pools (Professional Way)

Manual process management doesn’t scale.

Use `ProcessPoolExecutor`.

```python
from concurrent.futures import ProcessPoolExecutor


def cpu_work(x: int) -> int:
    return x * x


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(cpu_work, range(10)))
```

✔ True parallelism
✔ Worker reuse
✔ Managed lifecycle

---

## 8. Streaming Results from Process Pools

Same pattern as threads.

```python
from concurrent.futures import ProcessPoolExecutor, as_completed


if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        futures = [pool.submit(cpu_work, i) for i in range(100)]

        for future in as_completed(futures):
            print(future.result())
```

> Rule:
> **Never block waiting for all CPU tasks to finish.**

---

## 9. Serialization Constraints (Critical)

### What must be pickleable

* Functions (top-level only)
* Arguments
* Return values

❌ Lambdas
❌ Closures
❌ Local functions

> If it can’t be pickled, it can’t cross process boundaries.

---

## 10. Shared Memory (Advanced, Dangerous)

### `multiprocessing.shared_memory` (Python 3.8+)

```python
from multiprocessing import shared_memory
import numpy as np


shm = shared_memory.SharedMemory(create=True, size=100)
```

Used for:

* NumPy arrays
* Large numeric buffers
* Zero-copy workloads

> Warning:
> **Shared memory trades safety for speed.**

---

## 11. Processes + Async Event Loops

### The Rule

> **Async orchestrates. Processes compute.**

Pattern:

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor


def heavy(x: int) -> int:
    return x ** 2


async def main() -> None:
    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, heavy, 21)

    print(result)
```

This is:

* Async frontend
* Process backend
* Clean separation of concerns

---

## 12. Process Lifecycle Management

Processes can:

* Crash
* Hang
* Leak memory

Mitigate with:

* Timeouts
* Supervisor processes
* Restart policies

> Processes fail harder but safer than threads.

---

## 13. Process Pools vs Joblib / Ray / Dask

| Tool                  | Use                  |
| --------------------- | -------------------- |
| `ProcessPoolExecutor` | General purpose      |
| Joblib                | Scientific workloads |
| Ray                   | Distributed systems  |
| Dask                  | Dataframes, graphs   |

Rule:

> **Scale up with pools, scale out with frameworks.**

---

## 14. Common Mistakes (No Sugar-Coating)

* Forgetting `__main__` guard
* Passing unpickleable objects
* Oversubscribing CPUs
* Using processes for I/O
* Ignoring startup cost

---

## 15. Executive Summary

* Processes provide true parallelism
* Each has its own GIL
* Memory is isolated by default
* IPC is explicit and costly
* Process pools beat manual management
* Async + processes is a winning combo

> Final truth:
> **Threads hide latency. Processes deliver horsepower.**

If you want to push further:

* Process supervision trees
* Shared memory patterns
* Hybrid async + process pipelines
* Fault-tolerant worker pools
* Distributed process orchestration

Call the next move.
