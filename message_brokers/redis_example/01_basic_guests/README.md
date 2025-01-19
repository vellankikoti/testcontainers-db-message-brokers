# Example 01: Basic Guests

This example demonstrates how to register a guest using Redis as the data store, focusing on the asynchronous processing of guest registration requests. The example covers:

- Sending a message to register a guest.
- Handling guest registration confirmation.
- Error handling for registration failures.

## Features

### Guest Registration

- Send a message to the Redis database to register a new guest.
- Confirm successful registration through a response message.

### Error Handling

- Handle errors during the registration process.
- Send appropriate error messages back to the client.

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

For Redis:
```bash
pip install redis
```

or
```bash
pip3 install redis
```

### 2. Run the Test

Execute the test file using pytest:

For Redis:
```bash
python -m pytest 01_basic_guests.py -v -s
```

or
```bash
python3 -m pytest 01_basic_guests.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/d21cd14d-8510-443a-b604-c7aa266ec229)

---

### Key Points in the README

- **Overview**: Describes the purpose of the example.
- **Features**: Lists the main functionalities implemented in the example.
- **Installation Instructions**: Provides commands to install the necessary dependencies for Redis.
- **Execution Instructions**: Shows how to run the test using `pytest`.
- **Expected Output**: Placeholder for expected output, which can be replaced with actual output or screenshots once the example is implemented.

---
