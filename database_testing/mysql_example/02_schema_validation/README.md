# Example 2: Schema Validation (MySQL)

This example demonstrates how to use Testcontainers to test schema validation in MySQL. It covers the following:

- Setting up a MySQL container.
- Defining a database schema with constraints.
- Inserting valid and invalid records.
- Using assertions to validate schema enforcement.

---

## Overview

The test ensures that the MySQL table enforces schema constraints by allowing valid records and rejecting invalid ones. It performs the following operations:

1. **Define Schema**: Create a `users` table with validation rules.
2. **Insert Valid Data**: Add user records that comply with the schema.
3. **Insert Invalid Data**: Attempt to add records that violate constraints.
4. **Assertion Checks**: Verify that only valid records are stored.

---

## Features

### MySQL Container

- Uses the `MySqlContainer` class from the `testcontainers` library to spin up a MySQL database in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Schema Validation

- Defines a `users` table with constraints such as `NOT NULL`, `UNIQUE`, and `CHECK`.
- Ensures that invalid records are rejected.

### Assertions

- Confirms that only valid records are stored in the table.

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
python -m pytest 02_schema_validation.py -v -s
```

or

```bash
python3 -m pytest 02_schema_validation.py -v -s
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

### 2. Defining Schema Validation

The test defines a schema for the `users` table, enforcing rules for data consistency:

```python
cursor.execute("""
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT CHECK (age >= 18)
)
""")
```

- Requires `name` and `email` fields.
- Ensures `email` is unique.
- Adds a `CHECK` constraint to enforce `age >= 18`.

### 3. Performing Schema Validation

#### **Insert Valid Data**
```python
cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", ("Alice", "alice@example.com", 25))
```
- Inserts a valid user record.

#### **Insert Invalid Data**
```python
cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", ("Bob", "bob@example.com", 16))
```
- Attempts to insert an invalid record (should fail due to age constraint).

### 4. Assertions

The test uses assertions to validate that schema enforcement works:

```python
assert cursor.rowcount == 1  # Only one valid record should be inserted
```

- Ensures that only schema-compliant records are stored.

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable database containers.
- Automatically manages container lifecycle.

### MySQL Schema Validation

- Ensures data consistency and enforces field constraints.
- Prevents incorrect data from being stored.

### Assertions

- Validates that only schema-compliant records are stored.

---

