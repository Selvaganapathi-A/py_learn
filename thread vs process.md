Short answer first — then I’ll give you the *why*, the *how*, and the *production scars*.

---

## Executive summary (no fluff)

| Workload type | Threads per CPU core              | Processes per CPU core                    |
| ------------- | --------------------------------- | ----------------------------------------- |
| **I/O-bound** | **5–50× cores** (sometimes more)  | Usually **1**                             |
| **CPU-bound** | **1× cores** (threads don’t help) | **1× cores** (max), sometimes `cores − 1` |

If you remember **one rule**:

> **Threads wait. Processes compute.**

Now let’s unpack this properly. 💼⚙️

---

## I/O-bound tasks (network, disk, database, APIs)

### What

Tasks that spend most of their life **waiting**:

* HTTP requests
* Database queries
* File reads/writes
* Message queues
* Cloud SDK calls

### Why threads scale here

While one thread waits on I/O, **the CPU is idle**. Threads overlap waiting time.

The kernel wakes up whichever thread is ready next — cheap context switch, high throughput.

### How many threads per core?

### Practical ranges

* **Minimum**: `5 × CPU cores`
* **Typical**: `10–20 × CPU cores`
* **High-latency systems**: `50–100 × CPU cores`

Yes, **100 threads per core is normal** for I/O-heavy systems.

### Formula (rough but effective)

```text
Threads ≈ CPU cores × (1 + wait_time / compute_time)
```

If:

* Compute time = 1 ms
* Wait time = 100 ms

Then:

```
Threads ≈ cores × 101
```

### Python example (ThreadPoolExecutor)

```python
from concurrent.futures import ThreadPoolExecutor
import os

def io_task(url: str) -> str:
    """Simulate an I/O-bound task."""
    import time
    time.sleep(0.1)
    return url

max_threads: int = os.cpu_count() * 20

with ThreadPoolExecutor(max_workers=max_threads) as pool:
    results = list(pool.map(io_task, range(1000)))
```

### Hard truth

If you’re using **threads for I/O in Python**, you’re already doing it right — but **async beats threads** for very high fan-out.

> Threads scale. Async *explodes* scale. 🚀

---

## CPU-bound tasks (hashing, image processing, compression, ML)

### What

Tasks that **burn CPU cycles**:

* Image hashing (you’ve been there 😉)
* Encryption
* Data compression
* Parsing large files
* Numerical work

### Why threads fail in Python

The **Global Interpreter Lock** ensures:

> **Only one thread executes Python bytecode at a time**

So:

* 10 threads ≈ 1 thread
* More threads = more context switching = slower

### Correct answer: processes

### How many processes per core?

| Strategy            | Processes                     |
| ------------------- | ----------------------------- |
| Conservative        | `cores - 1`                   |
| Optimal             | `cores`                       |
| Hyper-threaded CPUs | `cores` (not logical threads) |

Never exceed physical cores for CPU-bound work.

### Python example (ProcessPoolExecutor)

```python
from concurrent.futures import ProcessPoolExecutor
import os

def cpu_task(x: int) -> int:
    """Simulate CPU-bound work."""
    total: int = 0
    for i in range(10_000_000):
        total += i ^ x
    return total

max_processes: int = os.cpu_count()

with ProcessPoolExecutor(max_workers=max_processes) as pool:
    results = list(pool.map(cpu_task, range(max_processes)))
```

### Key rule

> **Threads contend. Processes dominate.**

---

## Hybrid workloads (real world)

Most production systems are **mixed**:

* Fetch data (I/O)
* Process data (CPU)
* Store results (I/O)

### Correct architecture

```
[Async / Threads] → Queue → [Process Pool] → Queue → [Async / Threads]
```

### Pattern you should use (strong opinion)

* **Async or threads** for I/O stages
* **Process pool** for CPU stages
* **Bounded queues** between stages
* **Backpressure everywhere**

---

## Production disaster stories ☠️ (and fixes)

### Disaster #1: “Threads = faster”

**Symptom**

* 32-core server
* 500 threads
* CPU at 100%
* Throughput worse than single-thread

**Cause**

* CPU-bound work in threads
* GIL contention

**Fix**

* Switched to 32 processes
* Throughput jumped **8×**

---

### Disaster #2: “Just spawn more processes”

**Symptom**

* 64 processes on 16-core box
* Context-switch storm
* Memory pressure → OOM killer

**Cause**

* Over-subscribing CPU
* Process overhead ignored

**Fix**

* Cap at physical cores
* Introduced work stealing queue

---

### Disaster #3: I/O thread explosion

**Symptom**

* 10k threads
* File descriptor exhaustion
* Random failures

**Cause**

* No semaphore or rate limiting

**Fix**

```python
import asyncio

semaphore = asyncio.Semaphore(1000)

async def safe_io():
    async with semaphore:
        ...
```

---

## What to do / Not to do

### ✅ Do

* Measure **wait vs compute**
* Use async for massive I/O fan-out
* Cap concurrency with semaphores
* Use processes for CPU work

### ❌ Don’t

* Use threads for CPU-heavy Python
* Spawn “cores × 10” processes
* Trust benchmarks without production-like data
* Forget memory and file descriptor limits

---

## Final rulebook (print this)

* **I/O-bound** → Threads or Async → **many per core**
* **CPU-bound** → Processes → **one per core**
* **Python** → GIL is real, ignore it at your own risk
* **Production** → Measure, cap, observe, adapt

If you want, next we can:

* Design a **hybrid async + process pipeline**
* Pick numbers for **your exact workload**
* Benchmark properly (no fake micro-benchmarks)

Say the word. 💪🚀
