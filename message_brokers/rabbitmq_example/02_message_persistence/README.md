# Example 2: RabbitMQ Message Persistence

This example demonstrates how to use Testcontainers to test message persistence in RabbitMQ. It covers the following:

- Setting up a RabbitMQ container.
- Publishing persistent messages to a durable queue.
- Stopping and restarting RabbitMQ to test message durability.
- Using assertions to validate message persistence across restarts.

---

## Overview

The test ensures that RabbitMQ retains messages in a durable queue even when the broker restarts. It performs the following operations:

1. **Publish Persistent Messages**: Send durable messages to a RabbitMQ queue.
2. **Stop and Restart RabbitMQ**: Simulate broker failure and recovery.
3. **Consume Messages After Restart**: Ensure messages persist and can be retrieved after recovery.

---

## Features

### RabbitMQ Container

- Uses the `RabbitMqContainer` class from the `testcontainers` library to spin up a RabbitMQ instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Message Persistence

- Ensures RabbitMQ retains messages across restarts.
- Uses durable queues and persistent messages to validate data integrity.

### Assertions

- Ensures that stored messages remain available after a broker restart.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers pika
```

or

```bash
pip3 install pytest testcontainers pika
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

![image](https://github.com/user-attachments/assets/725e9979-685c-4073-80b1-fb466cb427b3)

---

## Code Walkthrough

### 1. RabbitMQ Container Setup

The test uses the `RabbitMqContainer` class to start a RabbitMQ broker in a Docker container:

```python
with RabbitMqContainer("rabbitmq:3.9-management") as rabbitmq:
    yield rabbitmq.get_connection_url()
```

- The container runs RabbitMQ version 3.9 with management UI.
- The `get_connection_url()` method provides the connection string for RabbitMQ clients.

### 2. Publishing Persistent Messages

The test publishes messages with explicit persistence settings:

```python
channel.queue_declare(queue='persistent_queue', durable=True)
channel.basic_publish(
    exchange='',
    routing_key='persistent_queue',
    body='Persistent Message',
    properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
)
```

- Declares a durable queue named `persistent_queue`.
- Sends persistent messages with `delivery_mode=2`.

### 3. Stopping and Restarting RabbitMQ

The test stops and restarts the RabbitMQ container to test persistence:

```python
rabbitmq_container.stop()
time.sleep(5)  # Simulate downtime
rabbitmq_container.start()
```

- Simulates a RabbitMQ broker failure and recovery.

### 4. Consuming Messages After Restart

After the restart, the test consumes messages to verify persistence:

```python
channel.queue_declare(queue='persistent_queue', durable=True)
method_frame, header_frame, body = channel.basic_get(queue='persistent_queue', auto_ack=True)
```

- Declares the same durable queue after restart.
- Retrieves the persisted messages.

### 5. Assertions

The test uses assertions to validate message persistence:

```python
assert body == b'Persistent Message'
```

- Ensures the message remains available after the broker restart.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable RabbitMQ containers.
- Automatically manages container lifecycle.

### RabbitMQ Message Persistence

- Ensures RabbitMQ retains durable messages across restarts.
- Demonstrates how to use durable queues and persistent messages.

### Assertions

- Validates message persistence and availability after broker recovery.

---

