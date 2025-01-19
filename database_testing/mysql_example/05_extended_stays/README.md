# Example 5: Extended Stays (MySQL)

This example demonstrates how to test scenarios where guests extend their stays in a hotel. It includes:

- Updating bookings with new check-out dates.
- Recalculating total prices based on the extended stay.

---

## Features

- **MySQL Container**:
  - Uses a custom MySQL container to spin up a database for testing.
  - Automatically handles container lifecycle.

- **Database Operations**:
  - Creates `rooms` and `bookings` tables.
  - Performs CRUD operations to update bookings and recalculate prices.

- **Assertions**:
  - Ensures the database operations produce the expected results.

---

## Directory Structure

The directory structure for this example is as follows:
```
mysql_example/
└── 05_extended_stays/
    ├── 05_extended_stays.py
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
python -m pytest 05_extended_stays.py -v -s
```
or
```bash
python3 -m pytest 05_extended_stays.py -v -s
```
---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/a00c0e1d-9240-4151-9c98-834ffb5335b4)


---

## Code Walkthrough

### 1. `05_extended_stays.py`
This file contains the test suite for extended stays. It includes:

- A custom `MySQLContainer` class to manage the MySQL container.
- Functions to set up the database schema and insert sample data.
- A test function to update bookings and verify the changes.

### 2. `conftest.py`
This file registers the `extended_stays` marker for pytest. It allows you to organize and run tests related to extended stays.

---

## Key Takeaways

- **Testcontainers**:
  - Simplifies testing by providing lightweight, disposable database containers.

- **SQLAlchemy**:
  - Provides a powerful ORM for interacting with the database.

- **Extended Stays**:
  - Demonstrates how to handle updates to bookings and recalculate prices.

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

- Add tests for concurrent updates to simulate real-world scenarios.
- Test edge cases, such as invalid check-out dates or overlapping bookings.
- Integrate with a frontend or API layer for end-to-end testing.

---
