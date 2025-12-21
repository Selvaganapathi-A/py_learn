# Event Sourcing — The Straight Story

## What It Is (No Poetry)

> **Event Sourcing = store facts (events), not state.**

You do **not** store “current balance = 100”.
You store:

```text
AccountOpened
MoneyDeposited(50)
MoneyDeposited(50)
```

Current state is **derived**, not persisted.

---

## Why It Exists (The Business Case)

Event Sourcing solves problems that CRUD never will:

* Full audit trail (legal, financial, compliance)
* Time travel (rebuild state at any point)
* Debugging production bugs *after the fact*
* Event-driven integration without coupling
* Deterministic behavior

If you don’t need **at least two** of these, don’t use it.

---

## Where It Makes Sense

**Good fits**

* Banking / payments
* Inventory & orders
* Workflow engines
* Identity & access
* Anything regulated or irreversible

**Bad fits**

* Simple admin dashboards
* CRUD forms
* CMS/blogs
* “We might need scale later”

Event sourcing is not a default choice. It’s a power tool.

---

## Core Building Blocks (Non-Optional)

### 1️⃣ Events (Facts)

Events are:

* immutable
* append-only
* named in past tense

```python
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True, slots=True)
class MoneyDeposited:
    account_id: UUID
    amount: int
    occurred_at: datetime
```

If you can’t freeze it, it’s not an event.

---

### 2️⃣ Aggregate (Business Authority)

Aggregates:

* enforce invariants
* decide whether events are allowed
* never talk to databases

```python
from typing import Iterable

class BankAccount:
    def __init__(self, account_id: UUID) -> None:
        self.id = account_id
        self.balance = 0

    def apply(self, event: object) -> None:
        match event:
            case MoneyDeposited(amount=amount):
                self.balance += amount

    def deposit(self, amount: int) -> MoneyDeposited:
        if amount <= 0:
            raise ValueError("Invalid deposit")
        return MoneyDeposited(self.id, amount, datetime.utcnow())
```

No side effects. No persistence. Pure domain logic.

---

### 3️⃣ Event Store (Source of Truth)

Append-only. No updates. No deletes.

```python
class EventStore:
    def append(self, stream_id: UUID, events: list[object]) -> None:
        ...

    def load(self, stream_id: UUID) -> list[object]:
        ...
```

The database stores **history**, not objects.

---

### 4️⃣ Rehydration (State Reconstruction)

```python
def load_account(
    store: EventStore,
    account_id: UUID,
) -> BankAccount:
    account = BankAccount(account_id)
    for event in store.load(account_id):
        account.apply(event)
    return account
```

Yes, this is O(n). That’s why snapshots exist.

---

## Snapshots (Performance Escape Hatch)

```python
@dataclass(slots=True)
class AccountSnapshot:
    balance: int
    version: int
```

Strategy:

* replay from snapshot forward
* snapshot every N events
* snapshots are **optimizations**, not truth

---

## Commands vs Events (Do Not Mix These)

| Command    | Event            |
| ---------- | ---------------- |
| Intent     | Fact             |
| Imperative | Declarative      |
| Can fail   | Already happened |
| User input | System record    |

```python
@dataclass(slots=True)
class DepositMoney:
    account_id: UUID
    amount: int
```

Commands **ask**.
Events **tell**.

---

## Event Versioning (This Will Hurt You If Ignored)

Events are forever. Your schema is not.

### Strategy

* Never mutate old events
* Add new event types
* Use upcasters

```python
def upcast(event: object) -> object:
    if isinstance(event, OldDeposit):
        return MoneyDeposited(
            event.account_id,
            event.amount,
            event.timestamp,
        )
    return event
```

If you rewrite history, you lose trust.

---

## Event Sourcing ≠ Event-Driven Architecture

This mistake is everywhere.

* Event sourcing → **storage model**
* Event-driven → **communication model**

You can have:

* ES without message brokers
* brokers without ES

They are orthogonal.

---

## Projections (Read Models)

You do NOT query aggregates.

You project events into read-optimized models.

```python
class BalanceProjection:
    def apply(self, event: object) -> None:
        match event:
            case MoneyDeposited(amount=amount):
                self.balance += amount
```

Multiple projections:

* per screen
* per report
* per integration

Throw them away. Rebuild anytime.

---

## Failure Modes (Be Honest)

Event sourcing costs you:

* higher complexity
* harder mental model
* schema evolution pain
* more code
* harder ad-hoc queries

If your team isn’t disciplined, this will implode.

---

## Real Bug Story (Why ES Wins)

A bank once said:

> “Customer balance went negative last Thursday.”

With CRUD: 🤷
With ES: replay to Thursday 14:32, find event, fix logic, replay forward.

That alone pays for the architecture.

---

## When NOT to Use Event Sourcing

If:

* you can’t name your events clearly
* you need frequent deletes
* compliance doesn’t matter
* your team is junior
* deadlines are brutal

Then don’t. This is not a flex.

---

## Executive Guidance (Tell-It-Like-It-Is)

* Start with CRUD
* Migrate hot paths to ES
* Keep aggregates small
* Snapshot early
* Test by replaying history
* Document invariants religiously

---

## One-Line Mental Model

> **State is a cache. Events are the truth.**

---

If you want next:

* event sourcing + FastAPI
* Postgres event store schema
* idempotency & concurrency control
* CQRS with projections
* how Stripe and Kafka-backed systems do this
* testing strategies (golden event streams)

Say the word.
