# Example 5: Resilience Testing (MongoDB)

This example demonstrates how to use Testcontainers to test MongoDB’s resilience under failure conditions. It covers the following:

- Setting up a MongoDB container.
- Simulating database failures and network interruptions.
- Testing automatic reconnection and data integrity.
- Using assertions to validate resilience mechanisms.

---

## Overview

The test ensures that MongoDB handles unexpected failures gracefully and maintains data consistency. It performs the following operations:

1. **Insert Data**: Add records to the database before failure.
2. **Simulate Failure**: Stop and restart the MongoDB container.
3. **Reconnect & Retrieve Data**: Verify that data remains intact after recovery.
4. **Assertions**: Ensure database operations resume successfully.

---

## Features

### MongoDB Container

- Uses the `MongoDbContainer` class from the `testcontainers` library to spin up a MongoDB database in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Resilience Testing

- Simulates database downtime.
- Tests automatic reconnection mechanisms.
- Ensures data integrity after recovery.

### Assertions

- Validates that data remains available after recovery.
- Ensures that new operations can be performed post-reconnection.

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
python -m pytest 05_resilience_testing.py -v -s
```

or

```bash
python3 -m pytest 05_resilience_testing.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

<img width="946" alt="image" src="https://github.com/user-attachments/assets/4a8a826d-b378-4042-9e08-b1c34265f38f" />

---

## Code Walkthrough

### 1. MongoDB Container Setup

The test uses the `MongoDbContainer` class to start a MongoDB database in a Docker container:

```python
with MongoDbContainer("mongo:6.0") as mongo:
    yield mongo.get_connection_url()
```

- The container runs MongoDB version 6.0.
- The `get_connection_url()` method provides the connection string for the MongoDB client.

### 2. Insert Initial Data

The test inserts sample records before simulating a failure:

```python
collection.insert_one({"name": "Alice", "email": "alice@example.com"})
```

- Ensures data is stored before downtime.

### 3. Simulating Database Failure

The test stops and restarts the container to simulate failure:

```python
mongo_container.stop()
time.sleep(5)  # Wait for downtime effect
mongo_container.start()
```

- Stops the MongoDB container for a brief period.
- Restarts it to test recovery.

### 4. Reconnecting and Verifying Data Integrity

After restart, the test reconnects and verifies data consistency:

```python
retrieved_user = collection.find_one({"name": "Alice"})
assert retrieved_user is not None
```

- Ensures that previously inserted data remains intact.

### 5. Performing New Operations Post-Recovery

The test checks if the database can accept new operations after recovery:

```python
collection.insert_one({"name": "Bob", "email": "bob@example.com"})
assert collection.count_documents({}) == 2
```

- Verifies that new inserts succeed after reconnection.

---

## Key Takeaways

### Testcontainers

- Simplifies resilience testing by providing lightweight, disposable database containers.
- Automatically manages container lifecycle.

### MongoDB Resilience Testing

- Tests how MongoDB handles failures and recoveries.
- Ensures automatic reconnection and data persistence.

### Assertions

- Confirms data remains intact after failures.
- Validates that new operations can be performed post-recovery.

---

