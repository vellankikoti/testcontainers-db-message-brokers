# Example 02: Room Management

This example demonstrates how to manage room availability using Kafka as the message broker, focusing on the asynchronous processing of room management requests. The example covers:

- Sending a message to update room availability.
- Handling room management confirmation.
- Error handling for management failures.

## Features

### Room Management

- Send a message to the Kafka topic to update room availability.
- Confirm successful updates through a response message.

### Error Handling

- Handle errors during the room management process.
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
python -m pytest 02_room_management.py -v -s
```

or
```bash
python3 -m pytest 02_room_management.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/be45d597-34f4-4559-8189-071fffa4ef6c)

