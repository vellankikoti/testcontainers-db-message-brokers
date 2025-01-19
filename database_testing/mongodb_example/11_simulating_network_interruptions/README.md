# Example 11: Simulating Network Interruptions (MongoDB)

This example demonstrates how to test the resilience of a MongoDB-based system by simulating network interruptions using Testcontainers. It covers:

- Simulating network instability.
- Testing database reconnection logic.
- Validating transaction rollbacks during interruptions.
- Ensuring data consistency after failures.

---

## Overview

The test simulates a hotel management system that interacts with a MongoDB database. It performs the following operations:

- **Network Interruptions**: Simulate network instability and test the system's ability to recover.
- **Reconnection Logic**: Validate the system's ability to reconnect to the database after interruptions.
- **Transaction Rollbacks**: Ensure that incomplete transactions are rolled back during failures.
- **Data Consistency**: Verify data integrity after network interruptions.

---

## Features

### Network Simulation

- Simulate network interruptions.
- Test system behavior during failures.
- Validate reconnection logic.

### Transaction Rollbacks

- Ensure incomplete transactions are rolled back.
- Test rollback logic during interruptions.
- Validate data consistency.

### Data Consistency

- Verify data integrity after failures.
- Test for missing or corrupted data.
- Ensure consistent state.

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
python -m pytest 11_simulating_network_interruptions.py -v -s
```

or

```bash
python3 -m pytest 11_simulating_network_interruptions.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/0d5c9a2b-46d1-43af-8c23-132a3014143d)


---

## Code Walkthrough

### 1. Network Interruption Simulation

Simulate network interruptions by stopping and starting the MongoDB container:

```python
container.stop()
time.sleep(5)
container.start()
```

- Stops and restarts the MongoDB container to simulate network interruptions.
- Tests the system's ability to handle database unavailability.

---

### 2. Reconnection Logic

Test reconnection logic by trying to reconnect to MongoDB:

```python
try:
    client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
except Exception as e:
    assert "No suitable servers" in str(e)
```

- Validates the system's ability to reconnect to the database.
- Ensures proper error handling during reconnection attempts.

---

### 3. Transaction Rollbacks

Test transaction rollback during interruptions:

```python
with client.start_session() as session:
    session.start_transaction()
    collection.insert_one({"guest_id": 1, "name": "Alice"}, session=session)
    container.stop()  # Simulate network failure
    session.abort_transaction()
```

- Ensures that incomplete transactions are rolled back during failures.
- Tests rollback logic under network interruptions.

---

### 4. Data Consistency

Validate data consistency after interruptions:

```python
assert collection.count_documents({}) == 0
```

- Verifies that no partial data is left in the database after failures.
- Ensures data consistency.

---

## Key Takeaways

### Resilience Testing

- Test system behavior under network instability.
- Validate reconnection logic.
- Ensure transaction rollbacks.

### Data Consistency

- Verify data integrity after failures.
- Test for missing or corrupted data.
- Ensure consistent state.

### Network Simulation

- Simulate real-world network issues.
- Test system recovery mechanisms.
- Validate error handling.

---

## Common Issues and Solutions

### 1. Network Interruptions

- Ensure proper container restart.
- Monitor container logs.
- Test reconnection logic.

### 2. Transaction Rollbacks

- Validate rollback logic.
- Test for partial transactions.
- Ensure consistent state.

### 3. Data Consistency

- Verify data integrity.
- Test for missing or corrupted data.
- Handle edge cases.

---

## Future Enhancements

### Planned Features

- Real-time network simulation.
- Advanced failure scenarios.
- Multi-database setups.
- Integration with monitoring tools.

### Testing Improvements

- Larger datasets.
- Concurrent transactions.
- Performance testing.
- Fault tolerance testing.

---
