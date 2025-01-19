# Example 06: Simulating Failures

This example demonstrates how to simulate failures in the reservation system using Redis as the data store. It focuses on testing the system's resilience and error handling capabilities under various failure scenarios. The example covers:

- Simulating network failures during reservation processing.
- Handling unexpected errors and exceptions.
- Ensuring the system can recover from failures.

## Features

### Failure Simulation

- Simulate network interruptions to test the system's response.
- Trigger exceptions during reservation processing to evaluate error handling.

### Error Handling

- Implement robust error handling to manage failures gracefully.
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

### 2. Run the Test

Execute the test file using pytest:

For Redis:
```bash
python -m pytest 06_simulating_failures.py -v -s
```

or
```bash
python3 -m pytest 06_simulating_failures.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/7ea6a870-402d-4392-927c-340210273c2c)

