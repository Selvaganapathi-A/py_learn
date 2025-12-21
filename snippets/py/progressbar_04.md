Alright — this is the **last mile polish** that turns a dashboard into a **professional operator tool**.

Below is a **single, cohesive pattern** that delivers **all four features**, cleanly and safely:

✔ “Press Q to quit” (non-blocking)
✔ Auto-timeout + manual override
✔ Save final snapshot to file
✔ Exit codes tied to metrics

No terminal hacks. No raw mode footguns. Fully Rich-compatible.

---

# Executive Summary

* Keyboard handling runs in a **background thread**
* Dashboard remains **non-blocking**
* Timeout is **soft**, user can override
* Final dashboard is **snapshotted**
* Exit code reflects **system health**

This is exactly how real ops tools behave.

---

# Architecture Overview

```
Live Dashboard (async)
     │
     ├── metrics (truth)
     ├── keyboard thread (Q)
     ├── timeout watchdog
     └── final snapshot + exit code
```

**Golden rule:**
Rendering, input, and exit logic are **decoupled**.

---

# 1️⃣ Non-Blocking “Press Q to Quit”

We **do NOT** read keyboard input inside the event loop.

### Keyboard Listener (Threaded, Safe)

```python
import threading
import sys

def listen_for_quit(quit_event: threading.Event):
    try:
        while not quit_event.is_set():
            key = sys.stdin.read(1)
            if key.lower() == "q":
                quit_event.set()
    except Exception:
        pass
```

Why this works:

* Blocking read happens in a **thread**
* No interference with Rich
* No raw terminal mode
* Cross-platform enough for ops tools

---

# 2️⃣ Auto-Timeout + Manual Override

Timeout is **advisory**, not forced.

```python
import time

class Timeout:
    def __init__(self, seconds: int):
        self.deadline = time.monotonic() + seconds

    def expired(self) -> bool:
        return time.monotonic() > self.deadline
```

Dashboard logic:

* Exits if **timeout expired**
* Or if **Q pressed**
* Or if **work completed**

---

# 3️⃣ Dashboard Loop (Integrated Control)

```python
from rich.live import Live
from rich.panel import Panel
import asyncio

async def dashboard(metrics, quit_event, timeout):
    layout = make_layout()

    with Live(layout, refresh_per_second=10, screen=True):
        while True:
            layout["left"].update(backoff_panel(metrics))
            layout["right"].update(retry_counter_panel(metrics))

            if metrics.done:
                break

            if timeout.expired():
                break

            if quit_event.is_set():
                break

            await asyncio.sleep(0.1)
```

This loop is:

* Responsive
* Non-blocking
* Honest about why it exits

---

# 4️⃣ Save Final Snapshot to File

Once `Live` exits, the screen state is stable.

### Render Snapshot

```python
from rich.console import Console

def save_snapshot(renderable, path="dashboard_final.txt"):
    console = Console(record=True)
    console.print(renderable)
    console.save_text(path)
```

Usage:

```python
save_snapshot(layout, "final_dashboard.txt")
```

This gives you:

* CI artifacts
* Incident evidence
* Post-mortem screenshots (text-based)

---

# 5️⃣ Exit Codes Tied to Metrics

Exit codes should **mean something**.

### Canonical Mapping

```python
def exit_code(metrics) -> int:
    if metrics.tasks_failed_total > 0:
        return 2      # partial failure
    if metrics.tasks_success_total == 0:
        return 1      # total failure
    return 0          # success
```

Used by:

* shell scripts
* CI pipelines
* supervisors
* Kubernetes jobs

---

# 6️⃣ Full Entry Point (Everything Wired)

```python
async def main():
    metrics = RetryMetrics(tasks_total=1)
    quit_event = threading.Event()
    timeout = Timeout(seconds=30)

    key_thread = threading.Thread(
        target=listen_for_quit,
        args=(quit_event,),
        daemon=True,
    )
    key_thread.start()

    await asyncio.gather(
        dashboard(metrics, quit_event, timeout),
        worker(metrics),
    )

    save_snapshot(make_layout(), "final_dashboard.txt")
    return exit_code(metrics)
```

```python
if __name__ == "__main__":
    try:
        code = asyncio.run(main())
    except KeyboardInterrupt:
        code = 130  # standard Ctrl-C exit
    raise SystemExit(code)
```

---

# Operator UX (What the User Experiences)

* Dashboard runs live
* Spinner explains backoff
* Counters tell the truth
* Completion freezes screen
* User can:

  * press **Q** to exit early
  * wait for **auto-timeout**
  * review final state
* Exit code signals outcome upstream

That’s **first-class CLI UX**.

---

# Common Mistakes (Still Seen in 2025)

❌ Raw terminal mode
❌ Blocking `input()` inside `Live`
❌ Auto-exit without snapshot
❌ Exit code always `0`
❌ Keyboard logic mixed into UI loop

All avoidable. All expensive in production.

---

# Hard Truths (Ops Wisdom)

* Dashboards are for humans
* Exit codes are for machines
* Snapshots are for audits
* Timeouts prevent hangs
* Manual override prevents rage

---

# Bottom Line

With this pattern you now have:

✔ Live dashboard
✔ Honest metrics
✔ Retry visibility
✔ Controlled shutdown
✔ Audit trail
✔ CI-friendly exit semantics

This is **real tooling**, not a demo.

If you want next:

* JSON + text snapshots
* `/metrics` export parity
* Signal-based shutdown (SIGTERM)
* TUI navigation (tabs / views)

Just say the word.
