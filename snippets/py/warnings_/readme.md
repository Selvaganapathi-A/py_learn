<!--
Alright, let’s get **warnings** straight. This is one of those features that quietly separates *toy code* from *production-grade Python*. Ignore it and you get noisy logs or missed deprecations. Use it right and you get **early risk signals without breaking users**.

--- -->

# Python Warnings

## What Are Warnings?

A **warning** is a **non-fatal runtime signal** that something is:

* deprecated
* risky
* inefficient
* likely to break in the future

Key point:

> **Warnings inform. Exceptions stop.**

Python lets your code continue running while still surfacing problems.

---

## Why Warnings Exist (Business Reason)

Warnings exist to solve a real dilemma:

* You **must** alert users about problems
* You **cannot** break backward compatibility immediately

So Python gives you:

* Gradual migration paths
* Soft enforcement
* Tooling-friendly signals (CI, tests, linters)

Deprecations without warnings are negligence.

---

## Where Warnings Are Used

You’ve seen these in the wild:

* Deprecated APIs
* Unsafe defaults
* Numeric precision issues
* Library version transitions
* Experimental features
* Performance foot-guns

Frameworks use warnings heavily because **breaking users is expensive**.

---

## When to Use Warnings (Clear Rules)

Use warnings when:

✔ The program can continue safely
✔ The issue is advisory or transitional
✔ You want visibility without failure

Do **not** use warnings when:

❌ State is corrupted
❌ Security is compromised
❌ Continuing is unsafe

That’s what exceptions are for.

---

## How Warnings Work (Mechanics)

Warnings are handled by the `warnings` module.

Core function:

```python
warnings.warn(message, category, stacklevel)
```

They are:

* Filterable
* Suppressible
* Upgradable to errors
* Capturable in tests

This is deliberate.

---

## Common Warning Categories (Know These)

```python
Warning                # Base class
UserWarning            # Default, general-purpose
DeprecationWarning     # Deprecated features
PendingDeprecationWarning
RuntimeWarning         # Runtime issues
FutureWarning          # Behavior will change
ResourceWarning        # Leaks (files, sockets)
SyntaxWarning
```

**Important reality check**:
`DeprecationWarning` is **ignored by default** outside tests.

---

## Basic Example (Typed)

```python
import warnings

def old_api(x: int) -> int:
    warnings.warn(
        "old_api() is deprecated, use new_api()",
        DeprecationWarning,
        stacklevel=2,
    )
    return x * 2
```

Why `stacklevel=2`?

* It points the warning to the **caller**
* Otherwise users blame *your* function, not *their usage*

This is non-negotiable in libraries.

---

## Using `UserWarning` (Visible by Default)

```python
def risky_operation(value: int) -> int:
    if value < 0:
        warnings.warn(
            "Negative values may produce unexpected results",
            UserWarning,
            stacklevel=2,
        )
    return value * value
```

---

## Turning Warnings Into Errors (CI Power Move)

```python
import warnings

warnings.simplefilter("error", DeprecationWarning)
```

Now this:

```python
old_api(5)
```

Raises:

```text
DeprecationWarning → Exception
```

This is how teams **force migrations in CI** without breaking prod.

---

## Filtering Warnings (Targeted Suppression)

```python
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module="legacy_module",
)
```

Rules:

* Filter narrowly
* Never blanket-ignore warnings globally
* Suppression should be intentional and documented

---

## Context Manager: Local Control

```python
import warnings

def run_experiment() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        risky_math()
```

Perfect for:

* Tests
* One-off migrations
* Third-party noise containment

---

## Capturing Warnings in Tests (Professional Move)

```python
import warnings

def test_deprecation() -> None:
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        old_api(1)

        assert len(captured) == 1
        assert issubclass(captured[0].category, DeprecationWarning)
```

This is how you **enforce deprecation contracts**.

---

## `warnings.warn` vs `logging.warning`

