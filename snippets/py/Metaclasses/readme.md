<!-- Alright. Buckle up. **Metaclasses** are not “advanced Python” — they’re **Python’s control plane**. You almost never need them, but when you do, nothing else fits.

I’ll be blunt, structured, and practical.

--- -->

# Metaclasses in Python

## What Is a Metaclass?

A **metaclass** is the **class of a class**.

If:

```python
obj = MyClass()
```

then:

```python
MyClass = MetaClass(...)
```

In one sentence:

> **Metaclasses control how classes are created.**

Not instances. **Classes themselves.**

---

## Why Metaclasses Exist

Because Python wanted:

* Framework-level validation
* Class-time transformation
* Automatic registration
* Contract enforcement
* DSL-style APIs (ORMs, serializers, models)

You cannot reliably do these with:

* decorators alone
* inheritance alone
* `__init_subclass__` alone

Metaclasses run **before the class exists**.

---

## Where Metaclasses Are Used (Real Systems)

| System      | Why                         |
| ----------- | --------------------------- |
| Django ORM  | Model field collection      |
| SQLAlchemy  | Table + column synthesis    |
| ABCs        | Abstract method enforcement |
| Enum        | Member construction         |
| Pydantic v1 | Model parsing               |
| Dataclasses | Field transformation        |
| FastAPI     | Schema introspection        |

Metaclasses are **framework scaffolding**.

---

## How Class Creation Works (Critical Mental Model)

When Python sees:

```python
class User(Base):
    name = "Element"
```

It actually does:

```python
User = Meta(
    "User",
    (Base,),
    {"name": "Element"}
)
```

Default metaclass:

```python
type
```

So yes:

```python
isinstance(User, type)  # True
```

---

## Your First Metaclass (Minimal, Typed)

```python
class Meta(type):
    def __new__(
        mcls: type[type],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> type:
        print(f"Creating class {name}")
        return super().__new__(mcls, name, bases, namespace)
```

```python
class Demo(metaclass=Meta):
    pass
```

Output:

```text
Creating class Demo
```

---

## `__new__` vs `__init__` in Metaclasses

| Method     | When                | Purpose          |
| ---------- | ------------------- | ---------------- |
| `__new__`  | Before class exists | Modify namespace |
| `__init__` | After class exists  | Final checks     |

90% of real work happens in `__new__`.

---

## Practical Use Case 1: Enforcing Class Contracts

### Goal

Every subclass **must define `id`**

```python
class RequireID(type):
    def __init__(
        cls: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> None:
        if name != "Base" and "id" not in namespace:
            raise TypeError(f"{name} must define 'id'")
        super().__init__(name, bases, namespace)
```

```python
class Base(metaclass=RequireID):
    pass
```

```python
class User(Base):
    id: int = 1  # OK
```

```python
class Bad(Base):
    pass  # 💥 TypeError
```

---

## Practical Use Case 2: Automatic Registration (Plugin System)

```python
class Registry(type):
    registry: dict[str, type] = {}

    def __new__(
        mcls: type[type],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> type:
        cls = super().__new__(mcls, name, bases, namespace)
        if name != "Plugin":
            mcls.registry[name] = cls
        return cls
```

```python
class Plugin(metaclass=Registry):
    pass
```

```python
class AuthPlugin(Plugin):
    pass
```

```python
Registry.registry
```

---

## Practical Use Case 3: Field Collection (ORM-Style)

```python
class Field:
    def __init__(self, type_: type) -> None:
        self.type = type_
```

```python
class ModelMeta(type):
    def __new__(
        mcls: type[type],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> type:
        fields: dict[str, Field] = {
            k: v for k, v in namespace.items()
            if isinstance(v, Field)
        }

        namespace["_fields"] = fields
        return super().__new__(mcls, name, bases, namespace)
```

```python
class Model(metaclass=ModelMeta):
    pass
```

```python
class User(Model):
    id = Field(int)
    name = Field(str)
```

```python
User._fields
```

This is how ORMs work. No exaggeration.

---

## Metaclass vs Alternatives (Be Honest)

| Need                   | Use                 |
| ---------------------- | ------------------- |
| Modify functions       | Decorator           |
| Modify attributes      | Descriptor          |
| Reuse behavior         | Mixin               |
| React to subclassing   | `__init_subclass__` |
| Control class creation | Metaclass           |

If `__init_subclass__` works, **use it instead**.
Metaclasses are last-resort power tools.

