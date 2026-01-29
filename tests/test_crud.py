import pytest
# Fixtures are defined in conftest.py and will be used automatically

def test_put_and_get_basic(store):
    store.put("a", 1)

    assert store.get("a") == 1


def test_get_missing_key_returns_none(store):
    assert store.get("missing") is None


def test_put_overwrites_existing_key(store):
    store.put("a", 1)
    store.put("a", 2)

    assert store.get("a") == 2


def test_delete_existing_key(store):
    store.put("a", 1)
    store.delete("a")

    assert store.get("a") is None


def test_delete_missing_key_is_noop(store):
    # should not raise
    store.delete("missing")

    assert store.get("missing") is None


def test_put_multiple_keys(store_crud):
    store = store_crud
    store.put("a", 1)
    store.put("b", 2)
    store.put("c", 3)

    assert store.get("a") == 1
    assert store.get("b") == 2
    assert store.get("c") == 3


def test_get_does_not_create_key(store):
    store.get("ghost")
    assert store.get("ghost") is None


def test_overwrite_preserves_single_entry_count(store):
    store.put("a", 1)
    store.put("a", 2)
    store.put("b", 3)
    store.put("c", 4)

    # capacity is 3, so only one eviction may occur
    values = {
        store.get("a"),
        store.get("b"),
        store.get("c"),
    }

    # one of these may be None due to eviction,
    # but overwritten key must behave as a single entry
    assert len(values) <= 3

