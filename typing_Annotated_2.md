Great question — this is where people *expect* annotations to do more than they actually do. Let’s be brutally clear and then show the **correct, Python-only way** to handle this.

---

# Goal

> **Annotate `num` so it must be between 0 and 10 — purely Python, no FastAPI, no frameworks.**

---

## Short, honest answer (tell-it-like-it-is)

**You CANNOT enforce numeric ranges with type annotations alone in Python.**
Annotations are **metadata**, not guards.

If you want enforcement, you **must add runtime code**.

---

## What annotations CAN do (and what they can’t)

### ❌ What they can’t do

```python
def f(num: int): ...
```

This does **nothing** to stop:

```python
f(-999)
f(999)
f("boom")
```

Python doesn’t care.

---

## The RIGHT mental model

| Tool           | Purpose         |
| -------------- | --------------- |
| Type hints     | Static analysis |
| Annotations    | Metadata        |
| Runtime checks | Safety          |
| Validation     | Correctness     |

You need **runtime checks**. Period.

---

# Option 1: Pure annotation (documentation only)

### What (metadata only)

```python
from typing import Annotated

def process(num: Annotated[int, "range 0..10"]):
    return num
```

### Why this exists

* Documentation
* Tooling hooks
* Future extensibility

### Reality check

❌ No enforcement
❌ No validation
❌ No safety

**This is a comment with better syntax.**

---

## Disaster Story 💣

A team relied on annotations like this for “constraints”.

Invalid values hit production.
Corrupt data went into the DB.
Cleanup took weeks.

**Annotations ≠ validation.**

---

# Option 2: Correct & Pythonic (runtime enforcement)

### ✅ This is the professional solution

```python
def process(num: int) -> int:
    if not 0 <= num <= 10:
        raise ValueError("num must be between 0 and 10")
    return num
```

### Why this wins

* Clear
* Fast
* Explicit
* Zero magic
* Production-safe

---

# Option 3: Annotation + runtime check (best balance)

This is the **recommended** pattern.

```python
from typing import Annotated

def process(num: Annotated[int, "0 <= num <= 10"]) -> int:
    if not 0 <= num <= 10:
        raise ValueError("num must be between 0 and 10")
    return num
```

### Why this is excellent

* Annotation documents intent
* Runtime code enforces reality
* Type checkers stay happy
* Humans understand immediately

---

# Option 4: Reusable constraint (clean, scalable)

### Define a helper

```python
def validate_0_10(num: int) -> int:
    if not 0 <= num <= 10:
        raise ValueError("num must be between 0 and 10")
    return num
```

### Use it everywhere

```python
from typing import Annotated

Num0To10 = Annotated[int, "0 <= num <= 10"]

def process(num: Num0To10) -> int:
    return validate_0_10(num)
```

This scales cleanly across codebases.

---

# Option 5: Descriptor (advanced, Python-only)

For class attributes:

```python
class Range0To10:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if not 0 <= value <= 10:
            raise ValueError("Must be between 0 and 10")
        obj.__dict__[self.name] = value


class Model:
    num = Range0To10()
```

Now:

```python
m = Model()
m.num = 5    # OK
m.num = 50   # 💥
```

Used in serious systems. Not beginner-friendly.

---

# pytest Test (because correctness matters)

```python
import pytest

def process(num: int) -> int:
    if not 0 <= num <= 10:
        raise ValueError
    return num

def test_valid():
    assert process(5) == 5

def test_invalid():
    with pytest.raises(ValueError):
        process(11)
```

---

# Expert Advice 🧠 (Strong Opinions)

* Annotations **document**, they don’t **protect**
* If safety matters, **write code**
* Don’t invent annotation-based validation unless you also write the interpreter for it
* Explicit checks beat clever tricks

---

# What NOT to do in Development 🚫

* ❌ Assume annotations enforce rules
* ❌ Hide validation in comments
* ❌ Trust static typing for runtime safety

---

# What NOT to do in Production 🚫🚫

* ❌ Accept unchecked user input
* ❌ Rely on `assert` (can be stripped!)
* ❌ Skip validation “for performance”

---

## Bottom Line (Executive Summary)

* **Pure Python cannot enforce ranges via annotations alone**
* Use annotations for **intent**
* Use runtime checks for **truth**
* Anything else is wishful thinking

If you want next:

* Custom validators
* Dataclasses with validation
* `__post_init__` patterns
* Writing an annotation processor (advanced)

Say where you want to go.
