# Example 8: Performance Testing (MongoDB)

This example demonstrates how to use Testcontainers to test the performance of MongoDB operations. It covers:

- Measuring query execution times.
- Testing bulk insert performance.
- Analyzing read and write performance.
- Identifying performance bottlenecks.

---

## Overview

The test simulates a performance testing scenario for a MongoDB-based hotel management system. It performs the following operations:

- **Bulk Insert**: Measure the time taken to insert a large number of records.
- **Query Performance**: Analyze the execution time of complex queries.
- **Read/Write Performance**: Test the speed of read and write operations.
- **Indexing Impact**: Evaluate the impact of indexes on query performance.

---

## Features

### Performance Metrics

- Measure query execution times.
- Analyze bulk insert performance.
- Test read and write speeds.
- Evaluate indexing impact.

### Bulk Operations

- Insert large datasets.
- Test database scalability.
- Analyze performance under load.

### Indexing

- Create indexes for faster queries.
- Test query performance with and without indexes.

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
python -m pytest 08_performance_testing.py -v -s
```

or

```bash
python3 -m pytest 08_performance_testing.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/7af0947c-ea2f-403c-aa32-6f1fef5e9036)



---

## Code Walkthrough

### 1. Bulk Insert

Insert 10,000 records into the database:

```python
start_time = time.time()
collection.insert_many([{"room_id": i, "status": "available"} for i in range(10000)])
end_time = time.time()
execution_time = end_time - start_time
```

- Measures the time taken to insert a large number of records.
- Tests database scalability under load.

---

### 2. Query Execution Time

Measure the time taken to execute a complex query:

```python
start_time = time.time()
result = collection.find({"status": "available"}).count()
end_time = time.time()
execution_time = end_time - start_time
```

- Analyzes the execution time of queries.
- Tests the impact of query complexity on performance.

---

### 3. Read/Write Performance

Measure the time taken to read and write records:

```python
start_time = time.time()
collection.find_one({"room_id": 1})
end_time = time.time()
read_time = end_time - start_time
```

- Tests the speed of read and write operations.
- Identifies potential bottlenecks.

---

### 4. Indexing Impact

Create an index and measure its impact on query performance:

```python
collection.create_index("room_id")
start_time = time.time()
result = collection.find({"room_id": 5000}).count()
end_time = time.time()
execution_time = end_time - start_time
```

- Evaluates the impact of indexes on query performance.
- Tests the effectiveness of indexing for large datasets.

---

## Key Takeaways

### MongoDB Benefits

- Efficient handling of large datasets.
- Flexible schema for performance testing.
- Powerful indexing capabilities.

### Testing Practices

- Measure execution times.
- Test under realistic loads.
- Analyze performance bottlenecks.
- Validate indexing impact.

### Performance Testing

- Bulk insert performance.
- Query execution analysis.
- Read/write speed testing.
- Indexing optimization.

---

## Common Issues and Solutions

### 1. Bulk Insert Performance

- Use `insert_many` for batch inserts.
- Optimize document size.
- Monitor memory usage.

### 2. Query Performance

- Use proper indexing.
- Optimize query filters.
- Avoid unnecessary fields.

### 3. Indexing Impact

- Test with and without indexes.
- Monitor index creation time.
- Validate index effectiveness.

---

## Future Enhancements

### Planned Features

- Advanced query testing.
- Real-time performance monitoring.
- Load testing with concurrent users.
- Integration with performance dashboards.

### Testing Improvements

- Larger datasets.
- Complex query scenarios.
- Multi-index testing.
- Performance under high concurrency.

---
