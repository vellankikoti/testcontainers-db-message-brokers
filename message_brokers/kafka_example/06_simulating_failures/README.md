# Example 06: Simulating Failures

This example demonstrates how to simulate failures in the reservation process using Kafka as the message broker. It focuses on testing the system's resilience and error handling capabilities. The example covers:

- Sending a message to simulate a failure during the reservation process.
- Handling failure notifications.
- Verifying the system's response to failures.

## Features

### Failure Simulation

- Send a message to the Kafka topic to simulate a failure in the reservation process.
- Confirm that the system correctly handles the failure.

### Error Handling

- Handle errors during the failure simulation.
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
python -m pytest 06_simulating_failures.py -v -s
```

or
```bash
python3 -m pytest 06_simulating_failures.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/3d5e5606-6110-4489-8820-080c2c1b3d3c)

