# Example 2: Kafka Message Persistence

This example demonstrates how to use Testcontainers to test Kafka message persistence. It covers the following:

- Setting up a Kafka container.
- Producing messages to a Kafka topic.
- Shutting down and restarting the Kafka broker.
- Validating message persistence across restarts.

---

## Overview

The test ensures that Kafka persists messages even when the broker restarts. It performs the following operations:

1. **Produce Message**: Send messages to a Kafka topic.
2. **Stop and Restart Kafka**: Simulate broker failure and recovery.
3. **Consume Messages After Restart**: Ensure messages persist and can be read after restart.

---

## Features

### Kafka Container

- Uses the `KafkaContainer` class from the `testcontainers` library to spin up a Kafka instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Message Persistence

- Ensures Kafka retains messages across restarts.
- Validates data integrity after broker recovery.

### Assertions

- Ensures that stored messages remain available after a broker restart.

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
python -m pytest 02_message_persistence.py -v -s
```

or

```bash
python3 -m pytest 02_message_persistence.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/dd40922b-2c11-49bf-878a-36bcce37f44b)

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

The test publishes messages to a Kafka topic before stopping the broker:

```python
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
producer.send("test_topic", b"Persistent Message")
producer.flush()
```

- Sends a persistent message to `test_topic`.

### 3. Stopping and Restarting Kafka

To test persistence, the Kafka container is stopped and restarted:

```python
kafka_container.stop()
time.sleep(5)  # Simulate downtime
kafka_container.start()
```

- Simulates a Kafka broker failure and recovery.

### 4. Consuming Messages After Restart

After the restart, the test attempts to consume the previously published messages:

```python
consumer = KafkaConsumer("test_topic", bootstrap_servers=kafka_bootstrap_server, auto_offset_reset="earliest")
message = next(consumer)
```

- Subscribes to `test_topic` and retrieves messages after restart.

### 5. Assertions

The test uses assertions to validate message persistence:

```python
assert message.value == b"Persistent Message"
```

- Ensures the message remains available after the broker restart.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable Kafka containers.
- Automatically manages container lifecycle.

### Kafka Message Persistence

- Demonstrates Kafka's ability to retain messages across restarts.
- Ensures reliability of Kafka messaging systems.

### Assertions

- Validates message persistence and availability after broker recovery.

---

