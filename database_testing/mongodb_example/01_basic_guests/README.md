# Example 1: Basic Guests (MongoDB)

This example demonstrates how to use Testcontainers to test basic MongoDB database operations. It covers the following:

- Setting up a MongoDB container.
- Creating a database collection.
- Performing basic CRUD (Create, Read, Update, Delete) operations.
- Using assertions to validate the operations.

---

## Overview

The test simulates a simple hotel guest management system. It creates a `guests` collection, inserts sample data, and performs the following operations:

1. **Insert**: Add guest records to the database.
2. **Select**: Retrieve and count the number of guests.
3. **Update**: Modify a guest's phone number.
4. **Delete**: Remove a guest record.

The test ensures that all operations are performed correctly and validates the results using assertions.

---

## Features

### MongoDB Container

- Uses the `MongoDbContainer` class from the `testcontainers` library to spin up a MongoDB database in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Database Operations

- Creates a `guests` collection in the MongoDB database.
- Performs CRUD operations and validates the results.

### Assertions

- Ensures the database operations produce the expected results.

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
python -m pytest 01_basic_guests.py -v -s
```

or

```bash
python3 -m pytest 01_basic_guests.py -v -s
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

### 2. Database Collection

The `guests_collection` fixture sets up the `guests` collection in the MongoDB database:

```python
db = mongodb_client.get_database("test_db")
collection = db.get_collection("guests")
```

- The `test_db` database is created automatically.
- The `guests` collection is used to store guest records.

### 3. CRUD Operations

- **Insert**: Adds guest records to the collection.
- **Select**: Retrieves guest records by specific criteria.
- **Update**: Updates the phone number of a guest.
- **Delete**: Deletes a guest record.

### 4. Assertions

The test uses assertions to validate the results of each operation:

```python
assert saved_guest["name"] == "Alice"
assert updated_guest["phone"] == "111-111-1111"
assert deleted_guest is None
```

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable database containers.
- Automatically manages container lifecycle.

### MongoDB

- Demonstrates how to use MongoDB for basic CRUD operations.
- Uses the `pymongo` library to interact with the database.

### CRUD Operations

- Demonstrates how to perform and validate basic database operations.

### Assertions

- Ensures the database behaves as expected.

---
