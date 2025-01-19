# Example 3: Reservations (MySQL)

This example demonstrates how to test reservation functionality using Testcontainers and MySQL. It includes:

- Creating a `reservations` table.
- Performing CRUD operations on the `reservations` table.
- Validating reservation constraints.

---

## Features

- **MySQL Container**:
  - Uses a custom MySQL container to spin up a database for testing.
  - Automatically handles container lifecycle.

- **Database Operations**:
  - Creates a `reservations` table with fields for guest name, room ID, check-in and check-out dates, and total price.
  - Performs CRUD operations and validates the results.

- **Assertions**:
  - Ensures the database operations produce the expected results.

---

## Directory Structure

The directory structure for this example is as follows:
```
mysql_example/
└── 03_reservations/
    ├── 03_reservations.py
    ├── conftest.py
    └── README.md
```

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers sqlalchemy mysql-connector-python
```
or
```bash
pip3 install pytest testcontainers sqlalchemy mysql-connector-python
```

### 2. Run the Test

Execute the test file using `pytest`:

```bash
python -m pytest 03_reservations.py -v -s
```
or
```bash
python3 -m pytest 03_reservations.py -v -s
```
---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/9efabb7e-74b3-4931-ac79-fcc283db71af)


---

## Code Walkthrough

### 1. `03_reservations.py`
This file contains the test suite for reservations. It includes:

- A custom `MySQLContainer` class to manage the MySQL container.
- Functions to set up the database schema and insert sample data.
- A test function to perform and validate CRUD operations.

### 2. `conftest.py`
This file registers the `reservations` marker for pytest. It allows you to organize and run tests related to reservations.

---

## Key Takeaways

- **Testcontainers**:
  - Simplifies testing by providing lightweight, disposable database containers.

- **SQLAlchemy**:
  - Provides a powerful ORM for interacting with the database.

- **Reservation Management**:
  - Demonstrates how to manage reservations and validate constraints.

- **Assertions**:
  - Ensures the database behaves as expected.

---

## Common Issues

- **Docker Not Running**:
  - Ensure Docker is installed and running on your system.

- **Port Conflicts**:
  - If the MySQL container fails to start, check for port conflicts on your system.

- **Missing Dependencies**:
  - Ensure all required Python packages are installed.

---

## Future Enhancements

- Add more complex queries, such as filtering reservations by date range or guest name.
- Test concurrent reservations to simulate real-world scenarios.
- Integrate with a frontend or API layer for end-to-end testing.

---
