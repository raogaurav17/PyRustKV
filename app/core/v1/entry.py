from typing import Any, Optional
import time

class Entry():
    """
    
    """

    __slots__ = (
        "key",
        "value",
        "expires_at",
    )
    
    def __init__(self, key: str, value: Any, ttl: Optional[float] = None):
        self.key = key
        self.value = value
        if ttl is not None:
            self.expires_at = time.time() + ttl
        else:
            self.expires_at = None
    
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at