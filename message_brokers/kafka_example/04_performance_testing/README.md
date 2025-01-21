# Example 4: Performance Testing with Kafka

This example demonstrates how to use Testcontainers to test Kafka's performance under high-load scenarios. It covers the following:

- Setting up a Kafka container.
- Producing a large volume of messages.
- Measuring execution time for message publishing and consumption.
- Using assertions to validate performance expectations.

---

## Overview

The test measures Kafka's performance under high-load conditions by producing and consuming a large number of messages. It performs the following operations:

1. **Bulk Message Production**: Send a large number of messages to a Kafka topic.
2. **Bulk Message Consumption**: Consume messages efficiently.
3. **Measure Execution Time**: Benchmark Kafka's performance.
4. **Optimize Processing**: Test with different consumer configurations.

---

## Features

### Kafka Container

- Uses the `KafkaContainer` class from the `testcontainers` library to spin up a Kafka instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Performance Testing

- Inserts and retrieves a large volume of messages.
- Measures execution time for message publishing and consumption.
- Tests different consumer configurations for performance optimization.

### Assertions

- Ensures that Kafka can handle high throughput efficiently.
- Validates that message processing occurs within acceptable time limits.

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
python -m pytest 04_performance_testing.py -v -s
```

or

```bash
python3 -m pytest 04_performance_testing.py -v -s
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

### 2. Bulk Message Production

The test publishes a large number of messages to a Kafka topic:

```python
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
for i in range(100000):
    producer.send("test_topic", f"Message {i}".encode())
producer.flush()
```

- Sends 100,000 messages to `test_topic`.

### 3. Bulk Message Consumption

The test retrieves messages efficiently:

```python
consumer = KafkaConsumer("test_topic", bootstrap_servers=kafka_bootstrap_server, auto_offset_reset="earliest")
messages = [msg.value.decode() for msg in consumer]
```

- Consumes all messages from `test_topic`.

### 4. Performance Measurement

The test measures execution time for Kafka operations:

```python
import time

start_time = time.time()
for i in range(100000):
    producer.send("test_topic", f"Message {i}".encode())
producer.flush()
end_time = time.time()
execution_time = end_time - start_time
```

- Measures the time taken to publish 100,000 messages.

### 5. Assertions

The test uses assertions to ensure acceptable execution times:

```python
assert execution_time < 5.0  # Ensure message publishing remains under 5 seconds
assert len(messages) == 100000  # Validate that all messages were received
```

- Ensures Kafka handles high throughput efficiently.

---

## Key Takeaways

### Testcontainers

- Simplifies performance testing by providing lightweight, disposable Kafka containers.
- Automatically manages container lifecycle.

### Kafka Performance Testing

- Measures Kafka's ability to handle high message throughput.
- Tests different consumer configurations for efficiency.

### Assertions

- Ensures bulk message processing occurs within acceptable time limits.
- Confirms that all messages are successfully processed.

---

