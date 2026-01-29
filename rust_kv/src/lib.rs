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
        if(capacity == 0){
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
