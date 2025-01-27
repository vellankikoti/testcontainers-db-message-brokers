# Example 4: Performance Testing (MongoDB)

This example demonstrates how to use Testcontainers to perform performance testing on MongoDB. It covers the following:

- Setting up a MongoDB container.
- Inserting a large volume of data.
- Measuring query execution time.
- Using assertions to validate performance expectations.

---

## Overview

The test measures MongoDB's performance under a high-load scenario by performing bulk insertions and running queries against large datasets. It performs the following operations:

1. **Insert Data**: Add a large number of records to the database.
2. **Measure Query Performance**: Execute queries and measure execution time.
3. **Optimize Queries**: Apply indexing to improve performance.
4. **Assertions**: Validate that query performance meets expectations.

---

## Features

### MongoDB Container

- Uses the `MongoDbContainer` class from the `testcontainers` library to spin up a MongoDB database in a Docker container.
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
pip install pytest testcontainers pymongo
```

or

```bash
pip3 install pytest testcontainers pymongo
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

![image](https://github.com/user-attachments/assets/3efca0c4-491c-4bab-87a0-c98a0ae0ef8b)

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

### 2. Bulk Data Insertion

The test inserts a large number of records to simulate high-load scenarios:

```python
bulk_data = [{"name": f"User{i}", "email": f"user{i}@example.com", "age": i % 100} for i in range(100000)]
collection.insert_many(bulk_data)
```

- Generates 100,000 sample user records.
- Inserts them into the `users` collection.

### 3. Query Performance Measurement

The test measures the execution time for a query:

```python
import time

start_time = time.time()
users_over_50 = list(collection.find({"age": {"$gt": 50}}))
end_time = time.time()
execution_time = end_time - start_time
```

- Queries for users older than 50.
- Measures the time taken for the query execution.

### 4. Indexing for Performance Optimization

To improve query performance, the test applies an index:

```python
collection.create_index("age")
```

- Creates an index on the `age` field.
- Reduces query execution time for searches involving `age`.

### 5. Assertions

The test uses assertions to ensure performance is within acceptable limits:

```python
assert execution_time < 1.0  # Ensure query executes within 1 second
assert len(users_over_50) > 0  # Ensure some results are returned
```

- Validates that queries execute quickly.
- Ensures data retrieval is successful.

---

## Key Takeaways

### Testcontainers

- Simplifies performance testing by providing lightweight, disposable database containers.
- Automatically manages container lifecycle.

### MongoDB Performance Testing

- Measures database performance under high load.
- Uses indexing to optimize query speed.

### Assertions

- Ensures query execution time meets performance expectations.
- Validates that large-scale data operations function correctly.

---

