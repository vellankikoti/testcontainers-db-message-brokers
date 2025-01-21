# Example 3: RabbitMQ Message Acknowledgements

This example demonstrates how to use Testcontainers to test message acknowledgements in RabbitMQ. It covers the following:

- Setting up a RabbitMQ container.
- Publishing messages to a queue with manual acknowledgements.
- Consuming messages and acknowledging them explicitly.
- Using assertions to validate message processing.

---

## Overview

The test ensures that RabbitMQ correctly handles message acknowledgements to prevent message loss or duplication. It performs the following operations:

1. **Publish Messages**: Send messages to a RabbitMQ queue.
2. **Consume Messages with Acknowledgements**: Explicitly acknowledge received messages.
3. **Validate Acknowledgements**: Ensure unacknowledged messages remain in the queue.

---

## Features

### RabbitMQ Container

- Uses the `RabbitMqContainer` class from the `testcontainers` library to spin up a RabbitMQ instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Message Acknowledgements

- Ensures that RabbitMQ does not remove messages from a queue until they are explicitly acknowledged.
- Demonstrates how to requeue unacknowledged messages for reliability.

### Assertions

- Ensures that acknowledged messages are removed from the queue.
- Confirms that unacknowledged messages remain available.

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

### 1. RabbitMQ Container Setup

The test uses the `RabbitMqContainer` class to start a RabbitMQ broker in a Docker container:

```python
with RabbitMqContainer("rabbitmq:3.9-management") as rabbitmq:
    yield rabbitmq.get_connection_url()
```

- The container runs RabbitMQ version 3.9 with management UI.
- The `get_connection_url()` method provides the connection string for RabbitMQ clients.

### 2. Publishing Messages

The test publishes messages to a RabbitMQ queue:

```python
channel.queue_declare(queue='ack_queue', durable=True)
channel.basic_publish(
    exchange='',
    routing_key='ack_queue',
    body='Acknowledged Message'
)
```

- Declares a durable queue named `ack_queue`.
- Sends a message without automatic acknowledgment.

### 3. Consuming Messages with Manual Acknowledgement

The test retrieves messages and acknowledges them explicitly:

```python
def callback(ch, method, properties, body):
    global received_message
    received_message = body
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='ack_queue', on_message_callback=callback, auto_ack=False)
channel.start_consuming()
```

- Subscribes to `ack_queue`.
- Acknowledges the message manually using `basic_ack`.

### 4. Assertions

The test uses assertions to validate message acknowledgements:

```python
assert received_message == b'Acknowledged Message'
```

- Ensures RabbitMQ removes the message from the queue only after acknowledgment.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable RabbitMQ containers.
- Automatically manages container lifecycle.

### RabbitMQ Message Acknowledgements

- Ensures RabbitMQ properly handles manual acknowledgements.
- Demonstrates reliability through message requeueing.

### Assertions

- Validates that messages are correctly acknowledged and removed.
- Ensures unacknowledged messages remain in the queue for redelivery.

---

