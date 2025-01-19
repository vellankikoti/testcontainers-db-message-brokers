# Example 12: Distributed Transactions

This example demonstrates how to manage distributed transactions in the reservation system using Redis as the data store. It focuses on ensuring data consistency across multiple services during transaction processing. The example covers:

- Implementing distributed transactions using Redis.
- Handling commit and rollback scenarios.
- Ensuring data integrity across services.

## Features

### Distributed Transaction Management

- Implement a mechanism to handle distributed transactions across multiple services.
- Ensure that all operations either complete successfully or are rolled back in case of failure.

### Error Handling

- Handle errors during transaction processing.
- Provide appropriate error messages for failed transactions or inconsistencies.

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

### 2. Run the Distributed Transaction Tests

Execute the test file using pytest:

For Redis:
```bash
python -m pytest 12_distributed_transactions.py -v -s
```

or
```bash
python3 -m pytest 12_distributed_transactions.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/6bff39b8-c5c1-416c-9bfd-2e7e40a442ed)

