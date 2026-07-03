from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class EventType(StrEnum):
    ADDED = 'ADDED'
    REMOVED = 'REMOVED'


@dataclass(frozen=True)
class Event:
    event_type: EventType
    data: str
    timestamp: datetime = field(default_factory=datetime.now)


class EventStore:
    def __init__(self) -> None:
        self._events: list[Event] = []

    def append(self, event: Event):
        self._events.append(event)

    def get_all_events(self):
        return list(self._events)
