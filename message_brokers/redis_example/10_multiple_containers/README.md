# Example 10: Multiple Containers

This example demonstrates how to manage multiple containers for the reservation system using Redis as the data store. It focuses on orchestrating multiple services to work together seamlessly. The example covers:

- Setting up multiple containers using Docker Compose.
- Configuring inter-service communication.
- Managing dependencies between services.

## Features

### Multi-Container Setup

- Use Docker Compose to define and run multiple containers for the application.
- Configure services such as the Redis database and the reservation service.

### Inter-Service Communication

- Ensure that services can communicate with each other effectively.
- Handle service dependencies and startup order.

## How to Run the Test

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
or
```bash
pip3 install -r requirements.txt
```

### 2. Run the Tests

Execute the test file using pytest:

For Redis:
```bash
python -m pytest 10_multiple_containers.py -v -s
```

or
```bash
python3 -m pytest 10_multiple_containers.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/9a3197ee-d4c6-47ea-8571-344a7e8ba60d)

