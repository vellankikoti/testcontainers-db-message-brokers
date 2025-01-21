# Example 1: Basic CRUD Operations (MySQL)

This example demonstrates how to use Testcontainers to test basic MySQL database operations. It covers the following:

- Setting up a MySQL container.
- Creating a database table.
- Performing basic CRUD (Create, Read, Update, Delete) operations.
- Using assertions to validate the operations.

---

## Overview

The test simulates a basic database interaction by performing essential operations. It creates a `users` table, inserts sample data, and performs the following actions:

1. **Insert**: Add user records to the database.
2. **Select**: Retrieve and count the number of users.
3. **Update**: Modify a user's email address.
4. **Delete**: Remove a user record.

The test ensures that all operations execute correctly and validates the results using assertions.

---

## Features

### MySQL Container

- Uses the `MySqlContainer` class from the `testcontainers` library to spin up a MySQL database in a Docker container.
- Automatically handles container lifecycle (start and stop).

### Database Operations

- Creates a `users` table in the MySQL database.
- Performs CRUD operations and validates the results.

### Assertions

- Ensures that database operations produce the expected results.

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
python -m pytest 01_basic_crud.py -v -s
```

or

```bash
python3 -m pytest 01_basic_crud.py -v -s
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

### 2. Database Table Creation

The test creates a `users` table:

```python
cursor.execute("""
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
)
""")
```

- Defines a table with `id`, `name`, and `email` columns.

### 3. CRUD Operations

#### **Insert Data**
```python
cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("Alice", "alice@example.com"))
```
- Adds a user record.

#### **Select Data**
```python
cursor.execute("SELECT COUNT(*) FROM users")
result = cursor.fetchone()
```
- Retrieves and counts user records.

#### **Update Data**
```python
cursor.execute("UPDATE users SET email = %s WHERE name = %s", ("alice@updated.com", "Alice"))
```
- Updates a user’s email address.

#### **Delete Data**
```python
cursor.execute("DELETE FROM users WHERE name = %s", ("Alice",))
```
- Removes a user record.

### 4. Assertions

The test uses assertions to validate the results of each operation:

```python
assert result[0] == 1  # Ensure a user was inserted
assert updated_email == "alice@updated.com"  # Validate email update
assert deleted_user is None  # Ensure the record was deleted
```

---

## Key Takeaways

### Testcontainers

- Simplifies testing by providing lightweight, disposable database containers.
- Automatically manages container lifecycle.

### MySQL Database Testing

- Demonstrates how to use MySQL for basic CRUD operations.
- Uses the `mysql-connector-python` library to interact with the database.

### CRUD Operations

- Demonstrates how to perform and validate basic database operations.

### Assertions

- Ensures the database behaves as expected.

---

