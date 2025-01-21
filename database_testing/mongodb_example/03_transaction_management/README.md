# Example 3: Transaction Management (MongoDB)

This example demonstrates how to use Testcontainers to test transaction management in MongoDB. It covers the following:

- Setting up a MongoDB container.
- Creating a database collection.
- Performing transactions with multiple operations.
- Using assertions to validate transaction behavior.

---

## Overview

The test ensures that MongoDB transactions behave as expected by committing or rolling back a series of operations. It performs the following operations:

1. **Begin Transaction**: Start a session-based transaction.
2. **Insert Data**: Add multiple user records within a transaction.
3. **Update Data**: Modify a record within the transaction.
4. **Commit Transaction**: Ensure all changes persist upon success.
5. **Rollback Transaction**: Validate that changes do not persist when rolling back.

---

## Features

### MongoDB Container

- Uses the `MongoDbContainer` class from the `testcontainers` library to spin up a MongoDB database in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Transaction Management

- Executes multiple database operations within a transaction.
- Commits or rolls back operations based on conditions.

### Assertions

- Ensures that committed transactions persist changes.
- Verifies that rolled-back transactions discard changes.

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
python -m pytest 03_transaction_management.py -v -s
```

or

```bash
python3 -m pytest 03_transaction_management.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/725e9979-685c-4073-80b1-fb466cb427b3)

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

### 2. Transaction Management

#### **Begin Transaction**
```python
session = mongodb_client.start_session()
session.start_transaction()
```
- Starts a transaction session.

#### **Insert Data**
```python
users_collection.insert_one({"name": "Alice", "email": "alice@example.com"}, session=session)
users_collection.insert_one({"name": "Bob", "email": "bob@example.com"}, session=session)
```
- Adds multiple records within a transaction.

#### **Update Data**
```python
users_collection.update_one({"name": "Alice"}, {"$set": {"email": "alice@updated.com"}}, session=session)
```
- Modifies a record within the transaction.

#### **Commit Transaction**
```python
session.commit_transaction()
```
- Ensures all operations persist upon success.

#### **Rollback Transaction**
```python
session.abort_transaction()
```
- Ensures no changes persist when rolling back.

### 3. Assertions

The test uses assertions to validate transaction behavior:

```python
assert users_collection.find_one({"name": "Alice"})["email"] == "alice@updated.com"
assert users_collection.find_one({"name": "Bob"}) is not None
```

- Ensures committed changes persist.
- Ensures rolled-back changes do not exist.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable database containers.
- Automatically manages container lifecycle.

### MongoDB Transactions

- Ensures data integrity by grouping operations into a single atomic transaction.
- Provides rollback capabilities for error scenarios.

### Assertions

- Validates that committed transactions persist and rolled-back transactions are discarded.

---

