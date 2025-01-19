# Example 8: Performance Testing

## Overview
This example demonstrates how to test the performance of database queries and operations using Testcontainers and pytest.

---

## Features
- Measure query execution time.
- Test bulk insert performance.
- Ensure database operations meet performance expectations.

---

## Code Structure
- **`08_performance_testing.py`**: Main test file.
- **`docker/Dockerfile`**: Custom Dockerfile for PostgreSQL.
- **`docker/init.sql`**: SQL script to initialize the database with sample data.
- **`conftest.py`**: Pytest configuration file for custom markers.

---

## How to Run

### 1. Build the Docker Image
Navigate to the `docker` directory and build the custom PostgreSQL image:
```bash
docker build -t custom-postgres:1.0 .
```

### 2. Run the Test
Execute the test using pytest:
```bash
python -m pytest 08_performance_testing.py -v
```
or
```bash
python3 -m pytest 08_performance_testing.py -v
```
---

## Expected Output

![image](https://github.com/user-attachments/assets/67796b35-e469-42e6-941b-8231cc15b297)


---

## Key Takeaways

### Performance Metrics
- Monitor and measure query execution time.
- Ensure bulk insert operations are efficient.
- Validate database performance against predefined benchmarks.

### Advantages
- Identify slow queries and optimize them.
- Test database performance under varying loads.
- Ensure scalable and reliable database operations.

---

## Common Pitfalls

### Performance Bottlenecks
- Inefficient SQL queries.
- Large batch sizes for bulk inserts.
- Insufficient database resources.

### Testing Issues
- Overhead introduced by test frameworks.
- Incorrect performance thresholds.

---

## Debugging Tips

### Common Issues
- Queries taking longer than expected.
- Errors during bulk inserts.
- Inconsistent performance results.

### Solutions
- Optimize SQL queries for better performance.
- Use appropriate batch sizes for bulk operations.
- Increase allocated resources for the database.

---

## Future Enhancements

### Additional Scenarios
- Test with concurrent database operations.
- Evaluate performance under stress conditions.
- Monitor resource usage during tests.

### Improvements
- Automate performance benchmarking.
- Include advanced analytics for query optimization.
- Extend tests to other database systems.

---

## Related Documentation
- [pytest Documentation](https://docs.pytest.org/en/latest/)
- [TestContainers Python](https://testcontainers-python.readthedocs.io/)
- [PostgreSQL Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [SQL Query Optimization](https://www.sqlshack.com/sql-query-optimization-tips-and-tricks/)

---
