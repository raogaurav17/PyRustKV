import threading
import time
# Fixtures are defined in conftest.py and will be used automatically


def test_concurrent_puts_do_not_crash(store_large):
    store = store_large
    def worker(start):
        for i in range(start, start + 100):
            store.put(f"key-{i}", i)

    threads = [
        threading.Thread(target=worker, args=(i * 100,))
        for i in range(5)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # capacity must not be exceeded
    count = 0
    for i in range(500):
        if store.get(f"key-{i}") is not None:
            count += 1

    assert count <= store_large.capacity if hasattr(store_large, 'capacity') else count <= 50


def test_concurrent_get_and_put(store_small):
    store = store_small
    store.put("shared", 0)

    def writer():
        for i in range(100):
            store.put("shared", i)

    def reader():
        for _ in range(100):
            val = store.get("shared")
            assert val is None or isinstance(val, int)

    threads = [
        threading.Thread(target=writer),
        threading.Thread(target=reader),
        threading.Thread(target=reader),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()


def test_concurrent_deletes(store_small):
    store = store_small

    for i in range(10):
        store.put(str(i), i)

    def deleter():
        for i in range(10):
            store.delete(str(i))

    threads = [threading.Thread(target=deleter) for _ in range(3)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # all keys should be gone
    for i in range(10):
        assert store.get(str(i)) is None


def test_concurrent_ttl_expiry_and_access(store_small):
    store = store_small
    store.put("temp", 1, ttl=0.05)

    def reader():
        for _ in range(20):
            store.get("temp")
            time.sleep(0.01)

    threads = [threading.Thread(target=reader) for _ in range(3)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # after TTL, key must be gone
    assert store.get("temp") is None
