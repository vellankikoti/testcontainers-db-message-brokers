# Example 08: Performance Testing

This example demonstrates how to conduct performance testing on a Kafka-based application. It focuses on measuring the throughput and latency of message processing. The example covers:

- Sending a high volume of messages to Kafka.
- Measuring the time taken for message processing.
- Analyzing the performance metrics.

## Features

### Performance Metrics

- Send a large number of messages to the Kafka topic to simulate load.
- Measure and log the time taken for message processing.

### Throughput and Latency Analysis

- Analyze the throughput (messages per second) and latency (time taken for processing) of the application.
- Generate performance reports based on the collected metrics.

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

For Kafka:
```bash
pip install kafka-python
```

or
```bash
pip3 install kafka-python
```

### 2. Run the Performance Test

Execute the performance test file using pytest:

For Kafka:
```bash
python -m pytest 08_performance_testing.py -v -s
```

or
```bash
python3 -m pytest 08_performance_testing.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/b6de06da-2bc5-497d-9c37-d6cc89b44a5d)

