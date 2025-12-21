Crystal clear. Here’s the **canonical, no-surprises pattern** for **Rich + threads**, exactly aligned with:

> Main thread owns rendering
> Workers report progress
> Queues are the contract

This is the version you can paste into production without sweating.

---

## Executive Summary

* **Rendering is centralized** → only the main thread touches Rich
* **Workers are dumb** → they do work and emit signals
* **Queues are the boundary** → clean, blocking, thread-safe

This is the only model that scales without terminal corruption or race conditions.

---

## The Mental Model (Lock This In)

```
[ Worker Threads ]  --->  Queue  --->  [ Main Thread + Rich ]
        |                                |
      work()                        progress.update()
```

Workers never:

* print
* log to stdout
* touch Rich objects

---

## Minimal, Correct Example

### Worker

```python
import time

def worker(n, q):
    for _ in range(n):
        time.sleep(0.05)   # simulate work
        q.put(1)           # report progress
    q.put(None)            # signal completion
```

### Main Thread (Owns Rich)

```python
import queue
import threading
from rich.progress import Progress, BarColumn, TextColumn

def main():
    total = 100
    q = queue.Queue()

    t = threading.Thread(target=worker, args=(total, q), daemon=True)
    t.start()

    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
    ) as progress:
        task = progress.add_task("Processing", total=total)

        while True:
            msg = q.get()          # blocking, zero CPU waste
            if msg is None:
                break
            progress.update(task, advance=msg)

    t.join()
```

---

## Multiple Workers (Still Clean)

```python
def worker(q):
    for _ in range(25):
        time.sleep(0.1)
        q.put(1)

q = queue.Queue()
threads = [
    threading.Thread(target=worker, args=(q,), daemon=True)
    for _ in range(4)
]

for t in threads:
    t.start()

with Progress() as progress:
    task = progress.add_task("Working", total=100)
    completed = 0

    while completed < 100:
        q.get()
        completed += 1
        progress.update(task, completed=completed)

for t in threads:
    t.join()
```

No locks. No shared state. No drama.

---

## Why the Queue Is the Contract

* **Thread-safe by design**
* **Blocks instead of polling**
* **Decouples UI from execution**
* **Extensible** (errors, cancellation, metrics)

You can later send:

```python
("progress", 1)
("error", exc)
("done", None)
```

Without touching worker logic.

---

## Hard Rules (Tell-It-Like-It-Is)

* If a worker touches Rich → bug
* If UI logic leaks into workers → bug
* If you poll instead of block → bug
* If it flickers → architecture failure

This isn’t stylistic. It’s operational hygiene.

---

## Bottom Line

This pattern is:

* Boring
* Predictable
* Scalable
* Production-safe

Exactly what UI + concurrency should be.

If you want next:

* `ThreadPoolExecutor` integration
* Cancellation + Ctrl-C handling
* Async (`asyncio`) version
* Multi-task Rich dashboards

Say the word.
