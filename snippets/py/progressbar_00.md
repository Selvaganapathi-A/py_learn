Alright, this is where Rich stops being “nice CLI candy” and starts being a **real operational dashboard**.

You want:

* **`rich.live.Live`**
* **`rich.layout.Layout`**
* **Spinners**
* **Dynamic status text** like
  **`(tasks_error - task_processed / total_tasks)`**
* Clean async-friendly design

Below is the **canonical pattern**. This is how you build something you can actually run in production without the UI lying to you.

---

# Executive Summary

* `Live` owns rendering
* `Layout` defines regions (header / body / footer)
* Spinners are **derived state**, not workers
* Metrics are **single source of truth**
* UI recomposes every tick

This is **reactive UI**, just without the JavaScript trauma.

---

# Mental Model (Non-Negotiable)

```
Workers ──► metrics (shared state)
                 │
                 ▼
        Live render loop
                 │
        Layout + Panels + Spinners
```

Spinners:

* Do NOT track progress
* Reflect **system state**

---

# Metrics Model (Source of Truth)

```python
from dataclasses import dataclass

@dataclass
class Metrics:
    total_tasks: int
    processed: int = 0
    errors: int = 0

    @property
    def remaining(self):
        return self.total_tasks - self.processed

    @property
    def status_text(self):
        return f"({self.errors} - {self.processed} / {self.total_tasks})"
```

Everything in the UI comes from this object.
No duplication. No guessing.

---

# Layout Definition

```python
from rich.layout import Layout

def make_layout():
    layout = Layout()

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )

    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )

    return layout
```

Think of this like CSS grid, but sane.

---

# Spinner Panel (Dynamic Text)

```python
from rich.panel import Panel
from rich.spinner import Spinner
from rich.align import Align

def spinner_panel(metrics: Metrics):
    spinner = Spinner(
        "dots",
        text=f"[bold yellow]Processing {metrics.status_text}[/]"
    )
    return Panel(
        Align.center(spinner),
        title="System Status",
        border_style="cyan",
    )
```

That text:

```
(errors - processed / total)
```

Is computed live, every refresh.

---

# Header / Footer Panels

```python
from rich.text import Text
from rich.panel import Panel

def header():
    return Panel(
        Text("LIVE TASK DASHBOARD", justify="center", style="bold white"),
        style="bold blue",
    )

def footer(metrics: Metrics):
    return Panel(
        f"[green]Remaining:[/] {metrics.remaining}",
        style="bold green",
    )
```

---

# Live Dashboard Loop (Async-Safe)

```python
import asyncio
from rich.live import Live

async def dashboard(metrics: Metrics):
    layout = make_layout()

    with Live(layout, refresh_per_second=10, screen=True):
        while metrics.processed < metrics.total_tasks:
            layout["header"].update(header())
            layout["left"].update(spinner_panel(metrics))
            layout["right"].update(
                Panel(
                    f"[red]Errors:[/] {metrics.errors}",
                    title="Errors",
                )
            )
            layout["footer"].update(footer(metrics))

            await asyncio.sleep(0.1)
```

This loop:

* Owns rendering
* Rebuilds UI declaratively
* Never blocks workers

---

# Simulated Worker Updates (Async Example)

```python
async def simulate_work(metrics: Metrics):
    for i in range(metrics.total_tasks):
        await asyncio.sleep(0.15)
        metrics.processed += 1
        if i % 7 == 0:
            metrics.errors += 1
```

---

# Entry Point

```python
async def main():
    metrics = Metrics(total_tasks=50)
    await asyncio.gather(
        dashboard(metrics),
        simulate_work(metrics),
    )

asyncio.run(main())
```

---

# Why This Design Works

### Spinners are informational

They show *state*, not progress math.

### Layout is static

Only content updates → zero flicker.

### Metrics are centralized

No race conditions.
No UI drift.

### Live loop is cheap

10 FPS is plenty for humans.

---

# Common Production Disasters (Avoid These)

### 💥 Spinner tied to worker lifecycle

Spinner stops → system “looks” dead while work continues.

### 💥 Progress logic inside UI

Now UI bugs break business logic.

### 💥 Multiple Live contexts

Terminal corruption guaranteed.

---

# Strong Opinions (Earned the Hard Way)

* Dashboards are **views**, not controllers
* Spinners should explain *why* work is happening
* Numbers beat animations
* If UI recomputes logic, your architecture is wrong

---

# Bottom Line

This pattern gives you:

* Live dashboards
* Accurate spinners
* Zero flicker
* Honest metrics
* Clean async integration

If you want next:

* Error lists scrolling live
* Per-task spinners
* Retry / backoff visualization
* Prometheus-style counters

Say the word.
