from typing import Any, Optional
from app.core.v1.entry import Entry

class KVStore():
    """ 
    In memory key value store
    """
    
    def __init__(self, capacity: int = 100):
        super().__init__()
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        self.capacity = capacity
        self._store: dict[str, Entry] = {}
        
    def put(self, key, value, ttl: Optional[int] = None):
        self._store[key] = Entry(key, value, ttl)
        if len(self._store) > self.capacity:
            self._store.pop(next(iter(self._store)))   
        
    def get(self, key):
        entry = self._store.get(key)
        if entry is not None and entry.is_expired():
            del self._store[key]
            return None
        return entry.value if entry is not None else None

    def delete(self, key):
        self._store.pop(key, None)
        
        