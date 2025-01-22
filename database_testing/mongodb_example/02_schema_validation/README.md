# Example 2: Schema Validation (MongoDB)

This example demonstrates how to use Testcontainers to test schema validation in MongoDB. It covers the following:

- Setting up a MongoDB container.
- Creating a database collection with schema validation.
- Inserting valid and invalid documents.
- Using assertions to validate the schema enforcement.

---

## Overview

The test ensures that the MongoDB collection enforces a defined schema by allowing valid documents and rejecting invalid ones. It performs the following operations:

1. **Define Schema**: Create a `users` collection with validation rules.
2. **Insert Valid Data**: Add user records that comply with the schema.
3. **Insert Invalid Data**: Attempt to add records that violate the schema.
4. **Assertion Checks**: Verify that only valid records are stored.

---

## Features

### MongoDB Container

- Uses the `MongoDbContainer` class from the `testcontainers` library to spin up a MongoDB database in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Schema Validation

- Creates a `users` collection with predefined schema rules.
- Ensures that invalid documents are rejected.

### Assertions

- Confirms that only valid documents are stored in the collection.

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
python -m pytest 02_schema_validation.py -v -s
```

or

```bash
python3 -m pytest 02_schema_validation.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/b8076e4a-2188-44dd-85d2-dcd588b097e7)

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

### 2. Defining Schema Validation

The test defines a schema for the `users` collection, enforcing rules for data consistency:

```python
schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "email", "age"],
            "properties": {
                "name": {"bsonType": "string", "description": "must be a string"},
                "email": {"bsonType": "string", "pattern": "^.+@.+\\..+$", "description": "must be a valid email"},
                "age": {"bsonType": "int", "minimum": 0, "description": "must be a positive integer"}
            }
        }
    }
}
```

- Requires `name`, `email`, and `age` fields.
- Ensures `name` is a string.
- Ensures `email` matches a valid pattern.
- Ensures `age` is a positive integer.

### 3. Performing Schema Validation

#### **Insert Valid Data**
```python
valid_user = {"name": "Alice", "email": "alice@example.com", "age": 30}
collection.insert_one(valid_user)
```
- Inserts a valid user document.

#### **Insert Invalid Data**
```python
invalid_user = {"name": "Bob", "email": "invalid-email", "age": "twenty"}
collection.insert_one(invalid_user)  # Should raise an error
```
- Attempts to insert an invalid document (should fail).

### 4. Assertions

The test uses assertions to validate that schema enforcement works:

```python
assert collection.count_documents({}) == 1  # Only the valid record should exist
assert collection.find_one({"name": "Alice"}) is not None
```

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable database containers.
- Automatically manages container lifecycle.

### MongoDB Schema Validation

- Ensures data consistency and enforces field constraints.
- Prevents incorrect data from being stored.

### Assertions

- Validates that only schema-compliant records are stored.

---