Tell-it-like-it-is comparison:

| Aspect              | `warnings` | `logging` |
| ------------------- | ---------- | --------- |
| Audience            | Developers | Operators |
| Suppressible        | Yes        | No        |
| Upgradable to error | Yes        | No        |
| API lifecycle       | Yes        | No        |
| Runtime diagnostics | No         | Yes       |

Rule:

* **Warnings → code evolution**
* **Logging → system behavior**

Mixing them is a design smell.

---

## Real-World Pattern: Soft Breaking Change

```python
def api_v2(x: int, *, strict: bool = False) -> int:
    if not strict:
        warnings.warn(
            "Default behavior will change in v3. "
            "Pass strict=True to opt in early.",
            FutureWarning,
            stacklevel=2,
        )
    return x + 1
```

This is how you migrate users without chaos.

---

## Anti-Patterns (Don’t Do This)

🚫 Using warnings for control flow
🚫 Ignoring warnings in libraries
🚫 Spamming warnings in loops
🚫 Raising warnings instead of exceptions
🚫 No `stacklevel`

Warnings should be **rare, precise, and actionable**.

---

## One-Line Mental Model

> **Warnings are promises about the future, not failures of the present.**

---

## Strategic Advice (Forward-Looking)

* Treat warnings as **technical debt signals**
* Fail CI on deprecations
* Keep prod permissive, tests strict
* Document every warning you emit
* Remove warnings once the transition is complete

Warnings are how mature systems evolve **without breaking trust**.

---
<!--

If you want next:

* real production bugs caused by ignored warnings
* warning policies for teams
* custom warning classes
* integrating warnings with pytest
* deprecation strategy playbooks

Say the word.
===

Perfect—this is **engineering governance**, not syntax trivia. I’ll give you **battle-tested policies**, **drop-in code**, and a **playbook you can hand to a team** without embarrassment.

---
-->

# 1️⃣ Warning Policies for Teams (Non-Negotiable)

## The Core Principle

> **Warnings are technical-debt signals.
> CI should treat them as blockers. Production should not.**

That split alone prevents 80% of warning-related chaos.

---

## Team-Wide Policy (Baseline)

### 🔹 Production

* Allow warnings
* Log *counts*, not stack traces
* Never crash user flows due to warnings

### 🔹 Development

* Show warnings loudly
* Never suppress globally
* Developers fix warnings they introduce

### 🔹 CI / Tests

* **Warnings = errors**
* Explicit exceptions only
* Zero tolerance for new deprecations

---

## Canonical Policy Table

| Environment | Rule                          |
| ----------- | ----------------------------- |
| Local dev   | Show all warnings             |
| CI          | Treat warnings as errors      |
| Tests       | Capture and assert            |
| Libraries   | Emit warnings, never silence  |
| Apps        | Filter narrowly, document why |

---

## Enforcing Policy (Centralized)

```python
# warnings_policy.py
import warnings

def configure_warnings(env: str) -> None:
    if env == "ci":
        warnings.simplefilter("error")
    elif env == "dev":
        warnings.simplefilter("default")
    elif env == "prod":
        warnings.filterwarnings("default", category=DeprecationWarning)
```

Call this **once**, at startup. Never ad hoc.

---

# 2️⃣ Custom Warning Classes (Professional Grade)

## Why Custom Warnings Matter

Built-in warnings are too generic.

Custom warnings let you:

* Filter precisely
* Track ownership
* Communicate intent clearly

> **If it’s your API, it deserves its own warning class.**

---

## Proper Custom Warning Hierarchy

```python
class AppWarning(Warning):
    """Base warning for the application."""

class AppDeprecationWarning(DeprecationWarning, AppWarning):
    """Deprecated application feature."""

class AppRuntimeWarning(RuntimeWarning, AppWarning):
    """Risky runtime behavior."""
```

Why this structure works:

