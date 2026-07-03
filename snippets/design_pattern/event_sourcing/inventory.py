from collections import Counter
from functools import cache

from events import Event, EventStore, EventType


class Inventory:
    def __init__(self, store: EventStore) -> None:
        self._store: EventStore = store

    def add_item(self, item: str):
        self._store.append(
            Event(
                EventType.ADDED,
                item,
            ),
        )
        self.get_items.cache_clear()

    def remove_item(self, item: str):
        if self.get_count(item) == 0:
            raise ValueError(item + ' not in Inventory.')
        self._store.append(
            Event(
                EventType.REMOVED,
                item,
            ),
        )
        self.get_items.cache_clear()

    @cache
    def get_items(self) -> list[tuple[str, int]]:
        counts = Counter[str]()
        for event in self._store.get_all_events():
            if event.event_type == EventType.ADDED:
                counts[event.data] += 1
            elif event.event_type == EventType.REMOVED:
                counts[event.data] -= 1
        return [(item, count) for item, count in counts.items() if count > 0]

    def get_count(self, item: str):
        return dict(self.get_items()).get(item, 0)
