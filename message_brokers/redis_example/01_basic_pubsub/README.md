# Example 1: Basic Publish-Subscribe (Redis)

This example demonstrates how to use Testcontainers to test basic publish-subscribe (pub/sub) messaging in Redis. It covers the following:

- Setting up a Redis container.
- Publishing messages to a channel.
- Subscribing and receiving messages in real-time.
- Using assertions to validate message delivery.

---

## Overview

The test simulates a simple Redis pub/sub system, where messages are published to a channel and consumed by subscribers. It performs the following operations:

1. **Publish Message**: Send messages to a Redis channel.
2. **Subscribe**: Listen to the channel and receive messages.
3. **Validate Message Delivery**: Ensure messages are correctly received by the subscriber.

---

## Features

### Redis Container

- Uses the `RedisContainer` class from the `testcontainers` library to spin up a Redis instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Pub/Sub Messaging

- Demonstrates how Redis pub/sub works.
- Shows how to send and receive messages through a channel.

### Assertions

- Ensures that published messages are received by subscribers.

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
python -m pytest 01_basic_pubsub.py -v -s
```

or

```bash
python3 -m pytest 01_basic_pubsub.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/1c87af28-0817-44a2-a5a0-cdbb191b863e)

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

### 2. Publishing Messages

The test publishes messages to a Redis channel:

```python
redis_client.publish("test_channel", "Hello, Redis!")
```

- Sends a message to the `test_channel`.

### 3. Subscribing to Messages

A subscriber listens to the channel and receives messages:

```python
pubsub = redis_client.pubsub()
pubsub.subscribe("test_channel")
message = pubsub.get_message(ignore_subscribe_messages=True)
```

- Subscribes to `test_channel`.
- Listens for incoming messages.

### 4. Assertions

The test uses assertions to validate message reception:

```python
assert message is not None
assert message["data"] == b"Hello, Redis!"
```

- Ensures that the subscriber successfully receives the published message.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable Redis containers.
- Automatically manages container lifecycle.

### Redis Pub/Sub

- Demonstrates how to use Redis for real-time messaging.
- Validates message publishing and subscription workflows.

### Assertions

- Ensures messages are successfully published and received.

---

