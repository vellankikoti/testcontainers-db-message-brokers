# Example 3: Kafka Data Integrity Testing

This example demonstrates how to use **Testcontainers** to test **Kafka data integrity**. It covers the following:

- Setting up a Kafka container.
- Producing messages to a Kafka topic.
- Validating message ordering and uniqueness.
- Ensuring message integrity upon consumption.

---

## Overview

The test ensures that Kafka maintains **message integrity, ordering, and uniqueness** when messages are produced and consumed. It performs the following operations:

1. **Produce Messages**: Send multiple messages to a Kafka topic.
2. **Consume Messages**: Retrieve messages from the topic.
3. **Validate Data Integrity**: Ensure messages are received in order, with no duplicates.

---

## Features

### Kafka Container

- Uses the `KafkaContainer` class from the `testcontainers` library to spin up a Kafka instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Data Integrity Validation

- Ensures **Kafka maintains message order**.
- Verifies that **no duplicate messages** exist.
- Ensures **all messages are accurately retrieved**.

### Assertions

- Validates **message ordering, uniqueness, and completeness**.

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
python -m pytest 03_kafka_data_integrity.py -v -s
```

or

```bash
python3 -m pytest 03_kafka_data_integrity.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

```bash
Producing messages to Kafka...
✅ Messages successfully produced!

Consuming messages from Kafka...

Validating message integrity...
✅ Kafka data integrity validation PASSED! 🎉
```

---

## Code Walkthrough

### 1. Kafka Container Setup

The test uses the `KafkaContainer` class to start a Kafka broker in a Docker container:

```python
with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
    yield kafka.get_bootstrap_server()
```

- The container runs the **latest version of Kafka**.
- The `get_bootstrap_server()` method provides the **connection string** for Kafka clients.

### 2. Producing Messages

The test publishes multiple messages to a Kafka topic:

```python
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
messages_sent = [b"Message 1", b"Message 2", b"Message 3"]

for message in messages_sent:
    producer.send("data_integrity_topic", message)
producer.flush()
```

- Sends three messages (`Message 1`, `Message 2`, `Message 3`) to the topic.

### 3. Consuming Messages

After messages are produced, the test retrieves them from Kafka:

```python
consumer = KafkaConsumer(
    "data_integrity_topic",
    bootstrap_servers=kafka_bootstrap_server,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    consumer_timeout_ms=5000
)
messages_received = [msg.value for msg in consumer]
```

- Subscribes to `data_integrity_topic`.
- Collects all received messages.

### 4. Data Integrity Validation

The test uses assertions to validate Kafka's data integrity:

```python
assert messages_received == messages_sent, "Message order was not preserved!"
assert len(messages_received) == len(set(messages_received)), "Duplicate messages detected!"
assert set(messages_received) == set(messages_sent), "Some messages are missing!"
```

- Ensures **message order is preserved**.
- Ensures **no duplicate messages** exist.
- Ensures **all messages were successfully retrieved**.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable Kafka containers.
- Automatically manages container lifecycle.

### Kafka Data Integrity

- Demonstrates **Kafka's ability to maintain message order and uniqueness**.
- Ensures **reliability of Kafka messaging systems**.

### Assertions

- Validates **message ordering, uniqueness, and completeness**.

---

## Troubleshooting

### Common Issues

1. **Docker Not Running**  
   - Ensure Docker is installed and running:  
     ```bash
     docker ps
     ```

2. **ModuleNotFoundError: No module named 'kafka-python'**  
   - Install the missing dependency:  
     ```bash
     pip install kafka-python
     ```

3. **Kafka Testcontainer Failing to Start**  
   - Try allocating more memory to Docker.

---

## Next Steps

You can extend this test by:
- **Testing high-volume messaging scenarios**.
- **Simulating message failures and retries**.
- **Validating performance under load**.

---

🔥 **Happy Testing!** 🚀

