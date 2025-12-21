Excellent choice.
`__init_subclass__` is one of those *architect-level* tools that quietly powers frameworks, ORMs, and plugin systems—yet most developers never touch it. Let’s break it down properly and keep it practical.

---

# `__init_subclass__` (Python 3.14)

## 1. What is `__init_subclass__`?

`__init_subclass__` is a **class hook** that runs **automatically whenever a class is subclassed**.

* It runs **once at class creation time**
* It runs **on the parent class**
* It configures or validates **child classes**
* It is **not** an instance method

> In plain English:
> **It lets a base class control how its subclasses are defined.**

---

## 2. Where does it sit in Python’s lifecycle?

When Python executes:

```python
class Child(Parent):
    ...
```

The order is roughly:

1. Class body is executed
2. Class object is created
3. `Parent.__init_subclass__(Child, **kwargs)` is called

No instances involved. This is **class-time**, not runtime.

---

## 3. Why does `__init_subclass__` exist?

Because **frameworks need rules**.

It exists to:

* Enforce subclass contracts
* Auto-register subclasses
* Attach metadata
* Validate class attributes
* Replace fragile metaclasses in 90% of cases

> Strong opinion:
> **If you’re thinking about a metaclass, try `__init_subclass__` first.**

---

## 4. When should you use it? (And when not)

### Use it when:

* You want to **validate subclasses**
* You’re building **framework-style base classes**
* You need **automatic registration**
* You want subclass configuration via keyword arguments
* You want clean, readable extensibility

### Don’t use it when:

* You only need instance behavior
* A decorator would suffice
* You’re enforcing logic at runtime instead of definition-time

---

## 5. How it works (mechanics)

### Signature

```python
class Base:
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
```

Key facts:

* `cls` is the **subclass being created**
* Called automatically
* Accepts keyword arguments from subclass definition
* Must call `super()` to preserve inheritance chains

---

## 6. Simple Example (Conceptual)

### Enforcing a required class attribute

```python
class PluginBase:
    name: str

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "name"):
            raise TypeError("Plugins must define a 'name' attribute")
```

Valid subclass:

```python
class MyPlugin(PluginBase):
    name: str = "analytics"
```

Invalid subclass:

```python
class BrokenPlugin(PluginBase):
    pass  # Raises TypeError at import time
```

**Value:** errors fail fast—before your app even starts.

---

## 7. Subclass Configuration via Keywords (Clean Pattern)

### Example

```python
class Endpoint:
    route: str
    method: str

    def __init_subclass__(cls, *, route: str, method: str = "GET", **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.route = route
        cls.method = method
```

Usage:

```python
class HealthCheck(Endpoint, route="/health", method="GET"):
    pass
```

Result:

* Declarative
* Readable
* Zero boilerplate

Frameworks *love* this pattern.

---

## 8. Real-World Example: Automatic Registration System

### Use case

* Plugin systems
* Event handlers
* Background jobs
* Admin panels

```python
from typing import Dict, Type


class Task:
    registry: Dict[str, Type["Task"]] = {}

    task_name: str

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "task_name"):
            raise TypeError("Task subclasses must define task_name")

        Task.registry[cls.task_name] = cls
```

Subclasses:

```python
class EmailTask(Task):
    task_name: str = "email"


class CleanupTask(Task):
    task_name: str = "cleanup"
```

Usage:

```python
task_cls: Type[Task] = Task.registry["email"]
task: Task = task_cls()
```

**Business impact:**

* Zero manual registration
* Extensible architecture
* Clean plugin onboarding

---

## 9. Real-World Example: ORM-style Field Validation

```python
from typing import Dict


class Model:
    fields: Dict[str, type]

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.fields = {
            name: value
            for name, value in cls.__annotations__.items()
        }
```

Usage:

```python
class User(Model):
    id: int
    email: str
```

Result:

```python
print(User.fields)
# {'id': int, 'email': str}
```

This is how ORMs *start* their magic.

---

## 10. `__init_subclass__` vs Metaclasses

| Feature           | `__init_subclass__` | Metaclass |
| ----------------- | ------------------- | --------- |
| Readability       | High                | Low       |
| Learning curve    | Low                 | Steep     |
| Power             | Medium–High         | Maximum   |
| Maintenance cost  | Low                 | High      |
| Recommended first | ✅                   | ❌         |

**Rule of thumb:**

> If `__init_subclass__` can solve it, don’t touch metaclasses.

---

## 11. Executive Summary (Straight Talk)

* `__init_subclass__` runs **once, at class definition**
* It enforces rules **before runtime**
* It replaces most metaclass use cases
* It enables clean, scalable frameworks
* It is **definition-time architecture**, not runtime logic

If you want to continue logically, the next power trio is:

* `__class_getitem__`
* `Protocol` + `typing`
* Metaclasses (only if you’re brave)

Say where you want to go next.
