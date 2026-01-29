import time
# Fixtures are defined in conftest.py and will be used automatically


def test_key_expires_after_ttl(store):
    store.put("a", 1, ttl=0.1)

    time.sleep(0.15)

    assert store.get("a") is None


def test_key_is_accessible_before_ttl_expires(store):
    store.put("a", 1, ttl=1.0)

    assert store.get("a") == 1


def test_key_without_ttl_never_expires(store):
    store.put("a", 1)

    time.sleep(0.2)

    assert store.get("a") == 1


def test_expired_key_is_removed_on_access(store):
    store.put("a", 1, ttl=0.05)

    time.sleep(0.1)
    assert store.get("a") is None

    # second access should behave like missing key
    assert store.get("a") is None


def test_ttl_resets_on_overwrite(store):
    store.put("a", 1, ttl=0.05)

    time.sleep(0.03)
    store.put("a", 2, ttl=0.2)

    time.sleep(0.1)
    assert store.get("a") == 2
