# Example 4: Performance Testing with Redis

This example demonstrates how to use Testcontainers to test Redis performance under high-load scenarios. It covers the following:

- Setting up a Redis container.
- Inserting and retrieving a large number of key-value pairs.
- Measuring execution time for various Redis operations.
- Using assertions to validate performance expectations.

---

## Overview

The test measures Redis performance under high-load scenarios by performing bulk insertions and retrievals. It performs the following operations:

1. **Bulk Data Insertion**: Store a large number of key-value pairs.
2. **Bulk Data Retrieval**: Fetch stored data efficiently.
3. **Measure Execution Time**: Benchmark performance of Redis operations.
4. **Optimize with Pipelining**: Compare performance with and without pipelining.

---

## Features

### Redis Container

- Uses the `RedisContainer` class from the `testcontainers` library to spin up a Redis instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Performance Testing

- Inserts and retrieves a large volume of data.
- Measures execution time for batch operations.
- Uses Redis pipelining to optimize performance.

### Assertions

- Ensures that Redis operations execute within acceptable time limits.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers redis
```

or

```bash
pip3 install pytest testcontainers redis
```

### 2. Run the Test

Execute the test file using `pytest`:

```bash
python -m pytest 04_performance_testing.py -v -s
```

or

```bash
python3 -m pytest 04_performance_testing.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/725e9979-685c-4073-80b1-fb466cb427b3)

---

## Code Walkthrough

### 1. Redis Container Setup

The test uses the `RedisContainer` class to start a Redis instance in a Docker container:

```python
with RedisContainer("redis:6.2") as redis:
    yield redis.get_connection_url()
```

- The container runs Redis version 6.2.
- The `get_connection_url()` method provides the connection string for the Redis client.

### 2. Bulk Data Insertion

The test inserts a large number of key-value pairs to simulate a high-load scenario:

```python
for i in range(100000):
    redis_client.set(f"user:{i}", f"value_{i}")
```

- Stores 100,000 key-value pairs in Redis.

### 3. Bulk Data Retrieval

The test retrieves multiple values efficiently:

```python
values = [redis_client.get(f"user:{i}") for i in range(100000)]
```

- Fetches stored values in bulk.

### 4. Performance Measurement

The test measures execution time for Redis operations:

```python
import time

start_time = time.time()
for i in range(100000):
    redis_client.get(f"user:{i}")
end_time = time.time()
execution_time = end_time - start_time
```

- Measures the time taken for retrieving 100,000 keys.

### 5. Optimizing with Pipelining

The test compares performance with Redis pipelining:

```python
pipeline = redis_client.pipeline()
for i in range(100000):
    pipeline.get(f"user:{i}")
pipeline.execute()
```

- Uses pipelining to reduce network round trips and improve performance.

### 6. Assertions

The test uses assertions to ensure acceptable execution times:

```python
assert execution_time < 5.0  # Ensure query execution remains under 5 seconds
assert len(values) == 100000  # Validate that all values were retrieved
```

- Ensures Redis handles bulk operations efficiently.

---

## Key Takeaways

### Testcontainers

- Simplifies performance testing by providing lightweight, disposable Redis containers.
- Automatically manages container lifecycle.

### Redis Performance Testing

- Measures Redis performance under high load.
- Uses pipelining to optimize execution time.

### Assertions

- Ensures bulk operations execute within acceptable time limits.
- Confirms efficient data retrieval in Redis.

---

