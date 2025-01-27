# Example 1: Basic Publish-Subscribe (Kafka)

This example demonstrates how to use Testcontainers to test basic Kafka publish-subscribe (pub/sub) messaging. It covers the following:

- Setting up a Kafka container.
- Producing messages to a Kafka topic.
- Consuming messages from the topic.
- Using assertions to validate message delivery.

---

## Overview

The test ensures that Kafka can publish and consume messages in a pub/sub model. It performs the following operations:

1. **Produce Message**: Send messages to a Kafka topic.
2. **Consume Messages**: Read messages from the topic.
3. **Validate Message Delivery**: Ensure messages are correctly received.

---

## Features

### Kafka Container

- Uses the `KafkaContainer` class from the `testcontainers` library to spin up a Kafka instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Pub/Sub Messaging

- Demonstrates how Kafka producers and consumers work.
- Ensures messages are delivered to subscribers.

### Assertions

- Ensures that published messages are received by consumers.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers kafka-python
```

or

```bash
pip3 install pytest testcontainers kafka-python
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

![image](https://github.com/user-attachments/assets/5b8882f4-8185-4ab1-8fb1-460be8c2d057)


---

## Code Walkthrough

### 1. Kafka Container Setup

The test uses the `KafkaContainer` class to start a Kafka broker in a Docker container:

```python
with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
    yield kafka.get_bootstrap_server()
```

- The container runs the latest version of Kafka.
- The `get_bootstrap_server()` method provides the connection string for Kafka clients.

### 2. Producing Messages

The test publishes messages to a Kafka topic:

```python
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
producer.send("test_topic", b"Hello, Kafka!")
producer.flush()
```

- Sends a message to `test_topic`.

### 3. Consuming Messages

A consumer subscribes to the topic and reads messages:

```python
consumer = KafkaConsumer("test_topic", bootstrap_servers=kafka_bootstrap_server, auto_offset_reset="earliest")
message = next(consumer)
```

- Subscribes to `test_topic`.
- Reads the next available message.

### 4. Assertions

The test uses assertions to validate message reception:

```python
assert message.value == b"Hello, Kafka!"
```

- Ensures the consumer successfully receives the published message.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable Kafka containers.
- Automatically manages container lifecycle.

### Kafka Pub/Sub

- Demonstrates how to use Kafka for real-time messaging.
- Validates message publishing and subscription workflows.

### Assertions

- Ensures messages are successfully published and received.

---

