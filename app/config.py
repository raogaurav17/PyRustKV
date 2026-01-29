from typing import Union
from app.core.v1.store import KVStore
import rust_kv

_STORE = None
_STORE_VERSION = "v2"

def init_store(capacity: int = 100, version: str = "v1") -> None:
    """
    Initialize the key-value store.
    
    Args:
        capacity: Maximum number of items to store
        version: Store version - "v1" (Python) or "v2" (Rust)
    """
    global _STORE, _STORE_VERSION
    if _STORE is None:
        if version == "v2":
            _STORE = rust_kv.KvStore(capacity)
            _STORE_VERSION = "v2"
        else:
            _STORE = KVStore(capacity=capacity)
            _STORE_VERSION = "v1"
        
def get_store() -> Union[KVStore, "rust_kv.KvStore"]:
    """Get the initialized store."""
    if _STORE is None:
        raise RuntimeError("Store not initialized. Call init_store() first.")
    return _STORE

def get_store_version() -> str:
    """Get the current store version."""
    return _STORE_VERSION