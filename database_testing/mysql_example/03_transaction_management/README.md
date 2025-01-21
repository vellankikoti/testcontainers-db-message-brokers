# Example 3: Transaction Management (MySQL)

This example demonstrates how to use Testcontainers to test transaction management in MySQL. It covers the following:

- Setting up a MySQL container.
- Creating a database table.
- Performing transactions with multiple operations.
- Using assertions to validate transaction behavior.

---

## Overview

The test ensures that MySQL transactions behave as expected by committing or rolling back a series of operations. It performs the following operations:

1. **Begin Transaction**: Start a transaction.
2. **Insert Data**: Add multiple user records within a transaction.
3. **Update Data**: Modify a record within the transaction.
4. **Commit Transaction**: Ensure all changes persist upon success.
5. **Rollback Transaction**: Validate that changes do not persist when rolling back.

---

## Features

### MySQL Container

- Uses the `MySqlContainer` class from the `testcontainers` library to spin up a MySQL database in a Docker container.
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
pip install pytest testcontainers mysql-connector-python
```

or

```bash
pip3 install pytest testcontainers mysql-connector-python
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

### 1. MySQL Container Setup

The test uses the `MySqlContainer` class to start a MySQL database in a Docker container:

```python
with MySqlContainer("mysql:8.0") as mysql:
    yield mysql.get_connection_url()
```

- The container runs MySQL version 8.0.
- The `get_connection_url()` method provides the connection string for the MySQL client.

### 2. Transaction Management

#### **Begin Transaction**
```python
cursor.execute("START TRANSACTION")
```
- Starts a new transaction.

#### **Insert Data**
```python
cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("Alice", "alice@example.com"))
cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("Bob", "bob@example.com"))
```
- Adds multiple records within a transaction.

#### **Update Data**
```python
cursor.execute("UPDATE users SET email = %s WHERE name = %s", ("alice@updated.com", "Alice"))
```
- Modifies a record within the transaction.

#### **Commit Transaction**
```python
cursor.execute("COMMIT")
```
- Ensures all operations persist upon success.

#### **Rollback Transaction**
```python
cursor.execute("ROLLBACK")
```
- Ensures no changes persist when rolling back.

### 3. Assertions

The test uses assertions to validate transaction behavior:

```python
cursor.execute("SELECT email FROM users WHERE name = %s", ("Alice",))
result = cursor.fetchone()
assert result[0] == "alice@updated.com"

cursor.execute("SELECT COUNT(*) FROM users")
count = cursor.fetchone()[0]
assert count == 2  # Ensures both users exist
```

- Ensures committed changes persist.
- Ensures rolled-back changes do not exist.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable database containers.
- Automatically manages container lifecycle.

### MySQL Transactions

- Ensures data integrity by grouping operations into a single atomic transaction.
- Provides rollback capabilities for error scenarios.

### Assertions

- Validates that committed transactions persist and rolled-back transactions are discarded.

---

