# Example 11: Simulating Network Interruptions

This example demonstrates how to simulate network interruptions in the reservation system using Redis as the data store. It focuses on testing the system's resilience and error handling capabilities when network issues occur. The example covers:

- Simulating network failures during reservation processing.
- Handling timeouts and retries.
- Ensuring the system can recover from network interruptions.

## Features

### Network Interruption Simulation

- Simulate network interruptions to test the system's response.
- Trigger timeouts and retries during reservation processing.

### Error Handling

- Implement robust error handling to manage network failures gracefully.
- Provide appropriate error messages and recovery options for users.

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

### 2. Run the Network Interruption Tests

Execute the test file using pytest:

For Redis:
```bash
python -m pytest 11_simulating_network_interruptions.py -v -s
```

or
```bash
python3 -m pytest 11_simulating_network_interruptions.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/0d54e9a8-3242-4fbf-8721-ae081b2dd656)

