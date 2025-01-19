# Example 2: Room Management (MySQL)

This example demonstrates how to test room management functionality using Testcontainers and MySQL. It includes:
- Creating a `rooms` table.
- Performing CRUD operations on the `rooms` table.
- Validating room availability and rate updates.

---

## Features

- **MySQL Container**:
  - Uses a custom MySQL container to spin up a database for testing.
  - Automatically handles container lifecycle.

- **Database Operations**:
  - Creates a `rooms` table with fields for room type, rate, and status.
  - Performs CRUD operations and validates the results.

- **Assertions**:
  - Ensures the database operations produce the expected results.

---

## Directory Structure

The directory structure for this example is as follows:

```plaintext
mysql_example/
└── 02_room_management/
    ├── 02_room_management.py
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

Execute the test file using pytest:

```bash
python -m pytest 02_room_management.py -v -s
```
or
```bash
python3 -m pytest 02_room_management.py -v -s
```
---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/c831d67b-9f3f-4512-b732-b619bec705ba)


---

## Code Walkthrough

### 1. 02_room_management.py
This file contains the test suite for room management. It includes:

- A custom MySQLContainer class to manage the MySQL container.
- Functions to set up the database schema and insert sample data.
- A test function to perform and validate CRUD operations.

### 2. conftest.py
This file registers the `room_management` marker for pytest. It allows you to organize and run tests related to room management.

---

## Key Takeaways

- **Testcontainers**:
  - Simplifies testing by providing lightweight, disposable database containers.

- **SQLAlchemy**:
  - Provides a powerful ORM for interacting with the database.

- **Room Management**:
  - Demonstrates how to manage room availability and rates.

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

- Add more complex queries, such as filtering rooms by availability and rate range.
- Test concurrent updates to simulate real-world scenarios.
- Integrate with a frontend or API layer for end-to-end testing.

---

## Conclusion

This example demonstrates how to test room management functionality using Testcontainers and MySQL. It highlights the power of Testcontainers for creating isolated, disposable test environments and the flexibility of SQLAlchemy for database interactions.

