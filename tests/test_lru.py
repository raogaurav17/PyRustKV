import time
# Fixtures are defined in conftest.py and will be used automatically


def test_lru_eviction_basic(store):
    store.put("a", 1)
    store.put("b", 2)
    store.put("c", 3)  # should evict "a"

    assert store.get("a") is None
    assert store.get("b") == 2
    assert store.get("c") == 3


def test_lru_updates_on_get(store):
    store.put("a", 1)
    store.put("b", 2)

    # access "a", making it most recently used
    assert store.get("a") == 1

    store.put("c", 3)  # should evict "b"

    assert store.get("b") is None
    assert store.get("a") == 1
    assert store.get("c") == 3


def test_lru_updates_on_put_overwrite(store):
    store.put("a", 1)
    store.put("b", 2)

    # overwrite "a" (counts as access)
    store.put("a", 10)

    store.put("c", 3)  # should evict "b"

    assert store.get("b") is None
    assert store.get("a") == 10
    assert store.get("c") == 3


def test_expired_entries_removed_before_lru_eviction(store):
    store.put("a", 1, ttl=0.05)
    store.put("b", 2)

    time.sleep(0.1)  # let "a" expire

    store.put("c", 3)  # should remove expired "a", not evict "b"

    assert store.get("a") is None
    assert store.get("b") == 2
    assert store.get("c") == 3


def test_multiple_lru_evictions(store):
    store.put("a", 1)
    store.put("b", 2)
    store.put("c", 3)
    store.put("d", 4)

    # only two most recent should remain
    remaining = {store.get("c"), store.get("d")}

    assert remaining == {3, 4}
    assert store.get("a") is None
    assert store.get("b") is None


def test_get_does_not_revive_expired_entry(store):
    store.put("a", 1, ttl=0.05)
    time.sleep(0.1)

    assert store.get("a") is None

    store.put("b", 2)
    store.put("c", 3)

    # expired "a" must not affect LRU ordering
    assert store.get("b") == 2
    assert store.get("c") == 3
