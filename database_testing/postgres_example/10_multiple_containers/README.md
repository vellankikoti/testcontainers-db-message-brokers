# Example 10: Multiple Containers

## Overview
This example demonstrates how to test scenarios involving multiple containers, such as a PostgreSQL database and a Redis cache.

## Features
- Set up and manage multiple containers.
- Test interactions between a database and a cache.
- Verify data consistency across services.

## Code Structure
- `10_multiple_containers.py`: Main test file.
- `Dockerfile`: Custom Dockerfile for PostgreSQL.
- `init.sql`: SQL script to initialize the database with sample data.
- `conftest.py`: Pytest configuration file for custom markers.

## How to Run

**Make sure you have all required dependencies installed:**

```bash
pip install testcontainers pytest sqlalchemy psycopg2-binary redis
```
or
```bash
pip3 install testcontainers pytest sqlalchemy psycopg2-binary redis
```
---
1. Build the Docker image:
   ```bash
   docker build -t custom-postgres:1.0 .
   ```

2. Run the tests:
   ```bash
   python -m pytest 10_multiple_containers.py -v
   ```
   or
   ```bash
   python3 -m pytest 10_multiple_containers.py -v
   ```

### Expected Output
- PostgreSQL and Redis containers are started.
- User data is cached from PostgreSQL to Redis.
- Cache verification is successful.

## Key Takeaways
- Testcontainers makes it easy to manage multiple containers in tests.
- Redis can be used as a caching layer for PostgreSQL data.
- Testing interactions between services ensures data consistency and correctness.

---

## Steps to Run

1. **Build the Docker Image**:
   ```bash
   docker build -t custom-postgres:1.0 .
   ```

2. **Run the Tests**:
   ```bash
   python -m pytest 10_multiple_containers.py -v
   ```
   or
     ```bash
   python3 -m pytest 10_multiple_containers.py -v
   ```

### Expected Output
If everything is set up correctly, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/67e69b74-89cd-4919-876d-ef78a4515862)

### For more detailed output:

   ```bash
   python -m pytest 10_multiple_containers.py -v -s
   ```
   or
   ```bash
   python3 -m pytest 10_multiple_containers.py -v -s
   ```

#### Expected Output

![image](https://github.com/user-attachments/assets/8fca7c3c-ec77-4cc1-bf22-c9d4d4d1f6b0)
