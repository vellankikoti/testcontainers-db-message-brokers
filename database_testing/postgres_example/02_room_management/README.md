# Example 2: Room Management

## Overview
This example demonstrates how to manage room inventory and pricing in the "Happy Hotel" database. It covers the following key operations:
- Creating a `rooms` table to store room inventory and pricing data.
- Inserting sample room data into the database.
- Retrieving and verifying the data to ensure accuracy.

This test uses **Testcontainers** to spin up a temporary PostgreSQL database, ensuring a clean and isolated environment for testing.

---

## Code Walkthrough

### 1. Starting the PostgreSQL Container
The `PostgresContainer` class from **Testcontainers** is used to start a temporary PostgreSQL instance. This container is automatically cleaned up after the test completes:
```python
with PostgresContainer("postgres:15.3") as postgres:
    engine = postgres.get_connection_engine()
```
- **PostgresContainer**: Spins up a PostgreSQL container using the specified image (`postgres:15.3`).
- **get_connection_engine()**: Provides a SQLAlchemy engine to interact with the database.

---

### 2. Creating the `rooms` Table
The `CREATE TABLE` SQL command is used to define the `rooms` table with the following schema:
- `room_id`: A unique identifier for each room (auto-incrementing primary key).
- `room_type`: The type of room (e.g., Single, Double, Suite).
- `price`: The price per night for the room.

```python
conn.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    room_id SERIAL PRIMARY KEY,
    room_type TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);
""")
```
- **CREATE TABLE IF NOT EXISTS**: Ensures the table is created only if it doesn't already exist.
- **NUMERIC(10, 2)**: Used for storing precise numeric values (e.g., prices with two decimal places).

---

### 3. Inserting Room Data
Sample room inventory and pricing data are added to the `rooms` table using the `INSERT INTO` SQL command:
```python
conn.execute("""
INSERT INTO rooms (room_type, price)
VALUES
    ('Single', 100.00),
    ('Double', 150.00),
    ('Suite', 300.00);
""")
```
- **INSERT INTO**: Adds new rows to the table.
- **VALUES**: Specifies the data to be inserted.

---

### 4. Retrieving and Verifying Data
The `SELECT` SQL command is used to fetch all room types and their prices from the table. The test verifies the data using assertions:
```python
result = conn.execute("SELECT room_type, price FROM rooms;")
rooms = {row[0]: row[1] for row in result}

assert len(rooms) == 3, "There should be exactly 3 room types in the database."
assert rooms["Single"] == 100.00, "The price for Single rooms should be 100.00."
assert rooms["Double"] == 150.00, "The price for Double rooms should be 150.00."
assert rooms["Suite"] == 300.00, "The price for Suites should be 300.00."
```
- **SELECT**: Retrieves data from the table.
- **Assertions**: Ensure the data is correct and matches expectations.

---

## How to Run
Follow these steps to run the test:

### Prerequisites
1. Ensure you have Python 3.8+ installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Run the Test
Run the test using one of the following commands:
```bash
python -m pytest 02_room_management.py -v
```
or
```bash
python3 -m pytest 02_room_management.py -v
```

---

## Expected Output
When you run the test, you should see the following output:

![image](https://github.com/user-attachments/assets/7ec39a81-2213-445f-94bd-4036feed2a9f)

### Run Specific Test Case

Run the test using one of the following commands:
```bash
python -m pytest 02_room_management.py::test_room_management -v
```
or
```bash
python3 -m pytest 02_room_management.py::test_room_management -v
```

---

## Expected Output
When you run the test, you should see the following output:

![image](https://github.com/user-attachments/assets/487f7dc0-663d-452d-97fe-a84352135e9d)

---

## Key Takeaways
- **Room Inventory Management**: Demonstrates how to manage room types and pricing in a database.
- **Data Validation**: Ensures the data is accurate using assertions.
- **SQL Basics**: Covers table creation, data insertion, and retrieval.
- **Testcontainers**: Provides a clean and isolated PostgreSQL environment for testing.

---
