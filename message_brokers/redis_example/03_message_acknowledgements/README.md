# Example 3: Redis Message Acknowledgements

This example demonstrates how to use Testcontainers to test message acknowledgements in Redis. It covers the following:

- Setting up a Redis container.
- Using Redis Lists for message queuing.
- Implementing message consumption with acknowledgements.
- Using assertions to validate message processing.

---

## Overview

The test ensures that messages are properly acknowledged upon consumption, preventing duplicate processing. It performs the following operations:

1. **Publish Message**: Store messages in a Redis List.
2. **Consume Messages**: Process and acknowledge messages.
3. **Validate Acknowledgements**: Ensure messages are removed after processing.

---

## Features

### Redis Container

- Uses the `RedisContainer` class from the `testcontainers` library to spin up a Redis instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Message Acknowledgements

- Demonstrates how Redis Lists can be used for reliable message processing.
- Ensures messages are acknowledged and removed from the queue after processing.

### Assertions

- Ensures that consumed messages are properly acknowledged.
- Confirms that acknowledged messages are removed from Redis.

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
python -m pytest 03_message_acknowledgements.py -v -s
```

or

```bash
python3 -m pytest 03_message_acknowledgements.py -v -s
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

### 2. Storing Messages in a Redis List

The test stores messages persistently in a Redis List:

```python
redis_client.rpush("message_queue", "Task 1")
redis_client.rpush("message_queue", "Task 2")
```

- Messages are added to a Redis List named `message_queue`.

### 3. Consuming and Acknowledging Messages

The test retrieves and processes messages, removing them after acknowledgment:

```python
while True:
    message = redis_client.lpop("message_queue")
    if message is None:
        break  # No more messages
    print(f"Processing: {message.decode()}")
```

- Uses `lpop` to remove and process messages.
- Ensures processed messages do not remain in the queue.

### 4. Assertions

The test uses assertions to validate message acknowledgements:

```python
remaining_messages = redis_client.lrange("message_queue", 0, -1)
assert len(remaining_messages) == 0  # Ensure all messages were processed
```

- Ensures that acknowledged messages are removed from Redis.
- Confirms that no unprocessed messages remain.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable Redis containers.
- Automatically manages container lifecycle.

### Redis Message Acknowledgements

- Demonstrates how Redis Lists can be used for reliable message processing.
- Ensures messages are properly acknowledged and removed.

### Assertions

- Validates that messages are processed and removed from the queue.
- Ensures no duplicate processing of messages.

---

