# Example 11: Simulating Network Interruptions

This example demonstrates how to simulate network interruptions in a Kafka-based application. It focuses on testing the resilience of the application when faced with network issues. The example covers:

- Introducing network latency and failures.
- Observing the application's behavior during interruptions.
- Verifying recovery mechanisms.

## Features

### Network Interruption Simulation

- Use tools like `tc` (traffic control) to simulate network latency and packet loss.
- Test how the application handles message delivery failures and retries.

### Resilience Testing

- Verify that the application can recover from network interruptions.
- Log the behavior of the application during and after the interruptions.

### Error Handling

- Ensure that appropriate error messages are generated during network failures.
- Confirm that the application can continue processing messages after recovery.

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

### 2. Simulate Network Interruptions

You can use the following command to introduce network latency (e.g., 100ms) on the Kafka container:
```bash
docker exec -it kafka-container-name tc qdisc add dev eth0 root netem delay 100ms
```

To simulate packet loss, you can use:
```bash
docker exec -it kafka-container-name tc qdisc change dev eth0 root netem loss 10%
```

### 3. Run the Test

Execute the network interruption test file using pytest:

For Kafka:
```bash
python -m pytest 11_simulating_network_interruptions.py -v -s
```

or
```bash
python3 -m pytest 11_simulating_network_interruptions.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/685d6296-9aa7-4d6a-a4b9-55e95464851d)

