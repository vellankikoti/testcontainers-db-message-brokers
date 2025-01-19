# Example 01: Basic Guests

This example demonstrates how to register a guest using Kafka as the message broker, focusing on the asynchronous processing of guest registration requests. The example covers:

- Sending a message to register a guest.
- Handling guest registration confirmation.
- Error handling for registration failures.

## Features

### Guest Registration

- Send a message to the Kafka topic to register a new guest.
- Confirm successful registration through a response message.

### Error Handling

- Handle errors during the registration process.
- Send appropriate error messages back to the client.

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

### 2. Run the Test

Execute the test file using `pytest`:

For Kafka:
```bash
python -m pytest 01_basic_guests.py -v -s
```
or
```bash
python3 -m pytest 01_basic_guests.py -v -s
```

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/ae9b5b85-3b9b-4d81-a995-c065f396e225)

