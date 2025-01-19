# Example 3: Reservation System

## Overview
This example demonstrates how to handle reservations in the "Happy Hotel" database. It introduces relationships between tables and covers the following:
- Creating `guests` and `reservations` tables
- Establishing relationships between `guests` and `reservations` using foreign keys
- Inserting and retrieving reservation data
- Verifying the data using assertions in test cases

This example uses `pytest` and `Testcontainers` to create a temporary PostgreSQL database for testing.

---

## Code Walkthrough

### 1. Starting the PostgreSQL Container
The `PostgresContainer` class from `Testcontainers` is used to start a temporary PostgreSQL instance. This container is automatically cleaned up after the test.

```python
with PostgresContainer("postgres:15.3") as postgres:
    engine = postgres.get_connection_engine()
```

- **`PostgresContainer`**: Spins up a PostgreSQL container using the specified image (`postgres:15.3`).
- **`get_connection_engine()`**: Provides a SQLAlchemy engine to interact with the database.

This ensures a clean and isolated database environment for each test.

---

### 2. Creating the `guests` and `reservations` Tables
Two tables are created:
- **`guests`**: Stores guest information (`guest_id` and `guest_name`).
- **`reservations`**: Stores reservation details, including the `guest_id` (foreign key), room type, and check-in/check-out dates.

```sql
CREATE TABLE IF NOT EXISTS guests (
    guest_id SERIAL PRIMARY KEY,
    guest_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reservations (
    reservation_id SERIAL PRIMARY KEY,
    guest_id INT NOT NULL,
    room_type TEXT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    FOREIGN KEY (guest_id) REFERENCES guests (guest_id),
    CONSTRAINT valid_dates CHECK (check_out > check_in)
);
```

- **`FOREIGN KEY`**: Establishes a relationship between the `reservations` table and the `guests` table.
- **`CHECK Constraint`**: Ensures that the `check_out` date is always after the `check_in` date.

---

### 3. Inserting Guest and Reservation Data
Sample data is added to both tables:
- **Guests**: "Alice" and "Bob"
- **Reservations**: Alice books a "Single" room, and Bob books a "Suite."

```sql
INSERT INTO guests (guest_name) VALUES ('Alice'), ('Bob');

INSERT INTO reservations (guest_id, room_type, check_in, check_out)
VALUES
    (1, 'Single', '2024-12-24', '2024-12-26'),
    (2, 'Suite', '2024-12-25', '2024-12-30');
```

- **`guest_id`**: Links the reservation to the corresponding guest in the `guests` table.

---

### 4. Retrieving and Verifying Data
The `SELECT` SQL command is used to fetch reservation details, including guest names, room types, and dates. The test verifies that the data matches expectations.

```sql
SELECT g.guest_name, r.room_type, r.check_in, r.check_out
FROM reservations r
JOIN guests g ON r.guest_id = g.guest_id;
```

- **`JOIN`**: Combines data from the `guests` and `reservations` tables based on the `guest_id` relationship.

The test then verifies the data using assertions:
```python
assert len(reservations) == 2, "There should be exactly 2 reservations."
assert reservations[0]["guest_name"] == "Alice", "The first reservation should be for Alice."
assert reservations[1]["room_type"] == "Suite", "The second reservation should be for a Suite."
```

---

## How to Run

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Docker
- Required Python packages: `pytest`, `testcontainers`, `sqlalchemy`, `psycopg2-binary`

Install the dependencies using `pip`:
```bash
pip install pytest testcontainers sqlalchemy psycopg2-binary
```

---

### Running the Tests
Run the test using the following command:
```bash
python3 -m pytest 03_reservations.py -v
```
#### Expected Output
When you run the test, you should see the following output:

![image](https://github.com/user-attachments/assets/744c3e75-2833-4a05-ac20-496b11380f98)


### You can also run specific tests or use markers:

```bash
# Run a specific test
python3 -m pytest 03_reservations.py::test_reservation_system -v

# Run tests with the "reservations" marker
python3 -m pytest -m reservations -v
```

---

#### Expected Output
When you run the test, you should see the following output:

![image](https://github.com/user-attachments/assets/01d60a05-fe37-4d07-8c0d-434dd08e878d)


---

## Key Takeaways
- **Relationships**: Demonstrates how to establish relationships between tables using foreign keys.
- **Data Integrity**: Ensures that reservations are linked to valid guests and that invalid dates are rejected.
- **SQL Joins**: Introduces the concept of joining tables to retrieve related data.
- **Testcontainers**: Provides a clean, isolated database environment for testing.