---

## Metaclass + Inheritance Rules (Gotcha)

You can have **only one metaclass**.

This fails:

```python
class A(metaclass=Meta1): ...
class B(metaclass=Meta2): ...

class C(A, B): ...  # 💥 conflict
```

Unless:

```python
class Meta3(Meta1, Meta2): ...
```

Metaclasses obey MRO too. Yes, really.

---

## When NOT to Use Metaclasses (Most of the Time)

* Business logic
* App-level code
* Simple validation
* Configuration
* Anything your teammates must debug at 3AM

Metaclasses are **library code**, not application code.

---

## One-Line Mental Model

> **Decorators change functions
> Descriptors change attributes
> Mixins change classes
> Metaclasses change class creation itself**

---

## Strategic Advice (Forward-Thinking)

Use metaclasses when:

* You’re building a framework
* You need class-time guarantees
* You want declarative APIs

Avoid them when:

* Readability matters more than power
* A decorator or hook would suffice

Metaclasses are a scalpel. Not a hammer.
<!--
---

If you want next:

* metaclass vs `__init_subclass__`
* typing metaclasses properly
* combining metaclasses + descriptors
* how Django & SQLAlchemy actually do this
* debugging MRO & metaclass conflicts

Say the word.
 -->

---

<!--

Good—this is where most “advanced Python” code quietly goes off the rails. **Typing metaclasses properly** is doable, but you need to be precise about *what you are typing*: the **class object**, not instances.

I’ll go from **baseline → practical → framework-grade**, with rules you can actually follow.

---
 -->

# Typing Metaclasses Properly (Python 3.14)

## First, Reset the Mental Model

Key facts (non-negotiable):

* **Classes are instances of metaclasses**
* A metaclass is a subclass of `type`
* When typing metaclasses, you are typing **class objects**
* `cls` ≠ `self`

If this clicks, typing becomes straightforward.

---

## 1️⃣ The Minimal, Correctly Typed Metaclass

```python
class Meta(type):
    def __new__(
        mcls: type[type],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> type:
        return super().__new__(mcls, name, bases, namespace)
```

### Why this is correct

| Parameter   | Meaning                  |
| ----------- | ------------------------ |
| `mcls`      | the metaclass itself     |
| `name`      | class name               |
| `bases`     | base classes             |
| `namespace` | class body dict          |
| return      | the new **class object** |

⚠️ Returning `type` is correct unless you’re doing something very specific.

---

## 2️⃣ Typing `cls` in Metaclass Methods

Inside metaclass methods:

```python
cls: type
```

**NOT**:

```python
cls: Self
```

Why?

* `Self` is for **instances**
* `cls` is a **class object**

Correct:

```python
class Meta(type):
    def __init__(
        cls: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> None:
        super().__init__(name, bases, namespace)
```

---

## 3️⃣ Typing Classes Created by a Metaclass

### Example: Base Class with Metaclass

```python
class ModelMeta(type):
    pass

class Model(metaclass=ModelMeta):
    pass
```

Type facts:

```python
isinstance(Model, ModelMeta)  # True
isinstance(Model, type)       # True
```

### Static typing view

* `Model` → `type[Model]`
* `ModelMeta` → `type[type]`

Yes, it’s meta all the way up.

---

## 4️⃣ Typed Metaclass That Adds Attributes

### Example: Field Collection (ORM-style)

```python
class Field:
    def __init__(self, py_type: type) -> None:
        self.py_type = py_type
```

### Typed Metaclass

```python
class ModelMeta(type):
    def __new__(
        mcls: type[type],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> type:
        fields: dict[str, Field] = {
            key: value
            for key, value in namespace.items()
            if isinstance(value, Field)
        }

        namespace["_fields"] = fields
        return super().__new__(mcls, name, bases, namespace)
```

### Typed Base Class

```python
class Model(metaclass=ModelMeta):
    _fields: dict[str, Field]
```

Why declare `_fields`?

* The metaclass injects it
* Static type checkers can’t see that
* You must **declare the contract explicitly**

This is a critical pattern.

---

## 5️⃣ Typing Metaclasses with Generics (Advanced but Real)

### Goal

Preserve the **actual subclass type** returned by the metaclass.

### TypeVar bound to `type`

```python
from typing import TypeVar

T = TypeVar("T", bound=type)
```

### Generic Metaclass