* Compatible with Python tooling
* Filterable by *your* namespace
* Doesn’t pollute global warning space

---

## Emitting a Custom Warning (Correctly)

```python
import warnings

def legacy_feature() -> None:
    warnings.warn(
        "legacy_feature() will be removed in v3.0",
        AppDeprecationWarning,
        stacklevel=2,
    )
```

**Rule:**
Every custom warning must include:

* Removal version
* Replacement path

No exceptions.

---

# 3️⃣ Integrating Warnings with Pytest (This Is Critical)

## Default Pytest Behavior (Know This)

* Pytest **shows DeprecationWarnings**
* It can **fail tests on warnings**
* It supports **fine-grained control**

---

## Enforce “Warnings as Errors” in Pytest

### `pytest.ini`

```ini
[pytest]
filterwarnings =
    error
```

This flips the default from permissive to strict.

---

## Allow Specific Warnings (Explicitly)

```ini
filterwarnings =
    error
    ignore:.*will be removed in v3.0:AppDeprecationWarning
```

If it’s allowed, it must be **named**.

---

## Capturing and Asserting Warnings

```python
import warnings
import pytest

def test_deprecation_warning() -> None:
    with pytest.warns(AppDeprecationWarning):
        legacy_feature()
```

This is how you:

* Lock deprecation behavior
* Prevent silent removal
* Communicate intent to future devs

---

## Asserting Warning Message Content

```python
def test_warning_message() -> None:
    with pytest.warns(AppDeprecationWarning, match="v3.0"):
        legacy_feature()
```

No vague warnings. Messages are part of the contract.

---

# 4️⃣ Deprecation Strategy Playbook (Real-World)

This is the part most teams botch.

---

## Phase 0 — Design Decision (Internal)

Before writing code, decide:

* What is deprecated?
* What replaces it?
* When is it removed?

If you don’t know removal version, **don’t deprecate yet**.

---

## Phase 1 — Soft Deprecation (Release N)

```python
warnings.warn(
    "X is deprecated and will be removed in v3.0. "
    "Use Y instead.",
    AppDeprecationWarning,
    stacklevel=2,
)
```

Rules:

* No behavior change
* No performance penalty
* Full backward compatibility

---

## Phase 2 — Loud Deprecation (Release N+1)

* Keep warning
* Update docs
* Add migration guide
* CI fails on usage internally

```python
warnings.simplefilter("error", AppDeprecationWarning)
```

Internal code **must not use deprecated APIs**.

---

## Phase 3 — Behavioral Change (Optional)

```python
warnings.warn(
    "Default behavior changed in v2.5. "
    "Set strict=False to preserve old behavior.",
    FutureWarning,
    stacklevel=2,
)
```

This is how you avoid surprise regressions.

---

## Phase 4 — Removal (Release N+2 / N+3)

* Remove code
* Remove warnings
* Raise `AttributeError` or `TypeError`

No warnings at this stage.
Deprecation time is over.

---

## Deprecation Timeline (Clean Example)

| Version | Action             |
| ------- | ------------------ |
| 2.0     | Introduce warning  |
| 2.1     | Fail CI internally |
| 2.2     | Docs + tooling     |
| 3.0     | Remove API         |

Anything faster is hostile. Anything slower is negligence.

---

# Executive Rules (Print These)

1. **Warnings are contracts**
2. **CI is strict, prod is tolerant**
3. **Custom warnings for custom APIs**
4. **Every warning has a removal version**
5. **Tests must assert warnings**
6. **Warnings are temporary by design**

---

## One-Line Takeaway

> **Teams that manage warnings intentionally ship stable software; teams that ignore them ship surprises.**
<!--
---

If you want next:

* end-to-end deprecation example (API + tests + docs)
* warning policies for libraries vs apps
* how NumPy/Django do this at scale
* tooling to track warning debt
* refactoring legacy codebases full of ignored warnings

Say the word. -->
