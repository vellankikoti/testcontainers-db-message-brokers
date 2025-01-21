# Example 5: Resilience Testing with Kafka

This example demonstrates how to use Testcontainers to test Kafka’s resilience under failure conditions. It covers the following:

- Setting up a Kafka container.
- Simulating Kafka failures and restarts.
- Testing automatic reconnection and message integrity.
- Using assertions to validate resilience mechanisms.

---

## Overview

The test ensures that Kafka handles unexpected failures gracefully and maintains message integrity. It performs the following operations:

1. **Produce Messages**: Send messages to a Kafka topic.
2. **Simulate Failure**: Stop and restart the Kafka broker.
3. **Reconnect & Consume Messages**: Verify that messages remain available after recovery.
4. **Assertions**: Ensure Kafka resumes operations successfully post-recovery.

---

## Features

### Kafka Container

- Uses the `KafkaContainer` class from the `testcontainers` library to spin up a Kafka instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Resilience Testing

- Simulates Kafka failures and restarts.
- Tests automatic reconnection mechanisms.
- Ensures message integrity after container recovery.

### Assertions

- Validates that messages remain available after a broker restart.
- Confirms Kafka resumes normal operations after failure recovery.

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
python -m pytest 05_resilience_testing.py -v -s
```

or

```bash
python3 -m pytest 05_resilience_testing.py -v -s
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

### 2. Producing Initial Messages

The test produces messages before simulating a failure:

```python
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
producer.send("test_topic", b"Message before failure")
producer.flush()
```

- Sends a message before Kafka goes down.

### 3. Simulating Kafka Failure

The test stops and restarts the Kafka container to simulate failure:

```python
kafka_container.stop()
time.sleep(5)  # Simulate downtime
kafka_container.start()
```

- Stops the Kafka container temporarily.
- Restarts it to test recovery.

### 4. Reconnecting and Consuming Messages

After the restart, the test reconnects and verifies message availability:

```python
consumer = KafkaConsumer("test_topic", bootstrap_servers=kafka_bootstrap_server, auto_offset_reset="earliest")
message = next(consumer)
```

- Ensures messages persist after the restart.

### 5. Performing New Operations Post-Recovery

The test verifies that Kafka can still process new messages after recovery:

```python
producer.send("test_topic", b"Message after recovery")
producer.flush()
new_message = next(consumer)
```

- Ensures Kafka can send and receive new messages post-recovery.

### 6. Assertions

The test uses assertions to validate Kafka resilience:

```python
assert message.value == b"Message before failure"
assert new_message.value == b"Message after recovery"
```

- Ensures that Kafka retains messages through failures.
- Validates Kafka resumes normal operation after restart.

---

## Key Takeaways

### Testcontainers

- Simplifies resilience testing by providing lightweight, disposable Kafka containers.
- Automatically manages container lifecycle.

### Kafka Resilience Testing

- Tests Kafka’s ability to recover from failures while maintaining message integrity.
- Ensures automatic reconnection and continued operation.

### Assertions

- Confirms messages remain available after failures.
- Validates Kafka continues to operate correctly post-recovery.

---

