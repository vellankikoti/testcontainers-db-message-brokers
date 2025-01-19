# Example 12: Distributed Transactions (MongoDB)

This example demonstrates how to test distributed transactions across multiple MongoDB databases using a simulated two-phase commit protocol. Distributed transactions ensure data consistency across multiple databases or services, even in the event of failures. This example covers:

- Coordinating transactions across multiple databases.
- Implementing a two-phase commit protocol.
- Validating data consistency across databases.
- Handling transaction failures in distributed systems.

---

## Features

### Two-Phase Commit Protocol

- **Prepare Phase**: Ensures all participants are ready to commit.
- **Commit Phase**: Commits the transaction across all participants.
- **Rollback Phase**: Aborts the transaction if any participant fails.

### Data Consistency

- Ensures all databases remain in a consistent state.
- Validates that no partial updates occur during failures.

### Error Handling

- Handles failures during the prepare or commit phases.
- Rolls back changes to maintain consistency.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers pymongo
```

or

```bash
pip3 install pytest testcontainers pymongo
```

### 2. Run the Test

Execute the test file using `pytest`:

```bash
python -m pytest 12_distributed_transactions.py -v -s
```

or

```bash
python3 -m pytest 12_distributed_transactions.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/93489651-5035-470e-821d-da01b449263f)


---

## Code Walkthrough

### 1. Two-Phase Commit Protocol

The `DistributedTransactionManager` class implements the two-phase commit protocol:

- **Prepare Phase**: Ensures both databases are reachable and ready for the transaction.
- **Commit Phase**: Commits the transaction in both databases.
- **Rollback Phase**: Aborts the transaction in both databases if an error occurs.

### 2. Distributed Transaction

The test simulates a distributed transaction across two MongoDB databases:

- Transfers funds between accounts in two separate databases.
- Uses the two-phase commit protocol to ensure consistency.

### 3. Transaction Failure

The test simulates a failure during the transaction:

- Rolls back changes in both databases.
- Ensures no partial updates occur.

---

## Key Takeaways

### Distributed Transactions

- Ensure data consistency across multiple databases.
- Handle failures gracefully with rollback mechanisms.
- Use the two-phase commit protocol for coordination.

### Testing Practices

- Simulate real-world failure scenarios.
- Validate data consistency after failures.
- Test rollback mechanisms thoroughly.

---

## Common Issues and Solutions

### 1. Transaction Coordination

- Ensure all participants are reachable during the prepare phase.
- Handle network interruptions gracefully.

### 2. Rollback Failures

- Test rollback mechanisms for all failure scenarios.
- Ensure no partial updates occur during rollback.

### 3. Data Consistency

- Validate data integrity after each transaction.
- Test for missing or corrupted data.

---

## Future Enhancements

### Planned Features

- Support for more complex distributed systems.
- Integration with monitoring tools for real-time transaction tracking.
- Automated testing for distributed transaction scenarios.

### Testing Improvements

- Larger datasets for stress testing.
- Concurrent distributed transactions.
- Performance testing under high load.

---
