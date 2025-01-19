# Example 12: Distributed Transactions

This example demonstrates how to manage distributed transactions in a Kafka-based application. It focuses on ensuring that multiple services can participate in a transaction while maintaining data consistency. The example covers:

- Coordinating transactions across multiple services.
- Implementing the Saga pattern for distributed transactions.
- Handling transaction failures and rollbacks.

## Features

### Distributed Transaction Management

- Use Kafka to coordinate transactions between different services.
- Implement the Saga pattern to manage long-running transactions.

### Transaction Coordination

- Ensure that all participating services can commit or rollback changes based on the transaction outcome.
- Log the transaction status and any errors encountered during the process.

### Error Handling

- Handle failures gracefully and ensure that the system can recover from transaction errors.
- Implement compensation actions to rollback changes if necessary.

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

### 2. Run the Distributed Transaction Test

Execute the distributed transaction test file using pytest:

For Kafka:
```bash
python -m pytest 12_distributed_transactions.py -v -s
```

or
```bash
python3 -m pytest 12_distributed_transactions.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/18478bd2-a34d-4a08-86d2-2304e0f57c90)

