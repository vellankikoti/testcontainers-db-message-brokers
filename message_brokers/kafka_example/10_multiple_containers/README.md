# Example 10: Multiple Containers

This example demonstrates how to set up and test a Kafka-based application using multiple containers. It focuses on orchestrating multiple services that communicate through Kafka, ensuring that they work together seamlessly. The example covers:

- Setting up multiple containers for different services.
- Configuring Kafka to facilitate communication between these services.
- Verifying the interaction between the containers.

## Features

### Multi-Container Setup

- Use Docker Compose to define and run multiple containers for your application.
- Each container can represent a different service (e.g., producer, consumer, database).

### Inter-Service Communication

- Configure Kafka to enable communication between the different services running in separate containers.
- Ensure that messages are correctly sent and received across the services.

### Verification

- Verify that all services are running and can communicate with each other through Kafka.
- Log interactions and confirm that messages are processed as expected.

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3` in each service:

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
python -m pytest 10_multiple_containers.py -v -s
```

or
```bash
python3 -m pytest 10_multiple_containers.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/c7ff8ac9-06d3-4083-b30c-08490b20406b)
