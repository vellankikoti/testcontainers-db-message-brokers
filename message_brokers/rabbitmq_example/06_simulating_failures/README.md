# Example 06: Simulating Failures

This example demonstrates how to simulate failures in a message broker environment, focusing on testing the system's resilience and error-handling capabilities. The example covers:

- Sending messages that trigger failure scenarios.
- Handling failure responses and recovery mechanisms.
- Logging and reporting errors during failure simulations.

---

## Features

### Failure Simulation

- Send messages to the message broker that intentionally cause failures (e.g., invalid data, timeouts).
- Observe how the system responds to these failures.

### Error Handling

- Handle errors during the failure simulation process.
- Log error messages and recovery attempts.

### Recovery Mechanisms

- Test the system's ability to recover from failures.
- Ensure that appropriate fallback mechanisms are in place.

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

### 2. Run the Test

Execute the test file using pytest:

```bash
python -m pytest 06_simulating_failures.py -v -s
```
or
```bash
python3 -m pytest 06_simulating_failures.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/f18e84c9-688d-4394-836e-896c542925cb)