```python
class RegistryMeta(type):
    registry: dict[str, type] = {}

    def __new__(
        mcls: type[type],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> type:
        cls = super().__new__(mcls, name, bases, namespace)
        if name != "Plugin":
            mcls.registry[name] = cls
        return cls
```

Usage:

```python
class Plugin(metaclass=RegistryMeta):
    pass

class AuthPlugin(Plugin):
    pass
```

Static typing:

* `RegistryMeta.registry` → `dict[str, type]`
* Correct and safe

---

## 6️⃣ Typing `__init_subclass__` (Often Better Than Metaclasses)

This deserves mention because it’s **far easier to type**.

```python
class Base:
    def __init_subclass__(cls: type) -> None:
        super().__init_subclass__()
```

With constraints:

```python
class RequiresID:
    id: int

class Base:
    def __init_subclass__(cls: type[RequiresID]) -> None:
        if not hasattr(cls, "id"):
            raise TypeError("id required")
        super().__init_subclass__()
```

Cleaner. Safer. More readable.

---

## 7️⃣ Metaclass + `Protocol` (Framework-Grade Typing)

### When You Need This

You want to **type the class interface**, not instances.

```python
from typing import Protocol

class ModelClass(Protocol):
    _fields: dict[str, Field]
```

Usage:

```python
def inspect_model(cls: ModelClass) -> None:
    print(cls._fields)
```

This is how you keep metaclass magic **type-safe and testable**.

---

## 8️⃣ Common Typing Mistakes (Real Ones)

### ❌ Using `Self` in metaclasses

```python
def __new__(...) -> Self  # WRONG
```

`Self` is instance-level only.

---

### ❌ Forgetting injected attributes

```python
class Model(metaclass=Meta):
    pass  # _fields added dynamically
```

Static typing will hate you. Declare it.

---

### ❌ Over-typing `bases`

```python
bases: tuple[type[Base], ...]  # Too strict
```

Use:

```python
bases: tuple[type, ...]
```

---

## 9️⃣ Practical Rules You Can Memorize

1. **Metaclasses subclass `type`**
2. **`__new__` returns `type`**
3. **`cls` is typed as `type`**
4. **Declare everything the metaclass injects**
5. **Prefer `__init_subclass__` when possible**
6. **Use `Protocol` to type class contracts**

---

## One-Line Executive Summary

> **Typing metaclasses is about typing class objects, not instances — once you respect that boundary, everything lines up.**

---

If you want next:

* typing Django-style metaclasses
* metaclass + descriptor typing
* enforcing abstract class contracts
* refactoring metaclasses into `__init_subclass__`
* mypy / pyright gotchas with metaclasses

Say the word.

<!--

 -->

Excellent set of topics. This is **advanced Python architecture**, the stuff that makes frameworks reliable—or utterly unmaintainable if done wrong. I’ll be direct, opinionated, and practical.

Python **3.14**, fully typed, real patterns—not academic fluff.

---

# 1️⃣ Typing Django-Style Metaclasses (The Right Way)

Django uses metaclasses to:

* inspect class attributes
* register fields
* mutate the class at definition time

### The Core Typing Problem

Metaclasses return **classes**, not instances.
Most people type them incorrectly—or not at all.

---

## Properly Typed Metaclass Skeleton

```python
from typing import Any, TypeVar, Type, Mapping

T = TypeVar("T", bound=type)

class ModelMeta(type):
    def __new__(
        mcls: Type[T],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> T:
        cls = super().__new__(mcls, name, bases, namespace)
        return cls
```

### Why This Matters

* `T` preserves the **actual class type**
* Prevents metaclass from collapsing everything to `type`
* mypy/pyright stop screaming

This is **non-optional** in serious code.

---

## Django-Style Usage

```python
class Model(metaclass=ModelMeta):
    ...
```

Typing works because:

* `ModelMeta.__new__` returns the same concrete class type
* Subclasses preserve identity

---

# 2️⃣ Metaclass + Descriptor Typing (The Hard Part)

This is where most people give up. You shouldn’t.

---

## Typed Descriptor (Field)

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Field(Generic[T]):
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type | None = None) -> T:
        if instance is None:
            return self  # type: ignore[return-value]
        return instance.__dict__[self.name]

    def __set__(self, instance: object, value: T) -> None:
        instance.__dict__[self.name] = value
