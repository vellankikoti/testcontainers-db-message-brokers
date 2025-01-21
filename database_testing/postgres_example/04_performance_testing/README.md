# Example 4: Performance Testing (PostgreSQL)

This example demonstrates how to use Testcontainers to perform performance testing on PostgreSQL. It covers the following:

- Setting up a PostgreSQL container.
- Inserting a large volume of data.
- Measuring query execution time.
- Using assertions to validate performance expectations.

---

## Overview

The test measures PostgreSQL's performance under a high-load scenario by performing bulk insertions and running queries against large datasets. It performs the following operations:

1. **Insert Data**: Add a large number of records to the database.
2. **Measure Query Performance**: Execute queries and measure execution time.
3. **Optimize Queries**: Apply indexing to improve performance.
4. **Assertions**: Validate that query performance meets expectations.

---

## Features

### PostgreSQL Container

- Uses the `PostgreSqlContainer` class from the `testcontainers` library to spin up a PostgreSQL database in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Performance Testing

- Inserts a large volume of data to simulate real-world usage.
- Measures execution time for queries.
- Applies indexing to analyze performance improvements.

### Assertions

- Ensures that queries execute within an acceptable time range.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers psycopg2-binary
```

or

```bash
pip3 install pytest testcontainers psycopg2-binary
```

### 2. Run the Test

Execute the test file using `pytest`:

```bash
python -m pytest 04_performance_testing.py -v -s
```

or

```bash
python3 -m pytest 04_performance_testing.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/725e9979-685c-4073-80b1-fb466cb427b3)

---

## Code Walkthrough

### 1. PostgreSQL Container Setup

The test uses the `PostgreSqlContainer` class to start a PostgreSQL database in a Docker container:

```python
with PostgreSqlContainer("postgres:15") as postgres:
    yield postgres.get_connection_url()
```

- The container runs PostgreSQL version 15.
- The `get_connection_url()` method provides the connection string for the PostgreSQL client.

### 2. Bulk Data Insertion

The test inserts a large number of records to simulate high-load scenarios:

```python
bulk_data = [(f"User{i}", f"user{i}@example.com") for i in range(100000)]
cursor.executemany("INSERT INTO users (name, email) VALUES (%s, %s)", bulk_data)
```

- Generates 100,000 sample user records.
- Inserts them into the `users` table.

### 3. Query Performance Measurement

The test measures the execution time for a query:

```python
import time

start_time = time.time()
cursor.execute("SELECT * FROM users WHERE name LIKE 'User9%'")
users = cursor.fetchall()
end_time = time.time()
execution_time = end_time - start_time
```

- Queries for users whose names start with 'User9'.
- Measures the time taken for the query execution.

### 4. Indexing for Performance Optimization

To improve query performance, the test applies an index:

```python
cursor.execute("CREATE INDEX idx_name ON users(name)")
```

- Creates an index on the `name` column.
- Reduces query execution time for searches involving `name`.

### 5. Assertions

The test uses assertions to ensure performance is within acceptable limits:

```python
assert execution_time < 1.0  # Ensure query executes within 1 second
assert len(users) > 0  # Ensure some results are returned
```

- Validates that queries execute quickly.
- Ensures data retrieval is successful.

---

## Key Takeaways

### Testcontainers

- Simplifies performance testing by providing lightweight, disposable database containers.
- Automatically manages container lifecycle.

### PostgreSQL Performance Testing

- Measures database performance under high load.
- Uses indexing to optimize query speed.

### Assertions

- Ensures query execution time meets performance expectations.
- Validates that large-scale data operations function correctly.

---

