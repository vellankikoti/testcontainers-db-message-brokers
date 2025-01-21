# Example 4: Performance Testing with RabbitMQ

This example demonstrates how to use Testcontainers to test RabbitMQ’s performance under high-load conditions. It covers the following:

- Setting up a RabbitMQ container.
- Publishing a large volume of messages.
- Measuring execution time for message publishing and consumption.
- Using assertions to validate performance expectations.

---

## Overview

The test measures RabbitMQ’s performance under high-load conditions by producing and consuming a large number of messages. It performs the following operations:

1. **Bulk Message Production**: Send a large number of messages to a RabbitMQ queue.
2. **Bulk Message Consumption**: Consume messages efficiently.
3. **Measure Execution Time**: Benchmark RabbitMQ’s performance.
4. **Optimize Processing**: Test with different consumer configurations.

---

## Features

### RabbitMQ Container

- Uses the `RabbitMqContainer` class from the `testcontainers` library to spin up a RabbitMQ instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Performance Testing

- Inserts and retrieves a large volume of messages.
- Measures execution time for message publishing and consumption.
- Tests different consumer configurations for performance optimization.

### Assertions

- Ensures that RabbitMQ can handle high throughput efficiently.
- Validates that message processing occurs within acceptable time limits.

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

### 1. RabbitMQ Container Setup

The test uses the `RabbitMqContainer` class to start a RabbitMQ broker in a Docker container:

```python
with RabbitMqContainer("rabbitmq:3.9-management") as rabbitmq:
    yield rabbitmq.get_connection_url()
```

- The container runs RabbitMQ version 3.9 with management UI.
- The `get_connection_url()` method provides the connection string for RabbitMQ clients.

### 2. Bulk Message Production

The test publishes a large number of messages to a RabbitMQ queue:

```python
for i in range(100000):
    channel.basic_publish(exchange='', routing_key='perf_queue', body=f'Message {i}')
```

- Sends 100,000 messages to `perf_queue`.

### 3. Bulk Message Consumption

The test retrieves messages efficiently:

```python
def callback(ch, method, properties, body):
    received_messages.append(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='perf_queue', on_message_callback=callback, auto_ack=False)
channel.start_consuming()
```

- Consumes messages from `perf_queue` and acknowledges them.

### 4. Performance Measurement

The test measures execution time for RabbitMQ operations:

```python
import time

start_time = time.time()
for i in range(100000):
    channel.basic_publish(exchange='', routing_key='perf_queue', body=f'Message {i}')
end_time = time.time()
execution_time = end_time - start_time
```

- Measures the time taken to publish 100,000 messages.

### 5. Assertions

The test uses assertions to ensure acceptable execution times:

```python
assert execution_time < 5.0  # Ensure message publishing remains under 5 seconds
assert len(received_messages) == 100000  # Validate that all messages were received
```

- Ensures RabbitMQ handles high throughput efficiently.

---

## Key Takeaways

### Testcontainers

- Simplifies performance testing by providing lightweight, disposable RabbitMQ containers.
- Automatically manages container lifecycle.

### RabbitMQ Performance Testing

- Measures RabbitMQ’s ability to handle high message throughput.
- Tests different consumer configurations for efficiency.

### Assertions

- Ensures bulk message processing occurs within acceptable time limits.
- Confirms that all messages are successfully processed.

---

