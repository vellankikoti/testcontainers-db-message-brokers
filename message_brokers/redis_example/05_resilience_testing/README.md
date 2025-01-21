# Example 5: Resilience Testing with Redis

This example demonstrates how to use Testcontainers to test Redis resilience under failure conditions. It covers the following:

- Setting up a Redis container.
- Simulating Redis failures and restarts.
- Testing automatic reconnection and data persistence.
- Using assertions to validate resilience mechanisms.

---

## Overview

The test ensures that Redis handles unexpected failures gracefully and maintains data consistency. It performs the following operations:

1. **Insert Data**: Store key-value pairs in Redis.
2. **Simulate Failure**: Stop and restart the Redis container.
3. **Reconnect & Retrieve Data**: Verify that data remains intact after recovery.
4. **Assertions**: Ensure Redis resumes operations successfully post-recovery.

---

## Features

### Redis Container

- Uses the `RedisContainer` class from the `testcontainers` library to spin up a Redis instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Resilience Testing

- Simulates Redis failures and restarts.
- Tests automatic reconnection mechanisms.
- Ensures data integrity after container recovery.

### Assertions

- Validates that stored data remains available after a restart.
- Confirms Redis resumes normal operations after failure recovery.

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
python -m pytest 05_resilience_testing.py -v -s
```

or

```bash
python3 -m pytest 05_resilience_testing.py -v -s
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

### 2. Insert Initial Data

The test inserts key-value pairs before simulating a failure:

```python
redis_client.set("key1", "value1")
redis_client.set("key2", "value2")
```

- Stores persistent key-value pairs in Redis.

### 3. Simulating Redis Failure

The test stops and restarts the Redis container to simulate a failure:

```python
redis_container.stop()
time.sleep(5)  # Simulate downtime
redis_container.start()
```

- Stops the Redis container temporarily.
- Restarts the container to test recovery.

### 4. Reconnecting and Verifying Data Integrity

After restart, the test reconnects and verifies data consistency:

```python
retrieved_value1 = redis_client.get("key1")
retrieved_value2 = redis_client.get("key2")
```

- Ensures that previously stored data remains accessible.

### 5. Performing New Operations Post-Recovery

The test checks if Redis can accept new operations after recovery:

```python
redis_client.set("key3", "value3")
retrieved_value3 = redis_client.get("key3")
```

- Confirms Redis continues functioning after restart.

### 6. Assertions

The test uses assertions to validate Redis resilience:

```python
assert retrieved_value1 == b"value1"
assert retrieved_value2 == b"value2"
assert retrieved_value3 == b"value3"
```

- Ensures that Redis preserves data through failures.
- Validates Redis continues to process new operations post-recovery.

---

## Key Takeaways

### Testcontainers

- Simplifies resilience testing by providing lightweight, disposable Redis containers.
- Automatically manages container lifecycle.

### Redis Resilience Testing

- Tests how Redis handles failures and recoveries.
- Ensures automatic reconnection and data persistence.

### Assertions

- Confirms data remains intact after failures.
- Validates Redis continues to operate correctly post-recovery.

---

