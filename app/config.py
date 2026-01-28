from app.core.v1.store import KVStore

_STORE = None

def init_store(capacity: int = 100) -> None:
    global _STORE
    if _STORE is None:
        _STORE = KVStore(capacity=capacity)
        
def get_store() -> KVStore:
    if _STORE is None:
        raise RuntimeError("Store not initialized. Call init_store() first.")
    return _STORE