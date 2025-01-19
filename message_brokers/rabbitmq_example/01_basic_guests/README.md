# Example 01: Basic Guests

This example demonstrates how to register a guest using a message broker, focusing on the asynchronous processing of guest registration requests. The example covers:

- Sending a message to register a guest.
- Handling guest registration confirmation.
- Error handling for registration failures.

---

## Features

### Guest Registration

- Send a message to the message broker to register a new guest.
- Confirm successful registration through a response message.

### Error Handling

- Handle errors during the registration process.
- Send appropriate error messages back to the client.

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

For RabbitMQ:
```bash
python -m pytest 01_basic_guests.py -v -s
```
or
```bash
python3 -m pytest 01_basic_guests.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/8e7ee738-7fda-49bf-a069-279e8dea1eba)

