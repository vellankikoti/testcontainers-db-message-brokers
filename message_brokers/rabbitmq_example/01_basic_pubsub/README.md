# Example 1: Basic Publish-Subscribe (RabbitMQ)

This example demonstrates how to use Testcontainers to test basic RabbitMQ publish-subscribe (pub/sub) messaging. It covers the following:

- Setting up a RabbitMQ container.
- Publishing messages to a RabbitMQ exchange.
- Subscribing to queues and consuming messages.
- Using assertions to validate message delivery.

---

## Overview

The test ensures that RabbitMQ can publish and consume messages in a pub/sub model. It performs the following operations:

1. **Publish Message**: Send messages to a RabbitMQ exchange.
2. **Consume Messages**: Read messages from a queue bound to the exchange.
3. **Validate Message Delivery**: Ensure messages are correctly received by subscribers.

---

## Features

### RabbitMQ Container

- Uses the `RabbitMqContainer` class from the `testcontainers` library to spin up a RabbitMQ instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Pub/Sub Messaging

- Demonstrates how RabbitMQ exchanges and queues work.
- Ensures messages are delivered to subscribers.

### Assertions

- Ensures that published messages are received by consumers.

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
python -m pytest 01_basic_pubsub.py -v -s
```

or

```bash
python3 -m pytest 01_basic_pubsub.py -v -s
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

The test publishes messages to a RabbitMQ exchange:

```python
channel.basic_publish(
    exchange='test_exchange',
    routing_key='',
    body='Hello, RabbitMQ!'
)
```

- Sends a message to `test_exchange`.
- Uses an empty `routing_key` for fan-out behavior.

### 3. Subscribing to Messages

A consumer subscribes to the queue and receives messages:

```python
def callback(ch, method, properties, body):
    global received_message
    received_message = body

channel.basic_consume(queue='test_queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```

- Subscribes to `test_queue`.
- Processes incoming messages.

### 4. Assertions

The test uses assertions to validate message reception:

```python
assert received_message == b'Hello, RabbitMQ!'
```

- Ensures the consumer successfully receives the published message.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable RabbitMQ containers.
- Automatically manages container lifecycle.

### RabbitMQ Pub/Sub

- Demonstrates how to use RabbitMQ for real-time messaging.
- Validates message publishing and subscription workflows.

### Assertions

- Ensures messages are successfully published and received.

---

