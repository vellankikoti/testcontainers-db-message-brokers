# Example 10: Multiple Containers (MongoDB and Redis)

This example demonstrates how to use Testcontainers to test interactions between multiple containers, specifically MongoDB and Redis. It covers:

- Synchronizing data between MongoDB and Redis.
- Testing data consistency across containers.
- Validating caching mechanisms.
- Handling multi-container setups.

---

## Overview

The test simulates a hotel management system that uses MongoDB as the primary database and Redis as a caching layer. It performs the following operations:

- **Data Synchronization**: Sync data from MongoDB to Redis.
- **Caching**: Test Redis as a caching layer for frequently accessed data.
- **Data Consistency**: Validate data consistency between MongoDB and Redis.
- **Multi-Container Setup**: Test interactions between MongoDB and Redis containers.

---

## Features

### Multi-Container Setup

- Start and manage multiple containers.
- Test interactions between containers.
- Validate data flow across containers.

### Data Synchronization

- Sync data from MongoDB to Redis.
- Test real-time data updates.
- Validate data consistency.

### Caching

- Use Redis as a caching layer.
- Test cache performance.
- Validate cache invalidation.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers pymongo redis
```

or

```bash
pip3 install pytest testcontainers pymongo redis
```

### 2. Run the Test

Execute the test file using `pytest`:

```bash
python -m pytest 10_multiple_containers.py -v -s
```

or

```bash
python3 -m pytest 10_multiple_containers.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/4191ef85-706f-4d67-85c5-d1cee5fcc014)


---

## Code Walkthrough

### 1. Multi-Container Setup

Start MongoDB and Redis containers and retrieve connection details:

```python
with MongoDbContainer("mongo:6.0") as mongo, RedisContainer("redis:7.0") as redis:
    mongodb_url = mongo.get_connection_url()
    redis_host = redis.get_container_host_ip()
    redis_port = redis.get_exposed_port(6379)
```

- Starts MongoDB and Redis containers.
- Retrieves connection details for both containers.

---

### 2. Data Synchronization

Sync data from MongoDB to Redis:

```python
for guest in guests_collection.find():
    redis_client.hset("guests", guest["_id"], guest["name"])
```

- Reads data from MongoDB.
- Writes data to Redis.

---

### 3. Caching

Test Redis caching:

```python
redis_client.hset("guests", "123", "Alice")
cached_guest = redis_client.hget("guests", "123")
assert cached_guest.decode() == "Alice"
```

- Stores data in Redis.
- Retrieves and validates cached data.

---

### 4. Data Consistency

Validate data consistency between MongoDB and Redis:

```python
for guest in guests_collection.find():
    cached_guest = redis_client.hget("guests", str(guest["_id"]))
    assert cached_guest.decode() == guest["name"]
```

- Compares data in MongoDB and Redis.
- Ensures data consistency.

---

## Key Takeaways

### Multi-Container Benefits

- Test interactions between services.
- Validate data flow across containers.
- Simulate real-world setups.

### Testing Practices

- Test data synchronization.
- Validate caching mechanisms.
- Ensure data consistency.
- Handle multi-container setups.

### Data Synchronization

- Sync data between services.
- Test real-time updates.
- Validate data consistency.

---

## Common Issues and Solutions

### 1. Container Startup

- Ensure containers are running.
- Check connection details.
- Monitor container logs.

### 2. Data Synchronization

- Handle missing fields.
- Validate data formats.
- Test for partial updates.

### 3. Caching

- Test cache invalidation.
- Validate cache performance.
- Handle cache misses.

---

## Future Enhancements

### Planned Features

- Real-time data synchronization.
- Advanced caching strategies.
- Multi-database setups.
- Integration with monitoring tools.

### Testing Improvements

- Larger datasets.
- Concurrent data updates.
- Performance testing.
- Fault tolerance testing.

---
