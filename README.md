# PyRustKV

> A high-performance, production-ready in-memory key-value store combining the best of Python and Rust

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-latest-brightgreen.svg)](https://fastapi.tiangolo.com/)
[![Rust](https://img.shields.io/badge/rust-1.70+-orange.svg)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

PyRustKV is an intelligent hybrid key-value store that leverages **Rust's performance** for core storage operations while maintaining **Python's accessibility** through a modern REST API. Built with thread-safe operations, automatic TTL expiration, and LRU eviction policies, it's designed for high-concurrency scenarios where performance and reliability matter.

### Why PyRustKV?

- **Hybrid Architecture**: Combines Rust's memory efficiency and speed with Python's developer-friendly ecosystem
- **Thread-Safe**: Built-in synchronization handles concurrent access without sacrificing performance
- **Intelligent Caching**: LRU eviction ensures optimal memory utilization
- **TTL Support**: Automatic expiration of entries with lazy cleanup to prevent memory leaks
- **REST API**: FastAPI-based HTTP interface for seamless integration
- **Production-Ready**: Comprehensive test coverage for CRUD operations, concurrency, TTL, and LRU policies

## Features

**Core Capabilities**

- **In-Memory Storage**: Ultra-fast get/put/delete operations
- **Capacity Management**: Configurable capacity with automatic LRU-based eviction
- **TTL Expiration**: Time-to-live support with automatic cleanup
- **Thread Safety**: Mutex-protected concurrent access across multiple clients
- **Type Flexibility**: Store any Python-serializable object as values

**Performance**

- Rust-based core store for critical operations
- Lock-optimized operations to minimize contention
- Efficient memory management with automatic eviction

  **API Design**

- RESTful endpoints for all operations
- Clean, intuitive request/response format
- Error handling with meaningful HTTP status codes

## Architecture

```
┌─────────────────────────────────────────┐
│          FastAPI REST Layer             │
│  (PUT/GET/DELETE endpoints, routing)    │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│      Python Store Wrapper Layer         │
│  (Configuration, initialization logic)  │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│    Rust KvStore (Performance Core)      │
│  • HashMap for O(1) lookups             │
│  • IndexMap for LRU tracking            │
│  • Arc<Mutex> for thread safety         │
│  • Instant-based TTL management         │
└─────────────────────────────────────────┘
```

### Key Design Decisions

1. **Rust for Core Store**: Critical path operations (get/put/delete) are implemented in Rust via PyO3 bindings for maximum performance
2. **Python for API Layer**: FastAPI handles HTTP routing, validation, and business logic - where Python excels
3. **Lazy Cleanup**: TTL expiration checks happen on access, reducing overhead
4. **LRU Eviction**: IndexMap maintains insertion order for efficient O(1) eviction of least-recently-used entries

## Installation

### Prerequisites

- Python 3.9+
- Rust 1.70+ (for building the Rust extension)
- pip or conda

### Setup

```bash
# Clone the repository
git clone https://github.com/raogaurav17/PyRustKV.git
cd PyRustKV

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build Rust extensions
maturin develop  # or: cargo build --release (then copy .so/.pyd to app/)
```

## Quick Start

### Running the Server

```bash
# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Usage Examples

#### Insert a Key-Value Pair

```bash
curl -X PUT http://localhost:8000/kv/insert \
  -H "Content-Type: application/json" \
  -d '{
    "key": "user:123",
    "value": {"name": "Alice", "age": 30},
    "ttl": 3600
  }'
# Response: {"status": "success"}
```

#### Retrieve a Value

```bash
curl -X GET http://localhost:8000/kv/user:123
# Response: {"key": "user:123", "value": {"name": "Alice", "age": 30}}
```

#### Delete a Key

```bash
curl -X DELETE http://localhost:8000/kv/delete/user:123
# Response: {"status": "success"}
```

#### Get Non-Existent Key

```bash
curl -X GET http://localhost:8000/kv/nonexistent
# Response: {"detail": "Key not found"} (404)
```

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Insert
requests.put(f"{BASE_URL}/kv/insert", json={
    "key": "cache:session",
    "value": {"user_id": 42, "token": "abc123"},
    "ttl": 1800  # 30 minutes
})

# Retrieve
response = requests.get(f"{BASE_URL}/kv/cache:session")
print(response.json())

# Delete
requests.delete(f"{BASE_URL}/kv/delete/cache:session")
```

## Testing

Comprehensive test suite covering all critical functionality:

```bash
# Run all tests
pytest

# Run specific test module
pytest tests/test_crud.py -v
pytest tests/test_concurrency.py -v
pytest tests/test_ttl.py -v
pytest tests/test_lru.py -v

# Run with coverage
pytest --cov=app --cov=tests
```

### Test Coverage

- **CRUD Operations**: Basic create, read, update, delete functionality
- **Concurrency**: Thread-safety under high concurrent load
- **TTL Management**: Expiration timing and lazy cleanup
- **LRU Eviction**: Capacity enforcement and least-recently-used tracking

## Performance Characteristics

| Operation    | Complexity     | Notes                               |
| ------------ | -------------- | ----------------------------------- |
| GET          | O(1)           | HashMap lookup + expiration check   |
| PUT          | O(1) amortized | May trigger LRU eviction            |
| DELETE       | O(1)           | Direct removal from both structures |
| LRU Eviction | O(1)           | IndexMap maintains order            |

## Project Structure

```
PyRustKV/
├── main.py                    # FastAPI application entry point
├── pytest.ini                 # Pytest configuration
├── README.md                  # This file
├── LICENSE                    # MIT License
│
├── app/
│   ├── config.py             # Configuration and store initialization
│   ├── api/
│   │   └── routes.py         # REST API endpoints
│   └── core/v1/
│       ├── entry.py          # Entry data structure with TTL
│       └── store.py          # Python store wrapper
│
├── rust_kv/                  # Rust extension module
│   ├── Cargo.toml           # Rust dependencies and metadata
│   └── src/
│       └── lib.rs           # Rust KvStore implementation (PyO3)
│
└── tests/
    ├── test_crud.py         # CRUD operation tests
    ├── test_concurrency.py  # Concurrency and thread-safety tests
    ├── test_ttl.py          # TTL and expiration tests
    └── test_lru.py          # LRU eviction policy tests
```

## Configuration

Edit `app/config.py` to customize store behavior:

```python
# Default capacity for the store
init_store(capacity=100)  # Adjust based on memory constraints
```

## Future Enhancements

- [ ] Persistence layer (RocksDB/SQLite backend)
- [ ] Distributed caching with replication
- [ ] Advanced eviction policies (LFU, W-TinyLFU)
- [ ] Metrics and monitoring (Prometheus integration)
- [ ] Batch operations endpoint
- [ ] Key pattern matching/scanning
- [ ] Transactions and ACID guarantees

## Technical Stack

| Component           | Technology | Why?                                               |
| ------------------- | ---------- | -------------------------------------------------- |
| **Language (Core)** | Rust       | Memory safety, zero-cost abstractions, performance |
| **Language (API)**  | Python     | Developer experience, rapid iteration              |
| **Web Framework**   | FastAPI    | Async support, automatic docs, type validation     |
| **FFI Binding**     | PyO3       | Safe Rust ↔ Python interop                         |
| **Testing**         | pytest     | Comprehensive assertions, great plugins            |

## Benchmarking

To understand performance characteristics:

```bash
# Compare different operation patterns
# Monitor memory usage with system tools
# Test latency under concurrent load

python -m pytest tests/ -v --durations=10
```

## Development

### Building from Source

```bash
# Install development dependencies
pip install -e ".[dev]"

# Build Rust extension in debug mode
maturin develop

# Build release version
maturin build --release
```

### Code Quality

```bash
# Type checking (if mypy is available)
mypy app/

# Formatting
black app/ tests/

# Linting
pylint app/
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## About

PyRustKV demonstrates how modern software engineering combines multiple languages to create robust, performant systems. It's ideal for learning about:

- **Systems Programming**: Rust's ownership model and performance
- **Python FFI**: PyO3 bindings and extending Python with Rust
- **Web APIs**: FastAPI and async Python web development
- **Data Structures**: HashMap, LRU caching, TTL mechanisms
- **Concurrency**: Thread-safe design patterns and synchronization

## Contact & Support

For questions, issues, or suggestions:

- Open an GitHub issue
- Check existing documentation
- Review test cases for usage examples

---

**Built with ❤️ by a engineer who care about performance and clean code.**
