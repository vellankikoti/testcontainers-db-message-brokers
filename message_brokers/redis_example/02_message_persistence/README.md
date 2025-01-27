# Example 2: Redis Message Persistence

This example demonstrates how to use Testcontainers to test message persistence in Redis. It covers the following:

- Setting up a Redis container.
- Using Redis Lists to store messages persistently.
- Publishing messages and retrieving them later.
- Using assertions to validate message persistence and retrieval.

---

## Overview

The test ensures that Redis can store messages persistently using lists, allowing them to be retrieved later. It performs the following operations:

1. **Publish Message**: Store messages in a Redis List.
2. **Retrieve Messages**: Fetch stored messages later.
3. **Validate Message Persistence**: Ensure messages persist until explicitly removed.

---

## Features

### Redis Container

- Uses the `RedisContainer` class from the `testcontainers` library to spin up a Redis instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Message Persistence

- Demonstrates how Redis Lists can be used for message persistence.
- Ensures messages remain in Redis until explicitly removed.

### Assertions

- Ensures that stored messages can be retrieved successfully.
- Confirms message persistence over multiple retrievals.

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
python -m pytest 02_message_persistence.py -v -s
```

or

```bash
python3 -m pytest 02_message_persistence.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/8cfd0ac7-76a5-4822-a1ef-e2df8301a019)

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

### 2. Storing Messages in a Redis List

The test stores messages persistently in a Redis List:

```python
redis_client.rpush("message_queue", "Message 1")
redis_client.rpush("message_queue", "Message 2")
```

- Messages are added to a Redis List named `message_queue`.

### 3. Retrieving Messages

The test retrieves messages from Redis:

```python
retrieved_messages = redis_client.lrange("message_queue", 0, -1)
```

- Fetches all messages stored in `message_queue`.

### 4. Assertions

The test uses assertions to validate message persistence:

```python
assert retrieved_messages == [b"Message 1", b"Message 2"]
```

- Ensures that stored messages are retrieved successfully.
- Confirms messages persist until explicitly removed.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable Redis containers.
- Automatically manages container lifecycle.

### Redis Message Persistence

- Demonstrates how Redis Lists can be used for message persistence.
- Ensures messages persist and can be retrieved later.

### Assertions

- Validates that messages are stored and retrieved correctly.
- Ensures messages remain available until explicitly deleted.

---

