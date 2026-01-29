import pytest
from app.core.v1.store import KVStore
import rust_kv


@pytest.fixture(params=["v1", "v2"], ids=["v1_python", "v2_rust"])
def store(request):
    """
    Parametrized fixture that provides both v1 (Python) and v2 (Rust) stores.
    Tests using this fixture will run twice: once with each store.
    Capacity: 2 (for LRU tests that expect eviction with 3 items)
    """
    version = request.param
    capacity = 2
    
    if version == "v2":
        return rust_kv.KvStore(capacity)
    else:
        return KVStore(capacity=capacity)


@pytest.fixture(params=["v1", "v2"], ids=["v1_python", "v2_rust"])
def store_crud(request):
    """Parametrized fixture for CRUD tests that need capacity for 3+ items."""
    version = request.param
    capacity = 3
    
    if version == "v2":
        return rust_kv.KvStore(capacity)
    else:
        return KVStore(capacity=capacity)


@pytest.fixture(params=["v1", "v2"], ids=["v1_python", "v2_rust"])
def store_large(request):
    """Parametrized fixture with larger capacity for concurrency tests."""
    version = request.param
    capacity = 50
    
    if version == "v2":
        return rust_kv.KvStore(capacity)
    else:
        return KVStore(capacity=capacity)


@pytest.fixture(params=["v1", "v2"], ids=["v1_python", "v2_rust"])
def store_small(request):
    """Parametrized fixture with small capacity for concurrency tests."""
    version = request.param
    capacity = 10
    
    if version == "v2":
        return rust_kv.KvStore(capacity)
    else:
        return KVStore(capacity=capacity)
