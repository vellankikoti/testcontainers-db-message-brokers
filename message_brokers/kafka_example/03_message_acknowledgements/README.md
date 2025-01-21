# Example 3: Kafka Message Acknowledgements

This example demonstrates how to use Testcontainers to test message acknowledgements in Kafka. It covers the following:

- Setting up a Kafka container.
- Producing messages with acknowledgements.
- Consuming messages to verify successful delivery.
- Using assertions to validate message acknowledgements.

---

## Overview

The test ensures that Kafka correctly handles message acknowledgements, ensuring reliable message delivery. It performs the following operations:

1. **Produce Message with Acknowledgement**: Send messages to a Kafka topic with acknowledgment settings.
2. **Consume Messages**: Read messages from the topic to verify delivery.
3. **Validate Acknowledgements**: Ensure that messages are acknowledged by Kafka before being consumed.

---

## Features

### Kafka Container

- Uses the `KafkaContainer` class from the `testcontainers` library to spin up a Kafka instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Message Acknowledgements

- Ensures that Kafka acknowledges message delivery before allowing consumption.
- Uses different acknowledgment modes to test Kafka’s reliability.

### Assertions

- Ensures that published messages are successfully acknowledged and delivered.

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

### 1. Kafka Container Setup

The test uses the `KafkaContainer` class to start a Kafka broker in a Docker container:

```python
with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
    yield kafka.get_bootstrap_server()
```

- The container runs the latest version of Kafka.
- The `get_bootstrap_server()` method provides the connection string for Kafka clients.

### 2. Producing Messages with Acknowledgements

The test publishes messages with explicit acknowledgment settings:

```python
producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_server,
    acks='all'  # Ensure Kafka fully acknowledges messages before confirming delivery
)
producer.send("test_topic", b"Acknowledged Message")
producer.flush()
```

- Uses `acks='all'` to require full acknowledgment before confirming delivery.
- Ensures messages are reliably stored before Kafka acknowledges them.

### 3. Consuming Messages to Verify Delivery

A consumer subscribes to the topic and reads messages:

```python
consumer = KafkaConsumer("test_topic", bootstrap_servers=kafka_bootstrap_server, auto_offset_reset="earliest")
message = next(consumer)
```

- Subscribes to `test_topic` and reads messages to confirm delivery.

### 4. Assertions

The test uses assertions to validate message acknowledgements:

```python
assert message.value == b"Acknowledged Message"
```

- Ensures Kafka acknowledges and successfully delivers the message.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable Kafka containers.
- Automatically manages container lifecycle.

### Kafka Message Acknowledgements

- Ensures Kafka properly acknowledges and commits messages.
- Tests different acknowledgment modes to improve message reliability.

### Assertions

- Validates that messages are acknowledged and received successfully.

---

