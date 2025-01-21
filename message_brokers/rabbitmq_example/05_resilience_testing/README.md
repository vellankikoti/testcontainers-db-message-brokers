# Example 5: Resilience Testing with RabbitMQ

This example demonstrates how to use Testcontainers to test RabbitMQ’s resilience under failure conditions. It covers the following:

- Setting up a RabbitMQ container.
- Simulating RabbitMQ failures and restarts.
- Testing automatic reconnection and message integrity.
- Using assertions to validate resilience mechanisms.

---

## Overview

The test ensures that RabbitMQ handles unexpected failures gracefully and maintains message integrity. It performs the following operations:

1. **Publish Messages**: Send messages to a RabbitMQ queue.
2. **Simulate Failure**: Stop and restart the RabbitMQ broker.
3. **Reconnect & Consume Messages**: Verify that messages remain available after recovery.
4. **Assertions**: Ensure RabbitMQ resumes operations successfully post-recovery.

---

## Features

### RabbitMQ Container

- Uses the `RabbitMqContainer` class from the `testcontainers` library to spin up a RabbitMQ instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Resilience Testing

- Simulates RabbitMQ failures and restarts.
- Tests automatic reconnection mechanisms.
- Ensures message integrity after container recovery.

### Assertions

- Validates that messages remain available after a broker restart.
- Confirms RabbitMQ resumes normal operations after failure recovery.

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

### 1. RabbitMQ Container Setup

The test uses the `RabbitMqContainer` class to start a RabbitMQ broker in a Docker container:

```python
with RabbitMqContainer("rabbitmq:3.9-management") as rabbitmq:
    yield rabbitmq.get_connection_url()
```

- The container runs RabbitMQ version 3.9 with management UI.
- The `get_connection_url()` method provides the connection string for RabbitMQ clients.

### 2. Producing Initial Messages

The test produces messages before simulating a failure:

```python
channel.queue_declare(queue='resilience_queue', durable=True)
channel.basic_publish(
    exchange='',
    routing_key='resilience_queue',
    body='Message before failure'
)
```

- Sends a message before RabbitMQ goes down.

### 3. Simulating RabbitMQ Failure

The test stops and restarts the RabbitMQ container to simulate failure:

```python
rabbitmq_container.stop()
time.sleep(5)  # Simulate downtime
rabbitmq_container.start()
```

- Stops the RabbitMQ container temporarily.
- Restarts it to test recovery.

### 4. Reconnecting and Consuming Messages

After the restart, the test reconnects and verifies message availability:

```python
method_frame, header_frame, body = channel.basic_get(queue='resilience_queue', auto_ack=True)
```

- Ensures messages persist after the restart.

### 5. Performing New Operations Post-Recovery

The test verifies that RabbitMQ can still process new messages after recovery:

```python
channel.basic_publish(
    exchange='',
    routing_key='resilience_queue',
    body='Message after recovery'
)
method_frame, header_frame, new_body = channel.basic_get(queue='resilience_queue', auto_ack=True)
```

- Ensures RabbitMQ can send and receive new messages post-recovery.

### 6. Assertions

The test uses assertions to validate RabbitMQ resilience:

```python
assert body == b'Message before failure'
assert new_body == b'Message after recovery'
```

- Ensures that RabbitMQ retains messages through failures.
- Validates RabbitMQ resumes normal operation after restart.

---

## Key Takeaways

### Testcontainers

- Simplifies resilience testing by providing lightweight, disposable RabbitMQ containers.
- Automatically manages container lifecycle.

### RabbitMQ Resilience Testing

- Tests RabbitMQ’s ability to recover from failures while maintaining message integrity.
- Ensures automatic reconnection and continued operation.

### Assertions

- Confirms messages remain available after failures.
- Validates RabbitMQ continues to operate correctly post-recovery.

---

