# Example 13: Testing with Mock Services

This example demonstrates how to use mock services in conjunction with a message broker to test the behavior of your application without relying on real external services. The example covers:

- Setting up mock services to simulate real service behavior.
- Sending and receiving messages through the message broker.
- Validating interactions with the mock services.

---

## Features

### Mock Service Setup

- Create mock services that mimic the behavior of real services.
- Use libraries like `unittest.mock` or `responses` to simulate responses.

### Message Broker Interaction

- Send messages to the mock services through the message broker.
- Receive and process messages as if they were coming from real services.

### Validation of Interactions

- Validate that the application interacts correctly with the mock services.
- Ensure that the expected messages are sent and received.

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

### 2. Run the Mock Service Test

Execute the test file using pytest:
```bash
python -m pytest 13_testing_with_mock_services.py -v -s
```
or
```bash
python3 -m pytest 13_testing_with_mock_services.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/5cbb55b7-2c2e-41f1-8a7a-75728b96051e)
