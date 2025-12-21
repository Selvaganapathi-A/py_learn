Excellent choice. **Prometheus-style counters** are exactly what you want when you care about **truthful metrics over flashy UI**.

Below is the **clean, correct, production-grade pattern** for using **Prometheus-style counters inside a Rich live dashboard**.

---

# Executive Summary

* Counters are **monotonic** (only go up)
* Rates are **derived**, never stored
* UI reads metrics, never mutates them
* Rich renders a **read-only view** of system health

This mirrors real Prometheus thinking—and prevents lying dashboards.

---

# What Is a Prometheus-Style Counter?

A counter:

* Starts at zero
* Only increments
* Is never reset (except on process restart)

Examples:

* `tasks_processed_total`
* `tasks_failed_total`
* `retries_total`

If a metric can go down → **it is not a counter**.

---

# Metrics Model (Single Source of Truth)

```python
import time
from dataclasses import dataclass, field

@dataclass
class Counters:
    start_time: float = field(default_factory=time.monotonic)

    tasks_total: int = 0
    tasks_processed_total: int = 0
    tasks_failed_total: int = 0

    @property
    def uptime(self) -> float:
        return time.monotonic() - self.start_time

    @property
    def processing_rate(self) -> float:
        if self.uptime == 0:
            return 0.0
        return self.tasks_processed_total / self.uptime
```

Key insight:

> **Rates are computed, not stored**

That’s pure Prometheus discipline.

---

# Incrementing Counters (Workers)

Workers **only increment counters**.
No resets. No math. No UI logic.

```python
async def worker(metrics: Counters, total: int):
    for i in range(total):
        await asyncio.sleep(0.15)
        metrics.tasks_processed_total += 1
        if i % 6 == 0:
            metrics.tasks_failed_total += 1
```

---

# Rich Counter Panel

```python
from rich.panel import Panel
from rich.table import Table

def counter_panel(metrics: Counters) -> Panel:
    table = Table.grid(padding=1)
    table.add_column(justify="left")
    table.add_column(justify="right")

    table.add_row(
        "Tasks processed",
        f"[green]{metrics.tasks_processed_total}[/]"
    )
    table.add_row(
        "Tasks failed",
        f"[red]{metrics.tasks_failed_total}[/]"
    )
    table.add_row(
        "Processing rate",
        f"[cyan]{metrics.processing_rate:.2f}/sec[/]"
    )
    table.add_row(
        "Uptime",
        f"{metrics.uptime:.1f}s"
    )

    return Panel(
        table,
        title="Counters",
        border_style="green",
    )
```

This is **exactly** how Prometheus dashboards work:

* Raw counts
* Derived rates
* No percentages stored anywhere

---

# Status Spinner (Derived Signal)

```python
from rich.spinner import Spinner
from rich.align import Align

def status_spinner(metrics: Counters):
    text = (
        f"[bold yellow]"
        f"({metrics.tasks_failed_total} - "
        f"{metrics.tasks_processed_total} / "
        f"{metrics.tasks_total})"
        f"[/]"
    )
    return Align.center(Spinner("dots", text=text))
```

This spinner:

* Shows **error count**
* Shows **progress**
* Does NOT drive logic

Pure visualization.

---

# Layout Assembly

```python
from rich.layout import Layout

def make_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )
    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )
    return layout
```

---

# Live Dashboard Loop

```python
import asyncio
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

async def dashboard(metrics: Counters):
    layout = make_layout()

    with Live(layout, refresh_per_second=10, screen=True):
        while metrics.tasks_processed_total < metrics.tasks_total:
            layout["header"].update(
                Panel(
                    Text("PROMETHEUS-STYLE METRICS", justify="center"),
                    style="bold blue",
                )
            )

            layout["left"].update(
                Panel(status_spinner(metrics), title="Status")
            )

            layout["right"].update(counter_panel(metrics))

            layout["footer"].update(
                Panel(
                    f"Total tasks: {metrics.tasks_total}",
                    style="bold green",
                )
            )

            await asyncio.sleep(0.1)
```

---

# Entry Point

```python
async def main():
    metrics = Counters()
    metrics.tasks_total = 60

    await asyncio.gather(
        dashboard(metrics),
        worker(metrics, metrics.tasks_total),
    )

asyncio.run(main())
```

---

# Why This Is “Prometheus-Correct”

✔ Counters never decrease
✔ Rates derived from monotonic time
✔ UI is a pure consumer
✔ Metrics are append-only
✔ Restart resets everything (as expected)

This means:

* You can export these metrics later
* You can compare runs
* You can reason about failures

---

# Common Anti-Patterns (Seen in Real Systems)

### ❌ Percent complete stored as a metric

Breaks on retries and restarts.

### ❌ “Remaining tasks” as a counter

That’s a **gauge**, not a counter.

### ❌ Resetting counters on errors

You just destroyed observability.

---

# Hard Truths (Prometheus Wisdom)

* Counters tell the truth
* Gauges lie when abused
* Rates explain behavior
* Dashboards should never do math you care about

---

# Bottom Line

This gives you:

* Honest metrics
* Predictable dashboards
* Prometheus-compatible thinking
* Zero UI-driven bugs

If you want next:

* Gauges vs counters (side-by-side)
* Histograms / buckets (latency)
* Exporting these metrics to `/metrics`
* Alert-style UI panels

Say the word.
