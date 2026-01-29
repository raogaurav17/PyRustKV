#![allow(unsafe_op_in_unsafe_fn)]

use pyo3::prelude::*;
use pyo3::types::PyAny;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};
use indexmap::IndexMap;

#[derive(Clone)]
struct Entry{
    value: Py<PyAny>,
    expires_at: Option<Instant>,
}

struct StoreInner{
    map: HashMap<String, Entry>,
    lru : IndexMap<String, ()>,
    capacity: usize,
}

#[pyclass]
struct KvStore {
    inner: Arc<Mutex<StoreInner>>,
}

#[pymethods]
impl KvStore {
    #[new]
    fn new(capacity: usize) -> Self {
        if capacity == 0 {
            panic!("Capacity must be greater than 0");
        }
        Self {
            inner: Arc::new(Mutex::new(StoreInner {
                map: HashMap::new(),
                lru: IndexMap::new(),
                capacity,
            })),
        }
    }

    fn put(&self, key: String, value: Py<PyAny>, ttl: Option<f64>) {
        let mut store = self.inner.lock().unwrap();
        let expires_at = ttl.map(|t| Instant::now() + Duration::from_secs_f64(t));

        if store.map.contains_key(&key) {
            store.lru.shift_remove(&key);
        } else if store.map.len() >= store.capacity {
            if let Some((oldest_key, _)) = store.lru.shift_remove_index(0) {
                store.map.remove(&oldest_key);
            }
        }

        store.map.insert(key.clone(), Entry { value, expires_at });
        store.lru.insert(key, ());
    }

    fn get(&self, key: String) -> Option<Py<PyAny>> {
        let mut store = self.inner.lock().unwrap();
        if let Some(entry) = store.map.get(&key) {
            if let Some(expiry) = entry.expires_at {
                if Instant::now() >= expiry {
                    store.map.remove(&key);
                    store.lru.shift_remove(&key);
                    return None;
                }
            }
            let value = entry.value.clone();
            store.lru.shift_remove(&key);
            store.lru.insert(key.clone(), ());
            return Some(value);
        }
        None
    }

    fn delete(&self, key: String) {
        let mut store = self.inner.lock().unwrap();
        store.map.remove(&key);
        store.lru.shift_remove(&key);
    }
}

#[pymodule]
fn rust_kv(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<KvStore>()?;
    Ok(())
}
