# Example 02: Room Management

This example demonstrates how to manage room availability using Redis as the message broker. It focuses on the asynchronous processing of room management requests, including updating room availability and handling confirmations.

## Features

### Room Management

- Send a message to the Redis list to update room availability.
- Confirm successful updates through a response message.

### Error Handling

- Handle errors during the room management process.
- Log appropriate error messages for debugging.

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install redis pytest testcontainers
```

or

```bash
pip3 install redis pytest testcontainers
```

### 2. Run the Test

Execute the test file using pytest:

```bash
python -m pytest 02_room_management.py -v -s
```

or

```bash
python3 -m pytest 02_room_management.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/cb48cf2b-0450-4146-859d-dd179ffc0eb7)

