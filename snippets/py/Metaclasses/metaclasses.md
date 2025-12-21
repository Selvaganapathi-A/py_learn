Alright. Metaclasses.
This is the **top of the Python power pyramid**. No mysticism, no folklore—just mechanics, intent, and disciplined usage.

---

# Metaclasses (Python 3.14)

## 1. What is a Metaclass?

A **metaclass is a class whose instances are classes**.

Let that land.

* Normal class → creates **objects**
* Metaclass → creates **classes**

In Python:

```python
type(int) is type
type(type) is type
```

So the default metaclass for *every* class is `type`.

> **Metaclasses define how classes themselves are constructed.**

---

## 2. Where do Metaclasses Fit in the Object Model?

Python’s hierarchy looks like this:

```
object
  ↑
class
  ↑
metaclass (type)
```

When Python executes:

```python
class User:
    pass
```

Internally, it does:

```python
User = type("User", (), {})
```

So yes:

> **`class` syntax is just a nicer way to call a metaclass.**

---

## 3. Why Do Metaclasses Exist?

Because some problems require **class-level enforcement**, not instance-level behavior.

Metaclasses exist to:

* Enforce class contracts
* Modify class attributes
* Auto-register classes
* Validate class definitions
* Build ORMs, serializers, frameworks
* Control inheritance behavior

> Brutal truth:
> **If `__init_subclass__` can do it, use that.
> If it can’t, you’re in metaclass territory.**

---

## 4. When Should You Use a Metaclass?

### Legitimate use cases

* Framework development
* ORMs (Django, SQLAlchemy)
* DSLs
* API schema enforcement
* Class-level validation that must happen **before subclass hooks**

### Red flags 🚩

* Business logic
* Data processing
* Application code
* “It feels cool”

> Metaclasses are a scalpel, not a hammer.

---

## 5. How a Metaclass Works (Lifecycle)

When a class is defined:

1. Class body is executed
2. Namespace dictionary is created
3. Metaclass is called:

   ```python
   MetaClass(name, bases, namespace)
   ```
4. Class object is returned

That’s it. No magic.

---

## 6. Basic Metaclass Structure (Minimal)

```python
class Meta(type):
    def __new__(
        mcls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> type:
        return super().__new__(mcls, name, bases, namespace)
```

Key points:

* `mcls` = metaclass itself
* `name` = class name
* `bases` = base classes
* `namespace` = class body contents

---

## 7. Simple Example: Enforcing a Class Attribute

### Goal

Every subclass **must define `table_name`**

```python
class ModelMeta(type):
    def __new__(
        mcls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> type:
        if name != "BaseModel" and "table_name" not in namespace:
            raise TypeError("Models must define table_name")
        return super().__new__(mcls, name, bases, namespace)
```

Base class:

```python
class BaseModel(metaclass=ModelMeta):
    pass
```

Valid:

```python
class User(BaseModel):
    table_name: str = "users"
```

Invalid (fails at import time):

```python
class Broken(BaseModel):
    pass
```

**Impact:**
Errors surface *before the app even runs*.

---

## 8. Real-World Example: ORM-Style Field Collection

This is not theoretical. This is how ORMs are born.

```python
from typing import Dict


class ModelMeta(type):
    def __new__(
        mcls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> type:
        fields: Dict[str, type] = {
            key: value
            for key, value in namespace.get("__annotations__", {}).items()
        }

        namespace["_fields"] = fields
        return super().__new__(mcls, name, bases, namespace)
```

Usage:

```python
class Model(metaclass=ModelMeta):
    pass


class User(Model):
    id: int
    email: str
```

Result:

```python
print(User._fields)
# {'id': int, 'email': str}
```

That’s ORM infrastructure in ~20 lines.

---

## 9. Metaclass vs `__init_subclass__`

| Feature     | `__init_subclass__`  | Metaclass             |
| ----------- | -------------------- | --------------------- |
| Complexity  | Low                  | High                  |
| Readability | High                 | Medium                |
| Power       | High                 | Maximum               |
| Runs        | After class creation | During class creation |
| Preferred   | ✅                    | ❌ (unless necessary)  |

**Rule of thumb:**

> Start with `__init_subclass__`.
> Escalate to metaclasses only if blocked.

---

## 10. Combining Metaclasses (The Hard Truth)

You can only have **one metaclass**.

This breaks naive designs.

Solution:

* Inherit metaclasses
* Compose behavior carefully

```python
class MetaA(type): ...
class MetaB(type): ...

class MetaCombined(MetaA, MetaB):
    pass
```

This is fragile. Plan ahead.

---

## 11. Metaclasses + `super()` (Non-Negotiable)

Bad metaclass:

```python
class BadMeta(type):
    def __new__(mcls, name, bases, namespace):
        return type(name, bases, namespace)  # ❌ breaks inheritance
```

Correct:

```python
class GoodMeta(type):
    def __new__(mcls, name, bases, namespace):
        return super().__new__(mcls, name, bases, namespace)
```

If you skip `super()`, you’re sabotaging other metaclasses.

---

## 12. Real-World Example: Auto-Registering Classes (Framework Pattern)

```python
from typing import Dict, Type


class RegistryMeta(type):
    registry: Dict[str, Type[object]] = {}

    def __new__(
        mcls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> type:
        cls = super().__new__(mcls, name, bases, namespace)
        if name != "Plugin":
            RegistryMeta.registry[name] = cls
        return cls
```

Usage:

```python
class Plugin(metaclass=RegistryMeta):
    pass


class AnalyticsPlugin(Plugin):
    pass


class AuthPlugin(Plugin):
    pass
```

Now:

```python
print(RegistryMeta.registry)
```

Zero manual registration.

---

## 13. Common Mistakes (Tell-It-Like-It-Is)

* Using metaclasses for instance logic
* Forgetting `super()`
* Solving solvable problems with `__init_subclass__`
* Overengineering application code
* Creating unreadable abstractions

> **Metaclasses are not “advanced Python.”
> They’re “Python internals.”**

---

## 14. Executive Summary

* Metaclasses control **class creation**
* `type` is the default metaclass
* Classes are instances of metaclasses
* Metaclasses run **before** `__init_subclass__`
* They power ORMs, frameworks, and DSLs
* Use sparingly, deliberately, and defensibly

> Final verdict:
> **If you don’t need a metaclass, don’t write one.
> If you do need one, nothing else will suffice.**

If you want the final boss levels:

* Writing a mini ORM
* Metaclasses + `__class_getitem__`
* Custom typing systems
* Rebuilding `dataclasses` from scratch

Say the word.
