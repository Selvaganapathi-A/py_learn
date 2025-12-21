# `__new__` Method (Python 3.14)

This is one of those *power-user* Python concepts that most people vaguely know exists—and then misuse or avoid entirely. We’ll do it properly.

---


## 1. What is `__new__`?

`__new__` is a __class-level method responsible for creating a new instance__ of a class.

* It runs __before__ `__init__`
* It must __return an instance__
* It controls __object creation__, not initialization

> __Think of it this way:__
> `__new__` = *birth*
> `__init__` = *upbringing*

---

## 2. Where does `__new__` fit in object creation?

When you do:

```python
obj = MyClass(arg1, arg2)
```

Python internally does:

1. Call `MyClass.__new__(MyClass, arg1, arg2)`
2. Receive an instance
3. Call `MyClass.__init__(instance, arg1, arg2)`
4. Return the instance

If `__new__` __does not return an instance of the class__, `__init__` is __never called__.

That’s not trivia — that’s leverage.

---

## 3. Why does `__new__` exist?

Because __some objects must control how they are created__, not just how they’re initialized.

Key reasons:

* __Immutable objects__ (`int`, `str`, `tuple`)
* __Singleton patterns__
* __Instance caching / flyweight pattern__
* __Returning existing objects instead of creating new ones__
* __Subclassing immutable built-ins__
* __Metaprogramming__

If you only need to set attributes → __use `__init__`__
If you need to __decide whether or how an object exists__ → __use `__new__`__

---

## 4. When should you use `__new__`? (And when not)

### Use `__new__` when

* The class is __immutable__
* You want __only one instance__ (singleton)
* You want to __reuse instances__
* You subclass `int`, `str`, `tuple`, `frozenset`
* You need to return a __different class instance__

### Do NOT use `__new__` when

* You’re just assigning attributes
* You want validation only
* You don’t fully understand object lifecycle (tell it like it is)

> Hot take:
> __90% of `__new__` usage in codebases is unnecessary cleverness.__

---

## 5. How `__new__` works (mechanics)

### Signature

```python
class MyClass:
    def __new__(cls, *args, **kwargs) -> "MyClass":
        instance = super().__new__(cls)
        return instance
```

Key rules:

* It is implicitly a __static method__
* First argument is __the class (`cls`)__
* Must return an __instance__
* Must call `super().__new__(cls)` unless you know exactly why you aren’t

---

## 6. Simple Example (Educational)

### Example: Logging object creation

```python
class Example:
    def __new__(cls) -> "Example":
        print("Creating instance")
        instance = super().__new__(cls)
        return instance

    def __init__(self) -> None:
        print("Initializing instance")
```

Usage:

```python
obj: Example = Example()
```

Output:

```
Creating instance
Initializing instance
```

__Key takeaway:__
`__new__` runs __first__, always.

---

## 7. Immutable Object Example (Real Reason `__new__` Exists)

### Subclassing `str`

```python
class UpperCaseString(str):
    def __new__(cls, value: str) -> "UpperCaseString":
        return super().__new__(cls, value.upper())
```

Usage:

```python
name: UpperCaseString = UpperCaseString("element")
print(name)  # ELEMENT
```

Why `__init__` won’t work here:

* `str` is immutable
* You can’t modify it *after* creation
* Transformation must happen __during creation__

---

## 8. Real-World Example: Singleton (Clean, Typed)

### Use case

* Database connection
* Configuration loader
* Metrics registry

### Implementation

```python
from typing import Optional


class DatabaseConnection:
    _instance: Optional["DatabaseConnection"] = None

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.connected: bool = True
```

Usage:

```python
db1: DatabaseConnection = DatabaseConnection()
db2: DatabaseConnection = DatabaseConnection()

assert db1 is db2
```

__Business value:__

* Controlled resource usage
* Predictable state
* Zero duplicate connections

---

## 9. Real-World Example: Object Caching (Flyweight)

### Use case

* Large-scale systems
* High-frequency object creation
* Memory optimization

```python
from typing import Dict


class User:
    _cache: Dict[int, "User"] = {}

    def __new__(cls, user_id: int) -> "User":
        if user_id not in cls._cache:
            instance = super().__new__(cls)
            cls._cache[user_id] = instance
        return cls._cache[user_id]

    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id
```

Result:

* Same `user_id` → same object
* Massive memory savings in real systems

---

## 10. `__new__` vs `__init__` (Executive Summary)

| Aspect                      | `__new__`       | `__init__`          |
| --------------------------- | --------------- | ------------------- |
| Purpose                     | Create instance | Initialize instance |
| Called first                | ✅               | ❌                   |
| Can return different object | ✅               | ❌                   |
| Used for immutables         | ✅               | ❌                   |
| Common usage                | Rare            | Constant            |

---

## Final Take (No Sugar-Coating)

* `__new__` is __not advanced__, it’s __low-level__
* You don’t *graduate* to `__new__` — you __earn the right to use it__
* If your class is mutable and you’re using `__new__`, you’re probably overengineering
* When used correctly, it unlocks patterns impossible with `__init__`

If you want, next logical jumps are:

* `__init_subclass__`
* Metaclasses
* `dataclasses` vs `__new__`
* How `Enum` and `typing` use `__new__`

Say the word.
