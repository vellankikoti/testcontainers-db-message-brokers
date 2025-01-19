# Example 12: Distributed Transactions

This example demonstrates how to manage distributed transactions using a message broker, focusing on ensuring data consistency across multiple services. The example covers:

- Coordinating transactions across different services.
- Implementing the Saga pattern for distributed transactions.
- Handling failures and rollbacks in a distributed environment.

---

## Features

### Distributed Transaction Coordination

- Use a message broker to coordinate transactions between multiple services.
- Ensure that all services involved in the transaction are notified and can participate.

### Saga Pattern Implementation

- Implement the Saga pattern to manage long-running transactions.
- Define compensating actions to roll back changes in case of failures.

### Error Handling and Rollbacks

- Handle errors that may occur during the distributed transaction process.
- Ensure that appropriate rollback mechanisms are in place to maintain data consistency.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

For RabbitMQ:
```bash
pip install pika
```
or
```bash
pip3 install pika
```

For Kafka:
```bash
pip install kafka-python
```
or
```bash
pip3 install kafka-python
```

For Redis:
```bash
pip install redis
```
or
```bash
pip3 install redis
```

---

### 2. Run the Distributed Transaction Test

Execute the test file using pytest:
```bash
python -m pytest 12_distributed_transactions.py -v -s
```
or
```bash
python3 -m pytest 12_distributed_transactions.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/2d122e3a-a349-47e8-aae3-f25c56d94fd0)