```

Yes, the `type: ignore` is **unavoidable** today. That’s reality.

---

## Metaclass Collecting Descriptors

```python
class ModelMeta(type):
    def __new__(
        mcls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        fields: dict[str, Field[Any]] = {
            k: v for k, v in namespace.items()
            if isinstance(v, Field)
        }

        cls = super().__new__(mcls, name, bases, namespace)
        cls.__fields__ = fields  # type: ignore[attr-defined]
        return cls
```

### Typing Reality Check

* Dynamic attribute injection = `type: ignore`
* Don’t fight it—**document it**
* Even Django accepts this tradeoff

---

# 3️⃣ Enforcing Abstract Class Contracts (Strong Guarantees)

## ❌ Wrong Way (Runtime Checks)

```python
if not hasattr(cls, "save"):
    raise TypeError("Must define save")
```

This is brittle and untyped.

---

## ✅ Correct Way: `ABCMeta`

```python
from abc import ABCMeta, abstractmethod

class Repository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, data: dict[str, object]) -> None:
        ...
```

Now:

* Runtime enforcement ✔
* Static typing ✔
* Tooling support ✔

---

## Metaclass + ABCMeta (Combined)

```python
class ModelMeta(ABCMeta):
    ...
```

This is exactly what Django does internally.

---

## Enforcing Class-Level Contracts

```python
class PluginMeta(type):
    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> None:
        super().__init__(name, bases, namespace)

        if not hasattr(cls, "plugin_name"):
            raise TypeError("plugin_name is required")
```

This enforces **structural rules at class creation time**.

---

# 4️⃣ Refactoring Metaclasses into `__init_subclass__`

### Hard Truth

> **If you can use `__init_subclass__`, you should.**

Metaclasses are a last resort.

---

## Metaclass Logic (Before)

```python
class RegistryMeta(type):
    registry: list[type] = []

    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)
        mcls.registry.append(cls)
        return cls
```

---

## `__init_subclass__` (After — Cleaner)

```python
class RegistryBase:
    registry: list[type] = []

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        RegistryBase.registry.append(cls)
```

### Why This Wins

* No metaclass conflicts
* Easier typing
* Works with multiple inheritance
* Clear intent

---

## Typed `__init_subclass__`

```python
class EnforcedBase:
    def __init_subclass__(cls, *, required: bool = False, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        cls.required = required
```

Usage:

```python
class MyClass(EnforcedBase, required=True):
    ...
```

This replaces **80% of metaclass use cases**.

---

# 5️⃣ mypy / pyright Gotchas (Real Pain Points)

## ❗ Gotcha #1: Dynamic Attributes

```python
cls.new_attr = 123
```

Static checkers hate this.

### Fix (Pick One)

* `typing.Protocol`
* `TypedDict` for metadata
* `# type: ignore[attr-defined]`

Be explicit. Silence is technical debt.

---

## ❗ Gotcha #2: Metaclass Return Types

If you don’t return `T` from `__new__`:

```text
error: incompatible return type "type" vs "MyClass"
```

Always use:

```python
T = TypeVar("T", bound=type)
```

---

## ❗ Gotcha #3: Descriptor `__get__`

Type checkers **cannot express**:

> “Return descriptor on class, value on instance”

You must choose between:

* correctness
* silence

Most frameworks choose correctness + ignore.

---

## ❗ Gotcha #4: Multiple Metaclasses

```python
TypeError: metaclass conflict
```

This is why Django prefers:

* one metaclass
* or `__init_subclass__`

Avoid stacking metaclasses. It’s a design smell.

---

## ❗ Gotcha #5: pyright Is Stricter Than mypy

pyright will flag:

* missing `**kwargs` in `__init_subclass__`
* incorrect metaclass signatures
* unsafe dynamic injection

If pyright passes, mypy usually will.

---

# Strategic Guidance (Blunt but Accurate)

* **Metaclasses are infrastructure**, not features
* If typing feels impossible, your design is suspect
* Prefer `__init_subclass__` for extensibility
* Accept limited `type: ignore`—but isolate them
* Document every metaclass with intent and invariants

---

## One-Line Mental Model

> **Metaclasses shape classes.
> Descriptors shape attributes.
> `__init_subclass__` shapes ecosystems.**

---

If you want next:

* a fully typed mini-Django ORM core
* Protocol-based alternatives to metaclasses
* how SQLAlchemy 2.x reduced metaclass usage
* writing plugins without metaclasses
* future typing improvements (PEP 544 / 649 / 695 impacts)

Say the word.
