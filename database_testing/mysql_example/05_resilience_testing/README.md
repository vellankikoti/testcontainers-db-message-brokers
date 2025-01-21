# Example 5: Resilience Testing (MySQL)

This example demonstrates how to use Testcontainers to test MySQL’s resilience under failure conditions. It covers the following:

- Setting up a MySQL container.
- Simulating database failures and network interruptions.
- Testing automatic reconnection and data integrity.
- Using assertions to validate resilience mechanisms.

---

## Overview

The test ensures that MySQL handles unexpected failures gracefully and maintains data consistency. It performs the following operations:

1. **Insert Data**: Add records to the database before failure.
2. **Simulate Failure**: Stop and restart the MySQL container.
3. **Reconnect & Retrieve Data**: Verify that data remains intact after recovery.
4. **Assertions**: Ensure database operations resume successfully.

---

## Features

### MySQL Container

- Uses the `MySqlContainer` class from the `testcontainers` library to spin up a MySQL database in a Docker container.
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
pip install pytest testcontainers mysql-connector-python
```

or

```bash
pip3 install pytest testcontainers mysql-connector-python
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

### 2. Insert Initial Data

The test inserts sample records before simulating a failure:

```python
cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("Alice", "alice@example.com"))
```

- Ensures data is stored before downtime.

### 3. Simulating Database Failure

The test stops and restarts the container to simulate failure:

```python
mysql_container.stop()
time.sleep(5)  # Wait for downtime effect
mysql_container.start()
```

- Stops the MySQL container for a brief period.
- Restarts it to test recovery.

### 4. Reconnecting and Verifying Data Integrity

After restart, the test reconnects and verifies data consistency:

```python
cursor.execute("SELECT * FROM users WHERE name = %s", ("Alice",))
retrieved_user = cursor.fetchone()
assert retrieved_user is not None
```

- Ensures that previously inserted data remains intact.

### 5. Performing New Operations Post-Recovery

The test checks if the database can accept new operations after recovery:

```python
cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("Bob", "bob@example.com"))
cursor.execute("SELECT COUNT(*) FROM users")
assert cursor.fetchone()[0] == 2
```

- Verifies that new inserts succeed after reconnection.

---

## Key Takeaways

### Testcontainers

- Simplifies resilience testing by providing lightweight, disposable database containers.
- Automatically manages container lifecycle.

### MySQL Resilience Testing

- Tests how MySQL handles failures and recoveries.
- Ensures automatic reconnection and data persistence.

### Assertions

- Confirms data remains intact after failures.
- Validates that new operations can be performed post-recovery.

---

