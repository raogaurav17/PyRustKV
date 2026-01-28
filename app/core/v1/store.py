from typing import Any, Optional
from collections import OrderedDict
from threading import RLock
from app.core.v1.entry import Entry


class KVStore:
    """
    In-memory key-value store with TTL and LRU eviction.
    """

    def __init__(self, capacity: int = 100):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")

        self.capacity = capacity
        self._store: OrderedDict[str, Entry] = OrderedDict()
        self._lock = RLock()

    def _remove_expired_entries(self) -> None:
        """
        Remove all expired entries.
        Called opportunistically (lazy cleanup).
        """
        expired_keys = [
            key for key, entry in self._store.items()
            if entry.is_expired()
        ]
        for key in expired_keys:
            self._store.pop(key, None)

    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        with self._lock:
            # overwrite counts as access
            if key in self._store:
                self._store.pop(key)

            self._store[key] = Entry(key, value, ttl)

            # first remove expired entries
            self._remove_expired_entries()

            # then enforce capacity using LRU
            while len(self._store) > self.capacity:
                self._store.popitem(last=False)

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None

            if entry.is_expired():
                self._store.pop(key, None)
                return None

            # mark as recently used
            self._store.move_to_end(key, last=True)
            return entry.value

    def delete(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)
