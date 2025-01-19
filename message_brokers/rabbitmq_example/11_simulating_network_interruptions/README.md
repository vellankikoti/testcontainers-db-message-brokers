# Example 11: Simulating Network Interruptions

This example demonstrates how to simulate network interruptions in a message broker environment, focusing on testing the system's resilience and error recovery capabilities. The example covers:

- Introducing network failures during message transmission.
- Handling message delivery failures and retries.
- Validating the system's behavior under network stress.

---

## Features

### Network Interruption Simulation

- Simulate network interruptions by blocking or dropping messages between services.
- Observe how the system responds to these interruptions.

### Error Recovery

- Implement retry mechanisms for failed message deliveries.
- Ensure that messages are not lost and are processed once the network is restored.

### System Behavior Validation

- Validate the system's behavior during and after network interruptions.
- Monitor logs and metrics to assess recovery performance.

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

### 2. Run the Network Interruption Test

Execute the test file using pytest:
```bash
python -m pytest 11_simulating_network_interruptions.py -v -s
```
or
```bash
python3 -m pytest 11_simulating_network_interruptions.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/8a2744ca-1886-4ca3-a227-8145c2ced3a7)
