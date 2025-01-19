# Example 08: Performance Testing

This example demonstrates how to conduct performance testing on a message broker, focusing on measuring throughput, latency, and resource utilization. The example covers:

- Sending a high volume of messages to the broker.
- Measuring response times and throughput.
- Analyzing resource usage during the test.

---

## Features

### Throughput Measurement

- Send a large number of messages to the message broker to measure throughput.
- Calculate the number of messages processed per second.

### Latency Measurement

- Measure the time taken for messages to be sent and acknowledged.
- Analyze the latency under different load conditions.

### Resource Utilization Analysis

- Monitor CPU and memory usage during the performance test.
- Ensure that the message broker operates within acceptable resource limits.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

For RabbitMQ:
```bash
pip install pika
```
or
```bash
pip3 install pika
```

For Kafka:
```bash
pip install kafka-python
```
or
```bash
pip3 install kafka-python
```

For Redis:
```bash
pip install redis
```
or
```bash
pip3 install redis
```

---

### 2. Run the Performance Test

Execute the performance test file using pytest:
```bash
python -m pytest 08_performance_testing.py -v -s
```
or
```bash
python3 -m pytest 08_performance_testing.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/dd968840-94a6-4c2d-9c13-5a9eb1fc7df4)
