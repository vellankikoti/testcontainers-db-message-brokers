# Example 1: Basic CRUD Operations (MongoDB)

This example demonstrates how to use Testcontainers to test basic MongoDB database operations. It covers the following:

- Setting up a MongoDB container.
- Creating a database collection.
- Performing basic CRUD (Create, Read, Update, Delete) operations.
- Using assertions to validate the operations.

---

## Overview

The test simulates a general-purpose document storage scenario. It creates a `users` collection, inserts sample data, and performs the following operations:

1. **Insert**: Add user records to the database.
2. **Select**: Retrieve and count the number of users.
3. **Update**: Modify a user's email address.
4. **Delete**: Remove a user record.

The test ensures that all operations are performed correctly and validates the results using assertions.

---

## Features

### MongoDB Container

- Uses the `MongoDbContainer` class from the `testcontainers` library to spin up a MongoDB database in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Database Operations

- Creates a `users` collection in the MongoDB database.
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
python -m pytest 01_basic_crud.py -v -s
```

or

```bash
python3 -m pytest 01_basic_crud.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:



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

The `users_collection` fixture sets up the `users` collection in the MongoDB database:

```python
db = mongodb_client.get_database("test_db")
collection = db.get_collection("users")
```

- The `test_db` database is created automatically.
- The `users` collection is used to store user records.

### 3. CRUD Operations

- **Insert**: Adds user records to the collection.
- **Select**: Retrieves user records by specific criteria.
- **Update**: Updates the email of a user.
- **Delete**: Deletes a user record.

### 4. Assertions

The test uses assertions to validate the results of each operation:

```python
assert saved_user["name"] == "Alice"
assert updated_user["email"] == "alice@example.com"
assert deleted_user is None
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

