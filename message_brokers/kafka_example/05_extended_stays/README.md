# Example 05: Extended Stays

This example demonstrates how to manage extended stays using Kafka as the message broker, focusing on the asynchronous processing of stay extension requests. The example covers:

- Sending a message to request an extension of a guest's stay.
- Handling extension confirmation.
- Error handling for extension failures.

## Features

### Extended Stay Management

- Send a message to the Kafka topic to request an extension of a stay.
- Confirm successful extensions through a response message.

### Error Handling

- Handle errors during the stay extension process.
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

Execute the test file using pytest:

For Kafka:
```bash
python -m pytest 05_extended_stays.py -v -s
```

or
```bash
python3 -m pytest 05_extended_stays.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/772b18ad-dab0-47ba-8a51-0b1525529ca0)
