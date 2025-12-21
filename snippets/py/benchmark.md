Alright, let’s cut through the noise. **Benchmarking async code** is where a lot of teams fool themselves. If you benchmark it like sync code, your numbers are fiction.

Below is the **battle-tested, production-grade approach**.

---

## Executive Summary

Async code must be benchmarked **inside an event loop**, with **real awaits**, and **controlled concurrency**.
`timeit` still works—but only when paired with `asyncio.run()` or loop-aware wrappers.

If you don’t do this, you’re benchmarking *setup overhead*, not async performance.

---

## What Does “Benchmarking Async Code” Mean?

You are measuring:

* Coroutine execution time
* Scheduling overhead
* Context switching
* Await points
* Concurrency behavior

You are **not** measuring:

* Network latency (unless intentionally)
* Task creation noise
* Cold-start effects (unless stated)

---

## Where People Screw This Up (Immediately)

```python
timeit.timeit(my_async_func)  # ❌ WRONG
```

This benchmarks **function creation**, not execution.

Async code must be:

* awaited
* executed in a running event loop

---

## The Right Way: Wrap Async in Sync

### Canonical Pattern (Python 3.14-safe)

```python
import asyncio
import timeit

async def work():
    await asyncio.sleep(0)

def run():
    asyncio.run(work())

time = timeit.timeit(run, number=10_000)
print(time)
```

This is the **minimum viable correct benchmark**.

---

## Benchmarking Await Cost

```python
import asyncio
import timeit

async def noop():
    return 42

async def run_many(n):
    for _ in range(n):
        await noop()

def runner():
    asyncio.run(run_many(1_000))

print(timeit.timeit(runner, number=100))
```

This isolates:

* coroutine scheduling
* await overhead

Useful for framework decisions.

---

## Benchmarking Concurrent Async Tasks

### Sequential vs Concurrent (Real Comparison)

```python
import asyncio
import timeit

async def task():
    await asyncio.sleep(0.01)

async def sequential():
    for _ in range(100):
        await task()

async def concurrent():
    await asyncio.gather(*(task() for _ in range(100)))

def run_seq():
    asyncio.run(sequential())

def run_con():
    asyncio.run(concurrent())

print("sequential:", timeit.timeit(run_seq, number=10))
print("concurrent:", timeit.timeit(run_con, number=10))
```

This shows:

* Why async exists
* Where it actually helps
* How concurrency changes the math

---

## Benchmarking With a Persistent Event Loop (More Accurate)

Creating a loop every run adds noise.

### Better Pattern

```python
import asyncio
import time

async def benchmark(coro, n):
    start = time.perf_counter()
    for _ in range(n):
        await coro()
    return time.perf_counter() - start

async def work():
    await asyncio.sleep(0)

async def main():
    result = await benchmark(work, 10_000)
    print(result)

asyncio.run(main())
```

Use this when:

* You care about microsecond differences
* You’re tuning frameworks
* You’re deep in the weeds

---

## CLI Benchmarking Async (Yes, You Can)

```bash
python -m timeit -s "import asyncio; from app import run" "asyncio.run(run())"
```

Ugly? Yes.
Effective? Also yes.

---

## Real-World Benchmarking Scenarios

### 1. Async vs Sync I/O

```python
# Sync
def sync_fetch():
    time.sleep(0.01)

# Async
async def async_fetch():
    await asyncio.sleep(0.01)
```

Benchmark concurrency, not single calls—or you’re lying to yourself.

---

### 2. Framework Decisions (FastAPI vs Flask)

You don’t benchmark one request.
You benchmark **1000 concurrent awaits**.

Anything else is theater.

---

## Disaster Stories (Straight from Production)

### 💥 Disaster #1: Benchmarking Await-Free Async

Async function had no `await`.

Benchmarks looked amazing.
Production blocked the event loop.

**Lesson:**
Async without await is just sync with extra steps.

---

### 💥 Disaster #2: Measuring Event Loop Creation

Benchmarked `asyncio.run()` inside the hot path.

Optimized the wrong thing.
Ignored real workload.

**Lesson:**
Separate loop cost from coroutine cost.

---

### 💥 Disaster #3: Ignoring Backpressure

Benchmarked 10,000 concurrent tasks.

Production allowed 100.
Latency exploded.

**Lesson:**
Benchmark realistic concurrency limits.

---

## Strong Opinions (These Save Careers)

* Never benchmark async without concurrency
* Always isolate loop creation cost
* Use `asyncio.gather` deliberately
* If you don’t control concurrency, your benchmark is fantasy
* Async is for I/O, not CPU

---

## Bottom Line

Benchmarking async code is **about context**, not raw speed.

Measure:

* Await cost
* Concurrency behavior
* Event loop overhead

Ignore:

* Single-call timings
* Cold starts
* Fake workloads

If you want next:

* Async vs threading benchmarks
* uvloop comparisons
* Async CPU-bound pitfalls
* Real FastAPI benchmark harness

Say the word.
